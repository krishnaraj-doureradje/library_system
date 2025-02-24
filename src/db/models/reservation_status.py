from sqlmodel import Field, SQLModel


class ReservationStatus(SQLModel, table=True):
    __tablename__ = "reservation_status"

    id: int | None = Field(default=None, primary_key=True, index=True, nullable=False)
    name: str = Field(unique=True, nullable=False, max_length=32)

    def __repr__(self) -> str:
        return f"<ReservationStatus(id={self.id}, author_id={self.name})>"
