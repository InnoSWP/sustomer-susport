import enum
import json
import logging
from dataclasses import dataclass
from functools import wraps
from typing import Optional, TypeVar

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


class IssueState(enum.Enum):
    open = 'OPEN'
    progress = 'IN PROGRESS'
    closed = 'CLOSED'

    def __str__(self):
        return self.value.__str__()


class CallbackQueryType(enum.IntEnum):
    ASSIGN = 1
    CLOSE = 2
    REJECT = 3

    def __str__(self):
        return self.value.__str__()


@dataclass
class DialogEntity:
    issue_id: int
    client_id: int

    volunteer_chat_id: Optional[int] = None

    question_text: str = ''
    answer_text: str = ''

    issue_message_id: Optional[int] = None
    state: IssueState = IssueState.open


def get_issue_message_text(dialog: DialogEntity, user_name=None):
    issue_line = f'*Issue #{dialog.issue_id}*\n\n'
    question_line = f'Question: _"{dialog.question_text}"_\n\n'

    if dialog.state == IssueState.open:
        return f'{issue_line}' \
               f'{question_line}' \
               f'status: *OPEN*'
    elif dialog.state == IssueState.progress and dialog.volunteer_chat_id:
        return f'{issue_line}' \
               f'{question_line}' \
               f'status: *IN PROGRESS* by {user_name}'
    elif dialog.state == IssueState.closed:
        return f'{issue_line}' \
               f'{question_line}' \
               f'Answers:\n{dialog.answer_text}\n\n' \
               f'status: *CLOSED* by {user_name}'
    else:
        return f'LOL why does this happen?'


T = TypeVar('T')


def search_by(entities_list: [T], field, value) -> Optional[list[T]]:
    l = list(filter(
        lambda d: d.__getattribute__(field) == value,
        entities_list
    ))

    if len(l) >= 1:  # TODO manage it
        return l[-1]
    else:
        return None


def keyboard_from_dialog(title: str, dialog: DialogEntity, btn_type: CallbackQueryType, group_message_id):
    btn_data = json.dumps({
        'issue_id': dialog.issue_id,
        'btn_type': btn_type,
        'group_message_id': group_message_id
    })
    return get_button_markup([title, btn_data])


def prepare_for_markdown_mode(message: str):
    message = message.replace('#', '\#')
    message = message.replace('-', '\-')
    message = message.replace('.', '\.')

    return message
