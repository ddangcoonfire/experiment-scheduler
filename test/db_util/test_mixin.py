"""
DBCommonMixin class method unittest
"""
from datetime import datetime
import pytest
from sqlalchemy import String, Column
from experiment_scheduler.db_util.mixin import DbCommonMixin
from experiment_scheduler.db_util.connection import Session, engine, Base


class Test(Base, DbCommonMixin):
    """
    desc : test table for mixin method test
    """

    __tablename__ = "test"
    id = Column(String(10), primary_key=True)


@pytest.fixture()
def connection():
    """
    desc : function scoped connection for unittest
    """
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(autouse=True)
def setup_db(connection, request):
    """
    desc : Creates all database tables as declared in SQLAlchemy models,
    then proceeds to drop all the created tables after all tests
    have finished running.
    """
    Base.metadata.create_all(bind=connection)

    def teardown():
        Base.metadata.drop_all(bind=connection)

    request.addfinalizer(teardown)
    return None


@pytest.fixture(autouse=True)
def db_session(connection, setup_db, request):
    """
    desc : function scoped session for unittest
    """
    session = Session(bind=connection)
    session.expire_on_commit = False

    def teardown():
        Session.remove()
        connection.rollback()

    request.addfinalizer(teardown)
    return session


def test_list(db_session):
    """
    desc : Test that the list method returns all the data that meets the specified conditions
    """
    # Arrange
    tests = [
        {
            "id": 1,
            "created_at": datetime(2023, 4, 23),
            "updated_at": datetime(2023, 4, 23),
        },
        {
            "id": 2,
            "created_at": datetime(2023, 4, 22),
            "updated_at": datetime(2023, 4, 22),
        },
    ]
    for test in tests:
        db_test = Test(**test)
        db_session.add(db_test)
    db_session.commit()

    # Act
    result = Test.list(order_by=Test.created_at)

    # Assert
    assert len(result) == 2
    assert result[0].created_at == datetime(2023, 4, 22)
    assert result[1].created_at == datetime(2023, 4, 23)


def test_get(db_session):
    """
    desc : Test that the get method returns a single row that meets the specified conditions
    """
    # Test that the get method returns a single row that meets the specified conditions
    # Arrange
    obj = Test(
        id="test1", created_at=datetime(2023, 4, 22), updated_at=datetime(2023, 4, 22)
    )
    db_session.add(obj)
    db_session.commit()

    # Act
    result = Test.get(id="test1")

    # Assert
    assert result == obj


def test_insert(db_session):
    """
    desc : Test that the insert method inserts data into the table
    """
    # Arrange
    obj = Test(
        id="test2", created_at=datetime(2023, 4, 22), updated_at=datetime(2023, 4, 22)
    )

    # Act
    Test.insert(obj)

    # Assert
    result = db_session.query(Test).get({"id": "test2"})
    assert result.id == obj.id
    assert result.created_at == obj.created_at
    assert result.updated_at == obj.updated_at


def test_update(db_session):
    """
    desc : Test that the insert method inserts data into the table
    """
    # Arrange
    obj = Test(
        id="test2", created_at=datetime(2023, 4, 22), updated_at=datetime(2023, 4, 22)
    )
    db_session.add(obj)
    db_session.commit()

    # Act
    target = Test.get(id="test2")
    target.updated_at = datetime(2023, 4, 25)
    target.commit()

    # Assert
    result = Test.get(id="test2")
    assert result.id == obj.id
    assert result.created_at == obj.created_at
    assert result.updated_at == datetime(2023, 4, 25)
