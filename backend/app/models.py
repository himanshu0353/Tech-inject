import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="customer")  # "admin" or "customer"
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    access_level = Column(String, default="free")  # "free" or "premium"
    status = Column(String, default="draft")        # "draft" or "published"
    version = Column(String, default="1.0.0")
    
    props_json = Column(JSON, nullable=True)          # List of prop definitions
    dependencies_json = Column(JSON, nullable=True)   # List of dependencies/packages required
    preview_data_json = Column(JSON, nullable=True)   # Preview variant configs
    source_files_json = Column(JSON, nullable=False)  # Dict of filename -> code content

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
