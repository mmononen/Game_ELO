# Calculates ELO ranking for games based on various curated top-lists.

import json, statistics

class Game:
    def __init__(self, name):
        self.name = name
        self.elo = 1000
        self.highest_elo = 1000
        self.wins = 0
        self.draws = 0
        self.loses = 0
        self.matches = 0
        self.k = 40
        self.lists = []
        self.id = 0
        self.year = 0
        self.country = []
        self.platforms = []
        self.developers = []
        self.publishers = []
        self.genre = []
        self.theme = []
        self.perspective = ""
        self.designer = []
        self.composer = []
        self.pegi = ""
        self.esrb = ""
        self.hltb = ""

    def add_matches(self):
        self.matches += 1
    
    def get_matches(self):
        return self.matches

    def add_win(self):
        self.wins += 1

    def add_draw(self):
        self.draws += 1

    def add_loss(self):
        self.loses += 1
    
    def set_elo(self, elo):
        self.elo = elo
    
    def get_elo(self):
        return self.elo

    def set_k(self, k):
        self.k = k
    
    def get_k(self):
        return self.k
    
    def get_highest_elo(self):
        return self.highest_elo
    
    def set_highest_elo(self):
        self.highest_elo = self.elo
    
    def add_list(self, album):
        self.lists.append(album)
    
    def get_lists(self):
        return self.lists
    
    def get_country(self):
        s = ""
        self.country.sort()
        for sg in self.country:
            s += sg + ", "
        return s[:len(s)-2]

    def get_platforms(self):
        s = ""
        self.platforms.sort()
        for sg in self.platforms:
            s += sg + ", "
        return s[:len(s)-2]

    def get_developers(self):
        s = ""
        self.developers.sort()
        for sg in self.developers:
            s += sg + ", "
        return s[:len(s)-2]

    def get_publishers(self):
        s = ""
        self.publishers.sort()
        for sg in self.publishers:
            s += sg + ", "
        return s[:len(s)-2]

    def get_genre(self):        
        s = ""
        self.genre.sort()
        for sg in self.genre:
            s += sg + ", "
        return s[:len(s)-2]

    def get_theme(self):
        s = ""
        self.theme.sort()
        for sg in self.theme:
            s += sg + ", "
        return s[:len(s)-2]

    def get_perspective(self):
        s = ""
        self.perspective.sort()
        for sg in self.perspective:
            s += sg + ", "
        return s[:len(s)-2]

    def get_designer(self):
        s = ""
        self.designer.sort()
        for sg in self.designer:
            s += sg + ", "
        return s[:len(s)-2]

    def get_composer(self):
        s = ""
        self.composer.sort()
        for sg in self.composer:
            s += sg + ", "
        return s[:len(s)-2]

class Person():
    def __init__(self, name):
        self.name = name
        self.elo = 1000
        self.highest_elo = 1000
        self.wins = 0
        self.draws = 0
        self.loses = 0
        self.matches = 0
        self.k = 40
        self.games = []

class Company():
    def __init__(self, name):
        self.name = name
        self.elo = 1000
        self.highest_elo = 1000
        self.wins = 0
        self.draws = 0
        self.loses = 0
        self.matches = 0
        self.k = 40
        self.games = []

class Developer(Company):
    def __init__(self, name):
        self.name = name
        self.elo = 1000
        self.highest_elo = 1000
        self.wins = 0
        self.draws = 0
        self.loses = 0
        self.matches = 0
        self.k = 40
        self.games = []

class Publisher(Company):
    def __init__(self, name):
        self.name = name
        self.elo = 1000
        self.highest_elo = 1000
        self.wins = 0
        self.draws = 0
        self.loses = 0
        self.matches = 0
        self.k = 40
        self.games = []

class Designer(Person):
    def __init__(self, name):
        self.name = name
        self.elo = 1000
        self.highest_elo = 1000
        self.wins = 0
        self.draws = 0
        self.loses = 0
        self.matches = 0
        self.k = 40
        self.games = []

class Composer(Person):
    def __init__(self, name):
        self.name = name
        self.elo = 1000
        self.highest_elo = 1000
        self.wins = 0
        self.draws = 0
        self.loses = 0
        self.matches = 0
        self.k = 40
        self.games = []


