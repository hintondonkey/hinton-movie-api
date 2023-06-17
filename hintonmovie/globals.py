from enum import Enum

# class syntax
class AccountTypeEnum(Enum):
    MASTER_ADMIN = "Master_Admin"
    EDITOR = 'Editor'
    BUSINESS_ADMIN = "Business_Admin"
    SUPERVISOR = "Supervisor"
    BUSINESS_EDITOR = "Business_Editor"
    END_USER = "End_User"