import tkinter as tk
from tkinter import ttk, messagebox


class QuizFrame(ttk.Frame):
    def __init__(self, parent, questions, username, user_manager):
        super().__init__(parent)
        self.questions = questions
        self.username = username
        self.user_manager = user_manager
        self.current_question_index = 0
        self.score = 0

        self.time_left = 30  # temps par question en secondes
        self.timer_label = ttk.Label(
            self, text=f"Temps restant : {self.time_left}s", font=("Helvetica", 12)
        )
        self.timer_label.pack(pady=10)
        self.timer_id = None

        self.build_ui()

    def build_ui(self):
        question_data = self.questions[self.current_question_index]
        self.question_label = ttk.Label(
            self, text=question_data["question"], font=("Helvetica", 16)
        )
        self.question_label.pack(pady=20)

        self.choix_var = tk.StringVar()

        for choix in question_data["choix"]:
            rb = ttk.Radiobutton(
                self, text=choix, variable=self.choix_var, value=choix)
            rb.pack(anchor="w", padx=20)

        self.submit_button = ttk.Button(
            self, text="Valider", command=self.validate_answer
        )
        self.submit_button.pack(pady=10)

        self.time_left = 30
        self.start_timer()

    def start_timer(self):
        self.timer_label.config(text=f"Temps restant : {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.after(1000, self.start_timer)
        else:
            messagebox.showinfo(
                "Temps écoulé", "Le temps est écoulé pour cette question.")
            self.validate_answer()

    def validate_answer(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        selected = self.choix_var.get()
        correct_answer = self.questions[self.current_question_index]["reponse"]

        if selected.lower() == correct_answer.lower():
            self.score += 1

        self.current_question_index += 1

        if self.current_question_index >= len(self.questions):
            total = len(self.questions)
            # Détermination du message selon le score
            if self.score == total:
                message = "Félicitations !"
            elif self.score >= total * 0.5:
                message = "Bien joué !"
            else:
                message = "Peu mieux faire !"

            # Debug : Affichage dans la console du score final et du message
            print(f"Quiz terminé. Score: {self.score}/{total} - {message}")

            messagebox.showinfo(
                "Quiz terminé", f"Score: {self.score}/{total}\n{message}")

            # Retour au menu principal
            self.destroy()
            self.winfo_toplevel().show_main_menu()
        else:
            self.update_question()

    def update_question(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        question_data = self.questions[self.current_question_index]
        self.question_label.config(text=question_data["question"])
        self.choix_var.set("")

        # Supprimer les anciens boutons radio
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Radiobutton):
                widget.destroy()

        for choix in question_data["choix"]:
            rb = ttk.Radiobutton(
                self, text=choix, variable=self.choix_var, value=choix)
            rb.pack(anchor="w", padx=20)

        self.time_left = 30
        self.start_timer()
