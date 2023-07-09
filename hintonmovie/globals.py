from enum import Enum
from datetime import datetime

# class syntax
class AccountTypeEnum(Enum):
    MASTER_ADMIN = "Master_Admin"
    EDITOR = 'Editor'
    BUSINESS_ADMIN = "Business_Admin"
    SUPERVISOR = "Supervisor"
    BUSINESS_EDITOR = "Business_Editor"
    END_USER = "End_User"


class BusinessTypeEnum(Enum):
    NPO = "NPO"
    PROFIT = 'Profit'
    GOVERNMENT = "Government"


def get_current_date_time():
    current_date_time = datetime.now()
    return current_date_time.strftime("%Y-%m-%d"), current_date_time.strftime("%H:%M:%S")

