# models.py

class Song:
    def __init__(self, title, from_user='', dedicated_to=''):
        self.title = title
        self.from_user = from_user
        self.dedicated_to = dedicated_to

    def __str__(self):
        return f"{self.title} (From: {self.from_user}, To: {self.dedicated_to})"

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.connected = True
        self.song_list = []
        self.secondary_list = []

    def disconnect(self):
        self.connected = False
        self.secondary_list = self.song_list.copy()
        self.song_list.clear()

    def reconnect(self):
        self.connected = True
        self.song_list = self.secondary_list.copy()
        self.secondary_list.clear()
