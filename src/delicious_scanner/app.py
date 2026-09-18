from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from delicious_scanner import __version__
from delicious_scanner.api import router as api_router
from delicious_scanner.config import settings
from delicious_scanner.logging_config import configure_logging
from delicious_scanner.web.routes import router as web_router
configure_logging(settings.log_level)
app=FastAPI(title="Delicious Scanner",version=__version__,description="Safe, reproducible API security research scanner.")
app.mount("/static",StaticFiles(directory=Path(__file__).parent/"web"/"static"),name="static")
app.include_router(api_router); app.include_router(web_router)
@app.get("/health")
def health()->dict[str,str]:return {"status":"healthy","service":"delicious-scanner","version":__version__}
