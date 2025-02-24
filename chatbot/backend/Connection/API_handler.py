from ..Connection.connector import Connector

class APIHandler:
    def __init__(self, token, model):
        self.token = token
        self.model = model

    def send_message_to_model(self, full_prompt):
        try:
            response = Connector.Request.send_prompt(self.token, self.model, full_prompt)
            return response
        except Exception as e:
            raise Exception(f"API çağrısında bir hata oluştu: {e}")