import os
import socket
import subprocess
from pathlib import Path
from urllib.parse import urlparse


MAX_OUTPUT = 12000


def _run(command: list[str], timeout: int = 20) -> str:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout.strip() or result.stderr.strip() or "No output."
        return output[:MAX_OUTPUT]
    except FileNotFoundError:
        return f"Command not found: {command[0]}"
    except Exception as e:
        return f"Command failed: {e}"


def _domain_only(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if "://" in value:
        parsed = urlparse(value)
        return parsed.netloc.replace("www.", "")
    return value.replace("www.", "").split("/")[0]


def _dig(domain: str, record_type: str) -> str:
    if not domain:
        return "No domain provided."
    return _run(["dig", "+short", record_type, domain], timeout=15)


def apache_config_generator(domain: str = "") -> str:
    domain = _domain_only(domain) or "example.com"
    root = f"/var/www/{domain}/public"

    return f"""APACHE CONFIG GENERATOR — PHASE 261

Read-only generator. No Apache files were written.

Domain: {domain}
DocumentRoot: {root}

Suggested Apache VirtualHost:

<VirtualHost *:80>
    ServerName {domain}
    ServerAlias www.{domain}
    DocumentRoot {root}

    <Directory {root}>
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${{APACHE_LOG_DIR}}/{domain}_error.log
    CustomLog ${{APACHE_LOG_DIR}}/{domain}_access.log combined
</VirtualHost>

Suggested commands after manual review:

sudo nano /etc/apache2/sites-available/{domain}.conf
sudo a2ensite {domain}.conf
sudo apache2ctl configtest
sudo systemctl reload apache2

Safety:
- This tool only generates config text.
- JARVIS must not write /etc/apache2 files without confirm-before-write.
"""


def ssl_setup_assistant(domain: str = "") -> str:
    domain = _domain_only(domain) or "example.com"

    return f"""SSL SETUP ASSISTANT — PHASE 262

Read-only SSL planning assistant. No certificate was requested.

Domain: {domain}

Pre-checks:
- Domain A record must point to this server.
- Port 80 must be reachable.
- Apache/Nginx config must serve the domain correctly.
- Firewall must allow HTTP/HTTPS.

Suggested Certbot command for Apache:

sudo certbot --apache -d {domain} -d www.{domain}

Suggested Certbot command for Nginx:

sudo certbot --nginx -d {domain} -d www.{domain}

Renewal test command:

sudo certbot renew --dry-run

Safety:
- This phase gives instructions only.
- Actual SSL installation must be a confirmed action later.
"""


def certbot_automation_helper(domain: str = "") -> str:
    domain = _domain_only(domain) or "example.com"
    certbot = _run(["which", "certbot"])

    return f"""CERTBOT AUTOMATION HELPER — PHASE 263

Read-only helper. No certbot command was executed.

Certbot availability:
{certbot}

Recommended safe workflow for {domain}:

1. Check DNS:
   dig +short A {domain}
   dig +short A www.{domain}

2. Check web server:
   sudo nginx -t
   sudo apache2ctl configtest

3. Issue certificate manually:
   sudo certbot --nginx -d {domain} -d www.{domain}
   OR
   sudo certbot --apache -d {domain} -d www.{domain}

4. Test auto-renewal:
   sudo certbot renew --dry-run

5. Check timer:
   systemctl list-timers | grep certbot

Safety:
- JARVIS should not auto-run certificate requests yet.
- Certificate creation changes server state and must require confirmation.
"""


def domain_dns_checker(domain: str = "") -> str:
    domain = _domain_only(domain)
    if not domain:
        return "DOMAIN DNS CHECKER — PHASE 264\n\nUsage: domain dns checker example.com"

    a = _dig(domain, "A")
    a_www = _dig(f"www.{domain}", "A")
    aaaa = _dig(domain, "AAAA")
    ns = _dig(domain, "NS")
    cname_www = _dig(f"www.{domain}", "CNAME")

    try:
        resolved = socket.gethostbyname(domain)
    except Exception as e:
        resolved = f"Resolution failed: {e}"

    return f"""DOMAIN DNS CHECKER — PHASE 264

Domain: {domain}

A record:
{a}

WWW A record:
{a_www}

WWW CNAME:
{cname_www}

AAAA record:
{aaaa}

Nameservers:
{ns}

Python socket resolution:
{resolved}

Advisor:
- If A record is empty, the domain is not pointing correctly.
- If www is empty, add CNAME www -> {domain} or an A record.
- If DNS recently changed, allow propagation time.
"""


def email_dns_checker(domain: str = "") -> str:
    domain = _domain_only(domain)
    if not domain:
        return "EMAIL DNS CHECKER — PHASE 265\n\nUsage: email dns checker example.com"

    mx = _dig(domain, "MX")
    txt = _dig(domain, "TXT")
    dmarc = _dig(f"_dmarc.{domain}", "TXT")
    default_dkim = _dig(f"default._domainkey.{domain}", "TXT")
    google_dkim = _dig(f"google._domainkey.{domain}", "TXT")
    selector1 = _dig(f"selector1._domainkey.{domain}", "TXT")

    return f"""EMAIL DNS CHECKER — PHASE 265

Domain: {domain}

MX records:
{mx}

TXT records:
{txt}

DMARC:
{dmarc}

DKIM checks:
default._domainkey:
{default_dkim}

google._domainkey:
{google_dkim}

selector1._domainkey:
{selector1}

Advisor:
- MX is required to receive email.
- SPF is usually stored as TXT beginning with v=spf1.
- DMARC is stored at _dmarc.{domain}.
- DKIM selector depends on your email provider.
"""


def spf_dkim_dmarc_advisor(domain: str = "") -> str:
    domain = _domain_only(domain) or "example.com"

    return f"""SPF / DKIM / DMARC ADVISOR — PHASE 266

Domain: {domain}

Baseline SPF example:

v=spf1 mx a include:_spf.google.com ~all

Strict DMARC starter example:

Host:
_dmarc.{domain}

Value:
v=DMARC1; p=quarantine; rua=mailto:postmaster@{domain}; adkim=s; aspf=s

Safer DMARC monitoring-first example:

Host:
_dmarc.{domain}

Value:
v=DMARC1; p=none; rua=mailto:postmaster@{domain}

DKIM:
- DKIM must be copied from your mail provider.
- Do not invent DKIM keys.
- Common selectors: default, google, selector1, selector2.

Professional recommendation:
- Start DMARC with p=none.
- Monitor reports.
- Move to quarantine.
- Then move to reject only after validation.

Safety:
- This tool advises only.
- DNS records must be manually verified before publishing.
"""


def cloudflare_integration_assistant(domain: str = "") -> str:
    domain = _domain_only(domain) or "example.com"

    return f"""CLOUDFLARE INTEGRATION ASSISTANT — PHASE 267

Domain: {domain}

Recommended setup checklist:

1. Add site to Cloudflare.
2. Replace registrar nameservers with Cloudflare nameservers.
3. Import DNS records.
4. Confirm A record points to the server IP.
5. Enable proxy only after origin server works.
6. SSL/TLS mode:
   - Use Full (strict) if server has valid SSL.
   - Avoid Flexible SSL for Laravel/modern apps.
7. Enable:
   - Always Use HTTPS
   - Brotli
   - HTTP/2 / HTTP/3
   - Auto Minify only after testing
8. Add page rules/cache rules carefully.

Laravel warning:
- If Cloudflare proxy causes redirect loops, check APP_URL, trusted proxies, and SSL mode.

Safety:
- This phase does not call Cloudflare API.
- API integration should be added later with token-based confirmation.
"""


def cdn_optimization_advisor(domain: str = "") -> str:
    domain = _domain_only(domain) or "example.com"

    return f"""CDN OPTIMIZATION ADVISOR — PHASE 268

Domain: {domain}

Recommended CDN strategy:

Static assets:
- Cache CSS, JS, images, fonts aggressively.
- Use versioned filenames from Vite/build tools.
- Cache-Control for static assets:
  public, max-age=31536000, immutable

HTML:
- Do not aggressively cache dynamic HTML unless app supports it.
- Laravel dashboards, auth pages, carts, checkout pages should usually bypass cache.

Images:
- Prefer WebP/AVIF where possible.
- Lazy-load non-critical images.
- Compress large uploaded images.

Cloudflare:
- Enable Brotli.
- Use CDN cache for /build/*, /assets/*, /images/*.
- Bypass cache for /admin, /login, /dashboard, /cart, /checkout.

Safety:
- Advisory only.
- No server/CDN settings changed.
"""


def static_asset_optimizer() -> str:
    cwd = Path.cwd()
    public = cwd / "public"
    build = public / "build"

    files = []
    for base in [public, build]:
        if base.exists():
            for path in base.rglob("*"):
                if path.is_file() and path.suffix.lower() in [".css", ".js", ".woff", ".woff2", ".ttf", ".svg"]:
                    try:
                        files.append((path.stat().st_size, path))
                    except Exception:
                        pass

    files = sorted(files, reverse=True)[:30]

    lines = [
        "STATIC ASSET OPTIMIZER — PHASE 269",
        "",
        f"Project path: {cwd}",
        "",
        "Largest static assets:",
    ]

    if not files:
        lines.append("No static CSS/JS/font/SVG assets found under public/ or public/build/.")
    else:
        for size, path in files:
            lines.append(f"- {round(size / 1024, 2)} KB | {path}")

    lines.extend([
        "",
        "Recommendations:",
        "- Run npm run build before deployment.",
        "- Use Vite hashed assets for long-term browser caching.",
        "- Remove unused CSS/JS libraries.",
        "- Prefer .woff2 fonts.",
        "- Serve Brotli/Gzip from Nginx/Apache/CDN.",
        "",
        "Safety:",
        "- Read-only inspection only.",
        "- No files were modified.",
    ])

    return "\n".join(lines)


def image_compression_assistant() -> str:
    cwd = Path.cwd()
    image_exts = [".jpg", ".jpeg", ".png", ".webp", ".gif"]
    roots = [cwd / "public", cwd / "storage" / "app" / "public"]

    images = []
    for root in roots:
        if root.exists():
            for path in root.rglob("*"):
                if path.is_file() and path.suffix.lower() in image_exts:
                    try:
                        images.append((path.stat().st_size, path))
                    except Exception:
                        pass

    images = sorted(images, reverse=True)[:30]

    lines = [
        "IMAGE COMPRESSION ASSISTANT — PHASE 270",
        "",
        f"Project path: {cwd}",
        "",
        "Largest images:",
    ]

    if not images:
        lines.append("No images found under public/ or storage/app/public/.")
    else:
        for size, path in images:
            lines.append(f"- {round(size / 1024, 2)} KB | {path}")

    lines.extend([
        "",
        "Recommended tools:",
        "- jpegoptim for JPG/JPEG",
        "- optipng for PNG",
        "- cwebp for WebP conversion",
        "- sharp/imagemin for Node-based pipelines",
        "",
        "Safe manual examples:",
        "jpegoptim --strip-all --max=82 path/to/image.jpg",
        "optipng -o2 path/to/image.png",
        "cwebp -q 82 input.jpg -o output.webp",
        "",
        "Safety:",
        "- This phase only reports candidates.",
        "- Actual compression should be confirm-based because it changes files.",
    ])

    return "\n".join(lines)


def hosting_dns_help() -> str:
    return """HOSTING / DNS COMMANDS — PHASES 261–270

261. apache config generator example.com
262. ssl setup assistant example.com
263. certbot automation helper example.com
264. domain dns checker example.com
265. email dns checker example.com
266. spf dkim dmarc advisor example.com
267. cloudflare integration assistant example.com
268. cdn optimization advisor example.com
269. static asset optimizer
270. image compression assistant
"""
