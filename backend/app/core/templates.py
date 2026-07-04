"""Template rendering with compiled-template caching.

Uses Jinja2 SandboxedEnvironment for safe template rendering.
Templates come from the database (NotificationTemplate.body), not the filesystem.
"""

from jinja2.sandbox import SandboxedEnvironment

from app.schemas.notification import NotificationContext


class TemplateRenderer:
    """Renders Jinja2 templates with compiled-template caching."""

    def __init__(self) -> None:
        self._env = SandboxedEnvironment(autoescape=True)
        self._cache: dict[int, object] = {}

    def render(self, template_body: str, context: NotificationContext) -> str:
        key = hash(template_body)
        if key not in self._cache:
            self._cache[key] = self._env.from_string(template_body)
        template = self._cache[key]
        return template.render(**context.to_template_namespace())

    def render_subject(self, subject: str | None, context: NotificationContext) -> str | None:
        if subject is None:
            return None
        return self.render(subject, context)
