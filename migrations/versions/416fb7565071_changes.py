"""changes

Revision ID: 416fb7565071
Revises: 53d7f22d45da
Create Date: 2021-09-07 19:35:35.005755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '416fb7565071'
down_revision = '53d7f22d45da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True, comment='Пусто :('))
    op.drop_column('user', 'about_user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_user', sa.VARCHAR(length=140), nullable=True))
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
