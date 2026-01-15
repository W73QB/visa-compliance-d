import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
VISAS = ROOT / "data" / "visas"
PRODUCTS = ROOT / "data" / "products"
MAPPINGS = ROOT / "data" / "mappings"

MAPPINGS.mkdir(exist_ok=True)

def load_all(folder):
    files = []
    for p in folder.rglob("*.json"):
        files.append(json.loads(p.read_text(encoding="utf-8")))
    return files

visas = load_all(VISAS)
products = load_all(PRODUCTS)

def get_req(visa, key):
    for r in visa["requirements"]:
        if r["key"] == key:
            return r
    return None

def product_spec(product, path):
    cur = product["specs"]
    for p in path.split("."):
        if cur is None or p not in cur:
            return None
        cur = cur[p]
    return cur

def evaluate(visa, product):
    reasons = []
    missing = []

    # Thai DTV - insurance not required
    req = get_req(visa, "insurance.mandatory")
    if req and req["value"] == False:
        return {
            "visa_id": visa["id"],
            "product_id": product["id"],
            "status": "NOT_REQUIRED",
            "reasons": [
                {
                    "text": "Visa does not require insurance",
                    "evidence": req["evidence"]
                }
            ],
            "missing": []
        }

    status = "GREEN"

    # Travel insurance not accepted
    req = get_req(visa, "insurance.travel_insurance_accepted")
    if req and req["value"] == False:
        ptype = product_spec(product, "type")
        if ptype is None:
            status = "UNKNOWN"
            missing.append("specs.type")
        elif "travel" in ptype:
            status = "RED"
            reasons.append({
                "text": "Travel insurance is not accepted for this visa",
                "evidence": req["evidence"]
            })

    # Authorized to operate in jurisdiction
    req = get_req(visa, "insurance.authorized_in_spain")
    if req and req["value"] == True:
        country = visa.get("id", "").upper()[:2]
        if country == "ES":
            jf = product_spec(product, f"jurisdiction_facts.{country}.authorized")
            if jf is None:
                if status == "GREEN":
                    status = "UNKNOWN"
                missing.append(f"specs.jurisdiction_facts.{country}.authorized")
            elif jf == False:
                status = "RED"
                reasons.append({
                    "text": f"Insurer not authorized to operate in {visa.get('country', 'jurisdiction')}",
                    "evidence": req["evidence"]
                })

    # No deductible
    req = get_req(visa, "insurance.no_deductible")
    if req and req["value"] == True:
        ded = product_spec(product, "deductible.amount")
        if ded is None:
            status = "UNKNOWN"
            missing.append("specs.deductible.amount")
        elif ded > 0:
            status = "RED"
            reasons.append({
                "text": f"Visa requires zero deductible but product has {ded}",
                "evidence": req["evidence"]
            })

    # Comprehensive coverage
    req = get_req(visa, "insurance.comprehensive")
    if req and req["value"] == True:
        comprehensive = product_spec(product, "comprehensive")
        if comprehensive is None:
            if status == "GREEN":
                status = "UNKNOWN"
            missing.append("specs.comprehensive")
        elif comprehensive == False:
            status = "RED"
            reasons.append({
                "text": "Comprehensive coverage required",
                "evidence": req["evidence"]
            })

    # Covers risks insured by public health system
    req = get_req(visa, "insurance.covers_public_health_system_risks")
    if req and req["value"] == True:
        covers = product_spec(product, "covers_public_health_system_risks")
        if covers is None:
            if status == "GREEN":
                status = "UNKNOWN"
            missing.append("specs.covers_public_health_system_risks")
        elif covers == False:
            status = "RED"
            reasons.append({
                "text": "Visa requires coverage of public health system risks",
                "evidence": req["evidence"]
            })

    # Unlimited coverage
    req = get_req(visa, "insurance.unlimited_coverage")
    if req and req["value"] == True:
        limit = product_spec(product, "overall_limit")
        unlimited = product_spec(product, "unlimited")
        if unlimited == True:
            pass
        elif limit is None and unlimited is None:
            if status == "GREEN":
                status = "UNKNOWN"
            missing.append("specs.overall_limit or specs.unlimited")
        elif unlimited == False or (limit is not None and limit < 10000000):
            status = "RED"
            reasons.append({
                "text": f"Unlimited coverage required, product has limit of {limit}",
                "evidence": req["evidence"]
            })

    # No co-payment
    req = get_req(visa, "insurance.no_copayment")
    if req and req["value"] == True:
        copay = product_spec(product, "copay")
        if copay is None:
            if status == "GREEN":
                status = "UNKNOWN"
            missing.append("specs.copay")
        elif copay == True:
            status = "RED"
            reasons.append({
                "text": "No co-payments required, product has co-payments",
                "evidence": req["evidence"]
            })

    # No moratorium/waiting period
    req = get_req(visa, "insurance.no_moratorium")
    if req and req["value"] == True:
        moratorium = product_spec(product, "moratorium_days")
        if moratorium is None:
            if status == "GREEN":
                status = "UNKNOWN"
            missing.append("specs.moratorium_days")
        elif moratorium > 0:
            status = "RED"
            reasons.append({
                "text": f"No moratorium required, product has {moratorium} day waiting period",
                "evidence": req["evidence"]
            })


    # Minimum coverage
    req = get_req(visa, "insurance.min_coverage")
    if req:
        limit = product_spec(product, "overall_limit")
        if limit is None:
            status = "UNKNOWN"
            missing.append("specs.overall_limit")
        elif limit < req["value"]:
            status = "RED"
            reasons.append({
                "text": f"Minimum coverage {req['value']} required, product has {limit}",
                "evidence": req["evidence"]
            })

    # Malta: no monthly payments
    req = get_req(visa, "insurance.monthly_payments_accepted")
    if req and req["value"] == False:
        cadence = product_spec(product, "payment_cadence")
        if cadence is None:
            status = "UNKNOWN"
            missing.append("specs.payment_cadence")
        elif cadence in ["monthly", "every_4_weeks"]:
            status = "RED"
            reasons.append({
                "text": "Monthly payments not accepted by visa authority",
                "evidence": req["evidence"]
            })

    # Costa Rica full period rule -> YELLOW if monthly
    req = get_req(visa, "insurance.must_cover_full_period")
    if req and req["value"] == True:
        cadence = product_spec(product, "payment_cadence")
        if cadence in ["monthly", "every_4_weeks"]:
            if status == "GREEN":
                status = "YELLOW"
            reasons.append({
                "text": "Visa requires coverage for full legal stay, monthly subscriptions can be cancelled",
                "evidence": req["evidence"]
            })

    if status == "GREEN" and missing:
        status = "UNKNOWN"

    return {
        "visa_id": visa["id"],
        "product_id": product["id"],
        "status": status,
        "reasons": reasons,
        "missing": missing
    }

for visa in visas:
    for product in products:
        result = evaluate(visa, product)
        out = MAPPINGS / f"{visa['id']}__{product['id']}.json"
        out.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print("Built", out)
