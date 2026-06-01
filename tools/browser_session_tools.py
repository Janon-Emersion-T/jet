from pathlib import Path
try:
    from playwright.sync_api import sync_playwright
except Exception:
    sync_playwright = None


BROWSER_SESSION_DIR = Path("storage/browser_session")
SCREENSHOT_DIR = Path("storage/browser_screenshots")
BROWSER_REPORT_DIR = Path("storage/browser_reports")


def ensure_browser_storage():
    BROWSER_SESSION_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    BROWSER_REPORT_DIR.mkdir(parents=True, exist_ok=True)


class PersistentBrowser:
    """
    Wrapper for Playwright persistent context.

    This is the core of phases:
    141 - Playwright persistent browser
    142 - Login session preservation
    """

    def __init__(self, headless: bool = True):
        ensure_browser_storage()
        self.headless = headless
        self.playwright = None
        self.context = None
        self.page = None

    def __enter__(self):
        if sync_playwright is None:
            raise RuntimeError(
                "Playwright is not installed for this JARVIS profile. "
                "Install the full profile to enable persistent browser sessions."
            )

        self.playwright = sync_playwright().start()

        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_SESSION_DIR),
            headless=self.headless,
            viewport={"width": 1440, "height": 1200},
        )

        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = self.context.new_page()

        return self.page

    def __exit__(self, exc_type, exc, tb):
        if self.context:
            self.context.close()

        if self.playwright:
            self.playwright.stop()
