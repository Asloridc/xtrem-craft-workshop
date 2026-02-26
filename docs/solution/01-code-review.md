# Backlog

## What can be improved in the codebase ?

### Bank.py

- Mauvais nommage : _exchange_rate pour l'attribut et addEchangeRate pour la méthode
- Changer create() en @classmethod à la place de @staticmethod car c'est l'équivalent d'un constructeur
- Changer le type de __exchange_rate en Dict[tuple[currency1, currency2], floar] car un string est trop abstrait et variable.
- Retirer le paramètre exchange_rate de ```python __init__``` car c'est un attribut de classe privé.
- Rajouter de la documentation pour la compréhension du code.

### monney_calculator.py

- Supprimer le paramètre cuurency des méthodes car il n'est pas utilisé.
- Spprimer la conversion en float du return car *amount* et *amount2* sont déja des floats