groups = []
groupnames = []
jsonlist = []
lists = ["data/1996-09-30 Next_Generation_1996_Top_100_Games_of_All_Time.txt",
         "data/1999-02-28 Next_Generation_1999_The_50_Best_Games_of_All_Time.txt",
         "data/2000-01-31 Edge Top 100 Games to Play Now.txt",
         "data/2001-07-31 GameSpy Top 50 Games of All Time.txt",
         "data/2001-08-31 Game_Informer_2001_Top_100_Games_Of_All_Time.txt",
         "data/2004-12-31 Retro_Gamer_2004_Reader's_Top_100_Games.txt",
         "data/2008-08-09 Pelaajalehti_2008_Kymmenen_kaikkien_aikojen_parasta_peliä.txt",
         "data/2009-02-27 Guinness_2009_top_50_games_of_all_time.txt",
         "data/2009-11-21 Game_Informer_2009_Top_200_Games_of_All_Time.txt",
         "data/2010-01-08 MuroBBS_2010_Maailman_Kaikkien_Aikojen_Paras_Peli.txt",
         "data/2011-12-31 PC_Gamer_2011_The_100_best_PC_games_of_all_time.txt",
         "data/2014-05-10 RPG_Codex_2014_Top_70_PC_RPGs.txt",
         "data/2014-06-09 Slant_2014_The_100_Greatest_Video_Games_of_All_Time.txt",
         "data/2014-12-31 Popular_Mechanics_2014_The_100_Greatest_Video_Games_of_All_Time.txt",
         "data/2015-02-25 GamesRadar_2015_The_100_best_games_ever.txt",
         "data/2015-06-12 Rock_Paper_Shotgun_2015_The_25_Best_Adventure_Games_Ever_Made.txt",
         "data/2015-12-31 Empire_2015_The_100_Greatest_Video_Games.txt",
         "data/2016-01-10 Retro Gamer 150 Greatest Games Ever.txt",
         "data/2016-08-23 Time_2016_The_50_Best_Video_Games_of_All_Time.txt",
         "data/2017-03-13 The_Wrap_2017_The_30_Best_Video_Games_of_All_Time.txt",
         "data/2017-08-30 Edge_Magazine_2017_The_100_Greatest_Videogames_2017_Edition.txt",
         "data/2017-09-01 WhatCulture_2017_30_Best_Video_Games_Of_All_Time.txt",
         "data/2017-10-06 Stuff_Best_Games_Ever_The_16_best_driving_games_of_all_time.txt",
         "data/2017-11-27 Polygon_2017_The_500_best_games_of_all_time.txt",
         "data/2017-12-27 Stuff_2017_Best_Games_Ever_The_25_best_Nintendo_games_of_all_time.txt",
         "data/2017-12-27 Stuff_2017_Best_Games_Ever_The_25_best_PlayStation_games_of_all_time.txt",
         "data/2017-12-27 Stuff_2017_Best_Games_Ever_The_25_best_Xbox_games_of_all_time.txt",
         "data/2017-12-27 Stuff_2017_Best_Games_Ever_The_50_greatest_games_of_all_time.txt",
         "data/2018-01-23 Comicbook_2018_10_Best_Video_Games_of_ALL_Time.txt",
         "data/2018-03-19 Game_Informer_2018_Reader's_Choice_Top_300_Games_Of_All_Time.txt",
         "data/2018-05-11 The_Indie_Game_Website_2018_The_100_Best_Indie_Games_of_All_Time.txt",
         "data/2018-06-08 Slant_2018_The_100_Greatest_Video_Games_of_All_Time.txt",
         "data/2018-08-07 VG247_2018_The_50_best_RPGs_EVER.txt",
         "data/2018-09-12 PC_Gamer_2018_The_PC_Gamer_Top_100.txt",
         "data/2018-10-30 Complex_2018_The_100_Best_Video_Games_of_the_2000s.txt",
         "data/2018-12-31 IGN_2018_Top_100_RPGs_of_All_Time.txt",
         "data/2018-12-31 IGN_2018_Top_100_Video_Games_of_All_Time.txt",
         "data/2018-12-31 Videogamer_2018_Top_PC_Games_of_All_Time.txt",
         "data/2019-03-21 The 100 Greatest Video Games of All Time (Popular Mechanics).txt",
         "data/2019-07-01 Hiconsumption_2019_The_100_Best_Video_Games_of_All_Time.txt",
         "data/2019-08-04 2019 RPG Codex Top RPGs.txt"
         "data/2019-09-19 Guardian The 50 best video games of the 21st century.txt",
         "data/2020-03-30 Esquire The 15 Best Video Games of All Time, Ranked.txt",
         "data/2020-04-13 Slant_2020_The_100_Best_Video_Games_of_All_Time.txt",
         "data/2020-09-07 The PC Gamer Top 100 (2020).txt",
         "data/2020-12-02 Gaming Bible The Greatest Games Of All Time.txt",
         "data/2021-06-10 Howchoo The 30 Best Video Games of All Time.txt",
         "data/2021-08-13 CRPG_Addict_2021_Top_100.txt",
         "data/2021-08-14 Shphhd_2021_top_100.txt"
        ]


