import re,subprocess,sys
patterns=[re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),re.compile(r"AKIA[0-9A-Z]{16}")]
proc=subprocess.run(["git","grep","-n","-I","-E","."],capture_output=True,text=True,check=True)
violations=[line for line in proc.stdout.splitlines() if any(p.search(line) for p in patterns)]
if violations: print("Potential secret material detected:",file=sys.stderr);print("\n".join(violations),file=sys.stderr);raise SystemExit(1)
print("Secret scan passed.")
