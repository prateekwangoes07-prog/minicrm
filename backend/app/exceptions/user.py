class EmailAlreadyExistsException(Exception):
    """
    Exception raised when a user tries to register with an email that already exists.
    """
    def __init__(self, email: str) -> None:
        self.email = email
        self.message = f"User with email '{email}' already exists."
        super().__init__(self.message)
