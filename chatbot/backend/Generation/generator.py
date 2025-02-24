import os
from queue import Queue
import threading
from ..Retrieval_Manager.RAG import RAG
from ..Connection.API_handler import APIHandler
from ..Scraping.scrape_manager import ScrapeManager
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("⚠️ 'sentence-transformers' yüklü değil. Model yüklenemedi.")
from ..Configuration.config import Config
from ..Token_Balancers.chat_history_summarizer import ChatHistorySummarizer


class Generator:
    def __init__(self):
        chat_summary_api_key = Config.CHAT_SUMMARY_API_KEY
        scrape_process_api_key = Config.SCRAPE_PROCESS_API_KEY
        context_merge_api_key = Config.CONTEXT_MERGE_API_KEY
        keyword_gen_api_key = Config.KEYWORD_GEN_API_KEY
        search_query_api_key = Config.SEARCH_QUERY_API_KEY
        custom_search_api_key = Config.CUSTOM_SEARCH_API_KEY
        custom_search_engine_id = Config.CUSTOM_SEARCH_ENGINE_ID

        llm_model = "llama-3.2-90b-vision-preview"

        sentence_transformer_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

        selenium_driver_path = os.path.join(os.path.dirname(__file__), "chromedriver-win64", "chromedriver.exe")

        self.context_introduction = (
            "Aşağıda bir sohbet oturumu yer alıyor. Bu oturum, kullanıcı komutu, özetlenmiş sohbet geçmişi ve kullanıcı komutuna uygun oluşturulan bağlamı içermektedir."
            "Bu oturumda, oluşturulacak bağlamlara ve sohbet geçmişine(istendiği vakit) yönelik yanıt verebilen bir asistan rolündesin."
            "Sohbet geçmişi, oturumda yapılan sohbetten haberdar olman için verilmiştir ve bir sonraki oluşturalacak bağlamı etkilememektedir."
            "Bağlam kullanıcının komutu sonucunda web araması ile oluşturulacaktır. Bu bağlama yönelik cevap verip vermemen kullanıcı komutunun uygunluğuna göredir. Eğer kullanıcı komutu uygunsa bu bağlama yönelik cevap ver!"
            "Yanıtlarını her zaman uygun ve tutarlı ver. Komutla alakalı olmayan içerikleri verme, içeriğin tutarlı olmasına ekstra önem ver!"
            "Kullanıcının sohbet etmesine gerektiğinde izin ver, eğer sohbet etmek amacıyla bir komut girdiyse web araması bağlamını gözardı edebilirsin!" 
            "Türkçe yanıt ver, gereksiz tekrarlar yapma! Türkçe karakter kullanımına özen göster!"
         )

        self.chat_history = []
        self.max_history_size = 5

        self.api_handler_merge = APIHandler(context_merge_api_key, llm_model)
        self.api_handler_key_gen = APIHandler(keyword_gen_api_key, llm_model)
        self.api_handler_scraped_data_editor = APIHandler(scrape_process_api_key, llm_model)
        self.api_handler_chat_history_summarizer = APIHandler(chat_summary_api_key, llm_model)
        self.rag = RAG(custom_search_api_key, custom_search_engine_id, search_query_api_key, llm_model, sentence_transformer_model, self.api_handler_key_gen, keyword_gen_api_key)
        self.scrape_manager = ScrapeManager(llm_model, selenium_driver_path, self.api_handler_key_gen, keyword_gen_api_key, self.api_handler_scraped_data_editor ,scrape_process_api_key)
        self.chat_history_summarizer = ChatHistorySummarizer(llm_model, self.api_handler_chat_history_summarizer, chat_summary_api_key)

        self.keywords = ""
        self.prompt = ""

    def send_message(self, prompt_from_frontend):
        
        self.prompt = prompt_from_frontend
        
        results_with_links = self.rag.process_query(self.prompt, self.chat_history)

        results_with_links = f"{results_with_links}".strip()

        print("Linkerle beraber sonuçlar",results_with_links)

        self.keywords = self.rag.keywords

        #print(f"\nKeyword yapısı bu şekilde:{self.keywords}\n")

        result_context = self.scrape_manager.results(results_with_links, self.prompt, self.keywords)

        #print("Result context(llm'e sunulacak context): ",result_context)

        if len(self.chat_history) >= self.max_history_size * 2:
            self.chat_history = self.chat_history[2:]

        
        #print("\nFull chat geçmişi:", self.chat_history)
        if self.chat_history != []:
            summarized_chat_history = self.chat_history_summarizer.SummarizeChatHistory(self.chat_history)
            #print("summarize edildi")
        else:
            summarized_chat_history = f"User: {self.prompt}"

        #print("\nÖzetlenmiş chat geçmişi:", summarized_chat_history)

        full_prompt = (
            f"{self.context_introduction}\n"
            f"Kullanıcı komutu: {self.prompt}\n"
            f"Özetlenmiş sohbet geçmişi: {summarized_chat_history}\n" +
            f"Web araması sonucu oluşturulan bağlam:{result_context}\n"
        )

        print("\nGönderilecek full prompt:",full_prompt,"\n")

        def api_call(queue):
            try:
                response = self.api_handler_merge.send_message_to_model(full_prompt)
                #token_usage = self.api_handler_merge.get_token_usage()
                #print("Token kullanımı: " + token_usage)
                self.chat_history.append(f"User: {self.prompt}")         
                self.chat_history.append(f"Assistant: {response}")
                queue.put(response)
            except Exception as e:
                queue.put(f"Hata: {e}") #Hata kodları burada düzenlencek

        queue = Queue()
        thread = threading.Thread(target=api_call, args=(queue,), daemon=True)
        thread.start()
        thread.join()

        final_response = queue.get()

        try:
            return final_response
        except Exception as e:
            print("Son cevap oluşturulurken hata çıktı:", e)
            return []

        
