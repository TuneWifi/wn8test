import sys

expAvgAPP = 0.68, 0.85, 1.07
expAvgFrag = 1, 1, 1
expAvgSpot = 0.78, 1, 1.24
expAvgDef = 0.1, 0.15, 0.17
expWin = 0.5
scale = {
    "full": 1450 / 1560,
    "individual": 1020 / 755,
    # value you want to lean towards to / actual value that leans to (if same as expected value)
}


# just testing for now

def float_check(value, name="", allow_none=True, min_val=None, max_val=None):
    if isinstance(value, float):
        return value

    if allow_none and value in ("none", "", None):
        return None

    try:
        val = float(value)
        if min_val is not None and val < min_val:
            raise ValueError
        if max_val is not None and val > max_val:
            raise ValueError
        return val
    except ValueError:
        print(f"Invalid input for {name}. Expected a number", end="")
        if allow_none:
            print(" or 'none'", end="")
        if min_val is not None or max_val is not None:
            print(f" between {min_val} and {max_val}", end="")
        print(". Exiting.")
        exit()

# rank Input
fields = [
    ("ranking", "Rank (bm / gm / wm): "),
    ("games", "total games: "),
    ("AvgAPP", "average APP: "),
    ("win", "winrate (0-100 or none): "),
    ("cheese", "cheese index: "),
    ("APPnDSpP", "APP+DS/p: "),
    ("DSpP", "DS/p: "),
]

input_data = {}
history = []

rank_index = 1
rank_key = "gm"

rank_defaults = {
    "bm": {
        "AvgAPP": expAvgAPP[0],
        "cheese": expAvgFrag[0],
        "APPnDSpP": expAvgSpot[0],
        "DSpP": expAvgDef[0],
    },
    "gm": {
        "AvgAPP": expAvgAPP[1],
        "cheese": expAvgFrag[1],
        "APPnDSpP": expAvgSpot[1],
        "DSpP": expAvgDef[1],
    },
    "wm": {
        "AvgAPP": expAvgAPP[2],
        "cheese": expAvgFrag[2],
        "APPnDSpP": expAvgSpot[2],
        "DSpP": expAvgDef[2],
    }
}

DEFAULT_VALUES = {
    "games": 100,
    "AvgAPP": expAvgAPP[rank_index],
    "win": 50,
    "cheese": expAvgFrag[rank_index],
    "APPnDSpP": expAvgSpot[rank_index],
    "DSpP": expAvgDef[rank_index],
    "ranking": "gm",
}

use_all_defaults = False
use_rest_defaults = False
forced_rank = None

i = 0
while i < len(fields):
    key, prompt = fields[i]

    while True:
        user_input = input(prompt).strip().lower()

        if user_input == "exit":
            print("Exiting program.")
            exit()

        if user_input.startswith("back"):
            parts = user_input.split("(")
            num_back = 1
            if len(parts) > 1 and parts[1].endswith(")"):
                try:
                    num_back = int(parts[1][:-1])
                    if num_back < 0:
                        print("Error: Negative number in back(). Try again.")
                        continue
                except ValueError:
                    print("Error: Invalid back(n) format. Try again.")
                    continue

            new_pos = max(0, i - num_back)
            for rem_i in range(new_pos, len(fields)):
                rem_key = fields[rem_i][0]
                input_data.pop(rem_key, None)

            i = new_pos
            history = history[:i]
            print(f"Going back to: {fields[i][1]}")
            break  # jump back

        # Handle default commands
        if user_input.startswith("use_default_all_"):
            tag = user_input.replace("use_default_all_", "")
            if tag in rank_defaults:
                forced_rank = tag
                use_all_defaults = True
                i = len(fields)
                break
            else:
                print("Invalid rank tag for use_default_all_. Try again.")
                continue
        elif user_input == "use_default_all":
            forced_rank = rank_key
            use_all_defaults = True
            i = len(fields)
            break

        elif user_input.startswith("use_default_rest_"):
            tag = user_input.replace("use_default_rest_", "")
            if tag in rank_defaults:
                forced_rank = tag
                use_rest_defaults = True
                input_data[key] = None
                i = len(fields)
                break
            else:
                print("Invalid rank tag for use_default_rest_. Try again.")
                continue
        elif user_input == "use_default_rest":
            forced_rank = rank_key
            use_rest_defaults = True
            input_data[key] = None
            i = len(fields)
            break


        elif user_input.startswith("use_default_"):
            tag = user_input.replace("use_default_", "")
            if tag in rank_defaults:
                input_data[key] = rank_defaults[tag].get(key, DEFAULT_VALUES.get(key))
            else:
                input_data[key] = DEFAULT_VALUES.get(key)
            history.append(key)
            i += 1
            break
        elif user_input == "use_default":
            input_data[key] = DEFAULT_VALUES[key]
            history.append(key)
            i += 1
            break

        # Special parsing for ranking
        if key == "ranking":
            if user_input in ("bm", "black major"):
                rank_index = 0
            elif user_input in ("gm", "gray major"):
                rank_index = 1
            elif user_input in ("wm", "white major"):
                rank_index = 2
            else:
                print("Invalid rank. Defaulted to Gray Major.")
                rank_index = 1
                user_input = "gm"

            rank_key = ["bm", "gm", "wm"][rank_index]

            DEFAULT_VALUES.update({
                "AvgAPP": expAvgAPP[rank_index],
                "cheese": expAvgFrag[rank_index],
                "APPnDSpP": expAvgSpot[rank_index],
                "DSpP": expAvgDef[rank_index],
                "ranking": user_input
            })

            input_data["ranking"] = user_input
            history.append(key)
            i += 1
            break

        # Regular input
        input_data[key] = user_input
        history.append(key)
        i += 1
        break

