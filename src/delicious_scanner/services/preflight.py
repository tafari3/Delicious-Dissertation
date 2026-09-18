from dataclasses import dataclass
from delicious_scanner.models import Target
@dataclass(frozen=True)
class PreflightResult: ok:bool; checks:tuple[tuple[str,str,bool],...]
def run_preflight(target:Target,profile:str)->PreflightResult:
    checks=[("Explicit target",target.host,bool(target.host.strip())),("Scheme",target.scheme,target.scheme in {"http","https"}),("Port",str(target.port),1<=target.port<=65535),("Profile",profile,profile in {"safe-read-only","controlled-lab-full","authorised-zchpc"})]
    operational=profile=="authorised-zchpc" or target.environment_class=="authorised-zchpc"
    checks += [("Authorisation reference",target.authorisation_reference or "Missing",bool(target.authorisation_reference)),("Mutation tests","disabled",True),("Resource-control tests","disabled",True)] if operational else [("Default mutation policy","disabled unless controlled lab",True)]
    checks += [("Network execution","locked until P4 scope engine",False)]
    return PreflightResult(ok=all(x[2] for x in checks),checks=tuple(checks))
