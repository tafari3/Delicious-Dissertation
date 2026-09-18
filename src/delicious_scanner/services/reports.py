from __future__ import annotations

import csv
import io
import json
from html import escape
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from delicious_scanner.models import Scan


def _report_model(scan: Scan) -> dict[str, Any]:
    severity_order = ["critical", "high", "medium", "low", "info"]
    counts = {s: 0 for s in severity_order}
    items = []
    for finding in scan.findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1
        items.append(
            {
                "rule_id": finding.rule_id,
                "severity": finding.severity,
                "confidence": finding.confidence,
                "state": finding.state,
                "method": finding.method,
                "endpoint": finding.endpoint,
                "title": finding.title,
                "description": finding.description,
                "evidence": json.loads(finding.evidence_json or "{}"),
                "remediation": finding.remediation,
                "owasp": finding.owasp,
                "cwe": finding.cwe,
            }
        )
    return {
        "report_version": "1.0",
        "scan": {
            "id": scan.id,
            "state": scan.state,
            "profile": scan.profile,
            "target": scan.target.name,
            "target_url": scan.target.display_url,
            "environment_class": scan.target.environment_class,
            "created_at": scan.created_at.isoformat(),
            "started_at": scan.started_at.isoformat() if scan.started_at else None,
            "completed_at": scan.completed_at.isoformat() if scan.completed_at else None,
            "endpoint_count": scan.endpoint_count,
            "request_count": scan.request_count,
            "finding_count": scan.finding_count,
        },
        "summary": counts,
        "findings": items,
        "limitations": [
            "This report covers the explicitly registered API target and same-authority endpoints discovered from its OpenAPI document.",
            "The default full scan is read-only and does not claim destructive, denial-of-service, lateral-movement or unrelated-network coverage.",
            "Authentication/authorisation differential testing requires approved test identities and is reported separately when configured.",
        ],
    }


def render_json(scan: Scan) -> bytes:
    return json.dumps(_report_model(scan), indent=2, ensure_ascii=False).encode()


def _csv_safe(value: object) -> str:
    text = str(value if value is not None else "")
    if text.startswith(("=", "+", "-", "@")):
        return "'" + text
    return text


def render_csv(scan: Scan) -> bytes:
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(
        ["rule_id", "severity", "confidence", "state", "method", "endpoint", "title", "remediation"]
    )
    for finding in scan.findings:
        writer.writerow(
            [
                _csv_safe(finding.rule_id),
                _csv_safe(finding.severity),
                _csv_safe(finding.confidence),
                _csv_safe(finding.state),
                _csv_safe(finding.method),
                _csv_safe(finding.endpoint),
                _csv_safe(finding.title),
                _csv_safe(finding.remediation),
            ]
        )
    return out.getvalue().encode()


