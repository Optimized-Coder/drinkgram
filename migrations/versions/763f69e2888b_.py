"""empty message

Revision ID: 763f69e2888b
Revises: 168d23b88911
Create Date: 2023-09-17 18:38:17.361404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '763f69e2888b'
down_revision = '168d23b88911'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('photo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_photo_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('photo', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_photo_timestamp'))
        batch_op.drop_column('timestamp')

    # ### end Alembic commands ###
