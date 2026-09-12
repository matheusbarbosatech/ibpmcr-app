import urllib.request
import json
import sys

def check_runs():
    url = "https://api.github.com/repos/matheusbarbosatech/ibpmcr-app/actions/runs"
    req = urllib.request.Request(url, headers={"User-Agent": "Python/CheckGH"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            runs = data.get("workflow_runs", [])
            print(f"Total runs encontradas: {len(runs)}")
            for run in runs[:3]:
                print(f"\n--- Run ID: {run['id']} ---")
                print(f"Nome: {run['name']}")
                print(f"Status: {run['status']} | Conclusao: {run['conclusion']}")
                print(f"Commit: {run['head_commit']['id'][:7]} - {run['head_commit']['message'][:50]}")
                print(f"URL: {run['html_url']}")
                
                # Check jobs
                jobs_url = run["jobs_url"]
                req_jobs = urllib.request.Request(jobs_url, headers={"User-Agent": "Python/CheckGH"})
                with urllib.request.urlopen(req_jobs) as r_jobs:
                    j_data = json.loads(r_jobs.read().decode("utf-8"))
                    for j in j_data.get("jobs", []):
                        print(f"  Job: {j['name']} [{j['status']}] - {j['conclusion']}")
                        for s in j.get("steps", []):
                            if s["status"] != "completed" or s["conclusion"] != "success":
                                print(f"    * Step: {s['name']} -> {s['status']} ({s['conclusion']})")
    except Exception as e:
        print("Erro ao consultar GitHub API:", e)

if __name__ == "__main__":
    check_runs()