# Apply defaults
if use_all_defaults:
    print(f"\nUsing all default values from {forced_rank.upper()}...\n")
    for key, _ in fields:
        input_data[key] = rank_defaults.get(forced_rank, {}).get(key, DEFAULT_VALUES.get(key))
        pass
elif use_rest_defaults:
    print(f"\nUsing default values from {forced_rank.upper()} for remaining fields...\n")
    for key, _ in fields:
        if input_data.get(key) in (None, "", "none"):
            input_data[key] = rank_defaults.get(forced_rank, {}).get(key, DEFAULT_VALUES.get(key))
            pass

# Final parsing
games = float_check(input_data["games"], "games")
AvgAPP = float_check(input_data["AvgAPP"], "AvgAPP")
win = float_check(input_data["win"], "winrate", allow_none=True, min_val=0, max_val=100)
cheese = float_check(input_data["cheese"], "cheese")
APPnDSpP = float_check(input_data["APPnDSpP"], "APP+DS/p")
DSpP = float_check(input_data["DSpP"], "DS/p")

rank_input = input_data["ranking"]
rank_index = {"bm": 0, "gm": 1, "wm": 2}.get(rank_input, 1)

aAPP = games * AvgAPP
expAPP = games * expAvgAPP[rank_index]
rAPP = aAPP / expAPP

if rAPP < 0.55:
  rAPP_scaled = (rAPP / 0.55) ** 2.2 * 0.55
elif rAPP <= 1.0:
  rAPP_scaled = 0.5 + ((rAPP - 0.5) / 0.5) ** 0.5 * 0.35
elif rAPP <= 1.3:
  rAPP_scaled = 0.85 + ((rAPP - 1.0) / 0.5) ** 2.2 * 0.4
else:
  rAPP_scaled = 1.05 + ((rAPP - 1.3) ** 0.75) * 0.5

rAPPc = max(0, ((rAPP_scaled - 0.22) / (1 - 0.22))) ** 1.7

# calculate calibrated app ig

aFrag = games * cheese   # treat it as total frags
expFrag = games * expAvgFrag[rank_index]
rFrag = aFrag/expFrag
rFRAGc = max(0, min(rAPPc + 0.2, (rFrag - 0.12) / (1 - 0.12)))

# calculate calibrated frags

aSpot = games * APPnDSpP   # you know the deal
expSpot = games * expAvgSpot[rank_index]
rSpot = aSpot/expSpot
rSPOTc = max(0, min(rAPPc + 0.1, (rSpot - 0.38) / (1 - 0.38)))

# calculate calibrated spots

aDef = games * DSpP
expDef = games * expAvgDef[rank_index]
rDef = aDef/expDef
rDEFc = max(0, min(rAPPc + 0.1, (rDef - 0.10) / (1 - 0.10)))

# calculate calibrated defense

if win is None:
   rWINc = 0.09 + 0.613*rAPPc + 0.131*rFRAGc*rAPPc + 0.097*rFRAGc*rSPOTc+0.047* rFRAGc*rDEFc
else:
    aWin = games * (win/100)
    expWin = games * expWin
    rWin = aWin/expWin
    rWINc = max(0, ((rWin - 0.71) / (1 - 0.71) ** 1.1 ))

# winrate ig
WN8 = int((1090*rAPPc + 152*rAPPc*rFRAGc + 65*rFRAGc*rSPOTc + 95*rDEFc*rFRAGc + 210 * rWINc * rAPPc + 378*min(1.8,rWINc)) * scale["full"])
# wn8 ig

print(f"Total WN8: {WN8}")

def wn8_status(wn8):
    statuses = {
        (0, 300): "Status: Dark Red (Very Bad)",
        (300, 450): "Status: Red (Bad)",
        (450, 650): "Status: Orange (Below Average)",
        (650, 900): "Status: Yellow (Average)",
        (900, 1200): "Status: Light Green (Above Average)",
        (1200, 1600): "Status: Green (Good)",
        (1600, 2000): "Status: Light Blue (Very Good)",
        (2000, 2450): "Status: Blue (Great)",
        (2450, 2900): "Status: Violet (Unicum)",
        (2900, 99999): "Status: Dark Violet (Super Unicum)"
    }
    for (low, high), status in statuses.items():
        if low <= wn8 < high:
            return status
    return "Status: Unknown"
print(wn8_status(WN8))

print(f"rAPPc: {rAPPc:.2f}, rFRAGc: {rFRAGc:.2f}, rSPOTc: {rSPOTc:.2f}, rDEFc: {rDEFc:.2f}, rWINc: {rWINc:.2f}")

ind_wn8 = int((1090*rAPPc)*scale["individual"])
print(f"APP WN8: {ind_wn8}")
print(wn8_status(ind_wn8))