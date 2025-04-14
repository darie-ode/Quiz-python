import tkinter as tk
from tkinter import ttk, messagebox


class QuizFrame(ttk.Frame):
    def __init__(self, parent, questions, username, user_manager, callback=None):
        super().__init__(parent)
        self.questions = questions.copy()
        self.username = username
        self.user_manager = user_manager
        self.callback = callback
        self.current_index = 0
        self.score = 0
        self.user_answers = []  # Détail des réponses

        self.build_ui()
        self.show_question()

    def build_ui(self):
        # Création des éléments de l'interface
        self.question_label = ttk.Label(
            self, text="", wraplength=550, font=("Helvetica", 14))
        self.question_label.pack(pady=20)

        self.options_var = tk.StringVar()
        self.options_frame = ttk.Frame(self)
        self.options_frame.pack(pady=10)

        self.option_buttons = []

        self.submit_btn = ttk.Button(
            self, text="Valider", command=self.submit_answer)
        self.submit_btn.pack(pady=10)

    def show_question(self):
        # Si toutes les questions ont été traitées, finir le quiz
        if self.current_index >= len(self.questions):
            self.finish_quiz()
            return

        # Réinitialiser les options précédentes
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        self.option_buttons = []
        self.options_var.set("")

        # Récupérer la question courante
        question_data = self.questions[self.current_index]
        question_text = question_data.get(
            "question", "Question non disponible")
        self.correct_answer = question_data.get("reponse", "")
        choices = question_data.get("choix", [])

        self.question_label.config(
            text=f"Q{self.current_index + 1}: {question_text}")

        if choices:
            # Créer des boutons radio pour les choix multiples
            for choice in choices:
                rb = ttk.Radiobutton(
                    self.options_frame, text=choice, value=choice, variable=self.options_var)
                rb.pack(anchor="w")
                self.option_buttons.append(rb)
        else:
            # S'il n'y a pas de choix, proposer une saisie manuelle
            self.answer_entry = ttk.Entry(
                self.options_frame, textvariable=self.options_var, width=50)
            self.answer_entry.pack()
            self.option_buttons.append(self.answer_entry)

    def submit_answer(self):
        answer = self.options_var.get()
        if not answer:
            messagebox.showwarning(
                "Alerte", "Veuillez sélectionner une réponse!")
            return

        # Vérifier la réponse (comparaison insensible à la casse)
        correct = answer.lower() == self.correct_answer.lower()
        if correct:
            messagebox.showinfo("Correct", "Bonne réponse !")
            self.score += 1
        else:
            messagebox.showinfo(
                "Incorrect", f"Mauvaise réponse. La bonne réponse était : {self.correct_answer}")

        self.user_answers.append({
            "question": self.questions[self.current_index].get("question", ""),
            "reponse_utilisateur": answer,
            "reponse_correcte": self.correct_answer,
            "correct": correct
        })

        self.current_index += 1
        self.show_question()

    def finish_quiz(self):
        messagebox.showinfo(
            "Résultat", f"{self.username}, votre score est {self.score} sur {len(self.questions)}")
        self.user_manager.update_user(
            self.username, self.score, len(self.questions), self.user_answers)
        if self.callback:
            self.callback()
