"""Updated enum mapping for day_of_week

Revision ID: 5be234ce7cc8
Revises: fff5cf5e4f83
Create Date: 2024-12-16 15:25:08.351849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5be234ce7cc8'
down_revision = 'fff5cf5e4f83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service_provider', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.alter_column('role',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=20),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

    with op.batch_alter_table('service_provider', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)

    # ### end Alembic commands ###
