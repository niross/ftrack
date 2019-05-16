"""empty message

Revision ID: 7f9d1d0921a0
Revises: 1b47f2a3a401
Create Date: 2019-05-15 21:10:31.809482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f9d1d0921a0'
down_revision = '1b47f2a3a401'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    op.create_table('starling_transaction',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('created_locally', sa.DateTime(), nullable=True),
        sa.Column('amount', sa.Integer(), nullable=True),
        sa.Column('transaction_uid', sa.String(length=255), nullable=True),
        sa.Column('type', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_starling_transaction_created_locally'), 'starling_transaction', ['created_locally'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_starling_transaction_created_locally'), table_name='starling_transaction')
    op.drop_table('starling_transaction')
    # ### end Alembic commands ###
