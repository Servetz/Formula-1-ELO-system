from multielo import MultiElo

#those are the parameters I chose to differently weight the results, feel free to play with them
#for reference look at the multielo github repository
race_mp = MultiElo(k_value=16, d_value=400)
race_1v1 = MultiElo(k_value=32, d_value=400)
qualy_mp = MultiElo(k_value=12, d_value=400)
qualy_1v1 = MultiElo(k_value=32, d_value=300)

#i get the elo for the drivers i'll watch in the current season
def getELO(lst, elo):
    elo = checkIfElo(lst, elo)
    teams = divideTeam(lst)
    if len(lst[0]) == 5:
        elo = qualyGroupElo(lst, elo)
        elo = qualyTeamElo(lst, elo, teams)
    elo = raceGroupElo(lst, elo)
    elo = raceTeamElo(lst, elo, teams)
    return elo

#if a driver has never raced his elo will be set to 1000 on his first race
def checkIfElo(lst, elo):
    for driver in lst:
        if not (driver[0] in elo):
            elo[driver[0]] = 1000
    return elo

def qualyGroupElo(lst, elo):
    drivers = []
    lst.sort(key = lambda row: row[2])
    for elem in lst:
        drivers.append(elo[elem[0]])
    drivers = qualy_mp.get_new_ratings(drivers)
    for i in range(len(lst)):
        elo[lst[i][0]] = drivers[i]
    return elo

def qualyTeamElo(lst, elo, teams):
    for team in teams:
        if type(teams[team]) == list and len(teams[team])>1:
            newlst = []
            drivers = []
            for elem in lst:
                if elem[0] in teams[team]:
                    newlst.append(elem)
            newlst.sort(key = lambda row: row[2])
            for elem in newlst:
                drivers.append(elo[elem[0]])
            drivers = qualy_1v1.get_new_ratings(drivers)
            for i in range(len(newlst)):
                elo[newlst[i][0]] = drivers[i]
    return elo

def raceGroupElo(lst, elo):
    drivers = []
    lst.sort(key = lambda row: row[3])
    for elem in lst:
        drivers.append(elo[elem[0]])
    drivers = race_mp.get_new_ratings(drivers)
    for i in range(len(lst)):
        elo[lst[i][0]] = drivers[i]
    return elo

def raceTeamElo(lst, elo, teams):
    for team in teams:
        if type(teams[team]) == list and len(teams[team])>1:
            newlst = []
            drivers = []
            for elem in lst:
                if elem[0] in teams[team]:
                    newlst.append(elem)
            newlst.sort(key = lambda row: row[3])
            for elem in newlst:
                drivers.append(elo[elem[0]])
            drivers = race_1v1.get_new_ratings(drivers)
            for i in range(len(newlst)):
                elo[newlst[i][0]] = drivers[i]
    return elo

#this function is needed to compare the drivers only between inside their team
def divideTeam(lst):
    teams = {}
    for elem in lst:
        if elem[1] in teams:
            teams[elem[1]].append(elem[0])
        else:
            teams[elem[1]] = []
            teams[elem[1]].append(elem[0])
    return teams