class EmployeeNotFoundException(Exception):
    """
    Exception raised when a requested employee (user) is not found.
    """
    def __init__(self, employee_id: str) -> None:
        self.employee_id = employee_id
        self.message = f"Employee with ID '{employee_id}' not found."
        super().__init__(self.message)


class EmployeeAlreadyExistsException(Exception):
    """
    Exception raised when an employee registration fails due to duplicate email.
    """
    def __init__(self, detail: str) -> None:
        self.detail = detail
        self.message = detail
        super().__init__(self.message)
