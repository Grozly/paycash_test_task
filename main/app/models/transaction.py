import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

from app.config.database import Base
from app.models.user import User


class Transaction(Base):
    __tablename__ = "transactions"

    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(15), nullable=False)
    amount = Column(Float, nullable=False, default=0.0)
    user_id = Column(Integer, ForeignKey(User.__tablename__ + ".id"))
    timestamp = Column(
        DateTime, server_default=func.now(), onupdate=func.current_timestamp()
    )

    user: Mapped["User"] = relationship(back_populates="transactions")
