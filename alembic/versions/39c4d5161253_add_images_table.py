"""“add_images_table”

Revision ID: 39c4d5161253
Revises: d636d746e8b4
Create Date: 2023-04-24 03:11:07.591706

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "39c4d5161253"
down_revision = "d636d746e8b4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "image",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("recipe_id", sa.Integer(), nullable=True),
        sa.Column(
            "image_type", sa.Enum("recipe", "step", name="imagetype"), nullable=True
        ),
        sa.Column("filename", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["recipe_id"],
            ["recipes.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_image_id"), "image", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_image_id"), table_name="image")
    op.drop_table("image")
    # ### end Alembic commands ###