def adjust_k(g):
    # adjust k according to number of matches played
    if (g.get_matches() >= 30 and g.get_elo() < 2400):
        g.set_k(20)
    elif (g.get_matches() >= 30 and (g.get_elo() or g.get_highest_elo() >= 2400)):
        g.set_k(10)



def calculate_elo(g1, g2, res):
    ra = g1.get_elo()
    rb = g2.get_elo()
    ea = 1 / (1 + 10**((rb-ra)/400))
    eb = 1 / (1 + 10**((ra-rb)/400))
    g1.add_matches()
    g2.add_matches()
    
    adjust_k(g1)
    adjust_k(g2)

    ka = g1.get_k()
    kb = g2.get_k()

    if res == 1:
        sa = 1
        sb = 0
        g1.add_win()
        g2.add_loss()
    elif res == 0.5:
        sa = 0.5
        sb = 0.5
        g1.add_draw()
        g2.add_draw()
    elif res == 0:
        sa = 0
        sb = 1
        g1.add_loss()
        g2.add_win()
        
    ra = (ra + ka * (sa -ea))
    rb = (rb + kb * (sb - eb))

    g1.set_elo(max(ra, g1.get_highest_elo()))
    g2.set_elo(max(rb, g2.get_highest_elo()))

    
def check_name(data, val):
    return any(g['name']==val for g in data['games'])

def check_year(data, val):
    return data['games'].index(val)['year']

def filter_year(olist, years):    
    a = len(max(groupnames, key=len)) + 4
    for g in groups:
        if g.matches > 0:
            s = ""
            if g.elo < 1000:
                s = "0"     
            
            s += f"{int(round(g.elo))}   {g.name:{a}} {(g.id):4} {len(g.lists):4}"
            if g.year in years:
                olist.append(s)
    return olist

def filter_platform(olist, platform):
    a = len(max(groupnames, key=len)) + 4
    for g in groups:
        if g.matches > 0:
            s = ""
            if g.elo < 1000:
                s = "0"      
            
            s += f"{int(round(g.elo))}   {g.name:{a}} {(g.id):4} {len(g.lists):4}"
            if platform in g.platforms:
                olist.append(s)
    return olist

def filter_country(olist, country):
    a = len(max(groupnames, key=len)) + 4
    for g in groups:
        if g.matches > 0:
            s = ""
            if g.elo < 1000:
                s = "0"      
            
            s += f"{int(round(g.elo))}   {g.name:{a}} {(g.id):4} {len(g.lists):4}"
            if country in g.country:
                olist.append(s)
    return olist

