from tools.topic_learning_tools import learn_topic


def handle_topic_learning_routes(user_input: str, text: str, clean_text: str):
    raw = user_input.lower().strip()

    if raw.startswith("learn about "):
        topic = user_input[12:].strip()
        return learn_topic(topic, max_sources=5)

    if raw.startswith("research and learn "):
        topic = user_input[19:].strip()
        return learn_topic(topic, max_sources=8)

    return None