import enum


class UserRole(enum.Enum):
    SUPERADMIN = "SUPERADMIN"
    ADMIN = "ADMIN"
    ANONYMOUS = "ANONYMOUS"
