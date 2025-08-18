
expAvgAPP = 0.68, 0.85, 1.07
expAvgFrag = 1, 1, 1
expAvgSpot = 0.78, 1, 1.24
expAvgDef = 0.1, 0.15, 0.17
expWin = 0.5
scaling = 1450/1696  # value you want to lean towards to / actual value that leans to (if same as expected value)
APPscal = 1020/758  # maybe i should try make a universal scaling

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
        print("incorrect winrate value")
        win = None
except ValueError:
    win = None
    print("set to no winrate value")

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
WN8 = int((1090*rAPPc + 152*rAPPc*rFRAGc + 65*rFRAGc*rSPOTc + 95*rDEFc*rFRAGc + 210 * rWINc * rAPPc + 378*min(1.8,rWINc)) * scaling)
# wn8 ig

print(f"Total WN8: {WN8}")

def wn8_status(wn8):
    if wn8 < 300:
        return "Status: Dark Red (Very Bad)"
    elif 300 <= wn8 < 450:
        return "Status: Red (Bad)"
    elif 450 <= wn8 < 650:
        return "Status: Orange (Below Average)"
    elif 650 <= wn8 < 900:
        return "Status: Yellow (Average)"
    elif 900 <= wn8 < 1200:
        return "Status: Light Green (Above Average)"
    elif 1200 <= wn8 < 1600:
        return "Status: Green (Good)"
    elif 1600 <= wn8 < 2000:
        return "Status: Light Blue (Very Good)"
    elif 2000 <= wn8 < 2450:
        return "Status: Blue (Great)"
    elif 2450 <= wn8 < 2900:
        return "Status: Violet (Unicum)"
    else:
        return "Status: Dark Violet (Super Unicum)"
print(wn8_status(WN8))

print(f"rAPPc: {rAPPc:.2f}, rFRAGc: {rFRAGc:.2f}, rSPOTc: {rSPOTc:.2f}, rDEFc: {rDEFc:.2f}, rWINc: {rWINc:.2f}")

ind_wn8 = int((1090*rAPPc)*scal2)
print(f"APP WN8: {ind_wn8}")
print(wn8_status(ind_wn8))