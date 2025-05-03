from lib.blinds import blinds
from lib.jokers import jokers
from lib.planets import planets
from lib.spectrals import spectrals
from lib.tarots import tarots
from lib.vouchers import vouchers
from Levenshtein import distance as levenshtein_distance

ALL_CATEGORIES = {
    'jokers': jokers,
    'blinds': blinds,
    'spectrals': spectrals,
    'tarots': tarots,
    'vouchers': vouchers,
    'planets': planets
}

def build_reply(input_string: str):
    input = input_string.lower()
    min_distance = float('inf')
    best_match = None

    for category, dataset in ALL_CATEGORIES.items():
        for obj_key, obj in dataset.items():
            name = obj.get("name", "").lower()
            dist = levenshtein_distance(name, input)

            if dist < min_distance:
                min_distance = dist
                best_match = obj.copy()
                best_match["category"] = category

                if 'bl_final' in obj_key:
                    best_match["boss"] = 'Final '

    if min_distance > 5:
        return None
    
    return best_match
