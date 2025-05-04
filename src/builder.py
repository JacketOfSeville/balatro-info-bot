from lib.blinds import blinds
from lib.jokers import jokers
from lib.planets import planets
from lib.spectrals import spectrals
from lib.tarots import tarots
from lib.vouchers import vouchers
from Levenshtein import distance as levenshtein_distance

CATEGORIES_TO_DATASETS = {
    'jokers': jokers,
    'blinds': blinds,
    'spectrals': spectrals,
    'tarots': tarots,
    'vouchers': vouchers,
    'planets': planets
}

def build_reply(search_term: str):
    input = search_term.lower()
    lowest_difference_score = float('inf')
    best_match = None

    for category, dataset in CATEGORIES_TO_DATASETS.items():
        for card_id, card_data in dataset.items():
            card_name = card_data.get("name", "").lower()
            name_difference_score = levenshtein_distance(card_name, input)

            if name_difference_score < lowest_difference_score:
                lowest_difference_score = name_difference_score
                best_match = card_data.copy()
                best_match["category"] = category

                if 'bl_final' in card_id:
                    best_match["boss"] = 'Final '

    return None if lowest_difference_score > 5 else best_match
