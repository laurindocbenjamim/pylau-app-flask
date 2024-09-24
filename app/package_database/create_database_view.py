
import sqlalchemy as sa
from .helper_view import view


def create_view():

    if __name__ == "__main__":
        engine = sa.create_engine("sqlite://", echo=True)
        metadata = sa.MetaData()

        stuff = sa.Table(
            "stuff", metadata,
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("data", sa.String(50))
        )

        more_stuff = sa.Table(
            "more_stuff", metadata,
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("stuff_id", sa.Integer, sa.ForeignKey("stuff.id")),
            sa.Column("data", sa.String(50))
        )

        stuff_view = view(
            "stuff_view", metadata,
            sa.select(
                stuff.c.id.label("id"),
                stuff.c.data.label("data"),
                more_stuff.c.data.label("moredata")
            ).select_from(stuff.join(more_stuff)).where(stuff.c.data.like("%orange%"))
        )

        with engine.begin() as conn:
            metadata.create_all(conn)


def create_view(db):

    if __name__ == "__main__":
        engine = sa.create_engine("sqlite://", echo=True)
        metadata = sa.MetaData()

        stuff = sa.Table(
            "stuff", metadata,
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("data", sa.String(50))
        )

        more_stuff = sa.Table(
            "more_stuff", metadata,
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("stuff_id", sa.Integer, sa.ForeignKey("stuff.id")),
            sa.Column("data", sa.String(50))
        )

        stuff_view = view(
            "stuff_view", db.metadata,
            db.select(
                stuff.c.id.label("id"),
                stuff.c.data.label("data"),
                more_stuff.c.data.label("moredata")
            ).select_from(stuff.join(more_stuff)).where(stuff.c.data.like("%orange%"))
        )

        with engine.begin() as conn:
            metadata.create_all(conn)
