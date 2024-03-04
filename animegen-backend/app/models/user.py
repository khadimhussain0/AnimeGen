from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from passlib.context import CryptContext

# CryptContext for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String, index=True, nullable=False)
    lastname = Column(String, index=True, default="")
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    prompts = relationship("Prompt", back_populates="user")
    images = relationship("Image", back_populates="user")
    credits = relationship("Credits", back_populates="user")

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)
