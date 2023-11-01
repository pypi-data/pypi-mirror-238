from enum import Enum
from typing import Dict, Iterable, Optional, Tuple

from mfire import get_logger
from mfire.utils.string_utils import concatenate_string, decapitalize


# Logging
LOGGER = get_logger(name="utils.wwmf_utils.mod", bind="utils.wwmf_utils")


# Enumeration of all families and subfamilies
class WWMF_FAMILIES(Enum):
    VISIBILITY = 0
    RAIN = 1
    SNOW = 2
    SHOWER = 3
    THUNDERSTORM = 4


def is_severe_phenomenon(wwmf: int) -> bool:
    return wwmf in [49, 59, 85, 98, 99]


def is_wwmf_visibility(wwmf: int) -> bool:
    return 30 <= wwmf <= 39


def are_wwmf_visibilities(*wwmfs: int) -> bool:
    return all(is_wwmf_visibility(wwmf) for wwmf in wwmfs)


def is_wwmf_precipitation(wwmf: int) -> bool:
    return 40 <= wwmf <= 99


def are_wwmf_precipitations(*wwmfs: int) -> bool:
    return all(is_wwmf_precipitation(wwmf) for wwmf in wwmfs)


WWMF_LABELS_BY_CODES: Dict[Tuple, str] = {
    # 1TS
    (0,): "Clair",
    (1,): "Peu nuageux",
    (2,): "Nuageux",
    (3,): "Très nuageux",
    (4,): "Couvert",
    (5,): "Variable",
    (6,): "Voilé",
    (10,): "Sable",
    (15,): "Trombe",
    (30,): "Brume/brouillard",
    (31,): "Brume",
    (32,): "Brouillard",
    (33,): "Brouillard dense",
    (38,): "Brouillard givrant",
    (39,): "Brouillard dense givrant",
    (40,): "Bruine",
    (49,): "Bruine verglaçante",
    (50,): "Pluie",
    (51,): "Pluie faible",
    (52,): "Pluie modérée",
    (53,): "Pluie forte",
    (58,): "Pluie et neige mêlées",
    (59,): "Pluie verglaçante",
    (60,): "Neige",
    (61,): "Neige faible",
    (62,): "Neige modérée",
    (63,): "Neige forte",
    (70,): "Averses",
    (71,): "Rares averses",
    (72,): "Rares averses avec ciel ouvert",
    (73,): "Averses avec ciel couvert",
    (77,): "Averses de pluie et neige mêlées",
    (78,): "Averses de pluie et neige mêlées avec ciel couvert",
    (80,): "Averses de neige",
    (81,): "Rares averses de neige",
    (82,): "Rares averses de neige avec ciel couvert",
    (83,): "Averses de neige avec ciel couvert",
    (84,): "Averses de grésil",
    (85,): "Averses de grêle",
    (90,): "Orages",
    (91,): "Orages possibles",
    (92,): "Averses orageuses",
    (93,): "Orages avec pluie",
    (97,): "Orages avec neige",
    (98,): "Orages avec grêle",
    (99,): "Orages violents",
    # 2TS Visibility family
    (32, 33): "Brouillard, parfois dense",
    (32, 38): "Brouillard, parfois givrant",
    (32, 39): "Brouillard, parfois dense et givrant",
    (33, 38): "Brouillard dense ou givrant",
    (33, 39): "Brouillard dense, parfois givrant",
    (38, 39): "Brouillard givrant, parfois dense",
    # 2TS Family precipitation > Subfamily rain
    (40, 49): "Bruine, parfois verglaçante",
    (49, (51, 52, 53)): "Bruine verglaçante ou pluie",
    (49, 59): "Précipitations verglaçantes",
    (51, 52): "Pluie faible à modérée",
    (51, 53): "Pluie",
    (52, 53): "Pluie modérée à forte",
    ((51, 52, 53), 58): "Pluie, parfois mêlée de neige",
    ((51, 52, 53), 59): "Pluie, parfois verglaçante",
    # 2TS Family precipitation > Subfamily snow
    (58, (61, 62, 63)): "Neige prédominante",
    (61, 62): "Neige parfois modérée",
    (61, 63): "Neige parfois forte",
    (62, 63): "Neige parfois forte",
    ((61, 62, 63), (80, 81, 82, 83)): "Épisodes neigeux",
    # 2TS Family precipitation > Subfamily shower
    (70, (71, 72, 73)): "Averses",
    (71, 72): "Rares averses",
    (71, 73): "Averses",
    (72, 73): "Averses avec ciel couvert",
    ((70, 71, 72, 73), (77, 78)): "Averses, parfois mêlées de neige",
    (77, 78): "Averses mêlées de neige",
    (80, (81, 82, 83)): "Averses de neige",
    (82, 83): "Averses de neige",
    (70, (80, 81, 82, 83)): "Averses, parfois neigeuses",
    (71, (80, 83)): "Averses, parfois neigeuses",
    ((71, 72), (81, 82)): "Rares averses, parfois neigeuses",
    (73, (80, 81)): "Averses, parfois neigeuses",
    (73, (82, 83)): "Averses avec ciel couvert, parfois neigeuses",
    (84, 85): "Averses de grésil ou grêle",
    ((70, 71, 72, 73), 92): "Averses, parfois orageuses",
    # 2TS Family precipitation > Subfamily thunderstorm
    (84, 92): "Averses de grésil parfois orageuses",
    (85, 92): "Averses orageuses parfois avec grêle",
    (85, 98): "Orages ou averses avec grêle",
    (91, 92): "Orages et averses orageuses",
    (91, 93): "Orages parfois avec pluie",
    (91, 97): "Orages, parfois avec neige",
    (93, 98): "Orages avec pluie et grêle",
    (93, 99): "Orages parfois violents avec pluie",
    (97, 99): "Orages, parfois violents avec neige",
    (98, 99): "Orages violents avec grêle",
    # 2TS Family precipitation > several subfamilies
    (51, 61): "Précipitations faibles, parfois neigeuses",
    (52, 62): "Précipitations modérées, parfois neigeuses",
    (53, 63): "Précipitations fortes, parfois neigeuses",
    ((51, 52, 53), (80, 81, 82, 83)): "Pluie, averses de neige",
    ((51, 52, 53), (91, 93)): "Pluie ou orages",
    ((51, 52, 53), 98): "Pluie ou orages avec grêle",
    ((51, 52, 53), 99): "Pluie ou orages violents",
    ((61, 62, 63), (70, 71, 72, 73)): "Averses, neige",
    ((61, 62, 63), (91, 97)): "Orages, neige",
    ((61, 62, 63), 98): "Giboulées orageuses, neige",
    ((61, 62, 63), 99): "Orages violents, neige",
    ((70, 71, 72, 73), (91, 93)): "Averses ou orages",
    ((70, 71, 72, 73), 98): "Averses ou orages avec grêle",
    ((70, 71, 72, 73), 99): "Averses ou orages violents",
    ((80, 81, 82, 83), (91, 97)): "Orages, averses de neige",
    ((80, 81, 82, 83), 98): "Giboulées orageuses, neige",
    ((80, 81, 82, 83), 99): "Orages violents, neige",
    # 3TS family visibility
    (31, 32, 33): "Temps brumeux avec brouillard, parfois dense",
    (31, 32, 38): "Temps brumeux avec brouillard, parfois givrant",
    (31, 32, 39): "Temps brumeux avec brouillard, parfois dense et givrant",
    (32, 33, 38): "Brouillard, parfois dense ou givrant",
    (32, 33, 39): "Brouillard, parfois dense et givrant",
    (33, 38, 39): "Brouillard dense ou givrant",
    # 4TS family visibility
    (31, 32, 33, (38, 39)): "Temps brumeux avec brouillard, parfois dense ou givrant",
    (31, 33, 38, 39): "Temps brumeux avec brouillard, parfois dense et givrant",
    (32, 33, 38, 39): "Brouillard, parfois dense ou givrant",
    # 4TS family precipitaton (special case not included in subgroup combinations)
    (40, (51, 52, 53), (52, 53), 53): "Pluie et bruine",
    # 5TS family visibility
    (31, 32, 33, 38, 39): "Temps brumeux avec brouillard, parfois dense ou givrant",
}


