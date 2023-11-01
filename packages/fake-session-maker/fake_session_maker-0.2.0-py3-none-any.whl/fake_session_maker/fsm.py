import contextlib
import typing

import pytest
import sqlalchemy.event
import sqlalchemy.ext.asyncio
import sqlalchemy.orm


@contextlib.contextmanager
def fsm(
    db_url: str,
    namespace: typing.Any,
    symbol_name: str,
    *,
    create_engine_kwargs: typing.Optional[typing.Mapping] = None,
    mock_callable_return_value: bool = False,
) -> typing.Generator[sqlalchemy.orm.sessionmaker, None, None]:
    """
    :param db_url: url of the test.py database
    :param namespace: namespace where the original session_maker is located
    :param symbol_name: name of the original session_maker symbol
    :param create_engine_kwargs: keyword arguments to pass to sqlalchemy.create_engine
    :param mock_callable_return_value: to mock a callable that returns the session_maker
    :return: a context manager that can be used as a session_maker
    """
    if create_engine_kwargs is None:
        create_engine_kwargs = {}

    engine = sqlalchemy.create_engine(
        url=db_url,
        **create_engine_kwargs,
    )

    if db_url.startswith("sqlite"):

        @sqlalchemy.event.listens_for(engine, "connect")
        def do_connect(dbapi_connection: typing.Any, _: typing.Any) -> None:
            # disable pysqlite's emitting of the "BEGIN" statement entirely.
            # also stops it from emitting COMMIT before any DDL.
            dbapi_connection.isolation_level = None

        @sqlalchemy.event.listens_for(engine, "begin")
        def do_begin(connexion: sqlalchemy.engine.Connection) -> None:
            # emit our own "BEGIN"
            connexion.exec_driver_sql("BEGIN")

    with engine.connect() as conn, conn.begin() as transaction:
        session_maker = sqlalchemy.orm.sessionmaker(
            bind=conn,
            join_transaction_mode="create_savepoint",
        )

        def session_maker_factory(
            *_: typing.Any, **__: typing.Any
        ) -> sqlalchemy.orm.sessionmaker:
            return session_maker

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                namespace,
                symbol_name,
                session_maker_factory if mock_callable_return_value else session_maker,
            )
            yield session_maker_factory if mock_callable_return_value else session_maker

        transaction.rollback()


@contextlib.asynccontextmanager
async def async_fsm(
    db_url: str,
    namespace: typing.Any,
    symbol_name: str,
    *,
    create_engine_kwargs: typing.Optional[typing.Mapping] = None,
    mock_callable_return_value: bool = False,
) -> typing.AsyncIterator[sqlalchemy.ext.asyncio.async_sessionmaker]:
    """
    :param db_url: url of the test.py database
    :param namespace: namespace where the original async_session_maker is located
    :param symbol_name: name of the original session_maker symbol
    :param create_engine_kwargs: keyword arguments to pass to sqlalchemy.create_engine
    :param mock_callable_return_value: to mock a callable that returns the session_maker
    :return: a context manager that can be used as a session_maker
    :raises NotImplementedError: if the db_url starts with "sqlite"
    """
    if create_engine_kwargs is None:
        create_engine_kwargs = {}

    engine = sqlalchemy.ext.asyncio.create_async_engine(
        url=db_url,
        **create_engine_kwargs,
    )

    if db_url.startswith("sqlite"):
        raise NotImplementedError("sqlite does not support async yet")

    async with engine.connect() as conn, conn.begin() as transaction:
        session_maker = sqlalchemy.ext.asyncio.async_sessionmaker(
            bind=conn,
            join_transaction_mode="create_savepoint",
        )

        def session_maker_factory(
            *_: typing.Any, **__: typing.Any
        ) -> sqlalchemy.ext.asyncio.async_sessionmaker:
            return session_maker

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                namespace,
                symbol_name,
                session_maker_factory if mock_callable_return_value else session_maker,
            )
            yield session_maker_factory if mock_callable_return_value else session_maker

        await transaction.rollback()
