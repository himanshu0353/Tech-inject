from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Component, User
from ..schemas import ComponentSummaryOut, ComponentDetailOut, InstallResponse, AgentPromptResponse
from ..auth import get_current_user_optional

router = APIRouter(prefix="/api/components", tags=["Components"])

@router.get("", response_model=List[ComponentSummaryOut])
def list_components(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    query = db.query(Component)

    # Unless user is admin, show ONLY published components
    if not user or user.role != "admin":
        query = query.filter(Component.status == "published")

    if category and category != "All":
        query = query.filter(Component.category == category)

    if search:
        search_fmt = f"%{search.lower()}%"
        query = query.filter(
            (Component.name.ilike(search_fmt)) |
            (Component.description.ilike(search_fmt)) |
            (Component.category.ilike(search_fmt))
        )

    return query.all()

@router.get("/{slug}", response_model=ComponentDetailOut)
def get_component(
    slug: str,
    user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    comp = db.query(Component).filter(Component.slug == slug).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Component not found")

    # Draft privacy: non-admin users cannot access drafts
    if comp.status == "draft" and (not user or user.role != "admin"):
        raise HTTPException(status_code=404, detail="Component not found")

    # Check premium access
    is_premium_comp = comp.access_level == "premium"
    has_premium_access = user and (user.is_premium or user.role == "admin")

    is_locked = is_premium_comp and not has_premium_access

    return ComponentDetailOut(
        id=comp.id,
        slug=comp.slug,
        name=comp.name,
        description=comp.description,
        category=comp.category,
        access_level=comp.access_level,
        status=comp.status,
        version=comp.version,
        created_at=comp.created_at,
        updated_at=comp.updated_at,
        published_at=comp.published_at,
        props=comp.props_json or [],
        dependencies=comp.dependencies_json or [],
        preview_data=comp.preview_data_json or {},
        source_files=comp.source_files_json if not is_locked else None,
        is_locked=is_locked
    )

@router.get("/{slug}/install", response_model=InstallResponse)
def get_install_payload(
    slug: str,
    user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    comp = db.query(Component).filter(Component.slug == slug).first()
    if not comp or (comp.status == "draft" and (not user or user.role != "admin")):
        raise HTTPException(status_code=404, detail="Component not found")

    if comp.access_level == "premium":
        if not user or (not user.is_premium and user.role != "admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Premium access required to install this component"
            )

    return InstallResponse(
        slug=comp.slug,
        name=comp.name,
        version=comp.version,
        files=comp.source_files_json or {},
        dependencies=comp.dependencies_json or []
    )

@router.get("/{slug}/agent-prompt", response_model=AgentPromptResponse)
def get_agent_prompt(
    slug: str,
    user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    comp = db.query(Component).filter(Component.slug == slug).first()
    if not comp or (comp.status == "draft" and (not user or user.role != "admin")):
        raise HTTPException(status_code=404, detail="Component not found")

    if comp.access_level == "premium":
        if not user or (not user.is_premium and user.role != "admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Premium access required to generate AI agent prompt for this component"
            )

    deps_str = ", ".join([d["name"] for d in (comp.dependencies_json or [])]) or "none"

    prompt_text = f"""Add the Tech Inject {comp.name} component to this React + TypeScript project.

Component Metadata:
- Slug: {comp.slug}
- Access: {comp.access_level}
- Version: {comp.version}
- Dependencies: {deps_str}

Instructions:
1. Use the official Tech Inject {comp.name} source code and style declarations.
2. Preserve the Tech Inject CSS theme variables (defined in tokens.css) and component structure.
3. Install required dependencies ({deps_str}) if not already present.
4. Integrate the component into the project layout without modifying its internal visual contracts.

Verification Steps:
- Verify TypeScript compiles without errors.
- Verify component renders and interactive states (hover/focus) respond properly.
"""

    return AgentPromptResponse(
        slug=comp.slug,
        name=comp.name,
        prompt=prompt_text
    )
