class GroupNotFoundError(Exception):
    def __init__(self, group_id: int | str) -> None:
        super().__init__(f"Group with ID {group_id} not found.")
        self.group_id = group_id


class UserNotFoundError(Exception):
    def __init__(self, user_id: int | str):
        super().__init__(f"User with ID {user_id} not found.")
        self.user_id = user_id