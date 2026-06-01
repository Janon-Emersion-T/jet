# JARVIS Install and Upgrade

## Install on Linux

From the repository root:

```bash
chmod +x scripts/install_jarvis.sh
./scripts/install_jarvis.sh
```

Or install the full heavyweight AI stack:

```bash
./scripts/install_jarvis.sh --full
```

What it does:

- creates `.venv`
- installs Python dependencies from `requirements-desktop.txt` by default
- installs frontend dependencies with `npm ci`
- builds the frontend with `npm run build`
- creates a launcher at `~/.local/bin/jarvis`
- creates a desktop entry at `~/.local/share/applications/jarvis.desktop`
- stores the selected install profile so upgrades reuse it automatically

After install, you can start JARVIS either from your app launcher or with:

```bash
jarvis
```

## Upgrade after Git push

From the repository root:

```bash
chmod +x scripts/upgrade_jarvis.sh
./scripts/upgrade_jarvis.sh
```

Or upgrade a specific branch:

```bash
./scripts/upgrade_jarvis.sh main
```

Or force a specific profile during upgrade:

```bash
./scripts/upgrade_jarvis.sh --profile desktop
./scripts/upgrade_jarvis.sh --full
```

What it does:

- checks that the git worktree is clean
- fetches and fast-forwards from `origin`
- refreshes Python dependencies using the saved install profile
- refreshes frontend dependencies
- rebuilds the frontend

## Notes

- The upgrader intentionally refuses to run on a dirty worktree to avoid overwriting local work.
- The desktop launcher starts the API in the local virtualenv and then launches Electron against the built frontend.
- The default `desktop` profile avoids large CUDA/ML dependencies so installs stay practical on normal machines.
- The `full` profile uses `requirements.txt` and includes the heavier local AI/image/browser stack.
- This is a Linux-first installer/upgrade path. Windows and macOS packaging can be added later if needed.
