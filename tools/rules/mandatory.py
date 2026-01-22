"""Rule: Check if insurance is mandatory for the visa."""
from tools.rules.base import Rule, RuleResult, get_req


class MandatoryInsuranceRule(Rule):
    """Check if insurance is mandatory. Returns NOT_REQUIRED if not mandatory."""
    
    name = "MandatoryInsurance"
    
    def check(self, visa, product):
        req = get_req(visa, "insurance.mandatory")
        if req and req["value"] is False:
            return RuleResult(
                status="NOT_REQUIRED",
                reasons=[{
                    "text": "Visa does not require insurance",
                    "evidence": req["evidence"]
                }],
                terminal=True
            )
        return None
