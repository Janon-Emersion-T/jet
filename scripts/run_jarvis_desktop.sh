#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
FRONTEND_DIR="${ROOT_DIR}/frontend"
VENV_PYTHON="${ROOT_DIR}/.venv/bin/python"
ELECTRON_BIN="${FRONTEND_DIR}/node_modules/.bin/electron"
API_HOST="127.0.0.1"
LOG_DIR="${ROOT_DIR}/storage/logs"

mkdir -p "${LOG_DIR}"

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

API_PORT="$("${VENV_PYTHON}" - <<'PY'
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(("127.0.0.1", 0))
    print(sock.getsockname()[1])
PY
)"
API_URL="http://${API_HOST}:${API_PORT}"
API_LOG_FILE="${LOG_DIR}/desktop-api.log"

cleanup() {
  if [[ -n "${API_PID:-}" ]] && kill -0 "${API_PID}" 2>/dev/null; then
    kill "${API_PID}" 2>/dev/null || true
    wait "${API_PID}" 2>/dev/null || true
  fi
}

trap cleanup EXIT

"${VENV_PYTHON}" -m uvicorn api_server:app --host "${API_HOST}" --port "${API_PORT}" >"${API_LOG_FILE}" 2>&1 &
API_PID=$!

for _ in $(seq 1 40); do
  if "${VENV_PYTHON}" - <<PY >/dev/null 2>&1
import urllib.request
urllib.request.urlopen("${API_URL}/", timeout=1)
PY
  then
    break
  fi

  if ! kill -0 "${API_PID}" 2>/dev/null; then
    echo "JARVIS API exited before becoming ready." >&2
    echo "Last API log output:" >&2
    tail -n 40 "${API_LOG_FILE}" >&2 || true
    exit 1
  fi

  sleep 0.5
done

if ! "${VENV_PYTHON}" - <<PY >/dev/null 2>&1
import urllib.request
urllib.request.urlopen("${API_URL}/", timeout=1)
PY
then
  echo "JARVIS API did not become ready in time." >&2
  echo "Last API log output:" >&2
  tail -n 40 "${API_LOG_FILE}" >&2 || true
  exit 1
fi

cd "${FRONTEND_DIR}"
JARVIS_API_URL="${API_URL}" "${ELECTRON_BIN}" --no-sandbox .
