class AuthenticationFailedException(Exception):
    """
    Exception raised when authentication fails due to invalid email or password.
    """
    def __init__(self, message: str = "Incorrect email or password") -> None:
        self.message = message
        super().__init__(self.message)
