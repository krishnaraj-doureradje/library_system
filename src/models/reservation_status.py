from enum import Enum


class ReservationStatus(str, Enum):
    """Enum representing the possible statuses of a reservation."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    RETURNED = "returned"
