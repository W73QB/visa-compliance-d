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


class AuthorizedInColombiaRule(Rule):
    """Check if the policy provides coverage in Colombian territory.

    Colombia's digital nomad visa requires a health policy with coverage in the
    national territory. We only know a product satisfies this when its evidence
    documents Colombia (CO) coverage; otherwise the status is UNKNOWN rather than
    an assumption that a worldwide or foreign policy is valid in Colombia.
    """

    name = "AuthorizedInColombia"

    def check(self, visa, product):
        req = get_req(visa, "insurance.authorized_in_colombia")
        if not req or req["value"] is not True:
            return None

        country = visa.get("id", "").upper()[:2]
        if country != "CO":
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
                    "text": "Policy does not document coverage in Colombian territory",
                    "evidence": req["evidence"]
                }]
            )
        return None


class AuthorizedInCroatiaRule(Rule):
    """Check if the policy covers the territory of the Republic of Croatia.

    Croatia's digital-nomad temporary stay requires that the insurance cover the
    territory of the Republic of Croatia. A product is only credited for this when
    its evidence documents Croatia (HR) coverage; otherwise the status is UNKNOWN
    rather than an assumption that a foreign/domestic policy is valid in Croatia.
    """

    name = "AuthorizedInCroatia"

    def check(self, visa, product):
        req = get_req(visa, "insurance.authorized_in_croatia")
        if not req or req["value"] is not True:
            return None

        country = visa.get("id", "").upper()[:2]
        if country != "HR":
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
                    "text": "Policy does not document coverage in the territory of Croatia",
                    "evidence": req["evidence"]
                }]
            )
        return None


class AuthorizedInCyprusRule(Rule):
    """Check if the policy is health insurance valid for medical care in Cyprus.

    Cyprus's digital nomad scheme requires a certificate of health insurance for
    medical care (the "Plan A" category) covering inpatient and outpatient care in
    Cyprus. A product is only credited for this when its evidence documents Cyprus
    (CY) coverage; otherwise the status is UNKNOWN rather than an assumption that a
    domestic or foreign policy is valid in Cyprus.
    """

    name = "AuthorizedInCyprus"

    def check(self, visa, product):
        req = get_req(visa, "insurance.authorized_in_cyprus")
        if not req or req["value"] is not True:
            return None

        country = visa.get("id", "").upper()[:2]
        if country != "CY":
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
                    "text": "Policy does not document health insurance valid in Cyprus",
                    "evidence": req["evidence"]
                }]
            )
        return None
