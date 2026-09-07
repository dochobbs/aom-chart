"""
Automated Orchestrator for High-Thinking Replicates 2 and 3:
Runs Replicate 2, then Replicate 3 across all 10 models and 4 acute pediatric cases.
"""

import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNNER = ROOT / "run_4cases_high_thinking.py"

def run_replicate(rep):
    print(f"\n{'='*70}")
    print(f"LAUNCHING HIGH-THINKING REPLICATE {rep}")
    print(f"{'='*70}\n", flush=True)
    cmd = [sys.executable, str(RUNNER), f"--rep={rep}", "--workers=6"]
    ret = subprocess.run(cmd)
    if ret.returncode != 0:
        print(f"ERROR: Replicate {rep} failed with return code {ret.returncode}", file=sys.stderr)
        sys.exit(ret.returncode)
    print(f"\n[DONE] High-Thinking Replicate {rep} completed successfully!\n", flush=True)

if __name__ == "__main__":
    run_replicate(2)
    run_replicate(3)
    print("\nALL HIGH-THINKING REPLICATES (2 & 3) FINISHED SUCCESSFULLY!\n")
