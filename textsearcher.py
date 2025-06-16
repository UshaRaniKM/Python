import string
import os
import re
import time
from collections import defaultdict

class TextSearcher(object):

    WORD_PATTERN = re.compile(r"[a-zA-Z0-9'-]+")

    def __init__(self):
        self.file_data = []
        self.processed_word_index = defaultdict(list)
    
    def load(self, file_path: str) -> bool:
        self.file_data = []
        if not file_path:
            return False
        
        def decode_bytes(line):
            for encoding in ("utf-8", "latin-1"): # add other encodings
                try:
                    return line.decode(encoding)
                except UnicodeDecodeError:
                    continue
            return None

        idx = 0
        try:
            # Open the file in binary mode to handle any encoding
            with open(file_path, "rb") as f:
                for line in f:
                    line_text = decode_bytes(line)
                    if line_text is None:
                        continue        
                
                    words = line_text.split()              
                    for word in words:
                        # Search for the substring in 'word' that matches the WORD_PATTERN regex
                        match = self.WORD_PATTERN.search(word)
                        processed_word = ''
                        if match:
                            processed_word = match.group(0).lower()
                            self.processed_word_index[processed_word].append((idx, word.strip()))
                        self.file_data.append(word.strip())
                        idx += 1
                return True
        except Exception as e:
            return False
    
  
    def search(self, word:str, context:int=0)->list:
        size = len(self.file_data)

        match = self.WORD_PATTERN.search(word)
        matches = None
        if match:
            normalized = match.group(0).lower()
            matches = self.processed_word_index.get(normalized, [])
            if word !=  match.group(0):
                matches = [(i, w) for i, w in matches if w == word.strip()]

        output = []
        for i, _ in matches:
            start = max(0, i - context)
            end = min(size, i + context + 1)            
            snippet = ' '.join(original for original in self.file_data[start:end])
            output.append(snippet)
        return output


    

