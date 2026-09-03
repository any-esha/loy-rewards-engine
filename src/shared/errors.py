class LoyaltyError(Exception):
    """Base class for domain errors in the loyalty rules engine."""


class InvalidEarnRequestError(LoyaltyError):
    """Raised when an earn request has invalid amount, tier, or member."""


class InvalidRedemptionRequestError(LoyaltyError):
    """Raised when a redemption request cannot be processed."""


class InsufficientBalanceError(InvalidRedemptionRequestError):
    """Raised when a redemption costs more points than are available."""
