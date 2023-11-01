import pytest
import sqlalchemy


@pytest.mark.parametrize("name", ["Joe", "Jane"])
def test_isolation(create_user, user_model, fake_session_maker, name):
    """
    this test is run twice thanks to the parametrize decorator, while the expected
    result from the database is that there is only one user with id=1
    """
    result = create_user(name)
    assert result == "success"

    stmt = sqlalchemy.select(user_model.name)

    with fake_session_maker() as session:
        assert session.scalars(stmt).all() == [name]


@pytest.mark.asyncio
@pytest.mark.parametrize("name", ["Joe", "Jane"])
async def test_async_isolation(
    async_create_user, user_model, async_fake_session_maker, name
):
    """
    this test is run twice thanks to the parametrize decorator, while the expected
    result from the database is that there is only one user with id=1
    """
    result = await async_create_user(name)
    assert result == "success"

    stmt = sqlalchemy.select(user_model.name)

    async with async_fake_session_maker() as session:
        names_query = await session.scalars(stmt)
        names = names_query.all()
    assert names == [name]


@pytest.mark.parametrize("name", ["Joe", "Jane"])
def test_commit(create_user_with_commit, user_model, fake_session_maker, name):
    """
    this test is run twice thanks to the parametrize decorator, while the expected
    result from the database is that there is only one user with id=1
    """
    result = create_user_with_commit(name)
    assert result == "success"

    stmt = sqlalchemy.select(user_model.name)

    with fake_session_maker() as session:
        assert session.scalars(stmt).all() == [name]


@pytest.mark.asyncio
@pytest.mark.parametrize("name", ["Joe", "Jane"])
async def test_async_commit(
    async_create_user_with_commit, user_model, async_fake_session_maker, name
):
    """
    this test is run twice thanks to the parametrize decorator, while the expected
    result from the database is that there is only one user with id=1
    """
    result = await async_create_user_with_commit(name)
    assert result == "success"

    stmt = sqlalchemy.select(user_model.name)

    async with async_fake_session_maker() as session:
        query = await session.scalars(stmt)
        names = query.all()
    assert names == [name]


def test_auto_rollback(
    create_user_joe, read_user_with_auto_rollback, user_model, fake_session_maker
):
    """
    this test is run twice thanks to the parametrize decorator, while the expected
    result from the database is that there is only one user with id=1
    """
    result = read_user_with_auto_rollback()
    assert len(result) == 1

    stmt = sqlalchemy.select(user_model.name)
    with fake_session_maker() as session:
        assert session.scalars(stmt).all() == ["Joe"]


@pytest.mark.asyncio
async def test_async_auto_rollback(
    async_create_user_joe,
    async_read_user_with_auto_rollback,
    user_model,
    async_fake_session_maker,
):
    """
    this test is run twice thanks to the parametrize decorator, while the expected
    result from the database is that there is only one user with id=1
    """
    result = await async_read_user_with_auto_rollback()
    assert len(result) == 1

    stmt = sqlalchemy.select(user_model.name)
    async with async_fake_session_maker() as session:
        query = await session.scalars(stmt)
        names = query.all()
    assert names == ["Joe"]


@pytest.mark.parametrize(["name1", "name2"], [["Joe", "Jane"], ["Jane", "Joe"]])
def test_rollback_commit_rollback(
    create_user_rollback_commit_rollback,
    user_model,
    fake_session_maker,
    name1,
    name2,
):
    create_user_rollback_commit_rollback(name1, name2)

    stmt = sqlalchemy.select(user_model.name)
    with fake_session_maker() as session:
        query = session.scalars(stmt)
        names = query.all()
    assert names == [name2]

    create_user_rollback_commit_rollback(name1, name2)
    stmt = sqlalchemy.select(user_model.name)
    with fake_session_maker() as session:
        query = session.scalars(stmt)
        names = query.all()
    assert names == [name2, name2]


@pytest.mark.asyncio
@pytest.mark.parametrize(["name1", "name2"], [["Joe", "Jane"], ["Jane", "Joe"]])
async def test_async_rollback_commit_rollback(
    async_create_user_rollback_commit_rollback,
    user_model,
    async_fake_session_maker,
    name1,
    name2,
):
    await async_create_user_rollback_commit_rollback(name1, name2)

    stmt = sqlalchemy.select(user_model.name)
    async with async_fake_session_maker() as session:
        query = await session.scalars(stmt)
        names = query.all()
    assert names == [name2]

    await async_create_user_rollback_commit_rollback(name1, name2)
    stmt = sqlalchemy.select(user_model.name)
    async with async_fake_session_maker() as session:
        query = await session.scalars(stmt)
        names = query.all()
    assert names == [name2, name2]


@pytest.mark.parametrize("name", ["Joe", "Jane"])
def test_session_maker_factory(
    create_user_with_factory, user_model, fake_session_maker_with_factory, name
):
    """
    this test is run twice thanks to the parametrize decorator, while the expected
    result from the database is that there is only one user with id=1
    """
    result = create_user_with_factory(name)
    assert result == "success"

    stmt = sqlalchemy.select(user_model.name)

    with fake_session_maker_with_factory()() as session:
        assert session.scalars(stmt).all() == [name]


@pytest.mark.asyncio
@pytest.mark.parametrize("name", ["Joe", "Jane"])
async def test_async_isolation_factory(
    async_create_user, user_model, async_fake_session_maker, name
):
    """
    this test is run twice thanks to the parametrize decorator, while the expected
    result from the database is that there is only one user with id=1
    """
    result = await async_create_user(name)
    assert result == "success"

    stmt = sqlalchemy.select(user_model.name)

    async with async_fake_session_maker() as session:
        names_query = await session.scalars(stmt)
        names = names_query.all()
    assert names == [name]
