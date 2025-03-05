class User:
    """
    User class to represent a user in the system.

    Attributes:
    - user_id (int): The unique id of the user.
    - name (str): The name of the user.
    """

    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name
