import sqlalchemy
from geoalchemy2 import Geometry

metadata = sqlalchemy.MetaData()

voivodeships = sqlalchemy.Table(
    'voivodeships',
    metadata,
    sqlalchemy.Column(
        'id',
        sqlalchemy.Integer,
        primary_key=True
    ),
    sqlalchemy.Column(
        'name',
        sqlalchemy.String(length=128)
    ),
    sqlalchemy.Column(
        'area',
        Geometry(geometry_type='POLYGON', srid=4326)
    )
)

events = sqlalchemy.Table(
    'events',
    metadata,
    sqlalchemy.Column(
        'id',
        sqlalchemy.Integer,
        primary_key=True
    ),
    sqlalchemy.Column(
        'name',
        sqlalchemy.String(length=128),
    ),
    sqlalchemy.Column(
        'description',
        sqlalchemy.String(length=1000)
    ),
    sqlalchemy.Column(
        "voivodeship_id",
        sqlalchemy.ForeignKey('voivodeships.id')
    )
)
