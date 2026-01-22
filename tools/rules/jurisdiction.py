"""Rule: Check authorization in jurisdiction (Spain)."""
from tools.rules.base import Rule, RuleResult, get_req, product_spec


class AuthorizedInSpainRule(Rule):
    """Check if insurer is authorized to operate in Spain."""
    
    name = "AuthorizedInSpain"
    
    def check(self, visa, product):
        req = get_req(visa, "insurance.authorized_in_spain")
        if not req or req["value"] is not True:
            return None
        
        country = visa.get("id", "").upper()[:2]
        if country != "ES":
            return None
        
        jf = product_spec(product, f"jurisdiction_facts.{country}.authorized")
        if jf is None:
            return RuleResult(
                status="UNKNOWN",
                missing=[f"specs.jurisdiction_facts.{country}.authorized"]
            )
        if jf is False:
            return RuleResult(
                status="RED",
                reasons=[{
                    "text": f"Insurer not authorized to operate in {visa.get('country', 'jurisdiction')}",
                    "evidence": req["evidence"]
                }]
            )
        return None
