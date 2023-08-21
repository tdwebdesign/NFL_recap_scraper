from asgiref.sync import sync_to_async
from fantasy_news.models import GameRecap


class DjangoSavePipeline(object):

    @sync_to_async
    def _get_or_create_recap(self, item):
        try:
            recap = GameRecap.objects.get(game_id=item['game_id'])
        except GameRecap.DoesNotExist:
            recap = GameRecap()

        recap.game_id = item['game_id']
        recap.date = item['game_recap_date']
        recap.title = item['game_recap_title']
        recap.body = item['game_recap_body']
        recap.save()

    async def process_item(self, item, spider):
        await self._get_or_create_recap(item)
        return item
