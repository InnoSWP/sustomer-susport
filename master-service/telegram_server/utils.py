import logging
from functools import wraps

import telegram


def call_decorator(func):
    @wraps(func)
    def inner(*args, **kwargs):
        logging.info(f'{func.__name__}: {args}, {kwargs}')

        return func(*args, **kwargs)

    return inner


def get_button_markup(*buttons: ([str, str])):
    """Get list of reply markup buttons

    Args:
        buttons ([title, data]): each button represented by tuple

    Returns:
        InlineKeyboardMarkup: Description
    """
    x = lambda t: telegram.InlineKeyboardButton(t[0], callback_data=t[1])

    return telegram.InlineKeyboardMarkup.from_row(list(map(x, buttons)))
