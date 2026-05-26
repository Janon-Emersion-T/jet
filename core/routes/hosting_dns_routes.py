from tools.hosting_dns_tools import (
    apache_config_generator,
    ssl_setup_assistant,
    certbot_automation_helper,
    domain_dns_checker,
    email_dns_checker,
    spf_dkim_dmarc_advisor,
    cloudflare_integration_assistant,
    cdn_optimization_advisor,
    static_asset_optimizer,
    image_compression_assistant,
    hosting_dns_help,
)


def _after(text: str, prefix: str) -> str:
    return text.replace(prefix, "", 1).strip()


def handle_hosting_dns_routes(user_input: str, text: str, clean_text: str):
    if text in ["hosting dns help", "hosting help", "dns help"]:
        return hosting_dns_help()

    if text.startswith("apache config generator"):
        return apache_config_generator(_after(user_input, "apache config generator"))

    if text.startswith("ssl setup assistant"):
        return ssl_setup_assistant(_after(user_input, "ssl setup assistant"))

    if text.startswith("certbot automation helper"):
        return certbot_automation_helper(_after(user_input, "certbot automation helper"))

    if text.startswith("domain dns checker"):
        return domain_dns_checker(_after(user_input, "domain dns checker"))

    if text.startswith("email dns checker"):
        return email_dns_checker(_after(user_input, "email dns checker"))

    if text.startswith("spf dkim dmarc advisor"):
        return spf_dkim_dmarc_advisor(_after(user_input, "spf dkim dmarc advisor"))

    if text.startswith("cloudflare integration assistant"):
        return cloudflare_integration_assistant(_after(user_input, "cloudflare integration assistant"))

    if text.startswith("cdn optimization advisor"):
        return cdn_optimization_advisor(_after(user_input, "cdn optimization advisor"))

    if text in ["static asset optimizer", "asset optimizer", "static optimizer"]:
        return static_asset_optimizer()

    if text in ["image compression assistant", "image optimizer", "compress images"]:
        return image_compression_assistant()

    return None
