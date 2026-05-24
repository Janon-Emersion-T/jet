import webbrowser

SAFE_SITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "gmail": "https://mail.google.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com",
    "lkprofessionals": "https://lkprofessionals.com",
}

def open_safe_site(site_name: str) -> str:
    key = site_name.lower().strip()

    if key not in SAFE_SITES:
        return f"Website '{site_name}' is not in the approved website list."

    webbrowser.open(SAFE_SITES[key])
    return f"Opening {site_name}."
