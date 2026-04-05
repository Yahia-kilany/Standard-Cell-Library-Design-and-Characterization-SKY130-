#!/bin/bash
cd "$(dirname "$0")/.."   # ensure we're always at project root

for f in scripts/char_*.py; do
    module=$(basename "$f" .py)        # char_inv.py → char_inv
    python -m scripts.$module &
done
wait