import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Component, User
from ..schemas import ComponentCreate, ComponentUpdate, ComponentDetailOut
from ..auth import require_admin

router = APIRouter(prefix="/api/admin/components", tags=["Admin Components"])

@router.post("", response_model=ComponentDetailOut)
def create_component(
    payload: ComponentCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    existing = db.query(Component).filter(Component.slug == payload.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Component slug already exists")

    comp = Component(
        slug=payload.slug,
        name=payload.name,
        description=payload.description,
        category=payload.category,
        access_level=payload.access_level,
        version=payload.version,
        status="draft",
        props_json=[p.dict() for p in (payload.props or [])],
        dependencies_json=[d.dict() for d in (payload.dependencies or [])],
        preview_data_json=payload.preview_data or {},
        source_files_json=payload.source_files
    )

    db.add(comp)
    db.commit()
    db.refresh(comp)

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
        source_files=comp.source_files_json,
        is_locked=False
    )

@router.patch("/{comp_id}", response_model=ComponentDetailOut)
def update_component(
    comp_id: int,
    payload: ComponentUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    comp = db.query(Component).filter(Component.id == comp_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Component not found")

    if payload.name is not None: comp.name = payload.name
    if payload.description is not None: comp.description = payload.description
    if payload.category is not None: comp.category = payload.category
    if payload.access_level is not None: comp.access_level = payload.access_level
    if payload.version is not None: comp.version = payload.version
    if payload.props is not None: comp.props_json = [p.dict() for p in payload.props]
    if payload.dependencies is not None: comp.dependencies_json = [d.dict() for d in payload.dependencies]
    if payload.preview_data is not None: comp.preview_data_json = payload.preview_data
    if payload.source_files is not None: comp.source_files_json = payload.source_files

    comp.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(comp)

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
        source_files=comp.source_files_json,
        is_locked=False
    )

@router.post("/{comp_id}/publish", response_model=ComponentDetailOut)
def publish_component(
    comp_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    comp = db.query(Component).filter(Component.id == comp_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Component not found")

    comp.status = "published"
    comp.published_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(comp)

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
        source_files=comp.source_files_json,
        is_locked=False
    )

@router.post("/{comp_id}/unpublish", response_model=ComponentDetailOut)
def unpublish_component(
    comp_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    comp = db.query(Component).filter(Component.id == comp_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Component not found")

    comp.status = "draft"
    db.commit()
    db.refresh(comp)

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
        source_files=comp.source_files_json,
        is_locked=False
    )

@router.delete("/{comp_id}")
def delete_component(
    comp_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    comp = db.query(Component).filter(Component.id == comp_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Component not found")

    db.delete(comp)
    db.commit()
    return {"message": f"Component '{comp.name}' deleted successfully"}
