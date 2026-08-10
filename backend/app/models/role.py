from enum import Enum


class UserRole(str, Enum):
    """
    Supported user roles in the MiniCRM system.
    """
    ADMIN = "admin"
    EMPLOYEE = "employee"
