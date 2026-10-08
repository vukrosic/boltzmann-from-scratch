#!/bin/bash
# Runs the seven steps, then the checks. About 4 minutes on a laptop; nothing to install.
set -e
cd "$(dirname "$0")"
for step in step1_box step2_count step3_reverse step4_share step5_air step6_anneal step7_softmax; do
  echo
  echo "=== $step.py"
  python3 $step.py
done
echo
python3 tests.py
