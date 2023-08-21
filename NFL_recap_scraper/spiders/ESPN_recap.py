import scrapy

import datefinder
from datetime import date


class EspnRecapSpider(scrapy.Spider):
    name = "ESPN_recap"
    allowed_domains = ["www.espn.com"]
    start_urls = [
        "https://www.espn.com/nfl/scoreboard/_/week/2/year/2023/seasontype/1",
        ]

    def parse(self, response):
        # Extract game ids from the scoreboard page
        game_ids = response.css('section::attr(id)').getall()

        # Loop through each game id and extract the recap
        for game_id in game_ids:
            # Get the recap url
            recap_url = f"https://www.espn.com/nfl/recap?gameId={game_id}"

            # Follow the recap url and parse the recap
            yield scrapy.Request(url=recap_url, callback=self.parse_recap)

    def parse_recap(self, response):

        game_id = response.url.split("=")[-1]

        # Extract game recap title
        game_recap_title = response.css('.Story__Headline::text').get()

        # Extract game recap text
        game_recap_body = response.css('.Story__Body p::text, .Story__Body p a::text').extract()
        game_recap_body = ' '.join(game_recap_body)

        # Extract game recap date
        game_recap_date_text = response.css('.Byline__Meta--publishDate::text').get()
        dates = list(datefinder.find_dates(game_recap_date_text))

        if dates:
            game_recap_date = dates[0]
        else:
            game_recap_date = date.today() # or a default date if you prefer
        # Create a dictionary for the game
        game = {
            'game_id': game_id,
            'game_recap_date': game_recap_date,
            'game_recap_title': game_recap_title,
            'game_recap_body': game_recap_body,
        }

        # Yield the game
        yield game

