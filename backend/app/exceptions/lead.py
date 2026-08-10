class LeadNotFoundException(Exception):
    """
    Exception raised when a requested lead is not found.
    """
    def __init__(self, lead_id: str) -> None:
        self.lead_id = lead_id
        self.message = f"Lead with ID '{lead_id}' not found."
        super().__init__(self.message)


class InvalidLeadRelationshipException(Exception):
    """
    Exception raised when a lead contains an invalid company, customer, or employee relationship.
    """
    def __init__(self, detail: str) -> None:
        self.detail = detail
        self.message = detail
        super().__init__(self.message)
