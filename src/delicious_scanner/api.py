from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from delicious_scanner import __version__
from delicious_scanner.db import get_db
from delicious_scanner.models import Project
router=APIRouter(prefix="/api")
@router.get("/health")
def health()->dict[str,str]:return {"status":"healthy","service":"delicious-scanner","version":__version__}
@router.get("/projects")
def projects(db:Session=Depends(get_db))->list[dict[str,object]]:
    items=db.scalars(select(Project).order_by(Project.created_at.desc())).all()
    return [{"id":x.id,"name":x.name,"description":x.description,"created_at":x.created_at.isoformat()} for x in items]
