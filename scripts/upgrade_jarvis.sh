#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
FRONTEND_DIR="${ROOT_DIR}/frontend"
STATE_DIR="${HOME}/.local/share/jarvis"
PROFILE_FILE="${STATE_DIR}/install-profile"
BRANCH=""
INSTALL_PROFILE=""
LOCAL_ONLY=false

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
    --local)
      LOCAL_ONLY=true
      shift
      ;;
    *)
      if [[ -z "${BRANCH}" ]]; then
        BRANCH="$1"
        shift
      else
        echo "Unknown option: $1" >&2
        echo "Usage: $0 [branch] [--profile desktop|full] [--full] [--local]" >&2
        exit 1
      fi
      ;;
  esac
done

if [[ -z "${BRANCH}" ]]; then
  BRANCH="$(git -C "${ROOT_DIR}" branch --show-current)"
fi

if [[ -z "${INSTALL_PROFILE}" ]] && [[ -f "${PROFILE_FILE}" ]]; then
  INSTALL_PROFILE="$(tr -d '[:space:]' < "${PROFILE_FILE}")"
fi

INSTALL_PROFILE="${INSTALL_PROFILE:-desktop}"

case "${INSTALL_PROFILE}" in
  desktop)
    REQUIREMENTS_FILE="requirements-desktop.txt"
    ;;
  full)
    REQUIREMENTS_FILE="requirements.txt"
    ;;
  *)
    echo "Unsupported install profile: ${INSTALL_PROFILE}" >&2
    echo "Supported profiles: desktop, full" >&2
    exit 1
    ;;
esac

cd "${ROOT_DIR}"

if [[ "${LOCAL_ONLY}" != true ]]; then
  if [[ -n "$(git status --porcelain)" ]]; then
    echo "Refusing to upgrade because the worktree has local changes." >&2
    echo "Commit or stash them first, then run the upgrader again, or use --local to rebuild from the current repository state." >&2
    exit 1
  fi

  git fetch origin
git checkout "${BRANCH}"
git pull --ff-only origin "${BRANCH}"
else
  if [[ -n "${BRANCH}" ]]; then
    git checkout "${BRANCH}"
  fi
  echo "Local upgrade mode enabled: rebuilding from current repository state without remote fetch/pull."
fi

if [[ -d "${ROOT_DIR}/.venv" ]]; then
  VENV_DIR="${ROOT_DIR}/.venv"
elif [[ -d "${ROOT_DIR}/venv" ]]; then
  VENV_DIR="${ROOT_DIR}/venv"
else
  VENV_DIR="${ROOT_DIR}/.venv"
  python3 -m venv "${VENV_DIR}"
fi

"${VENV_DIR}/bin/python" -m pip install --upgrade pip setuptools wheel
"${VENV_DIR}/bin/pip" install -r "${REQUIREMENTS_FILE}"

cd "${FRONTEND_DIR}"
npm ci
npm run build

cd "${ROOT_DIR}"
chmod +x scripts/run_jarvis_desktop.sh scripts/install_jarvis.sh scripts/upgrade_jarvis.sh
mkdir -p "${STATE_DIR}"
printf '%s\n' "${INSTALL_PROFILE}" > "${PROFILE_FILE}"

echo "JARVIS upgraded successfully on branch ${BRANCH}."
echo "Install profile: ${INSTALL_PROFILE}"
