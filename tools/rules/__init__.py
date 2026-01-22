"""Compliance rules package."""
from tools.rules.mandatory import MandatoryInsuranceRule
from tools.rules.travel_insurance import TravelInsuranceAcceptedRule
from tools.rules.jurisdiction import AuthorizedInSpainRule
from tools.rules.deductible import NoDeductibleRule
from tools.rules.copayment import NoCopaymentRule
from tools.rules.moratorium import NoMoratoriumRule
from tools.rules.coverage import (
    ComprehensiveCoverageRule,
    CoversPublicHealthSystemRisksRule,
    UnlimitedCoverageRule,
    MinimumCoverageRule,
)
from tools.rules.payment import MonthlyPaymentsAcceptedRule, MustCoverFullPeriodRule

__all__ = [
    "MandatoryInsuranceRule",
    "TravelInsuranceAcceptedRule",
    "AuthorizedInSpainRule",
    "NoDeductibleRule",
    "NoCopaymentRule",
    "NoMoratoriumRule",
    "ComprehensiveCoverageRule",
    "CoversPublicHealthSystemRisksRule",
    "UnlimitedCoverageRule",
    "MinimumCoverageRule",
    "MonthlyPaymentsAcceptedRule",
    "MustCoverFullPeriodRule",
]
