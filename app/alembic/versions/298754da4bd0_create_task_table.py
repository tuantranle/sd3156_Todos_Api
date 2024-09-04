from alembic import op
from uuid import uuid4
import sqlalchemy as sa
from schemas.task import TaskStatus, TaskPriority

# revision identifiers, used by Alembic.
revision = '298754da4bd0'
down_revision = 'a2c79e6002c4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column('summary', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('status', sa.Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING),
        sa.Column('priority', sa.Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM),
        sa.Column('owner_id', sa.UUID, nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    op.create_foreign_key('fk_task_owner', 'tasks', 'users', ['owner_id'], ['id'])

def downgrade() -> None:
    op.drop_table('tasks')
    op.execute("DROP TYPE taskstatus;")
    op.execute("DROP TYPE taskpriority;")
