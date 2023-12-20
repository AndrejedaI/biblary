from sqlalchemy import MetaData,Integer,String,Table,Column,ForeignKey


metadata = MetaData()

author = Table(
    "author",
    metadata,
    Column("id",Integer,primary_key=True, autoincrement=True),
    Column("name",String,nullable=False),
    Column("lastname",String,nullable=False),
    Column("surname",String,nullable=False),
)

publisher = Table(
    "publisher",
    metadata,
    Column("id",Integer,primary_key=True, autoincrement=True),
    Column("publisher",String,nullable=False),
    Column("city",String,nullable=False),
)

books = Table(
    "book",
    metadata,
    Column("id",Integer,primary_key=True, autoincrement=True),
    Column("title", String,nullable=False),
    Column("kind",String,nullable=False),
    Column("year",Integer,nullable=False),
    Column("id_author",Integer,ForeignKey("author.id")),
    Column("id_publisher",Integer,ForeignKey("publisher.id")),

)