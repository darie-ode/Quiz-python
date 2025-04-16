import json


def load_json(filepath):
    """
    Charge le contenu d'un fichier JSON et le retourne.
    En cas d'erreur, affiche le message et retourne une liste vide.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement du fichier {filepath}: {e}")
        return []
