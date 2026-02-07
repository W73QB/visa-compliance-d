import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from contextlib import contextmanager
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

try:
    import yaml
except Exception:
    yaml = None

try:
    from jsonschema import ValidationError, validate as jsonschema_validate
except Exception:
    ValidationError = Exception
    jsonschema_validate = None

SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
REQUIRED_11_BLOCKS = [
    "short answer",
    "key findings at a glance",
    "what the authority requires",
    "verified requirements",
    "how we evaluate",
    "proof package checklist",
    "common rejection traps",
    "faq",
    "check in the engine",
    "disclaimer",
    "affiliate disclosure",
    "evidence log",
]
BANNED_WORDS = [
    "best",
    "recommend",
    "recommended",
    "guarantee",
    "guaranteed",
    "100%",
    "approved",
    "surely",
]


def read_text(path_or_url: str) -> str:
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        with urlopen(path_or_url, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    return Path(path_or_url).read_text(encoding="utf-8")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def atomic_json_write(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", delete=False, dir=str(path.parent), encoding="utf-8"
    ) as tmp:
        json.dump(data, tmp, indent=2)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


def atomic_text_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", delete=False, dir=str(path.parent), encoding="utf-8"
    ) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


@contextmanager
def file_lock(lock_path: Path):
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "a+", encoding="utf-8") as fh:
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(fh.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl

            fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(fh.fileno(), fcntl.LOCK_UN)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def tokenize(text: str) -> set:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def classify_section(url: str) -> str:
    for section in ("posts", "guides", "traps", "visas"):
        if f"/{section}/" in url:
            return section
    return "root"


def parse_sitemap(xml_text: str) -> Tuple[str, List[str]]:
    root = ET.fromstring(xml_text)
    urls: List[str] = []
    if root.tag.endswith("urlset"):
        for node in root.findall("sm:url/sm:loc", SITEMAP_NS):
            if node.text:
                urls.append(node.text.strip())
        return ("urlset", urls)
    if root.tag.endswith("sitemapindex"):
        for node in root.findall("sm:sitemap/sm:loc", SITEMAP_NS):
            if node.text:
                urls.append(node.text.strip())
        return ("sitemapindex", urls)
    raise ValueError("Unsupported sitemap root")


def load_config(path: str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def score_source(url: str, config: Dict[str, Any]) -> Tuple[int, str]:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    scoring = config.get("source_scoring", {})
    suffixes = scoring.get("allow_suffixes", [])
    hosts = scoring.get("allow_hosts", [])
    if any(host.endswith(sfx) for sfx in suffixes):
        return (100, "allowed suffix")
    if host in hosts:
        return (85, "allowed host")
    return (0, "untrusted host")


def extract_front_matter(markdown: str) -> Dict[str, Any]:
    if not markdown.startswith("---\n"):
        return {}
    end = markdown.find("\n---\n", 4)
    if end < 0:
        return {}
    front_matter_text = markdown[4:end]
    if yaml is None:
        return {}

    def _normalize_yaml_scalars(value: Any) -> Any:
        if isinstance(value, dict):
            return {k: _normalize_yaml_scalars(v) for k, v in value.items()}
        if isinstance(value, list):
            return [_normalize_yaml_scalars(v) for v in value]
        if hasattr(value, "isoformat") and not isinstance(value, str):
            try:
                return value.isoformat()
            except Exception:
                return value
        return value

    try:
        parsed = yaml.safe_load(front_matter_text)
    except Exception:
        return {}
    if not isinstance(parsed, dict):
        return {}
    return _normalize_yaml_scalars(parsed)


def validate_front_matter(data: Dict[str, Any], schema_path: Path) -> Tuple[bool, str]:
    if jsonschema_validate is None:
        return (False, "jsonschema is not installed")
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        jsonschema_validate(instance=data, schema=schema)
        return (True, "ok")
    except ValidationError as exc:
        return (False, f"front matter schema validation failed: {exc}")
    except Exception as exc:
        return (False, f"front matter validation error: {exc}")


def parse_retry_after(value: str) -> int:
    if not value:
        return 0
    value = value.strip()
    if value.isdigit():
        return max(0, int(value))
    try:
        when = parsedate_to_datetime(value)
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        return max(0, int((when - now).total_seconds()))
    except Exception:
        return 0


def http_json_with_retry(
    req_or_url: Any, timeout: int, retries: int = 3
) -> Dict[str, Any]:
    for attempt in range(retries + 1):
        try:
            with urlopen(req_or_url, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as exc:
            retriable = exc.code == 429 or 500 <= exc.code < 600
            if retriable and attempt < retries:
                retry_after = parse_retry_after(exc.headers.get("Retry-After", ""))
                sleep_seconds = retry_after if retry_after > 0 else min(30, 2**attempt)
                time.sleep(sleep_seconds)
                continue
            raise
        except URLError:
            if attempt < retries:
                time.sleep(min(30, 2**attempt))
                continue
            raise
    raise RuntimeError("request failed after retries")


def compute_freshness(raw_item: Dict[str, Any], run_date: str) -> int:
    run_day = None
    try:
        run_day = datetime.strptime(run_date, "%Y-%m-%d").date()
    except Exception:
        run_day = datetime.now(timezone.utc).date()

    candidates: List[str] = []
    pagemap = raw_item.get("pagemap", {}) if isinstance(raw_item, dict) else {}
    metatags = pagemap.get("metatags", []) if isinstance(pagemap, dict) else []
    if metatags and isinstance(metatags, list) and isinstance(metatags[0], dict):
        mt = metatags[0]
        for key in [
            "article:published_time",
            "article:modified_time",
            "og:updated_time",
            "date",
            "pubdate",
        ]:
            if mt.get(key):
                candidates.append(str(mt.get(key)))
    if raw_item.get("snippet"):
        m = re.search(r"(20\d{2}-\d{2}-\d{2})", str(raw_item.get("snippet")))
        if m:
            candidates.append(m.group(1))

    source_day = None
    for candidate in candidates:
        text = candidate.strip().replace("Z", "+00:00")
        try:
            source_day = datetime.fromisoformat(text).date()
            break
        except Exception:
            try:
                source_day = datetime.strptime(text[:10], "%Y-%m-%d").date()
                break
            except Exception:
                continue
    if source_day is None:
        return 0
    age_days = max(0, (run_day - source_day).days)
    if age_days <= 30:
        return 100
    if age_days <= 180:
        return 70
    if age_days <= 365:
        return 40
    return 10


def build_search_query(config: Dict[str, Any], run_date: str) -> str:
    templates = config.get("query_templates", [])
    if not templates:
        return "visa insurance requirements"
    try:
        run_dt = datetime.strptime(run_date, "%Y-%m-%d")
    except Exception:
        run_dt = datetime.now(timezone.utc)
    weekday_key = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"][run_dt.weekday()]
    topic_hint = str(config.get("rotation", {}).get(weekday_key, "insurance"))
    template = templates[run_dt.toordinal() % len(templates)]
    values = {
        "country": "spain",
        "visa_type": topic_hint.replace("_", " "),
        "topic_slug": topic_hint,
    }
    try:
        return str(template).format(**values)
    except Exception:
        return str(template)


def validate_claim_references(
    post_text: str, claim_map: Dict[str, Any]
) -> Tuple[bool, str]:
    claim_ids = {
        str(item.get("claim_id", "")).strip()
        for item in claim_map.get("claims", [])
        if str(item.get("claim_id", "")).strip()
    }
    referenced_ids = set(re.findall(r"\bC\d+\b", post_text))
    unknown = sorted(x for x in referenced_ids if x not in claim_ids)
    if unknown:
        return (False, f"unknown claim reference(s): {', '.join(unknown)}")
    return (True, "ok")


def validate_checker_cta(text: str, run_date: str) -> Tuple[bool, str]:
    cta_pattern = re.compile(r"\{\{<\s*checker_cta\b[^>]*>\}\}", flags=re.IGNORECASE)
    cta_matches = cta_pattern.findall(text)
    if not cta_matches:
        return (False, "missing checker_cta shortcode")
    for match in cta_matches:
        if "snapshot=" in match.lower() and run_date in match:
            return (True, "ok")
    return (False, "checker_cta shortcode missing snapshot for run date")


def validate_faq_style(text: str) -> Tuple[bool, str]:
    if "## faq" not in text.lower():
        return (False, "missing FAQ section")
    if "**Q:" not in text or "**A:**" not in text:
        return (False, "faq must use bold Q/A format")
    return (True, "ok")


def extract_slug_fields(
    selected: Dict[str, Any], run_date: str, config: Dict[str, Any]
) -> Dict[str, str]:
    title_slug = slugify(selected.get("title", ""))
    host_slug = slugify(selected.get("source_host", ""))
    topic_key = slugify(selected.get("topic_key", ""))
    title_tokens = [t for t in title_slug.split("-") if t]

    stop_words = {
        "visa",
        "insurance",
        "requirements",
        "requirement",
        "guide",
        "checklist",
    }
    country = "global"
    for token in title_tokens:
        if token not in stop_words and len(token) > 2:
            country = token
            break

    visa_candidates = ["dnv", "dtv", "freelance", "elective", "schengen", "nomad"]
    visa_type = "route"
    for candidate in visa_candidates:
        if candidate in title_tokens or candidate in host_slug:
            visa_type = candidate
            break

    try:
        run_dt = datetime.strptime(run_date, "%Y-%m-%d")
    except Exception:
        run_dt = datetime.now(timezone.utc)
    weekday_key = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"][run_dt.weekday()]
    rotation_hint = slugify(str(config.get("rotation", {}).get(weekday_key, "update")))

    topic_slug = title_slug
    if topic_key:
        topic_slug = topic_key.replace(":", "-")
    if not topic_slug:
        topic_slug = f"{rotation_hint}-{run_date}"

    return {
        "country": slugify(country) or "global",
        "visa_type": slugify(visa_type) or "route",
        "topic_slug": slugify(topic_slug) or f"update-{run_date}",
    }


def build_post_path(
    run_date: str, selected: Dict[str, Any], config: Dict[str, Any]
) -> Path:
    slug_template = str(
        config.get("post", {}).get(
            "slug_template", "{country}-{visa_type}-{topic_slug}"
        )
    )
    fields = extract_slug_fields(selected, run_date, config)
    try:
        slug_raw = slug_template.format(**fields)
    except Exception:
        slug_raw = "{country}-{visa_type}-{topic_slug}".format(**fields)
    slug = slugify(slug_raw)
    if not slug:
        slug = f"update-{run_date}"
    return Path(f"content/posts/{slug}.md")


def parse_selection_ranking(config: Dict[str, Any]) -> List[str]:
    ranking_expr = str(
        config.get("selection_ranking", "credibility_score,freshness,title")
    ).strip()
    if not ranking_expr:
        return ["credibility_score", "freshness", "title"]
    fields = [field.strip() for field in ranking_expr.split(",") if field.strip()]
    return fields or ["credibility_score", "freshness", "title"]


def sort_candidates(items: List[Dict[str, Any]], config: Dict[str, Any]) -> None:
    ranking_fields = parse_selection_ranking(config)
    numeric_fields = {"credibility_score", "freshness"}

    def key_for(item: Dict[str, Any]) -> Tuple[Any, ...]:
        key_parts: List[Any] = []
        for field in ranking_fields:
            descending = field.startswith("-")
            name = field[1:] if descending else field
            value = item.get(name)
            if name in numeric_fields:
                num_value = int(value or 0)
                if descending or not field.startswith("+"):
                    key_parts.append(-num_value)
                else:
                    key_parts.append(num_value)
            else:
                str_value = str(value or "")
                key_parts.append(str_value.lower())
        return tuple(key_parts)

    items.sort(key=key_for)


def resolve_llm_runtime(config: Dict[str, Any]) -> Dict[str, str]:
    llm_cfg = config.get("llm", {})
    provider = str(llm_cfg.get("provider", "nvidia")).strip().lower()

    if provider == "openai":
        return {
            "provider": "openai",
            "api_key": os.environ.get("OPENAI_API_KEY", ""),
            "model": os.environ.get(
                "OPENAI_MODEL", str(llm_cfg.get("model", "gpt-4o-mini"))
            ),
            "endpoint": str(
                llm_cfg.get("base_url", "https://api.openai.com/v1/chat/completions")
            ),
        }

    return {
        "provider": "nvidia",
        "api_key": os.environ.get("NVIDIA_API_KEY", "")
        or os.environ.get("NGC_API_KEY", ""),
        "model": os.environ.get(
            "NVIDIA_MODEL", str(llm_cfg.get("model", "meta/llama-3.1-70b-instruct"))
        ),
        "endpoint": str(
            llm_cfg.get(
                "base_url", "https://integrate.api.nvidia.com/v1/chat/completions"
            )
        ),
    }


def ensure_blocks(text: str) -> Tuple[bool, str]:
    lower = text.lower()
    for block in REQUIRED_11_BLOCKS:
        if block not in lower:
            return (False, f"missing block: {block}")
    if "snapshot=" not in lower:
        return (False, "missing snapshot=")
    for word in BANNED_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", lower):
            return (False, f"banned word: {word}")
    return (True, "ok")


def sanitize_source_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    lines = []
    for ln in text.splitlines():
        if re.search(r"ignore previous|system:|<\|im_start\|>", ln.lower()):
            continue
        lines.append(ln)
    clean = "\n".join(lines)
    return clean[:500]


def cmd_index(args: argparse.Namespace) -> int:
    try:
        if args.sitemap.startswith("http://"):
            return 2
        xml_text = read_text(args.sitemap)
        kind, urls = parse_sitemap(xml_text)
        out_urls: List[str] = []
        if kind == "urlset":
            out_urls = urls
        else:
            count = 0
            for child in urls:
                if count >= args.max_sitemaps:
                    break
                child_xml = read_text(child)
                child_kind, child_urls = parse_sitemap(child_xml)
                if child_kind == "urlset":
                    out_urls.extend(child_urls)
                count += 1
        items = []
        for url in sorted(set(out_urls)):
            slug = slugify(url.rstrip("/").split("/")[-1] or "root")
            items.append(
                {
                    "url": url,
                    "slug": slug,
                    "section": classify_section(url),
                    "intent_tokens": sorted(list(tokenize(url))),
                }
            )
        atomic_json_write(Path(args.output), items)
        return 0
    except Exception:
        return 1


def cmd_search(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    state_dir = Path(args.state_dir)
    state_dir.mkdir(parents=True, exist_ok=True)
    quota_file = state_dir / "quota_usage.json"
    cache_file = state_dir / "search_cache.json"
    day = args.date
    quota = read_json(quota_file, {"daily": {}})
    daily = quota.get("daily", {})
    used = int(daily.get(day, 0))
    cap = int(config.get("cse_quota", {}).get("daily_query_cap", 100))
    query_key = slugify(args.query)
    cache_obj = read_json(cache_file, {})
    cross_day_cache = bool(config.get("cse_quota", {}).get("cross_day_cache", True))
    if used >= cap:
        if cross_day_cache and query_key in cache_obj:
            atomic_json_write(
                Path(args.output),
                {"status": "PASS", "items": cache_obj.get(query_key, [])},
            )
            return 0
        atomic_json_write(
            Path(args.output), {"status": "SKIP_QUOTA_EXHAUSTED", "items": []}
        )
        return 0

    if args.input_json:
        payload = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    else:
        api_key = os.environ.get("GOOGLE_CSE_API_KEY", "")
        cse_id = os.environ.get("GOOGLE_CSE_ID", "")
        if not api_key or not cse_id:
            atomic_json_write(
                Path(args.output), {"status": "SKIP_MISSING_SECRET", "items": []}
            )
            return 0
        params = urlencode({"key": api_key, "cx": cse_id, "q": args.query})
        try:
            payload = http_json_with_retry(
                f"https://www.googleapis.com/customsearch/v1?{params}", timeout=30
            )
        except Exception:
            return 1

    items = []
    for raw in payload.get("items", []):
        link = raw.get("link", "")
        score, reason = score_source(link, config)
        item = {
            "title": raw.get("title", ""),
            "link": link,
            "snippet": sanitize_source_text(raw.get("snippet", "")),
            "source_host": urlparse(link).netloc.lower(),
            "credibility_score": score,
            "score_reason": reason,
            "freshness": compute_freshness(raw, args.date),
        }
        items.append(item)
    sort_candidates(items, config)
    result = {"status": "PASS", "items": items}
    atomic_json_write(Path(args.output), result)
    cache_obj[query_key] = items
    atomic_json_write(cache_file, cache_obj)
    daily[day] = used + 1
    quota["daily"] = daily
    atomic_json_write(quota_file, quota)
    return 0


def compute_topic_key(item: Dict[str, Any]) -> str:
    title = slugify(item.get("title", ""))
    host = slugify(item.get("source_host", ""))
    return f"{host}:{title}"


def cmd_select(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    index_items = read_json(Path(args.index), [])
    candidates_json = read_json(Path(args.candidates), {"items": []})
    candidates = candidates_json.get("items", [])
    threshold = float(config.get("source_scoring", {}).get("threshold", 50))
    dedup_threshold = float(config.get("dedup", {}).get("jaccard_threshold", 0.55))
    state_dir = Path(args.state_dir)
    seen = read_json(state_dir / "seen_topics.json", {"topics": []}).get("topics", [])
    pending = read_json(state_dir / "pending_topics.json", {"topics": []}).get(
        "topics", []
    )
    seen_keys = set(seen + pending)

    existing_tokens = set()
    for item in index_items:
        existing_tokens |= set(item.get("intent_tokens", []))

    selected = None
    for cand in candidates:
        if int(cand.get("credibility_score", 0)) < threshold:
            continue
        key = compute_topic_key(cand)
        if key in seen_keys:
            continue
        score = jaccard(
            tokenize(cand.get("title", "") + " " + cand.get("link", "")),
            existing_tokens,
        )
        if score >= dedup_threshold:
            continue
        cand["topic_key"] = key
        selected = cand
        break

    if not selected:
        atomic_json_write(
            Path(args.output), {"status": "SKIP_NO_CANDIDATE", "selected": None}
        )
        return 0

    atomic_json_write(Path(args.output), {"status": "PASS", "selected": selected})
    return 0


def cmd_evidence(args: argparse.Namespace) -> int:
    selected = read_json(Path(args.selected), {}).get("selected")
    if not selected:
        atomic_json_write(Path(args.claim_map), {"date": args.date, "claims": []})
        Path(args.output).write_text(
            "# Evidence Pack\n\nNo selected topic.\n", encoding="utf-8"
        )
        return 0

    verification_status = "VERIFIED" if selected.get("link") else "UNKNOWN"
    source_id = "AUTO_SOURCE_1"
    claim_map = {
        "date": args.date,
        "claims": [
            {
                "claim_id": "C1",
                "claim_text": selected.get("title", ""),
                "requirement_id": "R1",
                "source_id": source_id,
                "source_url": selected.get("link", ""),
                "locator": "n/a",
                "verification_status": verification_status,
                "verification_date": args.date,
                "authority_level": "secondary",
            }
        ],
    }
    atomic_json_write(Path(args.claim_map), claim_map)

    md = [
        f"# Evidence Pack - {args.date}",
        "",
        "## Normalized Requirements Table",
        "| Requirement | Source URL | Locator | Verified on | Status |",
        "| --- | --- | --- | --- | --- |",
        f"| {selected.get('title', 'TBD')} | {selected.get('link', '')} | n/a | {args.date} | {verification_status} |",
        "",
        "## Claim Map",
        f"- C1 -> R1 ({source_id})",
    ]
    atomic_text_write(Path(args.output), "\n".join(md) + "\n")
    return 0


def body_word_count(text: str) -> int:
    parts = text.split("---\n")
    body = text
    if len(parts) >= 3:
        body = "---\n".join(parts[2:])
    return len(re.findall(r"\b\w+\b", body))


def cmd_write(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    llm_runtime = resolve_llm_runtime(config)
    run_date = args.date
    out = Path(args.output)
    if out.exists() and not bool(getattr(args, "allow_existing_output", False)):
        return 2

    claim_map_obj = read_json(Path(args.claim_map), {"claims": []})

    budget_file = Path(args.budget_file) if getattr(args, "budget_file", None) else None
    per_run_budget = int(config.get("llm", {}).get("per_run_budget", 0))
    max_tokens = int(config.get("llm", {}).get("max_tokens", 1800))
    used_tokens = 0
    if budget_file and per_run_budget > 0:
        usage = read_json(budget_file, {"total_tokens": 0})
        used_tokens = int(usage.get("total_tokens", 0))
        if used_tokens + max_tokens > per_run_budget:
            return 10

    if args.dry_run:
        text = Path(args.fixture).read_text(encoding="utf-8")
        text = text.replace("{{RUN_DATE}}", run_date)
    else:
        api_key = llm_runtime.get("api_key", "")
        if not api_key:
            return 3
        model = llm_runtime.get("model", "")
        endpoint = llm_runtime.get("endpoint", "")
        evidence = sanitize_source_text(Path(args.evidence).read_text(encoding="utf-8"))
        claim_map = sanitize_source_text(
            Path(args.claim_map).read_text(encoding="utf-8")
        )
        prompt = (
            "Generate Hugo markdown with valid front matter and all required compliance blocks. "
            f"Run date is {run_date}. Use snapshot={run_date}.\n"
            f"Evidence:\n{evidence}\nClaim map:\n{claim_map}\n"
        )
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You generate structured compliance markdown only.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
            "max_tokens": max_tokens,
        }
        req = Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            body = http_json_with_retry(req, timeout=60)
        except Exception:
            return 11
        spent_tokens = int(body.get("usage", {}).get("total_tokens", max_tokens))
        if budget_file and per_run_budget > 0:
            total_tokens = used_tokens + spent_tokens
            if total_tokens > per_run_budget:
                return 10
            atomic_json_write(budget_file, {"total_tokens": total_tokens})
        text = body["choices"][0]["message"]["content"]

    fm = extract_front_matter(text)
    schema_path = Path(
        getattr(
            args, "front_matter_schema", "tools/schemas/daily_front_matter.schema.json"
        )
    )
    ok_fm, msg_fm = validate_front_matter(fm, schema_path)
    if not ok_fm:
        print(msg_fm)
        return 4
    ok_blocks, msg_blocks = ensure_blocks(text)
    if not ok_blocks:
        print(msg_blocks)
        return 5
    ok_cta, msg_cta = validate_checker_cta(text, run_date)
    if not ok_cta:
        print(msg_cta)
        return 6
    min_wc, max_wc = config.get("post", {}).get("word_count_range", [100, 4000])
    wc = body_word_count(text)
    if wc < int(min_wc) or wc > int(max_wc):
        return 7
    ok_claim_refs, msg_claim_refs = validate_claim_references(text, claim_map_obj)
    if not ok_claim_refs:
        print(msg_claim_refs)
        return 8
    ok_faq, msg_faq = validate_faq_style(text)
    if not ok_faq:
        print(msg_faq)
        return 12

    atomic_text_write(out, text)
    return 0


def cmd_qa(args: argparse.Namespace) -> int:
    proc = subprocess.run(
        [sys.executable, "tools/lint_content.py", "--path", args.path],
        check=False,
        cwd=str(Path(__file__).resolve().parent.parent),
    )
    if proc.returncode != 0:
        return proc.returncode
    text = Path(args.path).read_text(encoding="utf-8")
    claim_map = read_json(Path(args.claim_map), {"claims": []})
    for claim in claim_map.get("claims", []):
        if claim.get("verification_status") == "VERIFIED":
            if claim.get("source_id", "") not in text:
                return 9
    return 0


def cmd_update_status(args: argparse.Namespace) -> int:
    state_file = Path(args.state_file)
    history = read_json(state_file, [])
    entry = {"date": args.date, "status": args.status, "reason": args.reason}
    if (
        history
        and isinstance(history[-1], dict)
        and history[-1].get("date") == args.date
    ):
        history[-1] = entry
    else:
        history.append(entry)
    atomic_json_write(state_file, history)
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    llm_runtime = resolve_llm_runtime(config)
    state_dir = Path(args.state_dir)
    runs_dir = Path(args.runs_dir)
    run_dir = runs_dir / args.date
    run_dir.mkdir(parents=True, exist_ok=True)
    config_hash = sha256_file(Path(args.config))
    code_version = sha256_file(Path(__file__))

    manifest = {
        "date": args.date,
        "config_hash": config_hash,
        "code_version": code_version,
        "status": "FAIL",
        "steps": [],
    }
    manifest_path = run_dir / "run_manifest.json"

    index_out = run_dir / "index.json"
    candidates_out = run_dir / "candidates.json"
    selected_out = run_dir / "selected.json"
    evidence_out = run_dir / "evidence.md"
    claim_map_out = run_dir / "claim_map.json"
    if args.output_post:
        post_out = Path(args.output_post)
    else:
        selected_for_path = (
            read_json(selected_out, {}).get("selected", {})
            if selected_out.exists()
            else {}
        )
        post_out = build_post_path(args.date, selected_for_path, config)

    existing_manifest = read_json(manifest_path, {})
    if (
        existing_manifest.get("status") == "PASS"
        and existing_manifest.get("config_hash") == config_hash
        and existing_manifest.get("code_version") == code_version
        and post_out.exists()
    ):
        return 0

    pending_file = state_dir / "pending_topics.json"
    if not pending_file.exists():
        atomic_json_write(pending_file, {"topics": []})

    rc = 0
    if not index_out.exists():
        rc = cmd_index(
            argparse.Namespace(
                sitemap=args.sitemap, output=str(index_out), max_sitemaps=20
            )
        )
    manifest["steps"].append({"step": "index", "rc": rc})
    if rc != 0:
        atomic_json_write(manifest_path, manifest)
        cmd_update_status(
            argparse.Namespace(
                state_file=str(state_dir / "run-status.json"),
                date=args.date,
                status="FAIL",
                reason="index",
            )
        )
        return 1

    rc = cmd_search(
        argparse.Namespace(
            input_json=args.search_input_json,
            output=str(candidates_out),
            query=build_search_query(config, args.date),
            date=args.date,
            state_dir=str(state_dir),
            config=args.config,
        )
    )
    manifest["steps"].append({"step": "search", "rc": rc})

    rc = cmd_select(
        argparse.Namespace(
            index=str(index_out),
            candidates=str(candidates_out),
            output=str(selected_out),
            state_dir=str(state_dir),
            config=args.config,
        )
    )
    manifest["steps"].append({"step": "select", "rc": rc})
    selected_json = read_json(selected_out, {"status": "FAIL"})
    if selected_json.get("status") != "PASS":
        status = selected_json.get("status", "SKIP_NO_CANDIDATE")
        manifest["status"] = status
        atomic_json_write(manifest_path, manifest)
        cmd_update_status(
            argparse.Namespace(
                state_file=str(state_dir / "run-status.json"),
                date=args.date,
                status=status,
                reason="select",
            )
        )
        return 0

    if not args.output_post:
        post_out = build_post_path(args.date, selected_json.get("selected", {}), config)

    rc = 0
    if not evidence_out.exists() or not claim_map_out.exists():
        rc = cmd_evidence(
            argparse.Namespace(
                selected=str(selected_out),
                output=str(evidence_out),
                claim_map=str(claim_map_out),
                date=args.date,
            )
        )
    manifest["steps"].append({"step": "evidence", "rc": rc})

    claims = read_json(claim_map_out, {"claims": []}).get("claims", [])
    has_verified = any(c.get("verification_status") == "VERIFIED" for c in claims)
    if not has_verified:
        manifest["status"] = "SKIP_NO_VERIFIED_EVIDENCE"
        atomic_json_write(manifest_path, manifest)
        cmd_update_status(
            argparse.Namespace(
                state_file=str(state_dir / "run-status.json"),
                date=args.date,
                status="SKIP_NO_VERIFIED_EVIDENCE",
                reason="evidence",
            )
        )
        return 0

    effective_dry_run = bool(args.dry_run or not llm_runtime.get("api_key", ""))
    if effective_dry_run and not args.draft_fixture:
        manifest["status"] = "FAIL"
        atomic_json_write(manifest_path, manifest)
        cmd_update_status(
            argparse.Namespace(
                state_file=str(state_dir / "run-status.json"),
                date=args.date,
                status="FAIL",
                reason="missing_draft_fixture",
            )
        )
        return 1

    rc = cmd_write(
        argparse.Namespace(
            evidence=str(evidence_out),
            claim_map=str(claim_map_out),
            output=str(post_out),
            date=args.date,
            config=args.config,
            dry_run=effective_dry_run,
            fixture=args.draft_fixture,
            allow_existing_output=True,
            budget_file=str(run_dir / "llm_usage.json"),
            front_matter_schema="tools/schemas/daily_front_matter.schema.json",
        )
    )
    manifest["steps"].append({"step": "write", "rc": rc})
    if rc != 0:
        manifest["status"] = "FAIL"
        atomic_json_write(manifest_path, manifest)
        cmd_update_status(
            argparse.Namespace(
                state_file=str(state_dir / "run-status.json"),
                date=args.date,
                status="FAIL",
                reason="write",
            )
        )
        return 1

    rc = cmd_qa(
        argparse.Namespace(
            path=str(post_out), claim_map=str(claim_map_out), config=args.config
        )
    )
    manifest["steps"].append({"step": "qa", "rc": rc})
    if rc != 0:
        manifest["status"] = "FAIL"
        atomic_json_write(manifest_path, manifest)
        cmd_update_status(
            argparse.Namespace(
                state_file=str(state_dir / "run-status.json"),
                date=args.date,
                status="FAIL",
                reason="qa",
            )
        )
        return 1

    selected = selected_json.get("selected", {})
    topic_key = selected.get("topic_key")
    if topic_key:
        lock_path = state_dir / "seen_topics.lock"
        with file_lock(lock_path):
            seen_obj = read_json(state_dir / "seen_topics.json", {"topics": []})
            topics = seen_obj.get("topics", [])
            if topic_key not in topics:
                topics.append(topic_key)
            atomic_json_write(state_dir / "seen_topics.json", {"topics": topics})

    manifest["status"] = "PASS"
    atomic_json_write(manifest_path, manifest)
    cmd_update_status(
        argparse.Namespace(
            state_file=str(state_dir / "run-status.json"),
            date=args.date,
            status="PASS",
            reason="ok",
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("index")
    p.add_argument("--sitemap", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--max-sitemaps", type=int, default=20)
    p.set_defaults(func=cmd_index)

    p = sub.add_parser("search")
    p.add_argument("--query", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--input-json")
    p.add_argument("--date", required=True)
    p.add_argument("--state-dir", required=True)
    p.add_argument("--config", required=True)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("select")
    p.add_argument("--index", required=True)
    p.add_argument("--candidates", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--state-dir", required=True)
    p.add_argument("--config", required=True)
    p.set_defaults(func=cmd_select)

    p = sub.add_parser("evidence")
    p.add_argument("--selected", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--claim-map", required=True)
    p.add_argument("--date", required=True)
    p.set_defaults(func=cmd_evidence)

    p = sub.add_parser("write")
    p.add_argument("--evidence", required=True)
    p.add_argument("--claim-map", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--date", required=True)
    p.add_argument("--config", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--fixture")
    p.add_argument("--budget-file")
    p.add_argument(
        "--front-matter-schema", default="tools/schemas/daily_front_matter.schema.json"
    )
    p.add_argument("--allow-existing-output", action="store_true")
    p.set_defaults(func=cmd_write)

    p = sub.add_parser("qa")
    p.add_argument("--path", required=True)
    p.add_argument("--claim-map", required=True)
    p.add_argument("--config", required=True)
    p.set_defaults(func=cmd_qa)

    p = sub.add_parser("update-status")
    p.add_argument("--state-file", required=True)
    p.add_argument("--date", required=True)
    p.add_argument("--status", required=True)
    p.add_argument("--reason", required=True)
    p.set_defaults(func=cmd_update_status)

    p = sub.add_parser("run")
    p.add_argument("--date", required=True)
    p.add_argument("--config", required=True)
    p.add_argument("--state-dir", default="docs/ops/daily-auto-blog/state")
    p.add_argument("--runs-dir", default="docs/ops/daily-auto-blog/runs")
    p.add_argument("--sitemap", required=True)
    p.add_argument("--search-input-json")
    p.add_argument("--draft-fixture")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--output-post")
    p.set_defaults(func=cmd_run)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
