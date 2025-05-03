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
            dist = levenshtein_distance(name, input_string)

            if dist < min_distance:
                min_distance = dist
                best_match = obj.copy()
                best_match["category"] = category

    if min_distance > 5:
        return None
    
    return best_match


def get_item_label(value):
    if value["key"].startswith("j_"):
        if ("rarity" in value["match"]):
            return f"{value['match']['rarity']} Joker"
        else:
            return "Common Joker"
    elif value["key"].startswith("bl_"):
        return "Blind"
    elif value["key"].startswith("s_"):
        return "Spectral Card"
    elif value["key"].startswith("t_"):
        return "Tarot Card"
    elif value["key"].startswith("v_"):
        return "Voucher"
    elif value["key"].startswith("p_"):
        return "Planet Card"
    else:
        return "Unknown"

def get_item_unlock(value):
    if value["key"].startswith("j_") or value["key"].startswith("v_"):
        return f"- **To Unlock**: {value['match']['unlock'] if 'unlock' in value['match'] else 'Available by default'}\n\n"
    else:
        return f"\n"

def format_item(item):
    item = item.lower().strip()
    if item.startswith("the "):
        item = item[4:]
    return item