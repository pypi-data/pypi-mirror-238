from typing import Optional

import xarray as xr

from mfire.composite import BaseComposite
from mfire.settings import get_logger

# Logging
LOGGER = get_logger(name="base_reducer.mod", bind="base_reducer")


class BaseReducer:
    """Classe de base pour implémenter un reducer.
    Il adopte le design pattern du constructeur:
    - il existe un produit "summary" à construire (ici un dictionnaire)
    - une méthode "reset" qui permet de recommencer le processus de construction
    - un ensemble de méthode qui permettent d'ajouter des caractéristiques au "summary"
    - une méthode "compute" qui exécute l'ensemble des étapes et renvoie le "summary"

    '/!\' Dans les classes héritant de BaseReducer,
    il est impératif de détailler au niveau de cette docstring principale
    le schéma du dictionnaire de résumé issu de la méthode "compute".
    """

    data: Optional[xr.DataArray] = None
    compo: Optional[BaseComposite] = None

    def __init__(self) -> None:
        self.data = None
        self.summary: dict = dict()
        self.reset()

    def reset(self) -> None:
        """Méthode permettant de remettre à zéros le processus de construction
        du summary
        """
        self.data = None
        self.summary: dict = dict()

    def compute(self, compo: BaseComposite) -> dict:
        """Méthode permettant d'exécuter toutes les étapes de construction

        Args:
            compo (Composite): Composant sur lequels on se base pour produire le texte
        Return:
            dict: Dictionnaire résumant les infos contenues dans le compo
        """
        self.reset()
        self.compo = compo
        self.data = compo.compute()

        return self.summary
