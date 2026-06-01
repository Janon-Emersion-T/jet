import { useEffect, useMemo, useRef, useState } from "react";
import { MessageCircle, RefreshCw, Bot } from "lucide-react";

import { API_URL } from "../config/api";

const WHATSAPP_URL = "https://web.whatsapp.com/";
const WHATSAPP_PARTITION = "persist:jarvis-whatsapp";
export default function WhatsAppWebPanel({
  settings,
  updateWhatsAppSettings,
  status,
  setStatus,
}) {
  const webviewRef = useRef(null);
  const replyLoopBusyRef = useRef(false);
  const seenSignaturesRef = useRef({});
  const [isReady, setIsReady] = useState(false);
  const [manualRunBusy, setManualRunBusy] = useState(false);
  const [apiOnline, setApiOnline] = useState(false);
  const [webState, setWebState] = useState({
    authenticated: false,
    awaitingQr: true,
    unreadCount: 0,
    activeChat: "",
    listReady: false,
    rowCount: 0,
  });

  const isElectron = Boolean(window.jarvisDesktop?.isElectron);

  const statusLabel = useMemo(() => {
    if (!isElectron) {
      return "WhatsApp Web only works inside the Electron desktop app.";
    }

    if (!isReady) {
      return "Loading WhatsApp Web...";
    }

    if (webState.authenticated) {
      return "WhatsApp is connected and ready.";
    }

    if (webState.awaitingQr) {
      return "Scan the QR code in the panel with WhatsApp Business.";
    }

    return "Waiting for WhatsApp Web to finish loading.";
  }, [isElectron, isReady, webState]);

  useEffect(() => {
    if (!isElectron) {
      return undefined;
    }

    const webview = webviewRef.current;
    if (!webview) {
      return undefined;
    }

    const handleReady = () => {
      setIsReady(true);
      setStatus("WhatsApp Web loaded.");
      refreshState();
    };

    webview.addEventListener("dom-ready", handleReady);

    return () => {
      webview.removeEventListener("dom-ready", handleReady);
    };
  }, [isElectron]);

  useEffect(() => {
    if (!isElectron) {
      return undefined;
    }

    const intervalId = window.setInterval(() => {
      refreshState();
    }, 4000);

    return () => window.clearInterval(intervalId);
  }, [isElectron, isReady]);

  useEffect(() => {
    checkApiStatus();
    const intervalId = window.setInterval(() => {
      checkApiStatus();
    }, 5000);

    return () => window.clearInterval(intervalId);
  }, []);

  useEffect(() => {
    if (!isElectron || !isReady || !settings.auto_reply) {
      return undefined;
    }

    const intervalId = window.setInterval(() => {
      processUnreadChats();
    }, 7000);

    return () => window.clearInterval(intervalId);
  }, [isElectron, isReady, settings.enabled, settings.auto_reply]);

  async function runInWebView(script) {
    const webview = webviewRef.current;

    if (!webview || typeof webview.executeJavaScript !== "function") {
      return null;
    }

    return webview.executeJavaScript(script, true);
  }

  async function refreshState() {
    try {
      const state = await runInWebView(`
        (() => {
          const pane =
            document.querySelector('#pane-side')
            || document.querySelector('[aria-label="Chat list"]')
            || document.querySelector('[data-testid="chat-list"]')
            || [...document.querySelectorAll('div')].find((node) => {
              const text = (node.textContent || '').trim();
              return text.includes('Search or start a new chat') && node.querySelector('input, div[contenteditable="true"]');
            })?.parentElement;

          const footer = document.querySelector('footer');
          const qrCanvas = document.querySelector('canvas');

          const rows = pane
            ? [...pane.querySelectorAll('div[role="listitem"], [data-testid="cell-frame-container"]')]
            : [];

          const unreadRows = rows.filter((row) => {
            const ariaUnread = [...row.querySelectorAll('[aria-label]')]
              .map((node) => node.getAttribute('aria-label') || '')
              .find((label) => /unread|new message|message unread/i.test(label));

            const numericBadge = [...row.querySelectorAll('span, div')]
              .map((node) => (node.textContent || '').trim())
              .find((text) => /^\\d{1,3}$/.test(text));

            const unreadMarker = row.querySelector(
              '[data-testid*="icon-unread"], [data-testid*="unread"], [aria-label*="unread" i]'
            );

            return Boolean(ariaUnread) || Boolean(numericBadge) || Boolean(unreadMarker);
          });

          const activeChat = document.querySelector('#main header span[title], #main header div[title]');
          const searchInput = document.querySelector('input[placeholder*="Search" i], div[contenteditable="true"][role="textbox"]');

          return {
            authenticated: Boolean(rows.length > 0 || (searchInput && pane)),
            awaitingQr: !rows.length && Boolean(qrCanvas),
            unreadCount: unreadRows.length,
            activeChat: activeChat
              ? (activeChat.getAttribute('title') || activeChat.textContent || '').trim()
              : '',
            listReady: Boolean(pane),
            rowCount: rows.length,
          };
        })();
      `);

      if (state) {
        setWebState(state);
      }
    } catch (error) {
      setStatus(`WhatsApp state read failed: ${error.message}`);
    }
  }

  async function checkApiStatus() {
    try {
      const response = await fetch(`${API_URL}/`);
      const data = await response.json();
      setApiOnline(data.status === "online");
    } catch {
      setApiOnline(false);
    }
  }

  async function reloadWhatsApp() {
    const webview = webviewRef.current;

    if (!webview) {
      return;
    }

    webview.reload();
    setStatus("Reloading WhatsApp Web...");
  }

  async function processUnreadChats() {
    if (replyLoopBusyRef.current) {
      return;
    }

    if (!apiOnline) {
      setStatus("Jarvis API is offline. Start the backend first for auto reply.");
      return;
    }

    replyLoopBusyRef.current = true;

    try {
      const unreadChats = await runInWebView(`
        (() => {
          const pane =
            document.querySelector('#pane-side')
            || document.querySelector('[aria-label="Chat list"]')
            || document.querySelector('[data-testid="chat-list"]')
            || [...document.querySelectorAll('div')].find((node) => {
              const text = (node.textContent || '').trim();
              return text.includes('Search or start a new chat') && node.querySelector('input, div[contenteditable="true"]');
            })?.parentElement;
          if (!pane) return [];

          return [...pane.querySelectorAll('div[role="listitem"], [data-testid="cell-frame-container"]')].map((row, index) => {
            const titleNode = row.querySelector('span[title], div[title]');
            const title = titleNode
              ? (titleNode.getAttribute('title') || titleNode.textContent || '').trim()
              : '';

            const ariaUnread = [...row.querySelectorAll('[aria-label]')]
              .map((node) => node.getAttribute('aria-label') || '')
              .find((label) => /unread|new message|message unread/i.test(label));

            const numericBadge = [...row.querySelectorAll('span, div')]
              .map((node) => (node.textContent || '').trim())
              .find((text) => /^\\d{1,3}$/.test(text));

            const unreadMarker = row.querySelector('[data-testid*="icon-unread"], [data-testid*="unread"], [aria-label*="unread" i]');

            return {
              index,
              title,
              hasUnread: Boolean(ariaUnread) || Boolean(numericBadge) || Boolean(unreadMarker),
            };
          }).filter((row) => row.hasUnread && row.title);
        })();
      `);

      if (!Array.isArray(unreadChats) || unreadChats.length === 0) {
        setStatus("No unread chats detected right now.");
        return;
      }

      for (const chat of unreadChats.slice(0, 3)) {
        setStatus(`Opening ${chat.title}...`);

        const opened = await runInWebView(`
          (() => {
            const rows = document.querySelectorAll('#pane-side div[role="listitem"], #pane-side [data-testid="cell-frame-container"]');
            const row = rows[${Number(chat.index)}];
            if (!row) return false;
            row.click();
            return true;
          })();
        `);

        if (!opened) {
          continue;
        }

        await wait(1200);

        await runInWebView(`
          (() => new Promise((resolve) => {
            const expectedTitle = ${JSON.stringify(chat.title)};
            const startedAt = Date.now();

            const tick = () => {
              const titleNode = document.querySelector('#main header span[title], #main header div[title]');
              const currentTitle = titleNode
                ? (titleNode.getAttribute('title') || titleNode.textContent || '').trim()
                : '';

              if (currentTitle === expectedTitle || Date.now() - startedAt > 5000) {
                resolve(currentTitle);
                return;
              }

              setTimeout(tick, 150);
            };

            tick();
          }))();
        `);

        const incoming = await runInWebView(`
          (() => {
            const nodes = [...document.querySelectorAll(
              '#main div[data-testid="msg-container"], #main .message-in, #main .message-out, #main [data-pre-plain-text]'
            )];

            for (let i = nodes.length - 1; i >= 0; i -= 1) {
              const node = nodes[i];
              const className = typeof node.className === 'string' ? node.className : '';
              const html = node.innerHTML || '';
              const plainTextPrefix = node.getAttribute && node.getAttribute('data-pre-plain-text');
              const isOutgoing =
                /message-out/.test(className) ||
                html.includes('msg-outgoing') ||
                (plainTextPrefix && /\\]:\\s*$/.test(plainTextPrefix) === false && plainTextPrefix.includes('You:'));
              if (isOutgoing) continue;

              const text = [...node.querySelectorAll('span.selectable-text span, div.copyable-text span, span[dir="ltr"], .selectable-text')]
                .map((part) => part.textContent || '')
                .join('')
                .trim();

              if (!text) continue;

              return {
                text,
                signature: ${JSON.stringify(chat.title)} + ':' + i + ':' + text,
              };
            }

            return null;
          })();
        `);

        if (!incoming?.text || !incoming?.signature) {
          setStatus(`Could not read the last incoming message for ${chat.title}.`);
          continue;
        }

        if (seenSignaturesRef.current[chat.title] === incoming.signature) {
          setStatus(`Latest unread message in ${chat.title} was already processed.`);
          continue;
        }

        setStatus(`Generating reply for ${chat.title}...`);
        const response = await fetch(`${API_URL}/social/whatsapp/web/reply-preview`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            chat_name: chat.title,
            message: incoming.text,
          }),
        });

        if (!response.ok) {
          setStatus(`Reply API failed for ${chat.title} with status ${response.status}.`);
          continue;
        }

        const data = await response.json();
        if (!data.ok || !data.reply) {
          setStatus(`Reply generation failed for ${chat.title}: ${data.error || "empty reply"}`);
          continue;
        }

        const replyText = JSON.stringify(data.reply.slice(0, 1500));

        setStatus(`Sending reply to ${chat.title}...`);
        const sendResult = await runInWebView(`
          (() => {
            const editor = document.querySelector('footer div[contenteditable="true"][role="textbox"]')
              || document.querySelector('footer div[contenteditable="true"]');
            if (!editor) return { ok: false, reason: 'editor-not-found' };

            editor.focus();

            const reply = ${replyText};
            const selection = window.getSelection();
            const range = document.createRange();
            range.selectNodeContents(editor);
            range.collapse(false);
            selection.removeAllRanges();
            selection.addRange(range);

            let inserted = false;

            try {
              inserted = document.execCommand('insertText', false, reply);
            } catch (error) {
              inserted = false;
            }

            if (!inserted || !(editor.textContent || '').trim()) {
              editor.textContent = '';
              const textNode = document.createTextNode(reply);
              editor.appendChild(textNode);
              editor.dispatchEvent(new InputEvent('beforeinput', {
                bubbles: true,
                cancelable: true,
                inputType: 'insertText',
                data: reply,
              }));
              editor.dispatchEvent(new InputEvent('input', {
                bubbles: true,
                inputType: 'insertText',
                data: reply,
              }));
            }

            const sendButton =
              document.querySelector('button[aria-label="Send"]')
              || document.querySelector('button[aria-label*="send" i]')
              || document.querySelector('span[data-icon="send"]')?.closest('button')
              || document.querySelector('[data-testid="send"]')
              || document.querySelector('[data-icon="send"]')?.closest('[role="button"]')
              || [...document.querySelectorAll('button,[role="button"]')].find((node) => {
                const label = node.getAttribute('aria-label') || '';
                return /send/i.test(label);
              });

            if (sendButton && typeof sendButton.click === 'function') {
              sendButton.click();
              return {
                ok: true,
                mode: 'button',
                sendButtonFound: true,
                composerText: (editor.textContent || '').trim(),
              };
            }

            return {
              ok: true,
              mode: 'webview-enter',
              sendButtonFound: false,
              composerText: (editor.textContent || '').trim(),
            };
          })();
        `);

        if (!sendResult?.ok) {
          setStatus(`Could not send reply to ${chat.title}: ${sendResult?.reason || "unknown error"}`);
          continue;
        }

        if (sendResult.mode === "webview-enter") {
          const webview = webviewRef.current;

          if (webview?.sendInputEvent) {
            webview.sendInputEvent({ type: "keyDown", keyCode: "Enter" });
            webview.sendInputEvent({ type: "char", keyCode: "\r" });
            webview.sendInputEvent({ type: "keyUp", keyCode: "Enter" });
            await wait(500);
          }
        }

        const sendVerified = await runInWebView(`
          (() => {
            const editor = document.querySelector('footer div[contenteditable="true"][role="textbox"]')
              || document.querySelector('footer div[contenteditable="true"]');
            const remaining = (editor?.textContent || '').trim();
            return {
              remaining,
              cleared: remaining.length === 0,
            };
          })();
        `);

        if (!sendVerified?.cleared) {
          setStatus(
            `Reply may not have sent in ${chat.title}. Composer still has text after ${sendResult.mode} send.`
          );
          continue;
        }

        seenSignaturesRef.current[chat.title] = incoming.signature;

        setStatus(`Auto replied to ${chat.title}.`);
        if (window.jarvisDesktop?.notify) {
          window.jarvisDesktop.notify({
            title: "JARVIS WhatsApp Auto Reply",
            body: `Replied to ${chat.title}`,
          });
        }

        await wait(1000);
      }

      await refreshState();
    } catch (error) {
      setStatus(`WhatsApp auto reply error: ${error.message}`);
    } finally {
      replyLoopBusyRef.current = false;
    }
  }

  async function runManualCheck() {
    setManualRunBusy(true);

    try {
      await processUnreadChats();
      await refreshState();
    } finally {
      setManualRunBusy(false);
    }
  }

  return (
    <div className="whatsapp-live-panel">
      <div className="whatsapp-toolbar">
        <div className="whatsapp-toolbar-copy">
          <div className="panel-title">
            <MessageCircle size={24} />
            <div>
              <h3>WhatsApp Web</h3>
              <p>{statusLabel}</p>
            </div>
          </div>

          <div className="whatsapp-status-row">
            <span className={webState.authenticated ? "web-badge success" : "web-badge"}>
              {webState.authenticated ? "Logged in" : "QR required"}
            </span>
            <span className={apiOnline ? "web-badge success" : "web-badge"}>
              {apiOnline ? "Jarvis API online" : "Jarvis API offline"}
            </span>
            <span className={settings.auto_reply ? "web-badge success" : "web-badge"}>
              {settings.auto_reply ? "Auto reply on" : "Auto reply off"}
            </span>
          </div>
        </div>

        <div className="whatsapp-toolbar-actions">
          <button
            type="button"
            className="secondary"
            onClick={runManualCheck}
            disabled={manualRunBusy}
          >
            {manualRunBusy ? <RefreshCw size={18} /> : <Bot size={18} />}
            {manualRunBusy ? "Checking..." : "Check Unread Now"}
          </button>

          <button type="button" className="secondary" onClick={reloadWhatsApp}>
            <RefreshCw size={18} />
            Reload WhatsApp
          </button>
        </div>
      </div>

      <div className="social-toggle-grid">
        <label className="social-toggle-card">
          <input
            type="checkbox"
            checked={Boolean(settings.auto_reply)}
            onChange={(event) =>
              updateWhatsAppSettings({
                auto_reply: event.target.checked,
              })
            }
          />
          <span>Unread Chat Auto Reply</span>
        </label>
      </div>

      <div className="whatsapp-meta-grid">
        <div className="web-stat">
          <span>Unread chats</span>
          <strong>{webState.unreadCount || 0}</strong>
        </div>
      </div>

      {!isElectron ? (
        <div className="web-error">
          WhatsApp Web embedding is only available in the Electron desktop app.
        </div>
      ) : (
        <div className="whatsapp-webview-shell">
          <webview
            ref={webviewRef}
            className="whatsapp-webview"
            src={WHATSAPP_URL}
            partition={WHATSAPP_PARTITION}
            allowpopups="false"
          />
        </div>
      )}

      {status && <div className="social-status">{status}</div>}
    </div>
  );
}

function wait(ms) {
  return new Promise((resolve) => {
    window.setTimeout(resolve, ms);
  });
}
