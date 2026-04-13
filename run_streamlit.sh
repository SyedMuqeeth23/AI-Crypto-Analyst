#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if [ -x ".venv/bin/python" ]; then
  .venv/bin/python -m streamlit run app.py
else
  echo "Error: virtual environment not found at .venv/bin/python"
  exit 1
fi
