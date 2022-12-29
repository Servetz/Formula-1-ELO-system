from multielo import MultiElo

race_mp = MultiElo(k_value=16, d_value=400)
race_1v1 = MultiElo(k_value=32, d_value=400)
qualy_mp = MultiElo(k_value=12, d_value=400)
qualy_1v1 = MultiElo(k_value=32, d_value=300)

def getELO(lista, elo):
    elo = checkIfElo(lista, elo)
    teams = divideTeam(lista)
    if len(lista[0]) == 5:
        elo = qualyGroupElo(lista, elo)
        elo = qualyTeamElo(lista, elo, teams)
    elo = raceGroupElo(lista, elo)
    elo = raceTeamElo(lista, elo, teams)
    return elo

def checkIfElo(lista, elo):
    for driver in lista:
        if not (driver[0] in elo):
            elo[driver[0]] = 1000
    return elo

def qualyGroupElo(lista, elo):
    drivers = []
    lista.sort(key = lambda row: row[2])
    for elem in lista:
        drivers.append(elo[elem[0]])
    drivers = qualy_mp.get_new_ratings(drivers)
    for i in range(len(lista)):
        elo[lista[i][0]] = drivers[i]
    return elo

def qualyTeamElo(lista, elo, teams):
    for team in teams:
        if type(teams[team]) == list and len(teams[team])>1:
            newlista = []
            drivers = []
            for elem in lista:
                if elem[0] in teams[team]:
                    newlista.append(elem)
            newlista.sort(key = lambda row: row[2])
            for elem in newlista:
                drivers.append(elo[elem[0]])
            drivers = qualy_1v1.get_new_ratings(drivers)
            for i in range(len(newlista)):
                elo[newlista[i][0]] = drivers[i]
    return elo

def raceGroupElo(lista, elo):
    drivers = []
    lista.sort(key = lambda row: row[3])
    for elem in lista:
        drivers.append(elo[elem[0]])
    drivers = race_mp.get_new_ratings(drivers)
    for i in range(len(lista)):
        elo[lista[i][0]] = drivers[i]
    return elo

def raceTeamElo(lista, elo, teams):
    for team in teams:
        if type(teams[team]) == list and len(teams[team])>1:
            newlista = []
            drivers = []
            for elem in lista:
                if elem[0] in teams[team]:
                    newlista.append(elem)
            newlista.sort(key = lambda row: row[3])
            for elem in newlista:
                drivers.append(elo[elem[0]])
            drivers = race_1v1.get_new_ratings(drivers)
            for i in range(len(newlista)):
                elo[newlista[i][0]] = drivers[i]
    return elo


def divideTeam(lista):
    teams = {}
    for elem in lista:
        if elem[1] in teams:
            teams[elem[1]].append(elem[0])
        else:
            teams[elem[1]] = []
            teams[elem[1]].append(elem[0])
    return teams