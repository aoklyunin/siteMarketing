from consumer.localCode import getViewCnt, leaveCampany, getRepostedCompanies
from consumer.models import ConsumerMarketCamp, Consumer
from django.core.management import BaseCommand

from mainApp.localCode import checkBotUser, getImages, getFriendsUsers, getFollowersUsers


# Алиса 32897432
# Я 303154598
# мама 2600557
# бот 453386628
# Игорь 32381970
# Михан 34499244


class Command(BaseCommand):
    def handle(self, *args, **options):
        #checkBotUser(2600557, Consumer.objects.first().vk_token)
        getFollowersUsers(34499244, Consumer.objects.first().vk_token)
        #for u in Consumer.objects.all():
        #    print(checkBotUser(u))