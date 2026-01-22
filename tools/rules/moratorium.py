"""Rule: Check no moratorium/waiting period requirement."""
from tools.rules.base import Rule, RuleResult, get_req, product_spec


class NoMoratoriumRule(Rule):
    """Check that product has no waiting period."""
    
    name = "NoMoratorium"
    
    def check(self, visa, product):
        req = get_req(visa, "insurance.no_moratorium")
        if not req or req["value"] is not True:
            return None
        
        moratorium = product_spec(product, "moratorium_days")
        if moratorium is None:
            return RuleResult(
                status="UNKNOWN",
                missing=["specs.moratorium_days"]
            )
        if moratorium > 0:
            return RuleResult(
                status="RED",
                reasons=[{
                    "text": f"No moratorium required, product has {moratorium} day waiting period",
                    "evidence": req["evidence"]
                }]
            )
        return None
