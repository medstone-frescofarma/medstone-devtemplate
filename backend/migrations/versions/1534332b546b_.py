"""empty message

Revision ID: 1534332b546b
Revises: 
Create Date: 2020-10-26 15:07:30.430995

"""
from alembic import op
import sqlalchemy as sa
import medstone_backend


# revision identifiers, used by Alembic.
revision = '1534332b546b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('street_name', sa.UnicodeText(), nullable=True),
    sa.Column('street_number', sa.UnicodeText(), nullable=True),
    sa.Column('city', sa.UnicodeText(), nullable=True),
    sa.Column('zipcode', sa.UnicodeText(), nullable=True),
    sa.Column('country', sa.UnicodeText(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.UnicodeText(), nullable=False),
    sa.Column('description', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['location.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('role',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.UnicodeText(), nullable=False),
    sa.Column('description', sa.UnicodeText(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('supplier',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.UnicodeText(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('is_admin', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('username', sa.UnicodeText(), nullable=False),
    sa.Column('email', medstone_backend.models.util.EmailType(length=255), nullable=False),
    sa.Column('password_hash', sa.Unicode(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('user_role',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('role_start', sa.DateTime(), nullable=True),
    sa.Column('role_end', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_role_role_end'), 'user_role', ['role_end'], unique=False)
    op.create_index(op.f('ix_user_role_role_id'), 'user_role', ['role_id'], unique=False)
    op.create_index(op.f('ix_user_role_role_start'), 'user_role', ['role_start'], unique=False)
    op.create_index(op.f('ix_user_role_user_id'), 'user_role', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_role_user_id'), table_name='user_role')
    op.drop_index(op.f('ix_user_role_role_start'), table_name='user_role')
    op.drop_index(op.f('ix_user_role_role_id'), table_name='user_role')
    op.drop_index(op.f('ix_user_role_role_end'), table_name='user_role')
    op.drop_table('user_role')
    op.drop_table('user')
    op.drop_table('supplier')
    op.drop_table('role')
    op.drop_table('location')
    op.drop_table('address')
    # ### end Alembic commands ###
