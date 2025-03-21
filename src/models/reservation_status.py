from enum import StrEnum


class ReservationStatus(StrEnum):
    """Enum representing the possible statuses of a reservation."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    RETURNED = "returned"
