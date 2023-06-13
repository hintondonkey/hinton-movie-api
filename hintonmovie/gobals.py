from enum import Enum

# class syntax
class AccountTypeEnum(Enum):
    MASTER_ADMIN = "Master_Admin"
    EDITOR = 'Editor'
    BUSINESS_ADMIN = "Business_Admin"
    END_USER = "End_User"