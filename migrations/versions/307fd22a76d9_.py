"""empty message

Revision ID: 307fd22a76d9
Revises: f68795a65873
Create Date: 2024-06-21 00:35:02.196519

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '307fd22a76d9'
down_revision = 'f68795a65873'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('node', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nodetype', sa.String(length=64), nullable=True))
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=64),
               type_=sa.String(length=256),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('node', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(length=256),
               type_=mysql.VARCHAR(length=64),
               existing_nullable=False)
        batch_op.drop_column('nodetype')

    # ### end Alembic commands ###
