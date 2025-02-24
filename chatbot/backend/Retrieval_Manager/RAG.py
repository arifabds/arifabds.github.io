from ..Connection.API_handler import APIHandler
from ..Retrieval_Manager.relevant_context import RelevantContext
from ..Token_Balancers.keyword_generator import KeywordGenerator

class RAG:
    def __init__(self,  custom_search_api_key, cx, search_query_api_key, llm_model, sentence_transformer_model, api_handler_key_gen, api_key_gen):
        self.model = sentence_transformer_model
        self.api_handler_search = APIHandler(search_query_api_key, llm_model)
        self.custom_search_api_key = custom_search_api_key
        self.cx = cx
        self.keyword_generator = KeywordGenerator(llm_model, api_handler_key_gen, api_key_gen)
        self.keywords = ""
        self.relevant_context = RelevantContext(self.model, self.api_handler_search, self.custom_search_api_key, self.cx)

    def process_query(self, prompt, chat_history):
        # Web arama sonuçlarını bul
        self.keywords = self.keyword_generator.generate_keywords(prompt)
        return self.relevant_context.find_relevant_results(prompt, chat_history, self.keywords)
            
    def get_query_embedding(self, query):
        """Sorgunun gömüsünü döndürür."""
        return self.model.encode(query)
    
    
