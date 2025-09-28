import pytest
from database import init_db, close_db
from database import (
    create_user, 
    create_group, 
    get_users_groups, 
    is_user_in_group,
    get_user,
    get_group,
)


@pytest.fixture(scope="module", autouse=True)
async def test_setup_db():
    # Initialize in-memory SQLite DB for tests
    await init_db()


@pytest.mark.asyncio
async def test_create_group_and_user():
    # Create groups
    await create_group(group_id=101, name="Admins")
    await create_group(group_id=102, name="Editors")

    # Create user and attach to group
    await create_user(user_id=1, username="alice", name="Alice Smith", group_id=101)

    # Test that user exists
    user = await get_user(user_id=1)
    assert user.username == "alice"
    assert user.name == "Alice Smith"

    # Test that group exists
    group = await get_group(group_id=101)
    assert group.name == "Admins"

    # Test relation
    in_group = await is_user_in_group(user_id=1, group_id=101)
    assert in_group is True

@pytest.mark.asyncio
async def test_user_groups_list():
    # Add another group
    await create_group(group_id=102, name="Editors")
    await create_user(user_id=1, username="alice", name="Alice Smith", group_id=102)

    # Fetch groups by name
    names = await get_users_groups(user_id=1)
    assert set(names) == {"Admins", "Editors"}

    # Fetch groups by ID
    ids = await get_users_groups(user_id=1, send_id=True)
    assert set(ids) == {101, 102}

@pytest.mark.asyncio
async def test_updating_user():
    # Update username and name
    await create_user(user_id=1, username="alice_wonder", name="Alice Wonderland", group_id=101)
    user = await get_user(user_id=1)
    assert user.username == "alice_wonder"
    assert user.name == "Alice Wonderland"

@pytest.mark.asyncio
async def test_nonexistent_user_or_group():
    # Nonexistent user
    groups = await get_users_groups(user_id=999)
    assert groups == []

    # Nonexistent group check
    in_group = await is_user_in_group(user_id=1, group_id=999)
    assert in_group is False