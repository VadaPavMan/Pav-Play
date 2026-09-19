#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

PYTHON=".venv/bin/python"
OUTPUT_DIR="dist"

if [[ ! -x "$PYTHON" ]]; then
    echo "ERROR: .venv/bin/python was not found."
    exit 1
fi

if [[ ! -f "assets/nav/appicon.png" ]]; then
    echo "ERROR: assets/appicon.png was not found."
    echo "Create assets/appicon.png for the Linux executable icon."
    exit 1
fi

rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

"$PYTHON" -m nuitka \
    --mode=onefile \
    --enable-plugin=pyside6 \
    --include-qt-plugins=multimedia,networkinformation,platforminputcontexts,imageformats \
    --include-data-dir=assets=assets \
    --linux-onefile-icon=assets/nav/appicon.png \
    --output-dir="$OUTPUT_DIR" \
    --output-filename=PavPlay.bin \
    --product-name=PavPlay \
    --file-description="Pav Play Media Player" \
    src/main.py

echo
echo "======================================"
echo "Pav Play Linux build completed."
echo "Output: $OUTPUT_DIR/PavPlay.bin"
echo "======================================"