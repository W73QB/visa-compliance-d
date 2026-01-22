"""Payment-related rules."""
from tools.rules.base import Rule, RuleResult, get_req, product_spec


class MonthlyPaymentsAcceptedRule(Rule):
    """Check if monthly payments are accepted."""
    
    name = "MonthlyPaymentsAccepted"
    
    def check(self, visa, product):
        req = get_req(visa, "insurance.monthly_payments_accepted")
        if not req or req["value"] is not False:
            return None
        
        cadence = product_spec(product, "payment_cadence")
        if cadence is None:
            return RuleResult(
                status="UNKNOWN",
                missing=["specs.payment_cadence"]
            )
        if cadence in ["monthly", "every_4_weeks"]:
            return RuleResult(
                status="RED",
                reasons=[{
                    "text": "Monthly payments not accepted by visa authority",
                    "evidence": req["evidence"]
                }]
            )
        return None


class MustCoverFullPeriodRule(Rule):
    """Check if policy must cover full legal stay period."""
    
    name = "MustCoverFullPeriod"
    
    def check(self, visa, product):
        req = get_req(visa, "insurance.must_cover_full_period")
        if not req or req["value"] is not True:
            return None
        
        cadence = product_spec(product, "payment_cadence")
        if cadence in ["monthly", "every_4_weeks"]:
            return RuleResult(
                status="YELLOW",
                reasons=[{
                    "text": "Visa requires coverage for full legal stay, monthly subscriptions can be cancelled",
                    "evidence": req["evidence"]
                }]
            )
        return None
