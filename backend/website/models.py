from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column, Integer, String, Table, DateTime, Boolean
from sqlalchemy.sql import func

Base = declarative_base()

# Smaller id goes first, easier lookup
Colab = Table(
    "colab_table",
    Base.metadata,
    Column("artist1_id", ForeignKey("artists.id"), primary_key=True),
    Column("artist2_id", ForeignKey("artists.id"), primary_key=True),
    # Column("track_id", ForeignKey("tracks.id"))
)


class Artist(Base):
    __tablename__ = "artists"

    id = Column(String, primary_key=True)
    name = Column(String)
    last_upadte = Column(DateTime(timezone=True), server_default=func.now())
    complete_node = Column(Boolean)
    colabs = relationship(
        "Artist",
        secondary=Colab,
        primaryjoin=id == Colab.c.artist1_id,
        secondaryjoin=id == Colab.c.artist2_id,
        backref="left_nodes",
    )

    def __repr__(self):
        return f"<Artist(id:{self.id}, name:{self.name})>"


class Track(Base):
    __tablename__ = "tracks"
    id = Column(String, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<Track(id:{self.id}, name:{self.name})>"
