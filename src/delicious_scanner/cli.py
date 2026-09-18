import json
from pathlib import Path
import typer
from alembic import command
from alembic.config import Config
from delicious_scanner import __version__
from delicious_scanner.config import settings
app=typer.Typer(no_args_is_help=True,help="Delicious Dissertation scanner operator CLI.")
@app.command()
def version()->None:typer.echo(__version__)
@app.command()
def health()->None:
    p=settings.database_path; typer.echo(json.dumps({"status":"healthy","version":__version__,"database":str(p) if p else settings.database_url,"database_parent_exists":bool(p is None or p.parent.exists()),"target_network_execution":"locked-until-P4"},indent=2))
@app.command("init-db")
def init_db()->None:
    p=settings.database_path
    if p is not None: Path(p).parent.mkdir(parents=True,exist_ok=True)
    command.upgrade(Config("alembic.ini"),"head"); typer.echo("Database migrated to head.")
