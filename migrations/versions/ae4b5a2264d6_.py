"""empty message

Revision ID: ae4b5a2264d6
Revises: 0a6971d40876
Create Date: 2023-05-08 14:19:31.477625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae4b5a2264d6'
down_revision = '0a6971d40876'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('moon',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('size', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('color', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('Planets', sa.Column('moon_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Planets', 'moon', ['moon_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Planets', type_='foreignkey')
    op.drop_column('Planets', 'moon_id')
    op.drop_table('moon')
    # ### end Alembic commands ###
