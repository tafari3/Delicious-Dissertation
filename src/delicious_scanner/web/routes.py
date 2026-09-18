from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from delicious_scanner.db import get_db
from delicious_scanner.models import Project, Scan, Target
from delicious_scanner.services.preflight import run_preflight

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


def stats(db: Session) -> dict[str, int]:
    return {
        "projects": db.scalar(select(func.count(Project.id))) or 0,
        "targets": db.scalar(select(func.count(Target.id))) or 0,
        "scans": db.scalar(select(func.count(Scan.id))) or 0,
    }


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    projects = db.scalars(select(Project).order_by(Project.created_at.desc()).limit(8)).all()
    scans = db.scalars(select(Scan).order_by(Scan.created_at.desc()).limit(8)).all()
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {"projects": projects, "scans": scans, "stats": stats(db), "page": "dashboard"},
    )


@router.get("/projects", response_class=HTMLResponse)
def project_list(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    projects = db.scalars(select(Project).order_by(Project.created_at.desc())).all()
    return templates.TemplateResponse(
        request, "projects.html", {"projects": projects, "stats": stats(db), "page": "projects"}
    )


@router.post("/projects")
def create_project(
    name: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)
) -> RedirectResponse:
    clean = name.strip()
    if not clean:
        raise HTTPException(400, "Project name is required")
    project = Project(name=clean[:120], description=description.strip()[:4000])
    db.add(project)
    db.commit()
    db.refresh(project)
    return RedirectResponse(f"/projects/{project.id}", status_code=303)


@router.get("/projects/{project_id}", response_class=HTMLResponse)
def project_detail(
    project_id: int, request: Request, db: Session = Depends(get_db)
) -> HTMLResponse:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(404, "Project not found")
    targets = db.scalars(
        select(Target).where(Target.project_id == project_id).order_by(Target.created_at.desc())
    ).all()
    scans = db.scalars(
        select(Scan).where(Scan.project_id == project_id).order_by(Scan.created_at.desc())
    ).all()
    return templates.TemplateResponse(
        request,
        "project_detail.html",
        {"project": project, "targets": targets, "scans": scans, "page": "projects"},
    )


@router.post("/projects/{project_id}/targets")
def create_target(
    project_id: int,
    name: str = Form(...),
    scheme: str = Form("https"),
    host: str = Form(...),
    port: int = Form(443),
    base_path: str = Form("/"),
    environment_class: str = Form("controlled-cloud"),
    authorisation_reference: str = Form(""),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    if db.get(Project, project_id) is None:
        raise HTTPException(404, "Project not found")
    if scheme not in {"http", "https"}:
        raise HTTPException(400, "Unsupported scheme")
    target = Target(
        project_id=project_id,
        name=name.strip()[:120],
        scheme=scheme,
        host=host.strip().lower()[:255],
        port=port,
        base_path=(base_path.strip() or "/")[:255],
        environment_class=environment_class,
        authorisation_reference=authorisation_reference.strip()[:255] or None,
    )
    db.add(target)
    db.commit()
    return RedirectResponse(f"/projects/{project_id}", status_code=303)


@router.get("/targets/{target_id}/preflight", response_class=HTMLResponse)
def preflight(
    target_id: int, request: Request, profile: str = "safe-read-only", db: Session = Depends(get_db)
) -> HTMLResponse:
    target = db.get(Target, target_id)
    if target is None:
        raise HTTPException(404, "Target not found")
    return templates.TemplateResponse(
        request,
        "preflight.html",
        {
            "target": target,
            "result": run_preflight(target, profile),
            "profile": profile,
            "page": "projects",
        },
    )


@router.post("/targets/{target_id}/scans")
def create_scan(
    target_id: int, profile: str = Form("safe-read-only"), db: Session = Depends(get_db)
) -> RedirectResponse:
    target = db.get(Target, target_id)
    if target is None:
        raise HTTPException(404, "Target not found")
    result = run_preflight(target, profile)
    scan = Scan(
        project_id=target.project_id,
        target_id=target.id,
        profile=profile,
        state="BLOCKED" if not result.ok else "PLANNED",
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return RedirectResponse(f"/scans/{scan.id}", status_code=303)


@router.get("/scans/{scan_id}", response_class=HTMLResponse)
def scan_detail(scan_id: int, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    scan = db.get(Scan, scan_id)
    if scan is None:
        raise HTTPException(404, "Scan not found")
    return templates.TemplateResponse(
        request,
        "scan_detail.html",
        {"scan": scan, "result": run_preflight(scan.target, scan.profile), "page": "scans"},
    )
