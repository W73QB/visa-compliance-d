"""Rule: Check the insurer holds a license to operate in the European Union."""
from tools.rules.base import Rule, RuleResult, get_req, product_spec


class EuLicensedInsurerRule(Rule):
    """Check the policy is issued by an insurer licensed in the European Union.

    Bulgaria's long-stay (D) visa requires the insurance policy to be "issued by
    an Insurance Company with a license to carry out insurance activities on the
    territory of the European Union". A product is only credited for this when its
    evidence documents that the insurer holds an EU insurance license; otherwise
    the status is UNKNOWN rather than an assumption that any provider qualifies.
    The key is generic so other EU member-state routes with the same clause can
    reuse it.
    """

    name = "EuLicensedInsurer"

    def check(self, visa, product):
        req = get_req(visa, "insurance.eu_licensed_insurer")
        if not req or req["value"] is not True:
            return None

        lic = product_spec(product, "eu_licensed_insurer")
        if lic is None:
            return RuleResult(
                status="UNKNOWN",
                missing=["specs.eu_licensed_insurer"]
            )
        if lic is False:
            return RuleResult(
                status="RED",
                reasons=[{
                    "text": "Policy not documented as issued by an insurer licensed in the European Union",
                    "evidence": req["evidence"]
                }]
            )
        return None
