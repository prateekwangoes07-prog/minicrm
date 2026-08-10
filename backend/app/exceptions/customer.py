class CustomerNotFoundException(Exception):
    """
    Exception raised when a requested customer is not found.
    """
    def __init__(self, customer_id: str) -> None:
        self.customer_id = customer_id
        self.message = f"Customer with ID '{customer_id}' not found."
        super().__init__(self.message)


class CustomerAlreadyExistsException(Exception):
    """
    Exception raised when attempting to create or update a customer with a duplicate email.
    """
    def __init__(self, detail: str) -> None:
        self.detail = detail
        self.message = detail
        super().__init__(self.message)
