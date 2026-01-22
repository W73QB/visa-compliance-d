"""Rule: Check no deductible requirement."""
from tools.rules.base import Rule, RuleResult, get_req, product_spec


class NoDeductibleRule(Rule):
    """Check that product has zero deductible."""
    
    name = "NoDeductible"
    
    def check(self, visa, product):
        req = get_req(visa, "insurance.no_deductible")
        if not req or req["value"] is not True:
            return None
        
        ded = product_spec(product, "deductible.amount")
        if ded is None:
            return RuleResult(
                status="UNKNOWN",
                missing=["specs.deductible.amount"]
            )
        if ded > 0:
            return RuleResult(
                status="RED",
                reasons=[{
                    "text": f"Visa requires zero deductible but product has {ded}",
                    "evidence": req["evidence"]
                }]
            )
        return None
