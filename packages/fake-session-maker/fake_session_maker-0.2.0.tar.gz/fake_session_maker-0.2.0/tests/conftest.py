import pytest
import pytest_asyncio
import sqlalchemy.ext.asyncio
import sqlalchemy.orm

from fake_session_maker import async_fsm, fsm


@pytest.fixture(autouse=True, scope="session")
def db_migrate():
    path = "postgresql://test:test@localhost:5432/test"
    engine = sqlalchemy.create_engine(path, echo=True)
    with engine.connect() as con:
        con.execute(
            sqlalchemy.text(
                'create table if not exists "users" ('
                '   "id" serial constraint users_pk primary key , '
                '   "name" text'
                ");"
            )
        )
        con.commit()
    yield
    with engine.connect() as con:
        con.execute(sqlalchemy.text('drop table "users";'))
        con.commit()


@pytest.fixture
def namespace():
    """Keep wrong db make a forgotten monkeypatch of namespace obvious"""

    class Namespace:
        engine = sqlalchemy.create_engine(
            "postgresql://test:test@localhost:5432/test",
            echo=True,
        )
        session_maker = sqlalchemy.orm.sessionmaker(bind=engine)

    return Namespace


@pytest.fixture
def namespace_of_factory():
    """Keep wrong db make a forgotten monkeypatch of namespace obvious"""

    class Namespace:
        engine = sqlalchemy.create_engine(
            "postgresql://test:test@localhost:5432/test",
            echo=True,
        )

        @staticmethod
        def session_maker():
            return sqlalchemy.orm.sessionmaker(bind=Namespace.engine)

    return Namespace


class Base(sqlalchemy.orm.DeclarativeBase):
    pass


@pytest.fixture(scope="session")
def user_model():
    class User(Base):
        __tablename__ = "users"
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String)

    return User


@pytest.fixture
def create_user(namespace, user_model):
    """
    this fixture is used to test a function that rely on the auto-commit feature
    of the session_maker begin method
    """

    def create_user_(name: str):
        with namespace.session_maker.begin() as session:
            session.add(user_model(name=name))
        return "success"

    return create_user_


@pytest.fixture
def create_user_with_factory(namespace_of_factory, user_model):
    """
    this fixture is used to test a function that rely on the auto-commit feature
    of the session_maker begin method
    """

    def create_user_(name: str):
        with namespace_of_factory.session_maker().begin() as session:
            session.add(user_model(name=name))
        return "success"

    return create_user_


@pytest_asyncio.fixture
def async_create_user(namespace, user_model):
    """
    this fixture is used to test a function that rely on the auto-commit feature
    of the session_maker begin method
    """

    async def create_user_(name: str):
        async with namespace.session_maker.begin() as session:
            session.add(user_model(name=name))
        return "success"

    return create_user_


@pytest_asyncio.fixture
def async_create_user_with_factory(namespace_of_factory, user_model):
    """
    this fixture is used to test a function that rely on the auto-commit feature
    of the session_maker begin method
    """

    async def create_user_(name: str):
        async with namespace_of_factory.session_maker().begin() as session:
            session.add(user_model(name=name))
        return "success"

    return create_user_


@pytest.fixture
def create_user_with_commit(namespace, user_model):
    """
    this fixture is used to test a function that do a manual commit
    """

    def create_user_(name: str):
        with namespace.session_maker() as session:
            session.add(user_model(name=name))
            session.commit()
        return "success"

    return create_user_


@pytest_asyncio.fixture
def async_create_user_with_commit(namespace, user_model):
    """
    this fixture is used to test a function that do a manual commit
    """

    async def create_user_(name: str):
        async with namespace.session_maker() as session:
            session.add(user_model(name=name))
            await session.commit()
        return "success"

    return create_user_


@pytest.fixture
def read_user_with_auto_rollback(namespace, user_model):
    """
    this fixture is used to test a function that rely on the auto-rollback feature
    """

    def read_users():
        stmt = sqlalchemy.select(user_model.name)
        with namespace.session_maker() as session:
            users = session.scalars(stmt).all()
        return users

    return read_users


@pytest.fixture
def async_read_user_with_auto_rollback(namespace, user_model):
    """
    this fixture is used to test a function that rely on the auto-rollback feature
    """

    async def read_users():
        stmt = sqlalchemy.select(user_model.name)
        async with namespace.session_maker() as session:
            query = await session.scalars(stmt)
            users = query.all()
        return users

    return read_users


@pytest.fixture
def create_user_rollback_commit_rollback(namespace, user_model):
    def create_user_(name1: str, name2: str):
        with namespace.session_maker() as session:
            session.add(user_model(name=name1))
            session.rollback()
            session.add(user_model(name=name2))
            session.commit()
            session.add(user_model(name=name1))
            session.rollback()

    return create_user_


@pytest.fixture
def async_create_user_rollback_commit_rollback(namespace, user_model):
    async def create_user_(name1: str, name2: str):
        async with namespace.session_maker() as session:
            session.add(user_model(name=name1))
            await session.rollback()
            session.add(user_model(name=name2))
            await session.commit()
            session.add(user_model(name=name1))
            await session.rollback()

    return create_user_


@pytest.fixture
def fake_session_maker(namespace) -> sqlalchemy.orm.sessionmaker:
    with fsm(
        db_url="postgresql://test:test@localhost:5432/test",
        namespace=namespace,
        symbol_name="session_maker",
        create_engine_kwargs={"echo": True},
    ) as fake_session_maker_:
        yield fake_session_maker_


@pytest.fixture
def fake_session_maker_with_factory(
    namespace_of_factory,
) -> sqlalchemy.orm.sessionmaker:
    with fsm(
        db_url="postgresql://test:test@localhost:5432/test",
        namespace=namespace_of_factory,
        symbol_name="session_maker",
        create_engine_kwargs={"echo": True},
        mock_callable_return_value=True,
    ) as fake_session_maker_:
        yield fake_session_maker_


@pytest_asyncio.fixture
async def async_fake_session_maker(
    namespace,
) -> sqlalchemy.ext.asyncio.async_sessionmaker:
    async with async_fsm(
        db_url="postgresql+asyncpg://test:test@localhost:5432/test",
        namespace=namespace,
        symbol_name="session_maker",
        create_engine_kwargs={"echo": True},
    ) as async_fake_session_maker_:
        yield async_fake_session_maker_


@pytest_asyncio.fixture
async def async_fake_session_maker_with_factory(
    namespace_of_factory,
) -> sqlalchemy.ext.asyncio.async_sessionmaker:
    async with async_fsm(
        db_url="postgresql+asyncpg://test:test@localhost:5432/test",
        namespace=namespace_of_factory,
        symbol_name="session_maker",
        create_engine_kwargs={"echo": True},
        mock_callable_return_value=True,
    ) as async_fake_session_maker_:
        yield async_fake_session_maker_


@pytest.fixture
def create_user_joe(namespace, user_model, fake_session_maker):
    with namespace.session_maker.begin() as session:
        session.add(user_model(name="Joe"))


@pytest_asyncio.fixture
async def async_create_user_joe(namespace, user_model, async_fake_session_maker):
    async with namespace.session_maker.begin() as session:
        session.add(user_model(name="Joe"))
