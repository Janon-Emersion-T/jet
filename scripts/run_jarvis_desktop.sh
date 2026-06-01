#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
FRONTEND_DIR="${ROOT_DIR}/frontend"
VENV_PYTHON="${ROOT_DIR}/.venv/bin/python"
ELECTRON_BIN="${FRONTEND_DIR}/node_modules/.bin/electron"

if [[ ! -x "${VENV_PYTHON}" ]]; then
  echo "JARVIS Python virtual environment not found at ${VENV_PYTHON}" >&2
  echo "Run scripts/install_jarvis.sh first." >&2
  exit 1
fi

if [[ ! -x "${ELECTRON_BIN}" ]]; then
  echo "Electron binary not found at ${ELECTRON_BIN}" >&2
  echo "Run scripts/install_jarvis.sh first." >&2
  exit 1
fi

if [[ ! -f "${FRONTEND_DIR}/dist/index.html" ]]; then
  echo "Frontend build is missing at ${FRONTEND_DIR}/dist/index.html" >&2
  echo "Run scripts/install_jarvis.sh or npm run build in frontend/." >&2
  exit 1
fi

cd "${ROOT_DIR}"

cleanup() {
  if [[ -n "${API_PID:-}" ]] && kill -0 "${API_PID}" 2>/dev/null; then
    kill "${API_PID}" 2>/dev/null || true
    wait "${API_PID}" 2>/dev/null || true
  fi
}

trap cleanup EXIT

"${VENV_PYTHON}" -m uvicorn api_server:app --host 127.0.0.1 --port 8000 &
API_PID=$!

sleep 3

cd "${FRONTEND_DIR}"
"${ELECTRON_BIN}" --no-sandbox .
