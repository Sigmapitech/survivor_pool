import re
from pathlib import Path


def render_template(template_path: str, **kwargs) -> str | None:
    """
    Load an HTML template and replace placeholders with kwargs.

    Example:
        render_template("templates/auth_verification.html",
                        verification_code="123456")
    will replace each instance of {{ verification_code }} by 123456
    """
    template = Path(template_path).read_text(encoding="utf-8")
    for key, value in kwargs.items():
        placeholder = "{{ " + key + " }}"
        template = template.replace(placeholder, str(value))
    if re.match(r"{{ \w+ }}", template):
        return None
    return template