def make_printable(olist):
    a = len(max(groupnames, key=len)) + 4
    
    olist.sort(reverse=True)
    #print (olist)
    printable = []
    temps = "GAME"
    printable.append(f" RANK   ELO   {temps:{a}}   ID  LST")
    printable.append("-"*(a+26))
    i = 0
    j = 0
    tempelo = 0


    line_between_elos = False
    for o in olist:      
        # test if group's played matches are at least in threshold level   
        if  int((o[-4:])) >= 1: 
            # if no other group is at the same rank, print a rank number
            if tempelo != int((o[0:5])):
                i += j
                i += 1
                j = 0
                
                if (line_between_elos):
                    s = "- "*(58)
                    printable.append(f"{s}")
                printable.append(f"{i:5}. {o} ")
                line_between_elos = True

            # otherwise leave the rank blank, but increase the rank count
            else:
                j += 1
                printable.append(f"")
                printable.append(f"       {o}")        
            
            bname = o[7:len(max(groupnames, key=len)) + 7].strip()
            
            band = groups[groupnames.index(bname)]
            
            # There should be data for all the fields in gamedb.json if there is an entry for the game
            if (band.id) != 0:
                printable.append(f"                  {band.get_country()} | {band.hltb} h | {band.get_perspective()} | PEGI: {band.pegi} | ESRB: {band.esrb}")
                printable.append(f"                  On: {band.get_platforms()}")
                printable.append(f"                  Genre: {band.get_genre()} | Theme: {band.get_theme()}")
                
                printable.append(f"                  Developers: {band.get_developers()}")
                printable.append(f"                  Publishers: {band.get_publishers()}")

                printable.append(f"                  Designer: {band.get_designer()}")
                printable.append(f"                  Composer: {band.get_composer()}")

            tempelo = int((o[0:5]))
    if len(olist) < 1:
        printable = []
    return printable

with open('gamedb.json', 'r', encoding='utf-8') as f:
    gamedb = json.load(f)

unlisted = []
developers = []
dev_names = []
old_l = ""
for l in lists:
    list_groups = []
    
    list_pos = []
    tmp_yr = 0
    try:
        f = open(l, "r", encoding="utf-8")
        for x in f:
            x = x.strip()
            if x[0] != "#":
                try:                
                    list_pos.append(x)
                    x = x.split(". ", 1)

                    if x[1] not in groups:
                        groups.append(Game(x[1]))                    
                        groupnames.append(x[1])
                        g = groups[groupnames.index(x[1])]
                        if x[1] not in gamedb:
                            if old_l != l:
                                unlisted.append("")
                                unlisted.append(f"{l}")    
                                unlisted.append(f"--------------------------")
                                old_l = l
                            unlisted.append(f"{x[0]}. {x[1]}")
                        else:
                            g.id = gamedb[x[1]]['id']
                            g.year = gamedb[x[1]]['year']
                            g.country = gamedb[x[1]]['country']
                            g.platforms = gamedb[x[1]]['platforms']
                            g.developers = gamedb[x[1]]['developers']
                            g.publishers = gamedb[x[1]]['publishers']
                            g.genre = gamedb[x[1]]['genre']
                            g.theme = gamedb[x[1]]['theme']
                            g.perspective = gamedb[x[1]]['perspective']
                            g.designer = gamedb[x[1]]['designer']
                            g.composer = gamedb[x[1]]['composer']
                            g.pegi = gamedb[x[1]]['pegi']
                            g.esrb = gamedb[x[1]]['esrb']
                            g.hltb = gamedb[x[1]]['hltb']

                            for d in g.developers:
                                if d not in dev_names:
                                    dev_names.append(d)
                                    developers.append(Developer(d))
                        g.add_list(l)                    
                    if x[1] not in list_groups:
                        list_groups.append(x[1])
                except Exception as e:                    
                    print(e)
        old_l = l
        f.close()
        print(f"processing: {l}")
    except Exception as e:        
        print(f"{e}: {l} is missing!")
   
    list_groups.reverse()
    tmp = [(a, b) for idx, a in enumerate(list_pos) for b in list_pos[idx + 1:]]
    for itm in tmp:
        i0 = itm[0].split(". ", 1)
        i1 = itm[1].split(". ", 1)
        wdl = 0
        ret1 = i0[0]
        ret2 = i1[0]
        if ret1 < ret2:
            itm = (i1[1], i0[1])
        else:
            itm = (i0[1], i1[1])
        if ret1 == ret2:
            wdl = 0.5
        elif ret1 > ret2:
            wdl = 1
        elif ret1 < ret2:
            wdl = 0
        
        if i0[1] != i1[1]:
            try:
                calculate_elo(groups[groupnames.index(itm[0])],groups[groupnames.index(itm[1])],wdl)
            except Exception as e:                
                print(e)

    
    for g in groups:
        if g.get_elo() > g.get_highest_elo():
            g.set_highest_elo()

