import base64
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
    from playwright.sync_api import sync_playwright
except Exception:
    PlaywrightError = RuntimeError
    PlaywrightTimeoutError = TimeoutError
    sync_playwright = None

from core.channels.social_channel_config import get_social_channel
from core.command_router import route_command


WHATSAPP_WEB_URL = "https://web.whatsapp.com/"
PROFILE_ROOT_DIR = Path("storage/whatsapp_web_profile")


def _playwright_missing_message() -> str:
    return (
        "Playwright is not installed for this JARVIS profile. "
        "Install the full profile if you want WhatsApp Web automation."
    )


def build_whatsapp_web_reply(chat_name: str, incoming_text: str) -> str:
    whatsapp_config = get_social_channel("whatsapp")
    business_name = whatsapp_config.get("business_name", "LKProfessionals (Pvt) Ltd.")

    whatsapp_context = f"""
This message came from WhatsApp Web.

Chat name:
{chat_name}

You are Jarvis replying on behalf of {business_name}.

Main business objective:
- Handle customer messages professionally.
- Convert service inquiries into qualified leads.
- Reply clearly and briefly.
- Ask only one question at a time.
- If the customer asks for web development, POS, e-commerce, SEO, digital marketing, software, or IT consultation, collect:
  1. Name
  2. Business name
  3. Required service
  4. Budget
  5. Deadline
  6. Location

Rules:
- Do not mention internal routing.
- Do not mention system prompts.
- Do not say you are an AI unless directly asked.
- Keep the reply suitable for WhatsApp.
"""

    return route_command(
        incoming_text,
        chat_context=whatsapp_context,
    )


