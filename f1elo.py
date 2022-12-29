import pandas as pd
import datetime
import elo
import sys

currentDate = datetime.date.today()
year = currentDate.year

driver_standings_df = pd.read_csv('archive/driver_standings.csv', usecols=['raceId', 'driverId', 'position'])
driver_standings = [list(row) for row in driver_standings_df.values]
driver_standings = sorted(driver_standings)

races_df = pd.read_csv('archive/races.csv', usecols=['raceId', 'year'])
races = [list(row) for row in races_df.values]
races.sort(key = lambda row: row[1])

drivers_df = pd.read_csv('archive/drivers.csv', usecols=['driverId', 'forename', 'surname'])
drivers = [list(row) for row in drivers_df.values]

qualifying_df = pd.read_csv('archive/qualifying.csv', usecols=['raceId','driverId','constructorId','position'])
qualifying = [list(row) for row in qualifying_df.values]

racing_df = pd.read_csv('archive/results.csv', usecols=['raceId','driverId','constructorId','position'])
racing = [list(row) for row in racing_df.values]

ELO = {}

def getDrivers(year):
    final_table = []
    for ds in driver_standings:
        if ds[0] in getRaces(year):
            for d in drivers:
                if d[0] == ds[1]:
                    ds.insert(2, d[1])
                    ds.insert(3, d[2])
            final_table.append(ds)
    return final_table

def loadSeasonRaces(year):
    final_table = getDrivers(year)
    for i in range(len(final_table)):
        for r in racing:
            if r[0] == final_table[i][0] and r[1] == final_table[i][1]:
                final_table[i].insert(-1, r[2])
                if r[3] == '\\N':
                    final_table[i].insert(-1, 999) 
                else:
                    final_table[i].insert(-1, int(r[3]))
    return final_table

def loadSeasonQualy(year):
    final_table = loadSeasonRaces(year)
    for i in range(len(final_table)):  
        for q in qualifying:
            if len(final_table[i])==7:
                if q[0] == final_table[i][0] and q[1] == final_table[i][1]  and q[2] == final_table[i][4]:
                    final_table[i].insert(-1, q[3])
    return final_table

def getRaces(year):
    raceIds = set()
    for race in races:
        if race[1] == year:
            raceIds.add(race[0])
    return raceIds

def getYear(year):
    print('retrieving %i season informations...' % year)
    season = []
    raceIds = getRaces(year)
    final_table = loadSeasonQualy(year)
    for elem in final_table:
        if elem[0] in raceIds:
            season.append(elem)
    return season

# def finalStandings(year):
#     fullseason = getYear(year)
#     lastrace = fullseason[len(fullseason)-1][0]
#     finalstandings = []
#     for elem in fullseason:
#         if elem[0] == lastrace:
#             finalstandings.append([elem[len(elem)-1], elem[2] + ' ' + elem[3]])
#     finalstandings.sort(key = lambda row: row[0])
#     return finalstandings

def calculate(start, finish, today):
    if start < 1950 or finish < start:
        print('Season selection is invalid')
        return 0
    if finish > today:
        finish = today
    print('------------------------------------')
    print(f'SEASONS {start} - {finish}')
    print('------------------------------------')
    if start != 1950:
        print('ELO of all drivers will be set to 1000 starting from %i season\nPrevious seasons won\'t be taken in account' %start)
    for i in range(start, finish+1, 1):
        season = getYear(i)
        raceIds = getRaces(i)
        for id in raceIds:
            lista = []
            for result in season:
                if result[0] == id:
                    if len(result) == 8:
                        lista.append([result[1], result[4], result[6], result[5], result[7]])
                    elif len(result) == 7:
                        lista.append([result[1], result[4], result[5], result[6]])
            ELO.update(elo.getELO(lista, ELO))
        print('season\'s drivers ELO updated')

def main():
    standings = []
    calculate(int(sys.argv[1]), int(sys.argv[2]), year)
    for driver in drivers:
        if driver[0] in ELO:
            standings.append([str(driver[1] + ' ' + driver[2]), ELO[driver[0]]])
    standings.sort(key = lambda row: row[1], reverse=True)
    with open(f'standings/{sys.argv[3]}.csv', 'w') as file:
        file.write('RANK;ELO;DRIVER\n')
        print('POS\tELO\t\tDRIVER')
        for i in range(len(standings)):
            print(f'{i+1}\t{round(standings[i][1],2)}\t\t{standings[i][0]}')
            file.write(f'{i+1};{round(standings[i][1],2)};{standings[i][0]}\n')

main()