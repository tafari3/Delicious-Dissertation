import re
from collections.abc import Mapping
from typing import Any
CONTROL_RE=re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\x1b]")
SENSITIVE_KEYS={"authorization","proxy-authorization","cookie","set-cookie","password","token","secret","api_key","apikey","session"}
def sanitise_terminal(value:str)->str:return CONTROL_RE.sub("",value)
def redact(value:Any)->Any:
    if isinstance(value,Mapping): return {str(k):"[REDACTED]" if str(k).lower() in SENSITIVE_KEYS else redact(v) for k,v in value.items()}
    if isinstance(value,list): return [redact(v) for v in value]
    if isinstance(value,tuple): return tuple(redact(v) for v in value)
    return sanitise_terminal(value) if isinstance(value,str) else value
