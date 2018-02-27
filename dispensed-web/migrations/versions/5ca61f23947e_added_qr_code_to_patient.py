"""Added QR code to Patient

Revision ID: 5ca61f23947e
Revises: 2a1be09d2c47
Create Date: 2018-02-21 23:15:18.360000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ca61f23947e'
down_revision = '2a1be09d2c47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patient', sa.Column('qr_code', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_patient_qr_code'), 'patient', ['qr_code'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_patient_qr_code'), table_name='patient')
    op.drop_column('patient', 'qr_code')
    # ### end Alembic commands ###
