class User():
    def __init__(self, name, uid):
        self.name = name
        self.uid = uid
    def __str__(self):
        return f"It works {self.uid}"