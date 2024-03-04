from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Prompt(Base):
    __tablename__ = "prompt"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    prompt = Column(String, nullable=False)
    negative_prompt = Column(String, nullable=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    guidance_scale = Column(Integer)
    num_inference_steps = Column(Integer, nullable=False)

    user = relationship("User", back_populates="prompts")
    images = relationship("Image", back_populates="prompt")