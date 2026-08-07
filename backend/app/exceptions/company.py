class CompanyNotFoundException(Exception):
    """
    Exception raised when a requested company is not found.
    """
    def __init__(self, company_id: str) -> None:
        self.company_id = company_id
        self.message = f"Company with ID '{company_id}' not found."
        super().__init__(self.message)


class CompanyAlreadyExistsException(Exception):
    """
    Exception raised when attempting to create or update a company with a name or email that already exists.
    """
    def __init__(self, detail: str) -> None:
        self.detail = detail
        self.message = detail
        super().__init__(self.message)
