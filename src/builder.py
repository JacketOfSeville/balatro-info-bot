from lib.blinds import blinds
from lib.jokers import jokers
from lib.planets import planets
from lib.spectrals import spectrals
from lib.tarots import tarots
from lib.vouchers import vouchers
from Levenshtein import distance as levenshtein_distance
from typing import Callable, Literal, Optional, Tuple, Union

type CardKeys = Literal['name', 'text', 'image', 'rarity', 'unlock']
type CardData = dict[CardKeys, Union[str, None]]
type DataSet = dict[str, CardData]
type Category = Literal['jokers', 'blinds', 'spectrals', 'tarots', 'vouchers', 'planets']
type Reply = dict[Union[CardKeys, Literal['category', 'boss']], Union[str, None]]

CATEGORIES_TO_DATASETS: dict[Category, DataSet] = {
    'jokers': jokers,
    'blinds': blinds,
    'spectrals': spectrals,
    'tarots': tarots,
    'vouchers': vouchers,
    'planets': planets
}

LOWEST_DIFFERENCE_TO_MATCH = 5

BOSS_ID_PREFIX = 'bl_final_'

def flatten_and_find_last(map: dict[Category, DataSet],
                          func: Callable[[CardData], bool]) -> Optional[Tuple[CardData, str, Category]]:
    """
    Looks for the last element in a nested dictionary that matches a condition.

    Returns the last element that matches the condition, or None if no match is
    found.
    """
    
    result: Optional[Tuple[CardData, str, Category]] = None
    
    for k1, v1 in map.items():
        for k2, v2 in v1.items():
            if func(v2):
                result = (v2, k2, k1)
    
    return result

def find_best_match(search_term: str) -> Optional[Tuple[CardData, str, Category]]:
    """
    Finds the best match for a search term in the card data.
    """

    lowest_difference_score: int = LOWEST_DIFFERENCE_TO_MATCH

    def is_best_match(card_data: CardData) -> bool:
        nonlocal search_term, lowest_difference_score
        card_name: str = card_data.get('name', '').lower()
        name_difference_score: int = levenshtein_distance(card_name, search_term)

        if name_difference_score >= lowest_difference_score:
            return False

        lowest_difference_score = name_difference_score
        return True

    return flatten_and_find_last(CATEGORIES_TO_DATASETS, is_best_match)

def build_reply(search_term: str) -> Optional[Reply]:
    """
    Builds a reply for the given search term.
    """

    best_match_info = find_best_match(search_term)

    if best_match_info is None:
        return None
    
    best_match, best_match_id, best_match_category = best_match_info

    return {
        **best_match,
        'category': best_match_category,
        'boss': 'Final ' if BOSS_ID_PREFIX in best_match_id else None,
    }
