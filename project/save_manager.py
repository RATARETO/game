import pickle
import os


class SaveManager:
    SAVE_FILE = "savegame.dat"

    @staticmethod
    def save(data):
        with open(SaveManager.SAVE_FILE, 'wb') as f:
            pickle.dump(data, f)

    @staticmethod
    def load():
        if os.path.exists(SaveManager.SAVE_FILE):
            with open(SaveManager.SAVE_FILE, 'rb') as f:
                return pickle.load(f)
        return None
