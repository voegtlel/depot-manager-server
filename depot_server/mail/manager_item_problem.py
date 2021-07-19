import traceback
from dataclasses import dataclass

from typing import Optional, List

from depot_server.db import DbItem, DbReservation
from depot_server.helper.auth import get_profiles
from depot_server.mail.mailer import mailer


@dataclass
class ProblemItem:
    problem: bool
    comment: str
    item: Optional[DbItem]


async def send_manager_item_problem(sender: dict, items: List[ProblemItem], reservation: Optional[DbReservation]):
    managers = [
        profile
        for profile in await get_profiles()
        if 'manager' in profile.get('roles', ()) and profile.get('email')
    ]

    for manager in managers:
        try:
            await mailer.async_send_mail(
                None,
                'manager_item_problem',
                manager['email'],
                {'sender': sender, 'user': manager, 'items': items, 'reservation': reservation},
            )
        except BaseException:
            traceback.print_exc()