printable = []


for i in range(1900, 2100, 1):
    olist = []    
    printable = make_printable(filter_year(olist, [*range(i,i+1,1)]))
    if len(printable) > 0:
        n = f"output/year/{i}.txt"
        with open(n, 'w', encoding='utf-8') as f_out:
            for p in printable:
                f_out.write(p+"\n")

platforms = []
for g in groups:
    for p in g.platforms:
        if p not in platforms:
            platforms.append(p)

for p in platforms:
    olist = []
    printable = make_printable(filter_platform(olist, p))
    if len(printable) > 0:
        n = f"output/platform/{p}.txt"
        with open(n, 'w', encoding='utf-8') as f_out:
            for p in printable:                
                f_out.write(p+"\n")

countries = []
for g in groups:
    for p in g.country:
        if p not in countries:
            countries.append(p)

for c in countries:
    olist = []
    printable = make_printable(filter_country(olist, c))
    if len(printable) > 0:
        n = f"output/country/{c}.txt"
        with open(n, 'w', encoding='utf-8') as f_out:
            for p in printable:                
                f_out.write(p+"\n")

printable = []
olist = []
printable = make_printable(filter_year(olist, [*range(1900,2100,1)]))
with open('all.txt', 'w', encoding='utf-8') as f_out:
    for p in printable:
        #print(p)
        f_out.write(p+"\n")

gamedb = sorted(gamedb)
with open('gamedb_list.txt', 'w', encoding='utf-8') as f_out:
    for g in gamedb:
        f_out.write(g+"\n")


with open('missing.txt', 'w', encoding='utf-8') as f_out:
    for l in unlisted:
        #print(l)
        f_out.write(l+"\n")
i = 0
countries = {}
platforms = {}
years = {}
genres = {}
themes = {}
developers = {}
publishers = {}
perspectives = {}
designers = {}
composers = {}
pegi = {}
esrb = {}
total_hltb = []

for g in gamedb:
    try:
        s = groups[groupnames.index(g)]
        total_hltb.append(s.hltb)
    except Exception as e:
        print(f"{e}: {g} not in lists!")
        break
    for x in s.country:
        if x not in countries:
            countries[x] = 1
        else:            
            a = countries[x]
            a = a + 1
            countries[x] = a
    for x in s.platforms:
        if x not in platforms:
            platforms[x] = 1
        else:            
            a = platforms[x]
            a = a + 1
            platforms[x] = a
    if s.year not in years:
        years[s.year] = 1
    else:
        a = years[s.year]
        a = a + 1
        years[s.year] = a
    if s.pegi not in pegi:
        pegi[s.pegi] = 1
    else:
        a = pegi[s.pegi]
        a = a + 1
        pegi[s.pegi] = a
    if s.esrb not in esrb:
        esrb[s.esrb] = 1
    else:
        a = esrb[s.esrb]
        a = a + 1
        esrb[s.esrb] = a            
    for x in s.genre:
        if x not in genres:
            genres[x] = 1
        else:            
            a = genres[x]
            a = a + 1
            genres[x] = a
    for x in s.theme:
        if x not in themes:
            themes[x] = 1
        else:            
            a = themes[x]
            a = a + 1
            themes[x] = a
    for x in s.developers:
        if x not in developers:
            developers[x] = 1
        else:            
            a = developers[x]
            a = a + 1
            developers[x] = a
    for x in s.publishers:
        if x not in publishers:
            publishers[x] = 1
        else:            
            a = publishers[x]
            a = a + 1
            publishers[x] = a
    for x in s.perspective:
        if x not in perspectives:
            perspectives[x] = 1
        else:            
            a = perspectives[x]
            a = a + 1
            perspectives[x] = a
    for x in s.designer:
        if x != "Unknown":
            if x not in designers:
                designers[x] = 1
            else:            
                a = designers[x]
                a = a + 1
                designers[x] = a
    for x in s.composer:
        if x != "Unknown":
            if x not in composers:
                composers[x] = 1
            else:            
                a = composers[x]
                a = a + 1
                composers[x] = a


