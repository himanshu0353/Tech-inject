from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, ConfigDict
import datetime

# --- User Schemas ---
class UserLogin(BaseModel):
    email: str
    password: str

class UserSignup(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    role: str
    is_premium: bool
    created_at: datetime.datetime
    token: Optional[str] = None

class UserUpdatePremium(BaseModel):
    is_premium: bool

# --- Component Schemas ---
class PropDef(BaseModel):
    name: str
    type: str
    default: Optional[str] = None
    description: str

class Dependency(BaseModel):
    name: str
    version: str
    is_dev: bool = False

class ComponentBase(BaseModel):
    name: str
    slug: str
    description: str
    category: str
    access_level: str = "free"  # "free" or "premium"
    version: str = "1.0.0"

class ComponentCreate(ComponentBase):
    props: Optional[List[PropDef]] = []
    dependencies: Optional[List[Dependency]] = []
    preview_data: Optional[Dict[str, Any]] = {}
    source_files: Dict[str, str]

class ComponentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    access_level: Optional[str] = None
    version: Optional[str] = None
    props: Optional[List[PropDef]] = None
    dependencies: Optional[List[Dependency]] = None
    preview_data: Optional[Dict[str, Any]] = None
    source_files: Optional[Dict[str, str]] = None

class ComponentSummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str
    description: str
    category: str
    access_level: str
    status: str
    version: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    published_at: Optional[datetime.datetime] = None

class ComponentDetailOut(ComponentSummaryOut):
    props: Optional[List[PropDef]] = []
    dependencies: Optional[List[Dependency]] = []
    preview_data: Optional[Dict[str, Any]] = {}
    source_files: Optional[Dict[str, str]] = None # Null if locked for premium user
    is_locked: bool = False

class InstallResponse(BaseModel):
    slug: str
    name: str
    version: str
    files: Dict[str, str]
    dependencies: List[Dependency]

class AgentPromptResponse(BaseModel):
    slug: str
    name: str
    prompt: str
