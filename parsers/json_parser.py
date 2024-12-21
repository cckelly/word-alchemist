import json

class JsonParser:
    def read_word_json(self, filename: str):
        with open(filename, 'r') as file:
            words = json.load(file)
        
        if not isinstance(words, list):
            raise ValueError(f"File {filename} needs to be a JSON array")
        
        for word in words:
            if not isinstance(word, str):
                raise ValueError(f"File {filename} contains a non-string element: {word}")

        return words