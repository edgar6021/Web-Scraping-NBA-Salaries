import json
import csv
import scrapy

class NbaSpider(scrapy.Spider):
    name = 'nba_spider'
    start_urls = ['https://hoopshype.com/salaries/players/']

    def parse(self, response):
        data = []

        for row in response.css('table.hh-salaries-ranking-table tr')[1:]:
            player_name = row.css('td.name::text').get().strip()
            player_url = row.css('td.name a::attr(href)').get()

            # Cargar la página del jugador y extraer los datos
            yield scrapy.Request(player_url, callback=self.parse_player, cb_kwargs=dict(player_name=player_name, data=data))

        # Guardar los datos extraídos en un archivo JSON
        with open('nba_salaries.json', 'w') as file:
            json.dump(data, file)

        # Calcular el salario promedio de cada temporada
        season_totals = {}
        for player_info in data:
            player_salaries = player_info['salaries']
            for season, salary in player_salaries:
                salary_value = float(salary.replace('$', '').replace(',', ''))
                if season not in season_totals:
                    season_totals[season] = {'total_salary': salary_value, 'count': 1}
                else:
                    season_totals[season]['total_salary'] += salary_value
                    season_totals[season]['count'] += 1

        average_salaries = {season: info['total_salary'] / info['count'] for season, info in season_totals.items()}

        # Mostrar los salarios promedio por temporada
        for season, average_salary in average_salaries.items():
            print(f'Temporada {season} - Salario promedio: ${average_salary:,.2f}')

        # Guardar los salarios promedio en un archivo CSV
        with open('average_salaries.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['season', 'average_salary']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for season, average_salary in average_salaries.items():
                writer.writerow({'season': season, 'average_salary': average_salary})

    def parse_player(self, response, player_name, data):
        salary_table = response.css('table.hh-salaries-ranking-table')
        salaries = []

        if salary_table:
            for row in salary_table.css('tr')[1:]:
                season = row.css('td::text')[0].get().strip()
                salary = row.css('td::text')[1].get().strip()
                salaries.append((season, salary))

        # Guardar los datos extraídos en la lista data
        data.append({'name': player_name, 'salaries': salaries})
