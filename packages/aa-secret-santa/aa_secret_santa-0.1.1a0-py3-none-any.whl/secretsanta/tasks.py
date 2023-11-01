from random import shuffle

from celery import shared_task

from allianceauth.services.hooks import get_extension_logger

from .app_settings import discordbot_active
from .models import Application, SantaPair, Year

logger = get_extension_logger(__name__)

if discordbot_active():
    from aadiscordbot.tasks import send_message


@shared_task
def generate_pairs(year: int):
    year_obj = Year.objects.get(year=year)
    applications = Application.objects.filter(year=year_obj)
    applications_list = list(applications)
    pairs = []
    invalid_list = True
    while invalid_list:
        pairs = []
        shuffle(applications_list)
        for i, santa in enumerate(applications):
            santee = applications_list[i]
            if santa.user == santee.user:
                invalid_list = True
                break
            else:
                pairs.append((santa.user, santee.user))

        if len(pairs) == applications.count():
            invalid_list = False

    for pair in pairs:
        SantaPair.objects.create(
            santa=pair[0],
            santee=pair[1],
            year=year_obj
        )
    year_obj.open = False
    year_obj.save()


@shared_task
def notify_santas(year: Year) -> None:
    year_obj = Year.objects.get(year=year)
    for pair in SantaPair.objects.filter(year=year_obj):
        if discordbot_active():
            message = f"henlo {pair.santa} please gib shinies to {pair.santee}"
            send_message(user=pair.santa, message=message)
    pass


@shared_task
def notify_outstanding_santees(year: Year) -> None:
    year_obj = Year.objects.get(year=year)
    for pair in SantaPair.objects.filter(year=year_obj, delivered=False):
        if discordbot_active():
            message = f"henlo {pair.santee} you have not marked your gift as received, please let leadership know if you havent received anything"
            send_message(user=pair.santee, message=message)
        pass
