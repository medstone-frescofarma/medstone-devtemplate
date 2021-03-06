"""empty message

Revision ID: b2059b30e60e
Revises: d0aeedab82db
Create Date: 2020-11-08 20:03:38.516325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2059b30e60e'
down_revision = 'd0aeedab82db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('location', sa.Column('company_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'location', 'company', ['company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'location', type_='foreignkey')
    op.drop_column('location', 'company_id')
    # ### end Alembic commands ###
