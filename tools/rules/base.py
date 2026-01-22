"""Base classes and utilities for compliance rules."""
from abc import ABC, abstractmethod
from typing import Any, Optional, List, Dict


class RuleResult:
    """Structured result from a rule check."""
    
    def __init__(
        self,
        status: str = "GREEN",
        reasons: Optional[List[Dict]] = None,
        missing: Optional[List[str]] = None,
        terminal: bool = False
    ):
        self.status = status
        self.reasons = reasons or []
        self.missing = missing or []
        self.terminal = terminal  # If True, stop processing other rules


class Rule(ABC):
    """Base class for compliance rules."""
    
    # Human-readable name for audit logs
    name: str = "BaseRule"
    
    @abstractmethod
    def check(self, visa: dict, product: dict) -> Optional[RuleResult]:
        """
        Check if visa/product combination passes this rule.
        
        Returns:
            None if rule doesn't apply (requirement not present).
            RuleResult with status, reasons, missing fields.
        """
        pass


def get_req(visa: dict, key: str) -> Optional[dict]:
    """Get requirement by key from visa."""
    for r in visa.get("requirements", []):
        if r["key"] == key:
            return r
    return None


def product_spec(product: dict, path: str) -> Any:
    """Navigate nested product specs by dot-separated path."""
    cur = product.get("specs")
    for p in path.split("."):
        if cur is None or not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur
