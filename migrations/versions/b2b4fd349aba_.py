"""empty message

Revision ID: b2b4fd349aba
Revises: 8370eaf59dfb
Create Date: 2024-06-18 23:45:19.793554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2b4fd349aba'
down_revision = '8370eaf59dfb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('idAccount', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('idAccount')
    )
    op.create_table('node',
    sa.Column('idNode', sa.Integer(), nullable=False),
    sa.Column('idAccount', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('photo', sa.String(length=256), nullable=True),
    sa.Column('desc', sa.String(length=512), nullable=True),
    sa.Column('address', sa.String(length=256), nullable=True),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idAccount'], ['account.idAccount'], ),
    sa.PrimaryKeyConstraint('idNode')
    )
    op.create_table('node_relation',
    sa.Column('idNode1', sa.Integer(), nullable=False),
    sa.Column('idNode2', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['idNode1'], ['node.idNode'], ),
    sa.ForeignKeyConstraint(['idNode2'], ['node.idNode'], ),
    sa.PrimaryKeyConstraint('idNode1', 'idNode2')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('node_relation')
    op.drop_table('node')
    op.drop_table('account')
    # ### end Alembic commands ###