from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    prompt_id = Column(Integer, ForeignKey("prompt.id"), nullable=False)
    filename = Column(String, nullable=False)
    separater = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    uuid = Column(String, nullable=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    is_community = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="images")
    prompt = relationship("Prompt", back_populates="images")
