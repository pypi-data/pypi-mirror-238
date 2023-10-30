import random
import string
from typing import Union

class AdminOneTimeTokenManager:
    def __init__(self, token_size = 32) -> None:
        self.tokens = {}
        self.token_size = token_size

    def _generate(self, size):
        return ''.join(random.choices(string.ascii_letters, k=size))
    
    def create(self, email: str):
        token = self._generate(self.token_size)
        self.tokens[token] = email 
        return token

    def release(self, token: str) -> Union[str, None]:
        try:
            return self.tokens.pop(token)
        except KeyError:
            pass

