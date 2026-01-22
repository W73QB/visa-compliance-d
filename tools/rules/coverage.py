"""Coverage-related rules."""
from tools.rules.base import Rule, RuleResult, get_req, product_spec


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
        if limit < req["value"]:
            return RuleResult(
                status="RED",
                reasons=[{
                    "text": f"Minimum coverage {req['value']} required, product has {limit}",
                    "evidence": req["evidence"]
                }]
            )
        return None