def render_html(scan: Scan) -> bytes:
    model = _report_model(scan)
    summary = model["summary"]
    findings = model["findings"]
    rows = (
        "".join(
            f"<tr><td><span class='sev {escape(str(f['severity']))}'>{escape(str(f['severity']).upper())}</span></td>"
            f"<td>{escape(str(f['rule_id']))}</td><td>{escape(str(f['title']))}</td>"
            f"<td><code>{escape(str(f['method']))} {escape(str(f['endpoint']))}</code></td>"
            f"<td>{escape(str(f['remediation']))}</td></tr>"
            for f in findings
        )
        or "<tr><td colspan='5'>No findings were recorded.</td></tr>"
    )
    html = f"""<!doctype html><html><head><meta charset='utf-8'><title>Delicious Scanner Report #{scan.id}</title>
<style>
body{{font-family:Arial,sans-serif;color:#14212b;margin:40px;background:#fff}}h1{{font-size:28px}}h2{{margin-top:32px}}
.brand{{color:#087f6b;font-weight:700;letter-spacing:.08em}}.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
.card{{border:1px solid #dce4e8;border-radius:10px;padding:16px}}.card strong{{font-size:24px;display:block;margin-top:6px}}
table{{width:100%;border-collapse:collapse;font-size:12px}}th,td{{border-bottom:1px solid #e4eaed;padding:10px;text-align:left;vertical-align:top}}
th{{background:#f3f7f8}}code{{word-break:break-all}}.sev{{font-weight:700}}.sev.high,.sev.critical{{color:#b42318}}.sev.medium{{color:#b54708}}
.muted{{color:#667985}}footer{{margin-top:38px;font-size:11px;color:#71808a}}
</style></head><body><div class='brand'>DELICIOUS SECURITY RESEARCH CONSOLE</div><h1>API Security Assessment Report</h1>
<p class='muted'>Scan #{scan.id} · {escape(scan.target.name)} · {escape(scan.target.display_url)}</p>
<div class='grid'><div class='card'>Endpoints<strong>{scan.endpoint_count}</strong></div><div class='card'>Requests<strong>{scan.request_count}</strong></div>
<div class='card'>Findings<strong>{scan.finding_count}</strong></div><div class='card'>High/Critical<strong>{summary.get("high", 0) + summary.get("critical", 0)}</strong></div></div>
<h2>Executive summary</h2><p>The scan completed with state <strong>{escape(scan.state)}</strong>. The assessment used the <strong>{escape(scan.profile)}</strong> profile and remained bounded to the registered target authority.</p>
<h2>Findings</h2><table><thead><tr><th>Severity</th><th>Rule</th><th>Finding</th><th>Endpoint</th><th>Remediation</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Scope and limitations</h2><ul>{"".join("<li>" + escape(str(x)) + "</li>" for x in model["limitations"])}</ul>
<footer>Generated by Delicious Scanner v0.2 · This report is an assessment artefact, not a compliance certification.</footer></body></html>"""
    return html.encode()


def render_pdf(scan: Scan) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, rightMargin=32, leftMargin=32, topMargin=36, bottomMargin=36
    )
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Delicious Security Research Console", styles["Heading3"]),
        Paragraph(f"API Security Assessment Report · Scan #{scan.id}", styles["Title"]),
        Paragraph(f"{scan.target.name} · {scan.target.display_url}", styles["Normal"]),
        Spacer(1, 14),
    ]
    data = [
        ["State", scan.state],
        ["Profile", scan.profile],
        ["Endpoints", str(scan.endpoint_count)],
        ["Requests", str(scan.request_count)],
        ["Findings", str(scan.finding_count)],
    ]
    table = Table(data, colWidths=[100, 380])
    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
            ]
        )
    )
    story.extend([table, Spacer(1, 16), Paragraph("Findings", styles["Heading2"])])
    for finding in scan.findings:
        story.append(
            Paragraph(
                f"<b>{finding.severity.upper()}</b> · {escape(finding.title)}", styles["Heading4"]
            )
        )
        story.append(
            Paragraph(f"{escape(finding.method)} {escape(finding.endpoint)}", styles["Code"])
        )
        story.append(Paragraph(escape(finding.description), styles["BodyText"]))
        story.append(
            Paragraph("<b>Remediation:</b> " + escape(finding.remediation), styles["BodyText"])
        )
        story.append(Spacer(1, 8))
    if not scan.findings:
        story.append(Paragraph("No findings were recorded.", styles["BodyText"]))
    story.extend(
        [
            Paragraph("Scope and limitations", styles["Heading2"]),
            Paragraph(
                "The scan is bounded to the registered API target and same-authority endpoints discovered from its OpenAPI document. The default profile is read-only.",
                styles["BodyText"],
            ),
        ]
    )
    doc.build(story)
    return buffer.getvalue()


def report_bytes(scan: Scan, fmt: str) -> tuple[bytes, str]:
    if fmt == "json":
        return render_json(scan), "application/json"
    if fmt == "csv":
        return render_csv(scan), "text/csv; charset=utf-8"
    if fmt == "html":
        return render_html(scan), "text/html; charset=utf-8"
    if fmt == "pdf":
        return render_pdf(scan), "application/pdf"
    raise ValueError("Unsupported report format")
