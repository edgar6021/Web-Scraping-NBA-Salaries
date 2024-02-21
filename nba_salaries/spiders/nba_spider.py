import scrapy

class NbaSpider(scrapy.Spider):
    name = 'nba_spider'
    allowed_domains = ['hoopshype.com']
    start_urls = ['https://hoopshype.com/salaries/players/']

    def parse(self, response):
        for row in response.css('.hh-salaries-table-sortable tbody tr'):
            player_name = row.css('td.name a::text').get()
            if player_name is not None:
                player_name = player_name.strip()
            salaries = []
            for salary_row in row.css('td.hh-salaries-sorted'):
                salary = salary_row.css('::text').get()
                if salary:
                    salaries.append(salary.strip())
            if player_name:
                yield {
                    'name': player_name,
                    'salaries': salaries
                }
