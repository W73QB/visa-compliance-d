"""Compliance evaluation engine."""
from tools.rules import (
    MandatoryInsuranceRule,
    TravelInsuranceAcceptedRule,
    AuthorizedInSpainRule,
    NoDeductibleRule,
    ComprehensiveCoverageRule,
    CoversPublicHealthSystemRisksRule,
    UnlimitedCoverageRule,
    NoCopaymentRule,
    NoMoratoriumRule,
    MinimumCoverageRule,
    MonthlyPaymentsAcceptedRule,
    MustCoverFullPeriodRule,
)

# Rule order matters - terminal rules first
RULES = [
    MandatoryInsuranceRule(),
    TravelInsuranceAcceptedRule(),
    AuthorizedInSpainRule(),
    NoDeductibleRule(),
    ComprehensiveCoverageRule(),
    CoversPublicHealthSystemRisksRule(),
    UnlimitedCoverageRule(),
    NoCopaymentRule(),
    NoMoratoriumRule(),
    MinimumCoverageRule(),
    MonthlyPaymentsAcceptedRule(),
    MustCoverFullPeriodRule(),
]


def evaluate(visa: dict, product: dict) -> dict:
    """Evaluate visa/product compliance using all rules."""
    reasons = []
    missing = []
    status = "GREEN"
    
    for rule in RULES:
        result = rule.check(visa, product)
        if result is None:
            continue
        
        # Terminal rule (e.g., NOT_REQUIRED)
        if result.terminal:
            return {
                "visa_id": visa["id"],
                "product_id": product["id"],
                "status": result.status,
                "reasons": result.reasons,
                "missing": result.missing
            }
        
        # Merge results
        reasons.extend(result.reasons)
        missing.extend(result.missing)
        
        # Status priority: RED > UNKNOWN > YELLOW > GREEN
        if result.status == "RED":
            status = "RED"
        elif result.status == "UNKNOWN" and status not in ("RED",):
            status = "UNKNOWN"
        elif result.status == "YELLOW" and status == "GREEN":
            status = "YELLOW"
    
    # Final check: missing evidence means UNKNOWN
    if status == "GREEN" and missing:
        status = "UNKNOWN"
    
    return {
        "visa_id": visa["id"],
        "product_id": product["id"],
        "status": status,
        "reasons": reasons,
        "missing": missing
    }
