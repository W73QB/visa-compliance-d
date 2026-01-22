"""Rule: Check if travel insurance is accepted."""
from tools.rules.base import Rule, RuleResult, get_req, product_spec


class TravelInsuranceAcceptedRule(Rule):
    """Check if travel insurance is accepted for this visa."""
    
    name = "TravelInsuranceAccepted"
    
    def check(self, visa, product):
        req = get_req(visa, "insurance.travel_insurance_accepted")
        if not req or req["value"] is not False:
            return None
        
        ptype = product_spec(product, "type")
        if ptype is None:
            return RuleResult(
                status="UNKNOWN",
                missing=["specs.type"]
            )
        if "travel" in str(ptype).lower():
            return RuleResult(
                status="RED",
                reasons=[{
                    "text": "Travel insurance is not accepted for this visa",
                    "evidence": req["evidence"]
                }]
            )
        return None
