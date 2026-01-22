"""Rule: Check no copayment requirement."""
from tools.rules.base import Rule, RuleResult, get_req, product_spec


class NoCopaymentRule(Rule):
    """Check that product has no co-payments."""
    
    name = "NoCopayment"
    
    def check(self, visa, product):
        req = get_req(visa, "insurance.no_copayment")
        if not req or req["value"] is not True:
            return None
        
        copay = product_spec(product, "copay")
        if copay is None:
            return RuleResult(
                status="UNKNOWN",
                missing=["specs.copay"]
            )
        if copay is True:
            return RuleResult(
                status="RED",
                reasons=[{
                    "text": "No co-payments required, product has co-payments",
                    "evidence": req["evidence"]
                }]
            )
        return None
