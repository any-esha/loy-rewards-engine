class LoyaltyError(Exception):
    """Base class for domain errors in the loyalty rules engine."""


class InvalidEarnRequestError(LoyaltyError):
    """Raised when an earn request has invalid amount, tier, or member."""
