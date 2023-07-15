from scraper.VikingsScraper import VikingsScraper
from SQL.VikingsDBScraperConnector import vikings_db_connector


def run_scraper():
    vikings_scraper = VikingsScraper()
    merged_cast_info = vikings_scraper.scrape_all_data()

    vikings_db_connector.insert_character_and_actor(merged_cast_info)

    vikings_db_connector.close_conn()
