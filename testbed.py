from core import *

count=7
houseCount=1467
village=18
idsSurveyed = []
numberSurveyed = 0
seed = random_org.org_randint(-(1 << 16), 1 << 16, 1)[0]
print("SEEDED:",seed)
random.seed(seed)
while numberSurveyed<count:
    housenum = random.randint(0, houseCount - 1)
    members = getHouseMembers(housenum, village)
    random.shuffle(members)
    for member in members:
        if getConsent(member[3]):
            runSurvey(member[3])
            numberSurveyed+=1
            idsSurveyed.append(member)
            break
print("Fin")