import json
import os
import csv


class UserManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def update_user(self, username, score, total, details):
        self.users[username] = {
            "score": score,
            "total": total,
            "details": details
        }
        self.save_users()
        self.update_scoreboard(username, score, total)

    def save_users(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.users, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("Erreur lors de la sauvegarde des utilisateurs:", e)

    def update_scoreboard(self, username, score, total):
        # Mise à jour du fichier CSV (scoreboard)
        scoreboard_file = os.path.join(os.path.dirname(
            self.filepath), "..", "bonus", "scoreboard.csv")
        file_exists = os.path.exists(scoreboard_file)
        try:
            with open(scoreboard_file, "a", newline='', encoding="utf-8") as csvfile:
                fieldnames = ["utilisateur", "score", "total"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(
                    {"utilisateur": username, "score": score, "total": total})
        except Exception as e:
            print("Erreur lors de la mise à jour du scoreboard:", e)

    def get_all_users(self):
        return self.users
