from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Mapped, relationship

from app.config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    balance = Column(Float, nullable=False, default=0.0)

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")
