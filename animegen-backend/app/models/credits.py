from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Credits(Base):
    __tablename__ = "credit"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    amount = Column(Integer, default=0)

    user = relationship("User", back_populates="credits")
