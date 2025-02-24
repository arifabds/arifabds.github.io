from ..Scraping.scraper import Scraper
from ..Scraping.scrape_editor import ScrapeEditor
from ..Token_Balancers.keyword_generator import KeywordGenerator
from ..Token_Balancers.scraped_data_editor import ScrapedDataEditor

class ScrapeManager:
    def __init__(self, model, selenium_driver_path, api_handler_key_gen, api_key_gen, api_handler_scraped_data_editor, api_key_scrape):
        self.scraper = Scraper(selenium_driver_path)
        self.scrape_editor = ScrapeEditor()
        #self.keyword_generator = KeywordGenerator(model, api_handler_key_gen, api_key_gen)
        self.scraped_data_final = ScrapedDataEditor(model, api_handler_scraped_data_editor, api_key_scrape )
        self.keywords = ""

    def results(self, results_with_links, query, keywords):

        links = []
        
        for line in results_with_links.splitlines():
            if line.strip().startswith("Link:"):
                link = line.split("Link:")[1].strip()
                links.append(link)
        #self.keywords = self.keyword_generator.generate_keywords(query)

        scraped_data = self.scraper.scrape_links(links, keywords)
        
        formatted_scrape_data = self.scrape_editor.format_scraped_data(scraped_data)

        #print("formatlanmış final olmayan scrape data:", formatted_scrape_data)

        # for i, data in enumerate(formatted_scrape_data):
        #     print(f"\nFormatlanmış {i}. veri:")
        #     print(f"  Link: {data['link']}") 
        #     if 'error' in data: 
        #         print(f"  Hata: {data['error']}")
        #     else:  
        #         print(f"  Başlık: {data.get('başlık', 'Başlık bulunamadı')}")
        #         print(f"  İçerik: {data.get('içerik', 'İçerik bulunamadı')}")
        #     print("-" * 30)


        final_data = self.scraped_data_final.EditScrapedData(formatted_scrape_data, query)

        return final_data