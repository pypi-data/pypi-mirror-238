from todolist_lb_me_ab.Tache import Tache, TacheStatus
from typing import Union


class TacheComercial(Tache):
    """
    Classe héritée de Tache pour gérer des tâches commerciales.

    :param TacheStatus status: Le statut de la tâche (doit être une valeur de l'enum TacheStatus).
    :param str projet: Le projet auquel la tâche appartient.
    :param Union[int, str] horodatage: L'horodatage associé à la tâche.
    :param str Nom: Le nom de la tâche.
    :param str Description: Une description détaillée de la tâche.
    :param str client: Le client associé à la tâche commerciale.
    """

    def __init__(self, status: TacheStatus, projet: str, horodatage: Union[int, str], Nom: str, Description: str, client: str):
        """
        Initialise une nouvelle instance de la classe TacheComercial.

        :param TacheStatus status: Le statut de la tâche (doit être une valeur de l'enum TacheStatus).
        :param str projet: Le projet auquel la tâche appartient.
        :param Union[int, str] horodatage: L'horodatage associé à la tâche.
        :param str Nom: Le nom de la tâche.
        :param str Description: Une description détaillée de la tâche.
        :param str client: Le client associé à la tâche commerciale.
        """
        super().__init__(status, projet, horodatage, Nom, Description)
        self.client = client

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères de l'objet TacheComercial.

        :return: Une représentation string de l'objet.
        :rtype: str
        """
        return f"TacheComercial({super().__str__()}, client={self.client})"
