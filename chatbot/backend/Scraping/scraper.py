import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    def __init__(self, selenium_driver_path):
        self.selenium_driver_path = selenium_driver_path
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-software-rasterizer")
        self.options.add_argument("--mute-audio")
        self.options.add_argument("--disable-features=VizDisplayCompositor")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--log-level=3")
        self.options.add_argument("--disable-media-session-api")
        self.options.add_argument("window-size=1920,1080")
        self.driver = None

        # Kullanılacak User-Agent listesi (Bot engelleme için)
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        ]

    def start_driver(self):
        if not self.driver:
            service = Service(self.selenium_driver_path)
            options = self.options

            # Selenium için rastgele User-Agent seç
            random_user_agent = random.choice(self.user_agents)
            options.add_argument(f"user-agent={random_user_agent}")

            self.driver = webdriver.Chrome(service=service, options=options)

    def stop_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def scrape_links(self, links, query_keywords=None):
        scraped_data = {}

        for link in links:
            try:
                headers = {"User-Agent": random.choice(self.user_agents)}
                response = requests.get(link, headers=headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                title = soup.title.string if soup.title else "Başlık bulunamadı"

                # HTML elemanlarından içeriği çek (Başlıklar dahil)
                elements = soup.find_all(['p', 'div', 'span', 'article', 'h1', 'h2', 'h3', 'h4'])
                all_texts = [element.get_text(strip=True) for element in elements if isinstance(element.get_text(strip=True), str)]
                content = self.scrape_relevant_texts(all_texts, query_keywords)

                # Eğer içerik boşsa Selenium ile çek
                if not content:
                    content = self.scrape_with_selenium(link, query_keywords)

                # Token limitini aşmamak için içerik kırp
                final_content = self.limit_payload(content, max_tokens=5000)

                scraped_data[link] = {
                    'başlık': title,
                    'içerik': final_content
                }
            except requests.exceptions.RequestException as e:
                scraped_data[link] = {'error': f"Hata oluştu: {e}"}
            except Exception as e:
                scraped_data[link] = {'error': f"Bilinmeyen bir hata oluştu: {e}"}

        return scraped_data

    def scrape_with_selenium(self, link, query_keywords=None):
        try:
            self.start_driver()
            self.driver.get(link)

            # Web sayfasının yüklenmesini bekle
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            elements = soup.find_all(['p', 'div', 'span', 'article', 'h1', 'h2', 'h3', 'h4'])
            all_texts = [element.get_text(strip=True) for element in elements if isinstance(element.get_text(strip=True), str)]
            content = self.scrape_relevant_texts(all_texts, query_keywords)

            return content if content else "İçerik bulunamadı"
        except (TimeoutException, WebDriverException) as e:
            return f"Selenium ile veri çekilemedi: {e}"
        finally:
            self.stop_driver()


    def scrape_relevant_texts(self, texts, query_keywords=None):
        relevant_content = []

        if query_keywords is None:  # Anahtar kelime verilmezse tüm metni döndür
            return "\n".join(texts) if texts else "İçerik bulunamadı."

        for text in texts:
            if not isinstance(text, str):
                continue
            for keyword in query_keywords:
                if not isinstance(keyword, str):
                    continue
                start_idx = text.lower().find(keyword.lower())
                if start_idx != -1:
                    snippet_start = max(0, start_idx - 1000)
                    snippet_end = min(len(text), start_idx + 1000)
                    snippet = text[snippet_start:snippet_end]
                    relevant_content.append(snippet)
                    break
        return "\n".join(relevant_content) if relevant_content else "İlgili içerik bulunamadı."

    def limit_payload(self, content, max_tokens=5000):
        def estimate_tokens(text):
            return len(text) // 4  # Ortalama her 4 karakter 1 token eder

        input_tokens = estimate_tokens(content)

        if input_tokens > max_tokens:
            allowed_characters = max_tokens * 4
            content = content[:allowed_characters]

        return content