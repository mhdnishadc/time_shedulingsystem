"""Add role column to User model

Revision ID: fff5cf5e4f83
Revises: c13577187109
Create Date: 2024-12-16 09:00:35.423923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fff5cf5e4f83'
down_revision = 'c13577187109'
branch_labels = None
depends_on = None
def upgrade():
    op.add_column('user', sa.Column('role', sa.String(length=50), nullable=True))

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('role')

    # ### end Alembic commands ###
