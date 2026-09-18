import json,logging
from datetime import datetime,timezone
from delicious_scanner.security import redact
class JsonFormatter(logging.Formatter):
    def format(self,record:logging.LogRecord)->str:return json.dumps(redact({"ts":datetime.now(timezone.utc).isoformat(),"level":record.levelname,"logger":record.name,"message":record.getMessage()}),ensure_ascii=False)
def configure_logging(level:str="INFO")->None:
    handler=logging.StreamHandler(); handler.setFormatter(JsonFormatter()); root=logging.getLogger(); root.handlers[:]=[handler]; root.setLevel(level.upper())
