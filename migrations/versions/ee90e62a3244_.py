"""empty message

Revision ID: ee90e62a3244
Revises: 32b55c822cb8
Create Date: 2024-02-15 01:13:14.474845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee90e62a3244'
down_revision = '32b55c822cb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Customers',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('GivenName', sa.String(length=50), nullable=False),
    sa.Column('Surname', sa.String(length=50), nullable=False),
    sa.Column('Streetaddress', sa.String(length=50), nullable=True),
    sa.Column('City', sa.String(length=50), nullable=True),
    sa.Column('Zipcode', sa.String(length=10), nullable=True),
    sa.Column('Country', sa.String(length=30), nullable=True),
    sa.Column('CountryCode', sa.String(length=2), nullable=True),
    sa.Column('Birthday', sa.DateTime(), nullable=True),
    sa.Column('PersonalNumber', sa.String(length=20), nullable=False),
    sa.Column('TelephoneCountryCode', sa.String(length=20), nullable=True),
    sa.Column('Telephone', sa.String(length=20), nullable=True),
    sa.Column('EmailAddress', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('User',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Username', sa.String(length=50), nullable=True),
    sa.Column('Password', sa.String(length=255), nullable=True),
    sa.Column('CompanyEmail', sa.String(length=50), nullable=True),
    sa.Column('FirstName', sa.String(length=50), nullable=True),
    sa.Column('LastName', sa.String(length=50), nullable=True),
    sa.Column('Role', sa.String(length=50), nullable=True),
    sa.Column('InformationPermission', sa.Boolean(), nullable=True),
    sa.Column('ManagementPermission', sa.Boolean(), nullable=True),
    sa.Column('PlaceholderPermission', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('Accounts',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('AccountType', sa.String(length=10), nullable=False),
    sa.Column('Created', sa.DateTime(), nullable=False),
    sa.Column('Balance', sa.Integer(), nullable=False),
    sa.Column('CustomerId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['CustomerId'], ['Customers.Id'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('CustomerContact',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('FirstName', sa.String(length=50), nullable=True),
    sa.Column('LastName', sa.String(length=50), nullable=True),
    sa.Column('Email', sa.String(length=50), nullable=True),
    sa.Column('Message', sa.String(length=255), nullable=True),
    sa.Column('CustomerId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CustomerId'], ['Customers.Id'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('Transactions',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Type', sa.String(length=20), nullable=False),
    sa.Column('Operation', sa.String(length=50), nullable=False),
    sa.Column('Date', sa.DateTime(), nullable=False),
    sa.Column('Amount', sa.Integer(), nullable=False),
    sa.Column('NewBalance', sa.Integer(), nullable=False),
    sa.Column('AccountId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['AccountId'], ['Accounts.Id'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Transactions')
    op.drop_table('CustomerContact')
    op.drop_table('Accounts')
    op.drop_table('User')
    op.drop_table('Customers')
    # ### end Alembic commands ###
