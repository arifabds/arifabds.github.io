import numpy as np
import requests
from numpy.linalg import norm
from queue import Queue
import threading

class RelevantContext:
    def __init__(self, model, api_handler_search, custom_search_api_key, cx):
        self.model = model
        self.api_handler_search = api_handler_search
        self.custom_search_api_key = custom_search_api_key
        self.cx = cx

    def find_relevant_results(self, query, chat_history, keywords,top_k=3):
        def api_call(queue):
            try:
                context = ("Sana verilen komutu bir arama sorgusuna dönüştüren ve kullanıcının sohbet mi ettiğini yoksa bir şeyler mi aramak istediğini söyleyen bir asistansın.\n"+
                           "Vereceğin yanıt Türkçe ve formatı {arama sorgusu},{sohbet belirteci} şeklinde olmalıdır:" +
                           "Örneğin:\n" +
                           "Sorgu: Türkiye Süper ligi puan durumuyla alakalı bir haber makalesi yaz\n" +
                           "Olması gereken yanıt: Türkiye Süper Ligi puan durumu,arama sorgusu\n" +
                           "Bir diğer örnek:\n" +
                           "En son maçını kimle yaptı(bu örnekte kullanıcı sohbet geçmişinden bir olay ile alakalı soru sormakta)\n" +
                           "Olması gereken yanıt: sohbet sorgusu\n" +
                           "Yanıtında chat geçmişini baz almak zorundasın Örneğin bir önceki konuşmadaki özneyi belirterek sorulan bir şey arama sorgusu konusu olabilir. \n"+
                           "Kullanıcı sana cümleler kurabilir, bu cümlelerden kullanıcının aslında aramak istediği kavramı bul ve komutla alakalı, mantıklı bir arama sorgusuna dönüştür\n"+
                           "Yanıtın tek bir cümle şeklinde olsun. Doğru ve olması gereken yanıt: Türkiye Süper Ligi puan durumu,arama sorgusu\n" +
                           "Sakın başka bir ek ekleyerek yanıt verme. Yanlış ve olmaması gereken yanıt: Anladım sana yanıt veriyorum arama sorgusu şu şekildedir, Türkiye Süper Ligi puan durumu,arama sorgusu")

                full_prompt = (f"Chat geçmişi: {chat_history}\n Yanıt bağlamın: {context} \n Şu anda sana yöneltilen komut: {query}")
                response = self.api_handler_search.send_message_to_model(full_prompt)
                queue.put(response)  
            except Exception as e:
                queue.put(f"Hata: {e}")

        queue = Queue()

        thread = threading.Thread(target=api_call, args=(queue,), daemon=True)
        thread.start()
        thread.join()

        print("Orjinal komut: ",query)  

        query_to_search = queue.get()
        print("Extractlenmemiş hali: ",query_to_search)
        
        if not query_to_search or query_to_search.startswith("Hata"):
            return f"Arama sorgusu oluşturulamadı: {query_to_search}"
        
        query_to_search_extracted = (
            query_to_search.replace("arama sorgusu", "") 
            if "arama sorgusu" in query_to_search 
            else query_to_search.replace("sohbet sorgusu", "") 
            if "sohbet sorgusu" in query_to_search 
            else query_to_search
        )
        print("Extracted hali: ",query_to_search_extracted)

        or_terms = " OR ".join(keywords) if isinstance(keywords, list) else query.replace(" ", " OR ")
        #print(f"\nor terms bu şekilde: {or_terms}\n")

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': self.custom_search_api_key,
            'cx': self.cx,
            'q': query_to_search_extracted,
            'num': 10,
            #'orTerms': or_terms 
        }

        #if "sohbet sorgusu" in query_to_search:
            #return "Sohbet geçmişine göre yanıt vermen gerekmekte"
        if "arama sorgusu" or "sohbet sorgusu" in query_to_search:
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                query_embedding = self.model.encode(query_to_search)

                similarities = []
                for item in data.get('items', []):
                    title = item.get('title', '')
                    snippet = item.get('snippet', '')
                    link = item.get('link', '')

                    combined_text = f"{title}. {snippet}"
                    result_embedding = self.model.encode(combined_text)

                    similarity = np.dot(query_embedding, result_embedding) / (
                        norm(query_embedding) * norm(result_embedding)
                    )
                    similarities.append((similarity, title, snippet, link))

                relevant_results = sorted(similarities, key=lambda x: x[0], reverse=True)[:top_k]

                result_context = "İlgili arama sonuçları:\n"
                for similarity, title, snippet, link in relevant_results:
                    result_context += (
                        f"- {title}\n"
                        f"  Açıklama: {snippet}\n"
                        f"  Benzerlik: {similarity:.2f}\n"
                        f"  Link: {link}\n\n"
                    )

                return result_context

            except requests.exceptions.RequestException as e:
                return f"API isteği sırasında bir hata oluştu: {str(e)}"
        else:
            return ""
