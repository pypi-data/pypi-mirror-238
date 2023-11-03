from typing import List

class CustomModel:
    def __init__(self, id: str, name: str, entities: List[str]):
        self.id = id
        self.name = name
        self.entities = entities

    def describe(self):
        print("Model Name: " + self.name)
        print("Model Id: " + self.id)
        print("Entities: " + ', '.join(self.entities))