print_countries = []
for i in countries:
    a = countries[i]
    b = int(a / len(gamedb) * 100)
    if a < 10:
        a = f"000{a}"
    elif a < 100:
        a = f"00{a}"
    elif a < 1000:
        a = f"0{a}"
    s = f"{a}: {i}  ({b}%)"
    print_countries.append(s)


print_platforms = []
for i in platforms:
    a = platforms[i]
    b = int(a / len(gamedb) * 100)
    if a < 10:
        a = f"000{a}"
    elif a < 100:
        a = f"00{a}"
    elif a < 1000:
        a = f"0{a}"
    s = f"{a}: {i}  ({b}%)"
    print_platforms.append(s)

print_years = []
for i in years:
    a = years[i]
    b = int(a / len(gamedb) * 100)
    if a < 10:
        a = f"000{a}"
    elif a < 100:
        a = f"00{a}"
    elif a < 1000:
        a = f"0{a}"
    s = f"{a}: {i}  ({b}%)"
    print_years.append(s)

print_pegi = []
for i in pegi:
    a = pegi[i]
    b = int(a / len(gamedb) * 100)
    if a < 10:
        a = f"000{a}"
    elif a < 100:
        a = f"00{a}"
    elif a < 1000:
        a = f"0{a}"
    s = f"{a}: {i}  ({b}%)"
    print_pegi.append(s)

print_esrb = []
for i in esrb:
    a = esrb[i]
    b = int(a / len(gamedb) * 100)
    if a < 10:
        a = f"000{a}"
    elif a < 100:
        a = f"00{a}"
    elif a < 1000:
        a = f"0{a}"
    s = f"{a}: {i}  ({b}%)"
    print_esrb.append(s)

print_genres = []
for i in genres:
    a = genres[i]
    b = int(a / len(gamedb) * 100)
    if a < 10:
        a = f"000{a}"
    elif a < 100:
        a = f"00{a}"
    elif a < 1000:
        a = f"0{a}"
    s = f"{a}: {i}  ({b}%)"
    print_genres.append(s)

print_themes = []
for i in themes:
    a = themes[i]
    b = int(a / len(gamedb) * 100)
    if a < 10:
        a = f"000{a}"
    elif a < 100:
        a = f"00{a}"
    elif a < 1000:
        a = f"0{a}"
    s = f"{a}: {i}  ({b}%)"
    print_themes.append(s)

print_developers = []
for i in developers:
    a = developers[i]
    b = int(a / len(gamedb) * 100)
    if a < 10:
        a = f"000{a}"
    elif a < 100:
        a = f"00{a}"
    elif a < 1000:
        a = f"0{a}"
    s = f"{a}: {i}  ({b}%)"
    print_developers.append(s)

print_publishers = []
for i in publishers:
    a = publishers[i]
    b = int(a / len(gamedb) * 100)
    if a < 10:
        a = f"000{a}"
    elif a < 100:
        a = f"00{a}"
    elif a < 1000:
        a = f"0{a}"
    s = f"{a}: {i}  ({b}%)"
    print_publishers.append(s)

print_perspectives = []
for i in perspectives:
    a = perspectives[i]
    b = int(a / len(gamedb) * 100)
    if a < 10:
        a = f"000{a}"
    elif a < 100:
        a = f"00{a}"
    elif a < 1000:
        a = f"0{a}"
    s = f"{a}: {i}  ({b}%)"
    print_perspectives.append(s)

print_designers = []
for i in designers:
    a = designers[i]
    b = int(a / len(gamedb) * 100)
    if a < 10:
        a = f"000{a}"
    elif a < 100:
        a = f"00{a}"
    elif a < 1000:
        a = f"0{a}"
    s = f"{a}: {i}  ({b}%)"
    print_designers.append(s)

print_composers = []
for i in composers:
    a = composers[i]
    b = int(a / len(gamedb) * 100)
    if a < 10:
        a = f"000{a}"
    elif a < 100:
        a = f"00{a}"
    elif a < 1000:
        a = f"0{a}"
    s = f"{a}: {i}  ({b}%)"
    print_composers.append(s)

