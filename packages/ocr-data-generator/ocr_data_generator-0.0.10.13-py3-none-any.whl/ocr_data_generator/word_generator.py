import numpy as np

class WordGenerator:
    def __init__(self, word_list_file):
        with open(word_list_file, encoding='utf8') as f:
            chars = f.read().strip().split()
        print(len(chars))
        self.chars = chars

    def generate(self, n=1):
        if n==1:
            return np.random.choice(self.chars)
        return np.random.choice(self.chars, size=n)

class MongolianWordGenerator:
    def __init__(self):
        unicode=(0xE234,0xE262) # menk code unicode range
        chars = [chr(c) for c in range(*unicode)]
        unicode=(0xE264,0xE34f+1) # menk code unicode range
        chars += [chr(c) for c in range(*unicode)]
        print(len(chars))
        self.chars = chars
        self.min_char_len = 1
        self.max_char_len = 20

    def generate_word(self):
        cn = np.random.randint(self.min_char_len, self.max_char_len)
        word = ''.join(np.random.choice(self.chars, cn))
        return word
        
    def generate(self, n=1):
        if n==1:
            return self.generate_word()
        return [self.generate_word() for _ in range(n)]    