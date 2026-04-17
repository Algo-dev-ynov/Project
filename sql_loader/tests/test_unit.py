from sql_loader.src.normalizer import SQLValueNormalizer
from sql_loader.src.exporter import PlaceExporter, RatingExporter


class DummyMongoReader:
    pass


class DummySQLConnection:
    def __init__(self):
        self.cursor = object()


def test_normalize_none():
    assert SQLValueNormalizer.normalize(None) is None


def test_normalize_string():
    assert SQLValueNormalizer.normalize("test") == "test"


def test_normalize_integer():
    assert SQLValueNormalizer.normalize(42) == 42


def test_normalize_float():
    assert SQLValueNormalizer.normalize(3.14) == 3.14


def test_normalize_list():
    result = SQLValueNormalizer.normalize(["a", "b"])
    assert result == '["a", "b"]'


def test_normalize_dict():
    result = SQLValueNormalizer.normalize({"key": "value"})
    assert result == '{"key": "value"}'


def test_normalize_object_to_string():
    class DummyObject:
        def __str__(self):
            return "dummy"

    assert SQLValueNormalizer.normalize(DummyObject()) == "dummy"


def test_place_exporter_initialization():
    mongo_reader = DummyMongoReader()
    sql_connection = DummySQLConnection()

    exporter = PlaceExporter(mongo_reader, sql_connection)

    assert exporter.mongo_reader is mongo_reader
    assert exporter.sql_connection is sql_connection
    assert exporter.cursor == sql_connection.cursor


def test_rating_exporter_initialization():
    mongo_reader = DummyMongoReader()
    sql_connection = DummySQLConnection()

    exporter = RatingExporter(mongo_reader, sql_connection)

    assert exporter.mongo_reader is mongo_reader
    assert exporter.sql_connection is sql_connection
    assert exporter.cursor == sql_connection.cursor