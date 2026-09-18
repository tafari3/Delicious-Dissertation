from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from delicious_scanner.db import Base


def utcnow() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    targets: Mapped[list[Target]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    scans: Mapped[list[Scan]] = relationship(back_populates="project", cascade="all, delete-orphan")


class Target(Base):
    __tablename__ = "targets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(120))
    scheme: Mapped[str] = mapped_column(String(10))
    host: Mapped[str] = mapped_column(String(255))
    port: Mapped[int] = mapped_column(Integer)
    base_path: Mapped[str] = mapped_column(String(255), default="/")
    environment_class: Mapped[str] = mapped_column(String(40))
    authorisation_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    project: Mapped[Project] = relationship(back_populates="targets")
    scans: Mapped[list[Scan]] = relationship(back_populates="target")

    @property
    def display_url(self) -> str:
        default = (self.scheme == "https" and self.port == 443) or (
            self.scheme == "http" and self.port == 80
        )
        port = "" if default else f":{self.port}"
        path = self.base_path if self.base_path.startswith("/") else f"/{self.base_path}"
        return f"{self.scheme}://{self.host}{port}{path}"


class Scan(Base):
    __tablename__ = "scans"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    target_id: Mapped[int] = mapped_column(ForeignKey("targets.id", ondelete="CASCADE"))
    profile: Mapped[str] = mapped_column(String(50), default="safe-read-only")
    state: Mapped[str] = mapped_column(String(30), default="PLANNED")
    request_count: Mapped[int] = mapped_column(Integer, default=0)
    endpoint_count: Mapped[int] = mapped_column(Integer, default=0)
    finding_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    project: Mapped[Project] = relationship(back_populates="scans")
    target: Mapped[Target] = relationship(back_populates="scans")
    findings: Mapped[list[Finding]] = relationship(
        back_populates="scan", cascade="all, delete-orphan"
    )


class Finding(Base):
    __tablename__ = "findings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id", ondelete="CASCADE"))
    rule_id: Mapped[str] = mapped_column(String(80))
    severity: Mapped[str] = mapped_column(String(20))
    confidence: Mapped[str] = mapped_column(String(20))
    state: Mapped[str] = mapped_column(String(30), default="CONFIRMED")
    method: Mapped[str] = mapped_column(String(12), default="GET")
    endpoint: Mapped[str] = mapped_column(String(1024))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    evidence_json: Mapped[str] = mapped_column(Text, default="{}")
    remediation: Mapped[str] = mapped_column(Text, default="")
    owasp: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cwe: Mapped[str | None] = mapped_column(String(40), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    scan: Mapped[Scan] = relationship(back_populates="findings")
