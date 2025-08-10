
expAvgAPP = 0.68, 0.85, 1.07
expAvgFrag = 1, 1, 1
expAvgSpot = 0.78, 1, 1.24
expAvgDef = 0.1, 0.15, 0.17
expWin = 0.5
scaling = 1350/1241.2  # value you want to lean towards to / actual value that leans to (

# just testing for now

def float_check(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        print("wrong input")
        exit()

games = float_check("total games: ")
AvgAPP = float_check("average APP: ")
win = input("winrate (0-100 or none): ")
cheese = float_check("cheese index: ")
APPnDSpP = float_check("APP+DS/p: ")
DSpP = float_check("DS/p: ")
ranking = input("Rank: ").lower()  # assuming they know

if ranking in ("bm", "black major"):
    rank_index = 0
elif ranking in ("wm", "white major"):
    rank_index = 2
else:
    rank_index = 1

try:
    win = float(win)
    if not (0 <= win <= 100):
        print("incorrect value")
        win = None
except ValueError:
    win = None
    print("set to no winrate value")

aAPP = games * AvgAPP
expAPP = games * expAvgAPP[rank_index]
rAPP = aAPP / expAPP

if rAPP < 0.55:
    rAPP_scaled = (rAPP / 0.55) ** 3 * 0.5
elif rAPP <= 1.0:
    rAPP_scaled = 0.5 + ((rAPP - 0.5) / 0.5) ** 0.5 * 0.35
elif rAPP <= 1.3:
    rAPP_scaled = 0.85 + ((rAPP - 1.0) / 0.5) ** 2 * 0.35
else:
    rAPP_scaled = 1.2 + ((rAPP - 1.3) ** 2) * 0.5

rAPPc = max(0, ((rAPP_scaled - 0.22) / (1 - 0.22))) ** 1.44

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
    rWINc = max(0, (rWin - 0.71) / (1 - 0.71))

# winrate ig
WN8 = int((1010*rAPPc + 130*rAPPc*rFRAGc + 30*rFRAGc*rSPOTc + 60*rDEFc*rFRAGc + 360*min(1.8,rWINc)) * scaling)
# wn8 ig

print(WN8)

if WN8 < 300:
    print("Status: Dark Red (Very Bad)")
elif 300 <= WN8 < 450:
    print("Status: Red (Bad)")
elif 450 <= WN8 < 650:
    print("Status: Orange (Below Average)")
elif 650 <= WN8 < 900:
    print("Status: Yellow (Average)")
elif 900 <= WN8 < 1200:
    print("Status: Light Green (Above Average)")
elif 1200 <= WN8 < 1600:
    print("Status: Green (Good)")
elif 1600 <= WN8 < 2000:
    print("Status: Light Blue (Very Good)")
elif 2000 <= WN8 < 2450:
    print("Status: Blue (Great)")
elif 2450 <= WN8 < 2900:
    print("Status: Violet (Unicum)")
else:
    print("Status: Dark Violet (Super Unicum)")

print(f"rAPPc: {rAPPc:.2f}, rFRAGc: {rFRAGc:.2f}, rSPOTc: {rSPOTc:.2f}, rDEFc: {rDEFc:.2f}, rWINc: {rWINc:.2f}")