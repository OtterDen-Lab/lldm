class Quest:
    def __init__(self, name, status='Pending'):
        self.name = name
        self.status = status

    def __str__(self):
        return f"Quest: {self.name} - Status: {self.status}"