with open('statistics.txt', 'w', encoding='utf-8') as f_out:
    f_out.write(f"Games in database: {len(gamedb)}\n")
    f_out.write(f"Total: {sum(total_hltb)} h | Average: {int(sum(total_hltb) / len(gamedb))} h | Median: {int(statistics.median(total_hltb))} h\n")
    #f_out.write(f"Average hours per game: {int(sum(total_hltb) / len(gamedb))} h\n")
    f_out.write("\n")
    topics = ["Countries (Top 10):",
              "Platforms (Top 10):"
             ]
    
    f_out.write(f"{topics[0]}\n")
    f_out.write("-"*len(topics[0])+"\n")
    print_countries.sort(reverse=True)
    k = 0
    k2 = 0
    temp = 0
    for i in print_countries:
        i = i.split(": ")
        j = i[1].split(" (")
        if temp != int(i[0]):
            k += k2
            k2 = 0
            k += 1
            s = f"{k:3}."     
        else:
            k2 += 1
            s = f"  = "
        temp = int(i[0])
        if k <= 10:
            f_out.write(f"{s} {j[0]:22}: {int(i[0]):3} ({j[1]:3}\n")
        else:
            break
    f_out.write(f"\n")
    f_out.write(f"{topics[1]}\n")
    f_out.write("-"*len(topics[1])+"\n")
    print_platforms.sort(reverse=True)
    k = 0
    k2 = 0
    temp = 0
    for i in print_platforms:
        i = i.split(": ")
        j = i[1].split(" (")
        if temp != int(i[0]):
            k += k2
            k2 = 0
            k += 1
            s = f"{k:3}."     
        else:
            k2 += 1
            s = f"  = "
        temp = int(i[0])
        if k <= 10:
            f_out.write(f"{s} {j[0]:22}: {int(i[0]):3} ({j[1]:3}\n")
        else:    
            break
    f_out.write("\n")
    f_out.write("Years (Top 10):\n")
    f_out.write("---------------\n")
    print_years.sort(reverse=True)
    k = 0
    k2 = 0
    temp = 0
    for i in print_years:
        i = i.split(": ")
        j = i[1].split(" (")
        if temp != int(i[0]):
            k += k2
            k2 = 0
            k += 1
            s = f"{k:3}."     
        else:
            k2 += 1
            s = f"  = "
        temp = int(i[0])
        if k <= 10:
            f_out.write(f"{s} {j[0]:22}: {int(i[0]):3} ({j[1]:3}\n")
        else:    
            break
    f_out.write("\n")
    f_out.write("PEGI Ratings:\n")
    f_out.write("-------------\n")
    print_pegi.sort(reverse=True)
    k = 0
    k2 = 0
    temp = 0
    for i in print_pegi:
        i = i.split(": ")
        j = i[1].split(" (")
        if temp != int(i[0]):
            k += k2
            k2 = 0
            k += 1
            s = f"{k:3}."     
        else:
            k2 += 1
            s = f"  = "
        temp = int(i[0])
        if k <= 10:
            f_out.write(f"{s} {j[0]:22}: {int(i[0]):3} ({j[1]:3}\n")
        else:    
            break    
    f_out.write("\n")
    f_out.write("ESRB Ratings:\n")
    f_out.write("-------------\n")
    print_esrb.sort(reverse=True)
    k = 0
    k2 = 0
    temp = 0
    for i in print_esrb:
        i = i.split(": ")
        j = i[1].split(" (")
        if temp != int(i[0]):
            k += k2
            k2 = 0
            k += 1
            s = f"{k:3}."     
        else:
            k2 += 1
            s = f"  = "
        temp = int(i[0])
        if k <= 10:
            f_out.write(f"{s} {j[0]:22}: {int(i[0]):3} ({j[1]:3}\n")
        else:    
            break
    f_out.write("\n")
    f_out.write("Genres (Top 10):\n")
    f_out.write("-------------------\n")
    print_genres.sort(reverse=True)
    k = 0
    k2 = 0
    temp = 0
    for i in print_genres:
        i = i.split(": ")
        j = i[1].split(" (")
        if temp != int(i[0]):
            k += k2
            k2 = 0
            k += 1
            s = f"{k:3}."     
        else:
            k2 += 1
            s = f"  = "
        temp = int(i[0])
        if k <= 10:
            f_out.write(f"{s} {j[0]:22}: {int(i[0]):3} ({j[1]:3}\n")
        else:   
            break
            f_out.write("\n")
    f_out.write("\n")
    f_out.write("Themes (Top 10):\n")
    f_out.write("-------------------\n")
    print_themes.sort(reverse=True)
    k = 0
    k2 = 0
    temp = 0
    for i in print_themes:
        i = i.split(": ")
        j = i[1].split(" (")
        if temp != int(i[0]):
            k += k2
            k2 = 0
            k += 1
            s = f"{k:3}."     
        else:
            k2 += 1
            s = f"  = "
        temp = int(i[0])
        if k <= 10:
            f_out.write(f"{s} {j[0]:22}: {int(i[0]):3} ({j[1]:3}\n")
        else:    
            break
    f_out.write("\n")
    f_out.write("Developers (Top 10):\n")
    f_out.write("--------------------\n")
    print_developers.sort(reverse=True)
    k = 0
    k2 = 0
    temp = 0
    for i in print_developers:
        i = i.split(": ")
        j = i[1].split(" (")
        if temp != int(i[0]):
            k += k2
            k2 = 0
            k += 1
            s = f"{k:3}."     
        else:
            k2 += 1
            s = f"  = "
        temp = int(i[0])
        if k <= 10:
            f_out.write(f"{s} {j[0]:22}: {int(i[0]):3} ({j[1]:3}\n")
        else:    
            break
    f_out.write("\n")
    f_out.write("Publishers (Top 10):\n")
    f_out.write("-------------------\n")
    print_publishers.sort(reverse=True)
    k = 0
    k2 = 0
    temp = 0
    for i in print_publishers:
        i = i.split(": ")
        j = i[1].split(" (")
        if temp != int(i[0]):
            k += k2
            k2 = 0
            k += 1
            s = f"{k:3}."     
        else:
            k2 += 1
            s = f"  = "
        temp = int(i[0])
        if k <= 10:
            f_out.write(f"{s} {j[0]:22}: {int(i[0]):3} ({j[1]:3}\n")
        else:    
            break
    f_out.write("\n")
    f_out.write("Perspectives:\n")
    f_out.write("-------------\n")
    print_perspectives.sort(reverse=True)
    k = 0
    k2 = 0
    temp = 0
    for i in print_perspectives:
        i = i.split(": ")
        j = i[1].split(" (")
        if temp != int(i[0]):
            k += k2
            k2 = 0
            k += 1
            s = f"{k:3}."     
        else:
            k2 += 1
            s = f"  = "
        temp = int(i[0])
        if k <= 10:
            f_out.write(f"{s} {j[0]:22}: {int(i[0]):3} ({j[1]:3}\n")
        else:    
            break
    f_out.write("\n")
    f_out.write("Designers (Top 10):\n")
    f_out.write("-------------------\n")
    print_designers.sort(reverse=True)
    k = 0
    k2 = 0
    temp = 0
    for i in print_designers:
        i = i.split(": ")
        j = i[1].split(" (")
        if temp != int(i[0]):
            k += k2
            k2 = 0
            k += 1
            s = f"{k:3}."     
        else:
            k2 += 1
            s = f"  = "
        temp = int(i[0])
        if k <= 10:
            f_out.write(f"{s} {j[0]:22}: {int(i[0]):3} ({j[1]:3}\n")
        else:    
            break
    f_out.write("\n")
    f_out.write("Composers (Top 10):\n")
    f_out.write("-------------------\n")
    print_composers.sort(reverse=True)
    k = 0
    k2 = 0
    temp = 0
    for i in print_composers:
        i = i.split(": ")
        j = i[1].split(" (")
        if temp != int(i[0]):
            k += k2
            k2 = 0
            k += 1
            s = f"{k:3}."     
        else:
            k2 += 1
            s = f"  = "
        temp = int(i[0])
        if k <= 10:
            f_out.write(f"{s} {j[0]:22}: {int(i[0]):3} ({j[1]:3}\n")
        else:    
            break