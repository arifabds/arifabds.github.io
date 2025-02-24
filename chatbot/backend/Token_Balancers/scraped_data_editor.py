import threading
from queue import Queue

class ScrapedDataEditor:
    def __init__(self, model, api_handler_scraped_data_editor, api_key):
        self.model = model
        self.api_handler_scraped_data_editor = api_handler_scraped_data_editor
        self.api_key = api_key

    def EditScrapedData(self, scraped_data_formatted, query):
        def api_call(queue):
            try:
                context = (
                    "Sen, önceden verilen komut hakkında scrape edilmiş bir veri bütününden komutla alakalı uygun ve mantıklı verileri bağlamıyla beraber çıkarıp özetleyen,"
                    "gereksiz karakter, noktalama işaretleri veya tekrarlamaları kaldıran, ingilizce veriyi türkçeleştirip anlamlı bir bağlam kuran"
                    "yardımcı bir asistansın."
                    "Sana bir komut ve scrape edilmiş veri verilecek ve bu veriyi söylenen şekilde özetleyip mantıklı bir bağlam çerçevesinde sunacaksın."
                    "Önemli noktaları mutlaka al, detaylara çok dikkat et! Detayları asla göz ardı etme!"
                )
                
                full_prompt = (
                    f"Yanıt bağlamın: {context}\n"
                    f"Komut: {query}\n"
                    f"Düzenleyeceğin scrape edilmiş veri bütünü: {scraped_data_formatted}"
                )
                final_full_prompt = self.limit_payload(full_prompt, max_tokens=4000)
                response = self.api_handler_scraped_data_editor.send_message_to_model(final_full_prompt)
                queue.put(response)  
            except Exception as e:
                queue.put(f"Hata: {e}")

        queue = Queue()
        thread = threading.Thread(target=api_call, args=(queue,), daemon=True)
        thread.start()
        thread.join()

       
        content = queue.get()

        final_content = self.limit_payload(content, max_tokens=7000)

        try:
            return final_content
        except Exception as e:
            print("Son bağlam oluşturulurken hata çıktı:", e)
            return []


    def limit_payload(self, content, max_tokens=5000):
        def estimate_tokens(text):
            return len(text) // 4

        #total_characters = len(content)
        input_tokens = estimate_tokens(content)

        # print(f"Düzenlenecek metindeki toplam karakter: {total_characters}")
        # print(f"Giren token sayısı valla: {input_tokens}")

        if input_tokens > max_tokens:
            #print(f"Mis gibi payload {input_tokens} token, kesiliyor...")
            allowed_characters = max_tokens * 4 
            content = content[:allowed_characters]
            #cut_tokens = input_tokens - max_tokens
            # print(f"Bu zımbırtıdan Kesilen token miktarı: {cut_tokens}")
            # print(f"Kalan  oohhh karakter: {len(content)}")
            # print(f"Kalan şu kadar token: {estimate_tokens(content)}")

        return content