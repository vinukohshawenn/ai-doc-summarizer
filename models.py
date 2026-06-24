import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = Column(String(50), nullable=False)
    user_email_id = Column(String(100), unique=True, nullable=False)
    user_status = Column(String(10), nullable=False, default="active")
    password_hash = Column(String(255), nullable=False)