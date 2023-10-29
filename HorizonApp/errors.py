class InvestorAppException(Exception):
    def __init__(self, message, code=None):
        self.message = message
        self.code = code


USER_NO_ACCESS = (1000, "User has no access.")
EMAIL_REQUIRED = (1001, "Email is required.")
PASSWORD_REQUIRED = (1002, "Password is required.")
EMAIL_DUPLICATE = (1003, "Email already exists.")
PASSWORD_DOES_NOT_MATCH = (1004, "Password does not match.")
INVALID_PASSWORD = (1005, "Password is invalid.")
TRANSACTION_LOG_CREATE_FAILED = (1006, "Transaction log create failed.")
REACHED_MAX_USERS_ON_BUSINESS = (1007, "Reached max users on creating business")
