from tools.website_learning_tools import learn_website


def handle_website_learning_routes(user_input: str, text: str, clean_text: str):
    if text.startswith("learn website "):
        url = user_input.replace("learn website ", "", 1).strip()
        return learn_website(url, max_pages=50, delay=1.0)

    if text.startswith("deep learn website "):
        url = user_input.replace("deep learn website ", "", 1).strip()
        return learn_website(url, max_pages=250, delay=1.0)

    return None
