import string
import os
import re
import time

class TextSearcher(object):

    WORD_PATTERN = re.compile(r"[a-zA-Z0-9'-]+")

    def __init__(self):
        self.file_data = None
    
    def load(self, file_path: str) -> bool:
        self.file_data = []
        if not file_path:
            return False
        try:
            # Open the file in binary mode to handle any encoding
            with open(file_path, "rb") as f:
                file_data = f.read()
        
            try:
                # Try to decode using common UTF-8 encoding
                text = file_data.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    # Try decoding as Latin-1 (fallback)
                    text = file_data.decode("latin-1")
                except UnicodeDecodeError:
                    return False
                
            words = text.split()
                
            for word in words:
                # Search for the substring in 'word' that matches the WORD_PATTERN regex
                match = self.WORD_PATTERN.search(word)
                if match:
                    processed_word = match.group(0).lower()
                    self.file_data.append((processed_word, word.strip()))
            return True
        except Exception as e:
            return False
    

    # Add doc string    
    def search(self, word:str, context:int=0)->list:
        output = []
        size = len(self.file_data)

        target = word.lower()
        for i, (changed_word, orig_word) in enumerate(self.file_data):
            if changed_word == target or target == orig_word:
                start = 0 if i- context < 0 else i - context
                end = i + context + 1
                if (context >= size or end >= size):
                    end = size

                data = []
                for _, orig_text in self.file_data[start:end]:
                    data.append(orig_text)
                output.append(' '.join(data))
        return output
            
       

if __name__ == "__main__" :

    searcher = TextSearcher()
    
    start_time = time.time()
    searcher.load("Siddhartha.txt")
    results = searcher.search("2500-8.txt", 1)
    start_time1 = time.time()

    print(f"\nLoad time: {start_time1 - start_time} seconds")
    print(results, end='')


