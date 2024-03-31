import json


class Data:
    def __init__(self, attribute, filepath):
        self.attribite = attribute
        self.filepath = filepath
        pass

    def to_file(self, message):
        with open(self.filepath, self.attribite) as file:
            file.writelines(message)

    def read_file(self):
        with open(self.filepath, self.attribite) as file:
            card_texts = file.readlines()
        return card_texts

    def read_json(self):
        with open(self.filepath, self.attribite) as file:
            card_texts = json.load(file)
        return card_texts
