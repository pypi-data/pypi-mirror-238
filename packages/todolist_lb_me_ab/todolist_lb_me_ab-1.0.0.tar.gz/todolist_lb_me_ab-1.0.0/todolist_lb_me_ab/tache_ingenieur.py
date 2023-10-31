# Assurez-vous que TacheStatus est bien défini dans le module 'tache'
from todolist_lb_me_ab.Tache import Tache, TacheStatus
from typing import Union, List


class TacheIngenieur(Tache):
    """
    Classe héritée de Tache pour gérer des tâches d'ingénierie.

    :param TacheStatus status: Le statut de la tâche (doit être une valeur de l'enum TacheStatus).
    :param str projet: Le projet auquel la tâche appartient.
    :param Union[int, str] horodatage: L'horodatage associé à la tâche.
    :param str Nom: Le nom de la tâche.
    :param str Description: Une description détaillée de la tâche.
    :param List[str] technologies: Une liste des technologies associées à la tâche.
    """

    def __init__(self, status: TacheStatus, projet: str, horodatage: Union[int, str], Nom: str, Description: str, technologies: List[str]):
        """
        Initialise une nouvelle instance de la classe TacheIngenieur.

        :param TacheStatus status: Le statut de la tâche (doit être une valeur de l'enum TacheStatus).
        :param str projet: Le projet auquel la tâche appartient.
        :param Union[int, str] horodatage: L'horodatage associé à la tâche.
        :param str Nom: Le nom de la tâche.
        :param str Description: Une description détaillée de la tâche.
        :param List[str] technologies: Une liste des technologies associées à la tâche.
        """
        super().__init__(status, projet, horodatage, Nom, Description)
        self.technologies = technologies

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères de l'objet TacheIngenieur.

        :return: Une représentation string de l'objet.
        :rtype: str
        """
        return f"TacheIngenieur({super().__str__()}, technologies={self.technologies})"
