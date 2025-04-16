import requests
import html
import random

API_URL = "https://opentdb.com/api.php"


def fetch_questions(preferences):
    """
    Préférences : dictionnaire avec les clés :
      - amount : nombre de questions
      - category : ID de catégorie (optionnel)
      - difficulty : 'easy', 'medium', 'hard' (optionnel)
      - type : 'multiple' ou 'boolean' (optionnel)
    """
    params = {"amount": preferences.get("amount", 10)}
    if preferences.get("category"):
        params["category"] = preferences["category"]
    if preferences.get("difficulty"):
        params["difficulty"] = preferences["difficulty"]
    if preferences.get("type"):
        params["type"] = preferences["type"]

    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        if data.get("response_code") == 0:
            questions = []
            for item in data.get("results", []):
                question_text = html.unescape(item.get("question", ""))
                correct_answer = html.unescape(item.get("correct_answer", ""))
                incorrect_answers = [html.unescape(
                    ans) for ans in item.get("incorrect_answers", [])]
                choices = []
                if item.get("type") == "multiple":
                    choices = incorrect_answers + [correct_answer]
                    random.shuffle(choices)
                questions.append({
                    "question": question_text,
                    "reponse": correct_answer,
                    "choix": choices,
                    "type": item.get("type")
                })
            return questions
        else:
            print("L'API n'a retourné aucun résultat.")
            return []
    except Exception as e:
        print("Erreur lors de l'appel API:", e)
        return []
