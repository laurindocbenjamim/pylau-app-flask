
from .twoFAModel import TwoFAModel

"""
    Load a TwoFAModel object with the provided data.

    Args:
        data (dict): A dictionary containing the data for the TwoFAModel object.

    Returns:
        TwoFAModel: The loaded TwoFAModel object.

    """

load_two_fa_obj = lambda data: TwoFAModel(
    userID = data.get('userID'),
    two_factor_auth_secret = data.get('two_factor_auth_secret'),
    method_auth = data.get('method_auth'),
    is_active = data.get('is_active')
)
