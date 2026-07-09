"""seed_event_reminder_in_app_template

Revision ID: 3d73935b275c
Revises: 2fb2ce85a26e
Create Date: 2026-07-09 01:05:28.576084

"""

from typing import Sequence, Union

from alembic import op


revision: str = "3d73935b275c"
down_revision: Union[str, None] = "2fb2ce85a26e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TEMPLATE_ID = "00000000-0000-0000-0000-000000000100"


def upgrade() -> None:
    op.execute(
        f"""
        INSERT INTO notification_templates (
            id, template_type, channel, subject, body, is_active, version, language,
            created_at, updated_at
        )
        VALUES (
            '{TEMPLATE_ID}',
            'event_reminder',
            'in_app',
            'Напоминание о событии',
            'Событие **{{{{ event_title }}}}** начнётся через **{{{{ time_left }}}}** в **{{{{ event_location }}}}**',
            true,
            1,
            'ru',
            now(),
            now()
        )
        ON CONFLICT (template_type, channel, language, version) DO NOTHING
        """
    )


def downgrade() -> None:
    op.execute(f"DELETE FROM notification_templates WHERE id = '{TEMPLATE_ID}'")
