from typing import List
import json

class JsonParser:
    """
        Validates and parses a JSON file into an array of strings (words).
    """
    def read_word_json(self, filename: str) -> List[str]:
        with open(filename, 'r') as file:
            words = json.load(file)
        
        # make sure we're dealing with a JSON array
        if not isinstance(words, list):
            raise ValueError(f"File {filename} needs to be a JSON array")
        
        # make sure we're dealing with only strings in the array
        for word in words:
            if not isinstance(word, str):
                raise ValueError(f"File {filename} contains a non-string element: {word}")

        return words