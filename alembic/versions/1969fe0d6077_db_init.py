"""db_init

Revision ID: 1969fe0d6077
Revises: 
Create Date: 2023-07-11 19:45:06.262699

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "1969fe0d6077"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("firstname", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("birthdate", sa.DATE(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone_number", sa.String(), nullable=True),
        sa.Column("profile_picture", sa.LargeBinary(), nullable=True),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("price", sa.FLOAT(), nullable=False),
        sa.Column("description", sa.TEXT(), nullable=True),
        sa.Column("characteristic", sa.ARRAY(item_type=sa.JSON), nullable=True),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("creator_id", sa.Integer(), nullable=False),
        sa.Column("pictures", sa.ARRAY(item_type=sa.LargeBinary), nullable=True),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["creator_id"], ["users.id"]),
    )
    op.create_table(
        "user_saved_post",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("user_id", "post_id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"]),
    ),
    op.create_table(
        "authentications",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )


def downgrade() -> None:
    pass
