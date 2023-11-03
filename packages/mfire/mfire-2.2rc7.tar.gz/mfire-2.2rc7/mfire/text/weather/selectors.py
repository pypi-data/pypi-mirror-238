from mfire.settings import get_logger
from mfire.text.base import BaseSelector

# Logging
LOGGER = get_logger(name="weather_selector.mod", bind="weather_selector")


class WeatherSelector(BaseSelector):
    """WeatherSelector spécifique pour la weather"""

    def compute(self, reduction: dict) -> str:
        """génération du dictionnaire de choix, recherche dans la matrice
        du texte de synthèse pour le température pour déterminer la clé du template
        en fonction du paramètre
        """

        LOGGER.info(f"reduction {reduction}")

        nbr_ts: int = len(set(reduction) - {"TSsevere"})

        if nbr_ts == 0:
            return "0xTS"
        elif nbr_ts == 1:
            key = "1xTS"
            if reduction["TS1"]["temporality"]:
                key += "_temp"
            if reduction["TS1"]["localisation"]:
                key += "_loc"
            if "TSsevere" in reduction:
                key += "_severe"
            return key
        elif nbr_ts == 2:
            key = "2xTS"

            has_temp1 = reduction["TS1"]["temporality"] is not None
            has_temp2 = reduction["TS2"]["temporality"] is not None
            if has_temp1 or has_temp2:
                key += "_temp"
                if has_temp1 ^ has_temp2:
                    key += "1" if has_temp1 else "2"

            if "TSsevere" in reduction:
                key += "_severe"
            else:
                has_loc1 = reduction["TS1"]["localisation"] is not None
                has_loc2 = reduction["TS2"]["localisation"] is not None
                if has_loc1 or has_loc2:
                    key += "_loc"
                    if has_loc1 ^ has_loc2:
                        key += "1" if has_loc1 else "2"
            return key
        elif nbr_ts == 3:
            key = "3xTS"
            has_temp1 = reduction["TS1"]["temporality"] is not None
            has_temp2 = reduction["TS2"]["temporality"] is not None
            has_temp3 = reduction["TS3"]["temporality"] is not None
            has_loc1 = reduction["TS1"]["localisation"] is not None
            has_loc2 = reduction["TS2"]["localisation"] is not None
            has_loc3 = reduction["TS3"]["localisation"] is not None
            if has_temp1 or has_temp2 or has_temp3:
                key += "_temp"
                if has_temp1:
                    key += "1"
                if has_temp2:
                    key += "2"
                if has_temp3:
                    key += "3"
            if has_loc1 or has_loc2 or has_loc3:
                key += "_loc"
                if has_loc1:
                    key += "1"
                if has_loc2:
                    key += "2"
                if has_loc3:
                    key += "3"
            return key
        else:
            return "Unimplemented"
