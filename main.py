import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from quiz import QuizFrame
from user import UserManager
from utils import load_json
import os

# Chemins d'accès aux données
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
QUESTIONS_FILE = os.path.join(DATA_DIR, "questions.json")
USERS_FILE = os.path.join(DATA_DIR, "utilisateurs.json")


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz Project")
        self.geometry("1200x400")
        self.resizable(False, False)

        # Initialisation du gestionnaire d'utilisateurs et chargement des questions
        self.user_manager = UserManager(USERS_FILE)
        self.questions = load_json(QUESTIONS_FILE)

        # Zone de contenu (Frame) pour changer d'affichage
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Création du menu
        self.create_menu()
        self.show_main_menu()

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=game_menu)
        game_menu.add_command(label="Jouer", command=self.start_quiz)
        game_menu.add_command(label="Voir les résultats",
                              command=self.show_results)
        game_menu.add_separator()
        game_menu.add_command(label="Quitter", command=self.quit)

    def show_main_menu(self):
        # Effacer l'affichage courant
        for widget in self.container.winfo_children():
            widget.destroy()
        frame = ttk.Frame(self.container)
        frame.pack(fill="both", expand=True)
        title = ttk.Label(frame, text="Bienvenue au Quiz",
                          font=("Helvetica", 20))
        title.pack(pady=20)
        btn_play = ttk.Button(frame, text="Jouer", command=self.start_quiz)
        btn_play.pack(pady=10)
        btn_results = ttk.Button(
            frame, text="Voir les résultats", command=self.show_results)
        btn_results.pack(pady=10)

    def start_quiz(self):
        # Demande du nom de l'utilisateur
        name = simpledialog.askstring("Nom d'utilisateur", "Entrez votre nom:")
        if not name:
            return
        # Effacer l'affichage courant
        for widget in self.container.winfo_children():
            widget.destroy()
        # Création de l'interface du quiz
        quiz_frame = QuizFrame(
            self.container, self.questions, name, self.user_manager)
        quiz_frame.pack(fill="both", expand=True)

    def show_results(self):
        results = self.user_manager.get_all_users()
        if not results:
            messagebox.showinfo("Résultats", "Aucun résultat disponible.")
            return

        # Création d'une nouvelle fenêtre pour afficher les résultats
        results_window = tk.Toplevel(self)
        results_window.title("Résultats")
        results_window.geometry("500x300")

        # Création du Treeview avec une colonne pour l'utilisateur, le score et le total
        tree = ttk.Treeview(results_window, columns=(
            "Utilisateur", "Score", "Total"), show="headings")
        tree.heading("Utilisateur", text="Utilisateur")
        tree.heading("Score", text="Score")
        tree.heading("Total", text="Total")
        tree.column("Utilisateur", width=200, anchor="center")
        tree.column("Score", width=100, anchor="center")
        tree.column("Total", width=100, anchor="center")
        tree.pack(fill="both", expand=True)

        for user, data in results.items():
            tree.insert("", "end", values=(user, data['score'], data['total']))

        close_btn = ttk.Button(results_window, text="Fermer",
                               command=results_window.destroy)
        close_btn.pack(pady=10)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