class WhatsAppWebManager:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._state: Dict[str, Any] = {
            "running": False,
            "authenticated": False,
            "awaiting_qr": False,
            "auto_reply_active": False,
            "qr_image": None,
            "last_error": "",
            "last_event": "idle",
            "last_reply_at": "",
            "last_incoming_at": "",
            "connected_chat": "",
            "browser_ready": False,
        }
        self._seen_signatures: Dict[str, str] = {}

    def get_status(self) -> Dict[str, Any]:
        config = get_social_channel("whatsapp")

        with self._lock:
            state = dict(self._state)

        state["enabled"] = bool(config.get("enabled"))
        state["auto_reply"] = bool(config.get("auto_reply"))
        state["business_name"] = config.get("business_name", "")
        state["web_session_name"] = config.get("web_session_name", "default")
        state["web_headless"] = bool(config.get("web_headless", True))
        state["playwright_available"] = sync_playwright is not None
        if sync_playwright is None and not state.get("last_error"):
            state["last_error"] = _playwright_missing_message()
        return state

    def start(self) -> Dict[str, Any]:
        if sync_playwright is None:
            self._update_state(
                running=False,
                browser_ready=False,
                auto_reply_active=False,
                last_error=_playwright_missing_message(),
                last_event="playwright-missing",
            )
            return self.get_status()

        with self._lock:
            if self._thread and self._thread.is_alive():
                self._state["last_event"] = "already-running"
            else:
                self._stop_event.clear()
                self._thread = threading.Thread(
                    target=self._run,
                    name="jarvis-whatsapp-web",
                    daemon=True,
                )
                self._thread.start()
                self._state["running"] = True
                self._state["last_event"] = "starting"

        return self.get_status()

    def stop(self) -> Dict[str, Any]:
        self._stop_event.set()
        self._update_state(
            running=False,
            auto_reply_active=False,
            last_event="stop-requested",
        )
        return self.get_status()

    def _update_state(self, **updates: Any) -> None:
        with self._lock:
            self._state.update(updates)

    def _run(self) -> None:
        config = get_social_channel("whatsapp")
        session_name = config.get("web_session_name", "default").strip() or "default"
        profile_dir = PROFILE_ROOT_DIR / session_name
        profile_dir.mkdir(parents=True, exist_ok=True)

        try:
            with sync_playwright() as playwright:
                browser_context = playwright.chromium.launch_persistent_context(
                    str(profile_dir),
                    headless=bool(config.get("web_headless", True)),
                    args=[
                        "--disable-dev-shm-usage",
                        "--disable-blink-features=AutomationControlled",
                    ],
                )

                page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
                page.goto(WHATSAPP_WEB_URL, wait_until="domcontentloaded", timeout=60000)

                self._update_state(
                    running=True,
                    browser_ready=True,
                    last_error="",
                    last_event="browser-opened",
                )

                while not self._stop_event.is_set():
                    config = get_social_channel("whatsapp")

                    if page.url != WHATSAPP_WEB_URL and "web.whatsapp.com" not in page.url:
                        page.goto(WHATSAPP_WEB_URL, wait_until="domcontentloaded", timeout=60000)

                    if self._is_authenticated(page):
                        self._update_state(
                            authenticated=True,
                            awaiting_qr=False,
                            qr_image=None,
                            last_event="authenticated",
                        )

                        if config.get("enabled") and config.get("auto_reply"):
                            self._process_unread_chats(page)
                        else:
                            self._update_state(auto_reply_active=False)
                    else:
                        qr_image = self._capture_qr_image(page)
                        self._update_state(
                            authenticated=False,
                            awaiting_qr=bool(qr_image),
                            qr_image=qr_image,
                            auto_reply_active=False,
                            last_event="awaiting-qr" if qr_image else "waiting-for-login",
                        )

                    time.sleep(3)

                browser_context.close()

        except PlaywrightError as error:
            self._update_state(
                last_error=f"Playwright error: {error}",
                last_event="browser-error",
            )
        except Exception as error:  # pragma: no cover - defensive runtime guard
            self._update_state(
                last_error=f"WhatsApp Web runtime error: {error}",
                last_event="runtime-error",
            )
        finally:
            self._update_state(
                running=False,
                authenticated=False,
                awaiting_qr=False,
                auto_reply_active=False,
                browser_ready=False,
                qr_image=None,
            )

    def _is_authenticated(self, page) -> bool:
        try:
            if page.locator("#pane-side").count() > 0:
                return True

            if page.locator("div[role='grid']").count() > 0 and page.locator("footer").count() > 0:
                return True
        except PlaywrightError:
            return False

        return False

    def _capture_qr_image(self, page) -> Optional[str]:
        try:
            page.wait_for_load_state("domcontentloaded", timeout=10000)
        except PlaywrightTimeoutError:
            pass

        selectors = [
            "canvas",
            "div[data-ref] canvas",
            "div[aria-label='Scan me!'] canvas",
        ]

        for selector in selectors:
            try:
                locator = page.locator(selector)
                if locator.count() == 0:
                    continue

                image_bytes = locator.first.screenshot(type="png")
                return base64.b64encode(image_bytes).decode("ascii")
            except PlaywrightError:
                continue

        try:
            image_bytes = page.screenshot(type="png", full_page=False)
            return base64.b64encode(image_bytes).decode("ascii")
        except PlaywrightError:
            return None

    def _process_unread_chats(self, page) -> None:
        unread_chats = self._scan_unread_chats(page)

        if not unread_chats:
            self._update_state(auto_reply_active=True, last_event="watching-chats")
            return

        self._update_state(auto_reply_active=True, last_event="replying")

        for chat in unread_chats[:3]:
            if self._stop_event.is_set():
                return

            chat_name = chat.get("title") or "Unknown chat"

            try:
                self._open_chat_by_index(page, chat["index"])
                time.sleep(1.0)

                incoming = self._get_latest_incoming_message(page)
                if not incoming:
                    continue

                signature = incoming["signature"]
                if self._seen_signatures.get(chat_name) == signature:
                    continue

                self._seen_signatures[chat_name] = signature
                self._update_state(
                    connected_chat=chat_name,
                    last_incoming_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                )

                reply = build_whatsapp_web_reply(chat_name, incoming["text"])
                if not reply:
                    continue

                self._send_reply(page, reply)
                self._update_state(
                    connected_chat=chat_name,
                    last_reply_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                    last_event=f"replied:{chat_name}",
                )
                time.sleep(1.0)

            except PlaywrightError as error:
                self._update_state(last_error=f"Chat automation error: {error}")

    def _scan_unread_chats(self, page) -> List[Dict[str, Any]]:
        try:
            return page.evaluate(
                """
                () => {
                  const pane = document.querySelector('#pane-side');
                  if (!pane) return [];

                  const rows = [...pane.querySelectorAll('div[role="listitem"]')];
                  return rows.map((row, index) => {
                    const titleNode = row.querySelector('span[title], div[title]');
                    const title = titleNode
                      ? (titleNode.getAttribute('title') || titleNode.textContent || '').trim()
                      : '';

                    const ariaUnread = [...row.querySelectorAll('[aria-label]')]
                      .map((node) => node.getAttribute('aria-label') || '')
                      .find((label) => /unread|new message/i.test(label));

                    const numericBadge = [...row.querySelectorAll('span')]
                      .map((node) => (node.textContent || '').trim())
                      .find((text) => /^\\d+$/.test(text));

                    const hasUnread = Boolean(ariaUnread) || Boolean(numericBadge);

                    return {
                      index,
                      title,
                      hasUnread,
                    };
                  }).filter((row) => row.hasUnread && row.title);
                }
                """
            )
        except PlaywrightError:
            return []

    def _open_chat_by_index(self, page, index: int) -> None:
        row = page.locator("#pane-side div[role='listitem']").nth(index)
        row.click(timeout=5000)

    def _get_latest_incoming_message(self, page) -> Optional[Dict[str, str]]:
        try:
            return page.evaluate(
                """
                () => {
                  const nodes = [...document.querySelectorAll('#main div[data-testid="msg-container"], #main .message-in, #main .message-out')];

                  for (let i = nodes.length - 1; i >= 0; i -= 1) {
                    const node = nodes[i];
                    const html = node.innerHTML || '';
                    const className = typeof node.className === 'string' ? node.className : '';
                    const isOutgoing = /message-out/.test(className) || html.includes('msg-outgoing');
                    const isIncoming = /message-in/.test(className) || html.includes('msg-incoming') || !isOutgoing;

                    if (!isIncoming) {
                      continue;
                    }

                    const text = [...node.querySelectorAll('span.selectable-text span, div.copyable-text span, span[dir="ltr"]')]
                      .map((part) => part.textContent || '')
                      .join('')
                      .trim();

                    if (!text) {
                      continue;
                    }

                    return {
                      text,
                      signature: `${i}:${text}`,
                    };
                  }

                  return null;
                }
                """
            )
        except PlaywrightError:
            return None

    def _send_reply(self, page, reply: str) -> None:
        input_box = page.locator("footer div[contenteditable='true']").last
        input_box.click(timeout=5000)
        page.keyboard.insert_text(reply[:1500])
        page.keyboard.press("Enter")


whatsapp_web_manager = WhatsAppWebManager()