# Some grouping of labels
class WWMF_SUBGRP(Enum):
    A1 = (40, 50, 51, 52, 53)
    A2 = (58, 60, 61, 62, 63)
    A3 = (70, 71, 72, 73)
    A4 = (77, 78, 80, 81, 82, 83)
    A5 = (90, 91, 92, 93, 97)
    B1 = (49, 59)
    B2 = (84,)
    B3 = (85,)
    B4 = (98,)
    B5 = (99,)

    @property
    def is_A_group(self) -> bool:
        return self in [self.A1, self.A2, self.A3, self.A4, self.A5]


WWMF_LABELS_BY_GROUPS: Dict[Tuple, str] = {
    # 1 subgroup
    (WWMF_SUBGRP.A1,): "Pluie",
    (WWMF_SUBGRP.A2,): "Neige",
    (WWMF_SUBGRP.A3,): "Averses",
    (WWMF_SUBGRP.A4,): "Averses de neige",
    (WWMF_SUBGRP.A5,): "Temps orageux",
    # 2 subgroups
    (WWMF_SUBGRP.A1, WWMF_SUBGRP.A2): "Pluie, neige",
    (WWMF_SUBGRP.A1, WWMF_SUBGRP.A3): "Pluie ou averses",
    (WWMF_SUBGRP.A1, WWMF_SUBGRP.A4): "Pluie, averses de neige",
    (WWMF_SUBGRP.A1, WWMF_SUBGRP.A5): "Pluie ou orages",
    (WWMF_SUBGRP.A1, WWMF_SUBGRP.B1): "Pluie parfois verglaçante",
    (WWMF_SUBGRP.A1, WWMF_SUBGRP.B2): "Pluie ou averses de grésil",
    (WWMF_SUBGRP.A1, WWMF_SUBGRP.B3): "Pluie ou averses de grêle",
    (WWMF_SUBGRP.A1, WWMF_SUBGRP.B4): "Pluie ou orages avec grêle",
    (WWMF_SUBGRP.A1, WWMF_SUBGRP.B5): "Pluie ou orages violents",
    (WWMF_SUBGRP.A2, WWMF_SUBGRP.A3): "Averses, neige",
    (WWMF_SUBGRP.A2, WWMF_SUBGRP.A4): "Épisodes neigeux",
    (WWMF_SUBGRP.A2, WWMF_SUBGRP.A5): "Orages, neige",
    (WWMF_SUBGRP.A2, WWMF_SUBGRP.B1): "Précipitations verglaçantes, neige",
    (WWMF_SUBGRP.A2, WWMF_SUBGRP.B2): "Averses de grésil, neige",
    (WWMF_SUBGRP.A2, WWMF_SUBGRP.B3): "Averses de grêle, neige",
    (WWMF_SUBGRP.A2, WWMF_SUBGRP.B4): "Giboulées orageuses, neige",
    (WWMF_SUBGRP.A2, WWMF_SUBGRP.B5): "Orages violents, neige",
    (WWMF_SUBGRP.A3, WWMF_SUBGRP.A4): "Averses parfois neigeuses",
    (WWMF_SUBGRP.A3, WWMF_SUBGRP.A5): "Orages ou averses",
    (WWMF_SUBGRP.A3, WWMF_SUBGRP.B1): "Précipitations verglaçantes ou averses",
    (WWMF_SUBGRP.A3, WWMF_SUBGRP.B2): "Averses avec parfois du grésil",
    (WWMF_SUBGRP.A3, WWMF_SUBGRP.B3): "Averses avec parfois de la grêle",
    (WWMF_SUBGRP.A3, WWMF_SUBGRP.B4): "Orages avec grêle ou averses",
    (WWMF_SUBGRP.A3, WWMF_SUBGRP.B5): "Averses ou orages violents",
    (WWMF_SUBGRP.A4, WWMF_SUBGRP.A5): "Orages, neige",
    (WWMF_SUBGRP.A4, WWMF_SUBGRP.B1): "Précipitations verglaçantes, neige",
    (WWMF_SUBGRP.A4, WWMF_SUBGRP.B2): "Giboulées neigeuses",
    (WWMF_SUBGRP.A4, WWMF_SUBGRP.B3): "Fortes giboulées neigeuses",
    (WWMF_SUBGRP.A4, WWMF_SUBGRP.B4): "Orages, giboulées neigeuses",
    (WWMF_SUBGRP.A4, WWMF_SUBGRP.B5): "Orages violents, averses de neige",
    (WWMF_SUBGRP.A5, WWMF_SUBGRP.B1): "Précipitations verglaçantes ou orages",
    (WWMF_SUBGRP.A5, WWMF_SUBGRP.B2): "Orages ou averses de grésil",
    (WWMF_SUBGRP.A5, WWMF_SUBGRP.B3): "Orages ou averses de grêle",
    (WWMF_SUBGRP.A5, WWMF_SUBGRP.B4): "Temps orageux avec grêle possible",
    (WWMF_SUBGRP.A5, WWMF_SUBGRP.B5): "Orages parfois violents",
    # 3 subgroups
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A3,
    ): "Précipitations, parfois neigeuses",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A4,
    ): "Précipitations, parfois neigeuses",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A5,
    ): "Orages, précipitations, parfois neigeuses",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.B1,
    ): "Précipitations verglaçantes, neige",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.B2,
    ): "Précipitations, temporairement avec grésil, ou neige",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.B3,
    ): "Précipitations, temporairement avec grêle, ou neige",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.B4,
    ): "Giboulées orageuses, pluie, mêlée de neige",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.B5,
    ): "Violentes giboulées orageuses, pluie, mêlée de neige",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A4,
    ): "Averses, mêlées de neige",
    (WWMF_SUBGRP.A1, WWMF_SUBGRP.A3, WWMF_SUBGRP.A5): "Temps pluvieux avec orages",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B1,
    ): "Pluie parfois verglaçante et averses",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B2,
    ): "Temps pluvieux avec averses de grésil",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B3,
    ): "Temps pluvieux avec averses de grêle",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B4,
    ): "Temps pluvieux avec orages de grêle",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B5,
    ): "Temps pluvieux avec orages violents",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.A5,
    ): "Orages, précipitations, parfois mêlées de neige",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B1,
    ): "Précipitations verglaçantes, neige",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B2,
    ): "Précipitations, temporairement avec grésil, ou neige",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B3,
    ): "Précipitations, temporairement avec grêle, ou neige",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B4,
    ): "Orages avec grêle, précipitations, temporairement neigeuses",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B5,
    ): "Orages violents, précipitations, temporairement neigeuses",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B1,
    ): "Pluie parfois verglaçante et orages",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B2,
    ): "Pluie et orages parfois avec grésil",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B3,
    ): "Pluie et orages parfois avec grêle",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B4,
    ): "Pluie et orages parfois avec grêle",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B5,
    ): "Pluie et orages parfois violents",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B2,
    ): "Pluie parfois verglaçante et averses de grésil",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B3,
    ): "Pluie parfois verglaçante et averses de grêle",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B4,
    ): "Pluie parfois verglaçante et orages de grêle",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B5,
    ): "Pluie parfois verglaçante et orages violents",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B3,
    ): "Pluie avec averses de grêle et de grésil",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B4,
    ): "Pluie avec averses de grésil et orages de grêle",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B5,
    ): "Pluie avec averses de grésil et orages violents",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.B3,
        WWMF_SUBGRP.B4,
    ): "Pluie avec averses et orages de grêle",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.B3,
        WWMF_SUBGRP.B5,
    ): "Pluie avec averses de grêle et orages violents",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.B4,
        WWMF_SUBGRP.B5,
    ): "Pluie avec orages violents parfois avec grêle",
    (WWMF_SUBGRP.A2, WWMF_SUBGRP.A3, WWMF_SUBGRP.A4): "Averses, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A5,
    ): "Orages, averses, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B1,
    ): "Précipitations parfois verglaçantes, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B2,
    ): "Averses parfois de grésil, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B3,
    ): "Averses parfois de grêle, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B4,
    ): "Giboulées orageuses, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B5,
    ): "Violentes giboulées orageuses, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.A5,
    ): "Orages, averses, parfois neigeuses",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B1,
    ): "Précipitations verglaçantes, neige prédominante",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B2,
    ): "Averses de grésil, neige prédominante",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B3,
    ): "Averses de grêle, neige prédominante",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B4,
    ): "Giboulées orageuses, neige prédominante",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B5,
    ): "Violentes giboulées orageuses, neige prédominante",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B1,
    ): "Orages, précipitations verglaçantes, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B2,
    ): "Giboulées orageuses, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B3,
    ): "Fortes giboulées orageuses, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B4,
    ): "Fortes giboulées orageuses, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B5,
    ): "Orages violents, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B2,
    ): "Précipitations parfois verglaçantes ou avec grésil, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B3,
    ): "Précipitations parfois verglaçantes ou avec grêle, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B4,
    ): "Giboulées orageuses, précipitations verglaçantes, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B5,
    ): "Orages violents, précipitations verglaçantes, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B3,
    ): "Giboulées orageuses, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B4,
    ): "Giboulées orageuses, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B5,
    ): "Orages violents parfois avec grésil, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.B3,
        WWMF_SUBGRP.B4,
    ): "Fortes giboulées orageuses, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.B3,
        WWMF_SUBGRP.B5,
    ): "Orages violents parfois avec grêle, neige",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.B4,
        WWMF_SUBGRP.B5,
    ): "Orages, averses parfois neigeuses",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.A5,
    ): "Orages et averses parfois neigeuses",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B1,
    ): "Précipitations verglaçantes, neige",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B2,
    ): "Giboulées neigeuses",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B3,
    ): "Fortes giboulées neigeuses",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B4,
    ): "Giboulées orageuses, neige",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B5,
    ): "Orages violents, averses parfois neigeuses",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B1,
    ): "Précipitations parfois verglaçantes et orages",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B2,
    ): "Averses, parfois de grésil, et orages",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B3,
    ): "Averses, parfois de grêle, et orages",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B4,
    ): "Orages parfois avec grêle et averses",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B5,
    ): "Orages parfois violents et averses",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B2,
    ): "Précipitations parfois verglaçantes et averses de grésil",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B3,
    ): "Précipitations parfois verglaçantes et averses de grêle",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B4,
    ): "Précipitations parfois verglaçantes et orages avec grêle",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B5,
    ): "Précipitations parfois verglaçantes et orages violents",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B3,
    ): "Averses, parfois de grésil ou de grêle",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B4,
    ): "Averses, parfois de grésil et orages avec grêle",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B5,
    ): "Averses, parfois de grésil et orages violents",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B3,
        WWMF_SUBGRP.B4,
    ): "Averses et orages avec grêle",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B3,
        WWMF_SUBGRP.B5,
    ): "Averses parfois de grêle et orages violents",
    (
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.B4,
        WWMF_SUBGRP.B5,
    ): "Averses et orages violents, parfois avec grêle",
    (
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B1,
    ): "Orages, précipitations verglaçantes, averses de neige",
    (
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B2,
    ): "Orages parfois avec grésil, averses de neige",
    (
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B3,
    ): "Orages parfois avec grêle, averses de neige",
    (
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B4,
    ): "Orages parfois avec grêle, averses de neige",
    (
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.A5,
        WWMF_SUBGRP.B5,
    ): "Orages parfois violents, averses de neige",
    (
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B2,
    ): "Précipitations parfois verglaçantes ou avec grésil, neige",
    (
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B3,
    ): "Précipitations parfois verglaçantes ou avec grêle, neige",
    (
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B4,
    ): "Orages avec grêle, précipitations verglaçantes, neige",
    (
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B5,
    ): "Orages violents, précipitations verglaçantes, neige",
    (
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B3,
    ): "Giboulées neigeuses",
    (
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B4,
    ): "Giboulées orageuses, neige",
    (
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B5,
    ): "Violentes giboulées orageuses, neige",
    (
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B3,
        WWMF_SUBGRP.B4,
    ): "Giboulées orageuses, neige",
    (
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B3,
        WWMF_SUBGRP.B5,
    ): "Violentes giboulées orageuses, neige",
    (
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.B4,
        WWMF_SUBGRP.B5,
    ): "Violentes giboulées orageuses, neige",
    (WWMF_SUBGRP.B2, WWMF_SUBGRP.B3, WWMF_SUBGRP.B4): "Orages avec grêle et grésil",
    (
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B3,
        WWMF_SUBGRP.B5,
    ): "Orages parfois violents et grêle",
    (
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B4,
        WWMF_SUBGRP.B5,
    ): "Orages parfois violents et grêle",
    (WWMF_SUBGRP.B3, WWMF_SUBGRP.B4, WWMF_SUBGRP.B5): "Orages violents avec grêle",
    # 4TS family precipitation
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A4,
    ): "Temps perturbé, précipitations, parfois neigeuses",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A5,
    ): "Temps perturbé, orages, précipitations parfois neigeuses",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.A5,
    ): "Temps perturbé, orages, précipitations parfois neigeuses",
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.A5,
    ): "Temps perturbé, orages, précipitations, parfois sous forme d'averses neigeuses",
    (
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.A5,
    ): "Temps perturbé, orages, précipitations parfois neigeuses",
    (
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B3,
        WWMF_SUBGRP.B4,
        WWMF_SUBGRP.B5,
    ): "Orages violents avec grêle et grésil",
    # 5TS family precipitations
    (
        WWMF_SUBGRP.A1,
        WWMF_SUBGRP.A2,
        WWMF_SUBGRP.A3,
        WWMF_SUBGRP.A4,
        WWMF_SUBGRP.A5,
    ): "Temps perturbé avec orages et précipitations, parfois neigeuses",
    (
        WWMF_SUBGRP.B1,
        WWMF_SUBGRP.B2,
        WWMF_SUBGRP.B3,
        WWMF_SUBGRP.B4,
        WWMF_SUBGRP.B5,
    ): "Précipitations verglaçantes, orages violents avec grêle et grésil",
}


