"""empty message

Revision ID: 3a25bee0a9bc
Revises: 4fd96eefc9b0
Create Date: 2022-08-06 13:29:27.101360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a25bee0a9bc'
down_revision = '4fd96eefc9b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('id', sa.Integer(), nullable=False))
    op.add_column('Show', sa.Column('venue_id', sa.Integer(), nullable=False))
    op.add_column('Show', sa.Column('start_time', sa.DateTime(), nullable=False))
    op.alter_column('Show', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('Show_Venue_id_fkey', 'Show', type_='foreignkey')
    op.create_foreign_key(None, 'Show', 'Venue', ['venue_id'], ['id'])
    op.drop_column('Show', 'time')
    op.drop_column('Show', 'Venue_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('Venue_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Show', sa.Column('time', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Show', type_='foreignkey')
    op.create_foreign_key('Show_Venue_id_fkey', 'Show', 'Venue', ['Venue_id'], ['id'])
    op.alter_column('Show', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('Show', 'start_time')
    op.drop_column('Show', 'venue_id')
    op.drop_column('Show', 'id')
    # ### end Alembic commands ###