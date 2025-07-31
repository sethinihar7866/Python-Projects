# manager.py

import time
import threading
from models import Song, User

class SongQueueManager:
    def __init__(self, song_library):
        self.song_library = song_library
        self.main_queue = []
        self.users = {}
        self.lock = threading.Lock()

    def find_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = User(user_id)
        return self.users[user_id]

    def add_song(self, user_id, song_name, from_user='', dedicated_to=''):
        user = self.find_user(user_id)
        if len(user.song_list) >= 3:
            return "You can only add up to 3 songs."
        if song_name not in self.song_library:
            return "Song not found in library."

        with self.lock:
            song = Song(song_name, from_user, dedicated_to)
            user.song_list.append(song)
            self.main_queue.append((user_id, song))
            self.check_duplicates(song_name)
            return f"Added '{song_name}' to queue."

    def remove_or_replace_song(self, user_id, old_song, new_song):
        user = self.find_user(user_id)
        for i, song in enumerate(user.song_list):
            if song.title == old_song:
                if new_song not in self.song_library:
                    return "Replacement song not in library."
                user.song_list[i] = Song(new_song, song.from_user, song.dedicated_to)
                for j, (uid, s) in enumerate(self.main_queue):
                    if uid == user_id and s.title == old_song:
                        self.main_queue[j] = (user_id, user.song_list[i])
                        return "Song corrected."
        return "Song to replace not found."

    def check_duplicates(self, song_name):
        count = sum(1 for uid, song in self.main_queue if song.title == song_name)
        if count > 1:
            print(f"[INFO] '{song_name}' has {count} duplicates in queue.")

    def get_queue(self):
        return [
            {"position": i+1, "title": song.title, "from": song.from_user, "to": song.dedicated_to, "user": uid}
            for i, (uid, song) in enumerate(self.main_queue)
        ]

    def play_song(self):
        if self.main_queue:
            user_id, song = self.main_queue.pop(0)
            self.users[user_id].song_list.remove(song)
            return f"Now Playing: {song.title} | From: {song.from_user} | To: {song.dedicated_to}"
        return "No songs in the queue."

    def handle_disconnect(self, user_id):
        user = self.find_user(user_id)
        user.disconnect()
        self.main_queue = [(uid, s) for uid, s in self.main_queue if uid != user_id]
        threading.Thread(target=self._remove_after_timeout, args=(user_id,)).start()

    def _remove_after_timeout(self, user_id):
        time.sleep(1800)
        user = self.find_user(user_id)
        if not user.connected:
            user.secondary_list.clear()

    def handle_reconnect(self, user_id):
        user = self.find_user(user_id)
        user.reconnect()
        with self.lock:
            for song in user.song_list:
                self.main_queue.append((user_id, song))