def is_snow_family(wwmf) -> bool:
    return wwmf == 58 or 60 <= wwmf <= 63 or 77 <= wwmf <= 83


def is_rain_family(wwmf) -> bool:
    return 40 <= wwmf <= 59 or 70 <= wwmf <= 78 or wwmf == 93


def is_shower_family(wwmf) -> bool:
    return 70 <= wwmf <= 85 or wwmf == 92


def is_thunderstorm_family(wwmf) -> bool:
    return wwmf in [84, 85] or 90 <= wwmf <= 99


def wwmf_families(*args) -> Tuple[WWMF_FAMILIES]:
    families = set()
    for wwmf in args:
        if is_wwmf_visibility(wwmf):
            families.add(WWMF_FAMILIES.VISIBILITY)
        else:
            if is_rain_family(wwmf):
                families.add(WWMF_FAMILIES.RAIN)
            if is_snow_family(wwmf):
                families.add(WWMF_FAMILIES.SNOW)
            if is_shower_family(wwmf):
                families.add(WWMF_FAMILIES.SHOWER)
            if is_thunderstorm_family(wwmf):
                families.add(WWMF_FAMILIES.THUNDERSTORM)
    return tuple(families)


def wwmf_subfamilies(*args) -> Tuple[WWMF_SUBGRP]:
    return tuple(
        subgroup for subgroup in WWMF_SUBGRP if set(subgroup.value) & set(args)
    )


def wwmf_label(*args, concat_if_not_found: bool = True) -> Optional[str]:
    nbr_args = len(args)
    if nbr_args == 1:
        return WWMF_LABELS_BY_CODES[(args[0],)]

    # If we have >= 3 precipitation TS then we regroup some repeated codes
    args = sorted(args)
    if nbr_args >= 3 and are_wwmf_precipitations(*args):
        subfamilies = wwmf_subfamilies(*args)
        try:
            return WWMF_LABELS_BY_GROUPS[subfamilies]
        except KeyError:
            LOGGER.warning(f"No sentence found for subfamilies {subfamilies}")
            return "Situation météorologique très perturbée"
    else:
        for key, value in WWMF_LABELS_BY_CODES.items():
            if len(key) != nbr_args:
                continue
            elif all(
                arg in key[i] if isinstance(key[i], Iterable) else arg == key[i]
                for i, arg in enumerate(args)
            ):
                return value

    if concat_if_not_found:
        labels = [WWMF_LABELS_BY_CODES[(args[0],)]] + [
            decapitalize(WWMF_LABELS_BY_CODES[(arg,)]) for arg in args[1:]
        ]
        return concatenate_string(labels)
    return None
