from alembic import op
from uuid import uuid4
from datetime import datetime, timezone
from schemas.company import CompanyMode
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '08e01ce8ac87'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    company_table = op.create_table(
        'companies',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('mode', sa.Enum(CompanyMode), nullable=False, default=CompanyMode.B2B),
        sa.Column('rating', sa.SmallInteger, default=0),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    
    # Data seed for first user
    op.bulk_insert(company_table, [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "NashTech",
            "mode": "B2B",
            "rating": 5,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
    ])


def downgrade() -> None:
    op.drop_table('companies')
