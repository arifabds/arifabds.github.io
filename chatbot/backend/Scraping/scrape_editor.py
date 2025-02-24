class ScrapeEditor:
    def __init__(self):
        pass

    def format_scraped_data(self, scraped_data):

        formatted_output = []

        for link, data in scraped_data.items():
            if 'error' in data:
                formatted_output.append({
                    'link': link,
                    'error': data['error']
                })
            else:
                title = data.get('başlık', 'Başlık bulunamadı')
                content = data.get('içerik', 'İçerik bulunamadı')
                formatted_output.append({
                    'link': link,
                    'başlık': title,
                    'içerik': content
                })

        return formatted_output