from __future__ import annotations

from collections.abc import Awaitable, Callable
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import Response

from delicious_scanner import __version__
from delicious_scanner.api import router as api_router
from delicious_scanner.auth import (
    COOKIE_NAME,
    credentials_valid,
    make_session_cookie,
    verify_session_cookie,
)
from delicious_scanner.config import settings
from delicious_scanner.logging_config import configure_logging
from delicious_scanner.web.routes import router as web_router

configure_logging(settings.log_level)

if settings.auth_enabled and (
    not settings.auth_username or not settings.auth_password_hash or not settings.session_secret
):
    raise RuntimeError("Authentication is enabled but credentials/session secret are incomplete")

app = FastAPI(
    title="Delicious Scanner",
    version=__version__,
    description="Safe, reproducible API security research scanner.",
    docs_url="/docs",
    redoc_url=None,
)
static_dir = Path(__file__).parent / "web" / "static"
templates = Jinja2Templates(directory=str(Path(__file__).parent / "web" / "templates"))
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.middleware("http")
async def authentication_and_headers(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    public_paths = {"/health", "/api/health", "/login"}
    path = request.url.path
    is_public = path in public_paths or path.startswith("/static/")

    if settings.auth_enabled and not is_public:
        username = verify_session_cookie(request.cookies.get(COOKIE_NAME))
        if username != settings.auth_username:
            if path.startswith("/api/") or path in {"/openapi.json", "/docs"}:
                response: Response = JSONResponse(
                    {"detail": "Authentication required"}, status_code=401
                )
            else:
                next_path = request.url.path
                if request.url.query:
                    next_path += "?" + request.url.query
                response = RedirectResponse(f"/login?next={next_path}", status_code=303)
            response.headers["Cache-Control"] = "no-store"
            return response

    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/login")
def login_page(request: Request, next: str = "/") -> Response:
    if (
        settings.auth_enabled
        and verify_session_cookie(request.cookies.get(COOKIE_NAME)) == settings.auth_username
    ):
        return RedirectResponse("/", status_code=303)
    safe_next = next if next.startswith("/") and not next.startswith("//") else "/"
    return templates.TemplateResponse(
        request,
        "login.html",
        {"error": None, "next_path": safe_next},
    )


@app.post("/login")
def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    next: str = Form("/"),
) -> Response:
    safe_next = next if next.startswith("/") and not next.startswith("//") else "/"
    if not settings.auth_enabled or not credentials_valid(username, password):
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "Invalid username or password.", "next_path": safe_next},
            status_code=401,
        )

    response = RedirectResponse(safe_next, status_code=303)
    response.set_cookie(
        COOKIE_NAME,
        make_session_cookie(username),
        max_age=settings.session_ttl_seconds,
        httponly=True,
        secure=settings.secure_cookies,
        samesite="lax",
        path="/",
    )
    return response


@app.post("/logout")
def logout() -> Response:
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie(COOKIE_NAME, path="/")
    return response


app.include_router(api_router)
app.include_router(web_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "service": "delicious-scanner", "version": __version__}
