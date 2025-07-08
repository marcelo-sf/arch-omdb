"""create movies and reviews tables

Revision ID: 0001_create_movies_and_reviews
Revises:
Create Date: 2025-07-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

TIMESTAMP_NOW_SQL = 'now()'

# revision identifiers
revision = '0001_create_movies_and_reviews'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'movies',
        sa.Column('imdb_id', sa.String(15), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('year', sa.Integer, nullable=True),
        sa.Column('metadata', sa.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text(TIMESTAMP_NOW_SQL), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True),
                  server_default=sa.text(TIMESTAMP_NOW_SQL), nullable=False),
    )
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer,
                  autoincrement=True, primary_key=True),
        sa.Column('imdb_id', sa.String(15),
                  sa.ForeignKey('movies.imdb_id', ondelete='CASCADE'),
                  nullable=False),
        sa.Column('user_opinion', sa.Text, nullable=False),
        sa.Column('user_rating', sa.SmallInteger,
                  sa.CheckConstraint('user_rating BETWEEN 1 AND 10'),
                  nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text(TIMESTAMP_NOW_SQL), nullable=False),
    )
    op.create_index('idx_reviews_imdb', 'reviews', ['imdb_id'])


def downgrade():
    op.drop_index('idx_reviews_imdb', table_name='reviews')
    op.drop_table('reviews')
    op.drop_table('movies')
