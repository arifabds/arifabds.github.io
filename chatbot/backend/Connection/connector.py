import requests
#import json
#from json_response import ApiResponse, Message

class Connector:
    class Request:
        @staticmethod
        def send_prompt(api_key: str, model: str, prompt: str) -> str:
            token_usage = 0
            #print("Tokeni aldı sorun yok \n")
            url = "https://api.groq.com/openai/v1/chat/completions"  # GroqCloud API URL
            #print("URL'yi aldı sorun yok \n")
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            #print("headers aldı sorun yok: \n", headers)
            MAX_LENGTH = 15000  
            shortened_prompt = prompt[:MAX_LENGTH]
            data = {
                "model": model,  
                "messages": [{"role": "user", "content": shortened_prompt}],
                "temperature": 0.7  
            }
            print("data aldı sorun yok: \n", data)

            try:
                response = requests.post(url, headers=headers, json=data)
                #print("response aldı sorun yok: \n", response)
                print("🔥 API Response İçeriği:", response.text)
                response.raise_for_status()  

                response_dict = response.json()
                
                if "usage" in response_dict:
                    token_usage += response_dict["usage"].get("total_tokens", 0)

                if 'choices' in response_dict and len(response_dict['choices']) > 0:
                    Connector.Request.analyze_response_usage(response_dict)
                    return response_dict['choices'][0]['message']['content']
                
                return "Yanıt alınamadı"
            except requests.exceptions.RequestException as e:
                return f"API isteği çok unique bir şekilde başarısız oldu işte bu da onun kodu: 72b6858683254cc5c7658cbc13bb6f3ebe1e7ed74be6c27f592ce2ff621f7c3a  {e}"
            
        @staticmethod    
        def analyze_response_usage(response_dict):
            """
            API yanıtından kullanılan toplam token miktarını kontrol et.
            """
            if "usage" in response_dict:
                input_tokens = response_dict["usage"].get("prompt_tokens", 0)
                output_tokens = response_dict["usage"].get("completion_tokens", 0)
                total_tokens = response_dict["usage"].get("total_tokens", 0)

                print(f"Girdi tokenleri: {input_tokens}")
                print(f"Çıktı tokenleri: {output_tokens}")
                print(f"Toplam token: {total_tokens}")

                if total_tokens > 7000:
                    print("UYARI: Toplam token sayısı 7000 limitini aşıyor!")
            else:
                print("API yanıtında token kullanımı bilgisi bulunamadı.")
            
