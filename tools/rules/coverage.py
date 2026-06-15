"""Coverage-related rules."""
from tools.rules.base import Rule, RuleResult, get_req, product_spec

# Fixed conversion rates to EUR, pinned for snapshot reproducibility
# (mid-2026 reference values; intentionally static, never fetched live, so a
# given snapshot always evaluates a min_coverage threshold the same way).
FX_TO_EUR = {
    "EUR": 1.0,
    "USD": 0.92,
    "GBP": 1.17,
    "JPY": 0.0061,
    "KRW": 0.00069,
    "ISK": 0.0066,
}


class ComprehensiveCoverageRule(Rule):
    """Check if comprehensive coverage is required and provided."""
    
    name = "ComprehensiveCoverage"
    
    def check(self, visa, product):
        req = get_req(visa, "insurance.comprehensive")
        if not req or req["value"] is not True:
            return None
        
        comprehensive = product_spec(product, "comprehensive")
        if comprehensive is None:
            return RuleResult(
                status="UNKNOWN",
                missing=["specs.comprehensive"]
            )
        if comprehensive is False:
            return RuleResult(
                status="RED",
                reasons=[{
                    "text": "Comprehensive coverage required",
                    "evidence": req["evidence"]
                }]
            )
        return None


class CoversPublicHealthSystemRisksRule(Rule):
    """Check if product covers risks insured by public health system."""
    
    name = "CoversPublicHealthSystemRisks"
    
    def check(self, visa, product):
        req = get_req(visa, "insurance.covers_public_health_system_risks")
        if not req or req["value"] is not True:
            return None
        
        covers = product_spec(product, "covers_public_health_system_risks")
        if covers is None:
            return RuleResult(
                status="UNKNOWN",
                missing=["specs.covers_public_health_system_risks"]
            )
        if covers is False:
            return RuleResult(
                status="RED",
                reasons=[{
                    "text": "Visa requires coverage of public health system risks",
                    "evidence": req["evidence"]
                }]
            )
        return None


class UnlimitedCoverageRule(Rule):
    """Check if unlimited coverage is required."""
    
    name = "UnlimitedCoverage"
    
    def check(self, visa, product):
        req = get_req(visa, "insurance.unlimited_coverage")
        if not req or req["value"] is not True:
            return None
        
        limit = product_spec(product, "overall_limit")
        unlimited = product_spec(product, "unlimited")
        
        if unlimited is True:
            return None
        
        if limit is None and unlimited is None:
            return RuleResult(
                status="UNKNOWN",
                missing=["specs.overall_limit or specs.unlimited"]
            )
        
        if unlimited is False or (limit is not None and limit < 10000000):
            return RuleResult(
                status="RED",
                reasons=[{
                    "text": f"Unlimited coverage required, product has limit of {limit}",
                    "evidence": req["evidence"]
                }]
            )
        return None


class MinimumCoverageRule(Rule):
    """Check if minimum coverage requirement is met."""
    
    name = "MinimumCoverage"
    
    def check(self, visa, product):
        req = get_req(visa, "insurance.min_coverage")
        if not req:
            return None
        
        limit = product_spec(product, "overall_limit")
        if limit is None:
            return RuleResult(
                status="UNKNOWN",
                missing=["specs.overall_limit"]
            )

        # Compare like-for-like. When the requirement states a currency and the
        # product limit has one too, convert both to EUR using fixed rates so a
        # large threshold in one currency (e.g. JPY 10,000,000) is not falsely
        # judged against a smaller raw number in another (e.g. USD 250,000).
        # When no currency is given, fall back to the historical raw compare.
        threshold = req["value"]
        req_ccy = req.get("currency")
        prod_ccy = product_spec(product, "currency")
        limit_cmp, threshold_cmp = limit, threshold
        if req_ccy in FX_TO_EUR and prod_ccy in FX_TO_EUR:
            limit_cmp = limit * FX_TO_EUR[prod_ccy]
            threshold_cmp = threshold * FX_TO_EUR[req_ccy]

        if limit_cmp < threshold_cmp:
            unit = f" {req_ccy}" if req_ccy else ""
            return RuleResult(
                status="RED",
                reasons=[{
                    "text": f"Minimum coverage {threshold}{unit} required, product has {limit} {prod_ccy or ''}".strip(),
                    "evidence": req["evidence"]
                }]
            )
        return None
