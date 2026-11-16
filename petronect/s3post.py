import json, sys, subprocess
d = json.load(open(sys.argv[1]))
args = ["curl", "-sS", "-w", "%{http_code}", "-o", "/tmp/s3resp.txt", "--max-time", "60", d["url"]]
for k, v in d["fields"].items():
    args += ["--form-string", f"{k}={v}"]
args += ["-F", f"file=@{d['file']};type={d['fields']['Content-Type']}"]
r = subprocess.run(args, capture_output=True, text=True)
print(r.stdout, r.stderr, open('/tmp/s3resp.txt').read()[:300])
