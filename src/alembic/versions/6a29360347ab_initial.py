"""initial

Revision ID: 6a29360347ab
Revises: 
Create Date: 2022-12-24 11:44:37.088353

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '6a29360347ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_table(
        'files',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('size', sa.Integer(), nullable=False),
        sa.Column('path', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('user', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['user'], ['users.id'], name='fk_files_users_id_user'
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('path'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('files')
    op.drop_table('users')
    # ### end Alembic commands ###
