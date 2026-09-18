from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from delicious_scanner.db import get_db
from delicious_scanner.models import Finding, Project, Scan, Target
from delicious_scanner.services.preflight import run_preflight
from delicious_scanner.services.reports import report_bytes
from delicious_scanner.services.scanner import run_full_scan

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


def _stats(db: Session) -> dict[str, int]:
    return {
        "projects": db.scalar(select(func.count(Project.id))) or 0,
        "targets": db.scalar(select(func.count(Target.id))) or 0,
        "scans": db.scalar(select(func.count(Scan.id))) or 0,
        "findings": db.scalar(select(func.count(Finding.id))) or 0,
        "high": db.scalar(
            select(func.count(Finding.id)).where(Finding.severity.in_(["critical", "high"]))
        )
        or 0,
    }


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    projects = db.scalars(select(Project).order_by(Project.created_at.desc()).limit(6)).all()
    scans = db.scalars(
        select(Scan).options(selectinload(Scan.target)).order_by(Scan.created_at.desc()).limit(8)
    ).all()
    findings = db.scalars(select(Finding).order_by(Finding.created_at.desc()).limit(8)).all()
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "projects": projects,
            "scans": scans,
            "findings": findings,
            "stats": _stats(db),
            "page": "dashboard",
        },
    )


@router.get("/projects", response_class=HTMLResponse)
def project_list(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    projects = db.scalars(select(Project).order_by(Project.created_at.desc())).all()
    return templates.TemplateResponse(
        request,
        "projects.html",
        {"projects": projects, "stats": _stats(db), "page": "projects"},
    )


@router.post("/projects")
def create_project(
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    clean_name = name.strip()
    if not clean_name:
        raise HTTPException(400, "System group name is required")
    project = Project(name=clean_name[:120], description=description.strip()[:4000])
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
        raise HTTPException(404, "System group not found")
    targets = db.scalars(
        select(Target).where(Target.project_id == project_id).order_by(Target.created_at.desc())
    ).all()
    scans = db.scalars(
        select(Scan)
        .options(selectinload(Scan.target))
        .where(Scan.project_id == project_id)
        .order_by(Scan.created_at.desc())
        .limit(20)
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
    environment_class: str = Form("authorised-government"),
    authorisation_reference: str = Form(""),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(404, "System group not found")
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
        authorisation_reference=(authorisation_reference.strip()[:255] or None),
    )
    db.add(target)
    db.commit()
    db.refresh(target)
    return RedirectResponse(f"/targets/{target.id}/preflight", status_code=303)


@router.get("/targets/{target_id}/preflight", response_class=HTMLResponse)
def preflight(
    target_id: int,
    request: Request,
    profile: str = "safe-read-only",
    db: Session = Depends(get_db),
) -> HTMLResponse:
    target = db.get(Target, target_id)
    if target is None:
        raise HTTPException(404, "System not found")
    result = run_preflight(target, profile)
    return templates.TemplateResponse(
        request,
        "preflight.html",
        {"target": target, "result": result, "profile": profile, "page": "projects"},
    )


@router.post("/targets/{target_id}/scan/full")
def full_scan(target_id: int, db: Session = Depends(get_db)) -> RedirectResponse:
    target = db.get(Target, target_id)
    if target is None:
        raise HTTPException(404, "System not found")
    preflight = run_preflight(target, "safe-read-only")
    scan = Scan(
        project_id=target.project_id,
        target_id=target.id,
        profile="safe-read-only",
        state="PLANNED" if preflight.ok else "BLOCKED",
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    if preflight.ok:
        run_full_scan(db, scan, target)
    else:
        scan.error_message = "Preflight blocked: authorisation/scope requirements are incomplete."
        db.commit()
    return RedirectResponse(f"/scans/{scan.id}", status_code=303)


@router.get("/scans/{scan_id}", response_class=HTMLResponse)
def scan_detail(scan_id: int, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    scan = db.scalar(
        select(Scan)
        .options(selectinload(Scan.target), selectinload(Scan.findings))
        .where(Scan.id == scan_id)
    )
    if scan is None:
        raise HTTPException(404, "Assessment not found")
    severity_counts: dict[str, int] = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for finding in scan.findings:
        severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1
    return templates.TemplateResponse(
        request,
        "scan_detail.html",
        {
            "scan": scan,
            "severity_counts": severity_counts,
            "page": "scans",
        },
    )


@router.get("/scans/{scan_id}/report/{fmt}")
def download_report(scan_id: int, fmt: str, db: Session = Depends(get_db)) -> Response:
    scan = db.scalar(
        select(Scan)
        .options(selectinload(Scan.target), selectinload(Scan.findings))
        .where(Scan.id == scan_id)
    )
    if scan is None:
        raise HTTPException(404, "Assessment not found")
    if scan.state not in {"COMPLETED", "ERROR"}:
        raise HTTPException(409, "Assessment is not reportable yet")
    try:
        content, media_type = report_bytes(scan, fmt)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    filename = f"delicious-scan-{scan.id}.{fmt}"
    return Response(
        content,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
