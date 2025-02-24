import threading
from queue import Queue

class KeywordGenerator:
    def __init__(self, model, api_handler_key_gen, api_key):
        self.model = model
        self.api_handler_key_gen = api_handler_key_gen
        self.api_key = api_key

    def generate_keywords(self, query):
        def api_call(queue):
            try:
                context = (
                    "Sana verilen sorgudan 15-20 adet anahtar kelime oluşturması gereken bir asistansın. "
                    "Her bir anahtar kelime, verilen sorgunun anlamına en uygun şekilde olmalıdır. "
                    "Anahtar kelimeleri hem türkçe hem de ingilizce ver. Örneğin: stats, istatistikler. bu şekilde ver ve sakın tr: istatistikler, en: stats şeklinde verme!"
                    "Yanıtın formatı bir JSON listesi olarak olmalıdır. Örneğin:\n\n"
                    "Sorgu: Türkiye Süper ligi puan durumuyla alakalı bir haber makalesi yaz\n"
                    "Olması gereken yanıt: [\"Türkiye Süper Ligi\", \"puan durumu\", \"haber\", \"futbol\"]\n\n"
                    "Başka bir örnek:\n"
                    "Sorgu: Fenerbahçe maçının nasıl geçtiğini, oyuncularını ve sonucunu veren bir haber yaz\n"
                    "Olması gereken yanıt: [\"Fenerbahçe\", \"maç sonucu\", \"match results\", \"kadrolar\", \"squads\", \"oyuncular\", \"players\", \"futbol\", \"football\"]\n\n"
                    "Yanıtın sadece JSON formatında, yalnızca anahtar kelimeleri döndürmelidir. Hem türkçe hem ingilizce olmak zorunda."
                    "Yanıtın formatı şu şekilde olmak zorunda: [\"keyword1\", \"keyword2\",\"keyword3\", \"keyword4\", \"keyword5\", \"keyword6\"]"
                )
                
                full_prompt = (
                    f"Yanıt bağlamın: {context}\n"
                    f"Şu anda sana yöneltilen komut: {query}"
                )
                response = self.api_handler_key_gen.send_message_to_model(full_prompt)
                queue.put(response)  
            except Exception as e:
                queue.put(f"Hata: {e}")

        # Queue ile API çağrısını başlat
        queue = Queue()
        thread = threading.Thread(target=api_call, args=(queue,), daemon=True)
        thread.start()
        thread.join()

        # Orijinal sorgu ve dönüşen anahtar kelimeler
        query_to_keywords = queue.get()
        #print("Orijinal Sorgu: ", query)
        #print("Dönüştürülmüş Anahtar Kelimeler: ", query_to_keywords)

        try:
            # Anahtar kelimeleri JSON olarak döndür
            return eval(query_to_keywords) if query_to_keywords.startswith("[") else []
        except Exception as e:
            print("Anahtar kelimeler işlenirken bir hata oluştu:", e)
            return []

