#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
FRONTEND_DIR="${ROOT_DIR}/frontend"
PYTHON_BIN="${PYTHON_BIN:-python3}"
APP_DIR="${HOME}/.local/share/applications"
BIN_DIR="${HOME}/.local/bin"
STATE_DIR="${HOME}/.local/share/jarvis"
DESKTOP_FILE="${APP_DIR}/jarvis.desktop"
LAUNCHER_FILE="${BIN_DIR}/jarvis"
PROFILE_FILE="${STATE_DIR}/install-profile"

INSTALL_PROFILE="desktop"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --full)
      INSTALL_PROFILE="full"
      shift
      ;;
    --profile)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for --profile" >&2
        exit 1
      fi
      INSTALL_PROFILE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Usage: $0 [--profile desktop|local-ai|full] [--full]" >&2
      exit 1
      ;;
  esac
done

case "${INSTALL_PROFILE}" in
  desktop)
    REQUIREMENTS_FILE="requirements-desktop.txt"
    ;;
  local-ai)
    REQUIREMENTS_FILE="requirements-local-ai.txt"
    ;;
  full)
    REQUIREMENTS_FILE="requirements.txt"
    ;;
  *)
    echo "Unsupported install profile: ${INSTALL_PROFILE}" >&2
    echo "Supported profiles: desktop, local-ai, full" >&2
    exit 1
    ;;
esac

mkdir -p "${APP_DIR}" "${BIN_DIR}" "${STATE_DIR}"

cd "${ROOT_DIR}"

if [[ -d "${ROOT_DIR}/.venv" ]]; then
  VENV_DIR="${ROOT_DIR}/.venv"
elif [[ -d "${ROOT_DIR}/venv" ]]; then
  VENV_DIR="${ROOT_DIR}/venv"
else
  VENV_DIR="${ROOT_DIR}/.venv"
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

"${VENV_DIR}/bin/python" -m pip install --upgrade pip setuptools wheel
"${VENV_DIR}/bin/pip" install -r "${REQUIREMENTS_FILE}"

if [[ "${INSTALL_PROFILE}" == "local-ai" || "${INSTALL_PROFILE}" == "full" ]]; then
  "${VENV_DIR}/bin/python" "${ROOT_DIR}/scripts/manage_local_ai.py" prepare || true
fi

cd "${FRONTEND_DIR}"
npm ci
npm run build

cd "${ROOT_DIR}"
chmod +x scripts/run_jarvis_desktop.sh

cat > "${LAUNCHER_FILE}" <<EOF
#!/usr/bin/env bash
exec "${ROOT_DIR}/scripts/run_jarvis_desktop.sh"
EOF
chmod +x "${LAUNCHER_FILE}"

printf '%s\n' "${INSTALL_PROFILE}" > "${PROFILE_FILE}"

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=JARVIS
Comment=Local AI Workstation
Exec=${LAUNCHER_FILE}
Icon=${ROOT_DIR}/frontend/public/icon.png
Terminal=false
Categories=Development;Utility;
StartupNotify=true
EOF

update-desktop-database "${APP_DIR}" >/dev/null 2>&1 || true

echo "JARVIS installed successfully."
echo "Install profile: ${INSTALL_PROFILE}"
echo "Launcher: ${LAUNCHER_FILE}"
echo "Desktop entry: ${DESKTOP_FILE}"
