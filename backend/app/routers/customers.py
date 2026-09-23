from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserOut
from ..auth import require_admin

router = APIRouter(prefix="/api/admin/customers", tags=["Admin Customers"])

@router.get("", response_model=List[UserOut])
def list_customers(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return db.query(User).filter(User.role == "customer").all()

@router.post("/{user_id}/grant-premium", response_model=UserOut)
def grant_premium(
    user_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id, User.role == "customer").first()
    if not user:
        raise HTTPException(status_code=404, detail="Customer not found")

    user.is_premium = True
    db.commit()
    db.refresh(user)
    return user

@router.post("/{user_id}/revoke-premium", response_model=UserOut)
def revoke_premium(
    user_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id, User.role == "customer").first()
    if not user:
        raise HTTPException(status_code=404, detail="Customer not found")

    user.is_premium = False
    db.commit()
    db.refresh(user)
    return user
