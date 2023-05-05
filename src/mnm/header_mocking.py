from .wrapper import MnmWrapper

import requests.utils
import requests.sessions

class HeaderMocking(MnmWrapper):
    def __init__(self,):
        super().__init__()
    
    def enable(self):
        if self.saved_state:
            return

        def wrap_default_headers():
            import requests.structures
            return requests.structures.CaseInsensitiveDict({
                'Sec-Ch-Ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US;q=0.8,en;q=0.7',
            })

        self.saved_state = {
            'utils.default_headers': requests.utils.default_headers,
            'sessions.default_headers': requests.sessions.default_headers
        }
        requests.utils.default_headers = wrap_default_headers
        requests.sessions.default_headers = wrap_default_headers
    
    def disable(self):        
        if self.saved_state:
            requests.utils.default_headers = self.saved_state['utils.default_headers']
            requests.sessions.default_headers = self.saved_state['sessions.default_headers']

        self.saved_state = None