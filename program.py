import pandas as pd 
import os
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
datadir="data"

def findgame(shotsdf):
    while True:
        hometeam = input("insert the home team name: (ex: LAL) \n")
        if hometeam in shotsdf['HOME_TEAM'].values:
            break
        else:
            print ("team not found or wrong format, please retry ")

    while True:
        awayteam = input("Insert the away team name: (ex: GSW) \n")
        if awayteam in shotsdf['HOME_TEAM'].values:
            break
        else:
            print ("team not found or wrong format, please retry ")
    
    while True:
        userinput = input("insert the season (ex: if you want 2005-06, type in 2006) \n")
        try:
            season = int(userinput)
            if season in shotsdf['SEASON_1'].values:
                break  
            else:
                print(f"season {season} is not valid (go from 2005 to 2025) \n")
        except ValueError:
            print("this value has to be a number(ex 2006), not text, retry \n")
    
    possiblegames = (
        shotsdf[
            (shotsdf['SEASON_1'] == season) &
            (shotsdf['HOME_TEAM'] == hometeam) &
            (shotsdf['AWAY_TEAM'] == awayteam)
        ][['GAME_ID', 'GAME_DATE']]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    if possiblegames.empty:
        print("No games exist with those parameters, retry")
        return None

    if len(possiblegames) == 1:
        print("Game found!")
        return possiblegames.loc[0, 'GAME_ID']

    print("\nThese are the available games:\n")
    for i, row in possiblegames.iterrows():
        print(f"[{i}] Date: {row['GAME_DATE']}")

    while True:
        choice = int(input(" insert the number of the game you want to select \n"))
        if 0 <= choice < len(possiblegames):
            return possiblegames.loc[choice, 'GAME_ID']
        else:
            print("invalid choice or wrong format, please retry")
        
def findplayer(shotsdf):
    while True:
        name = input("insert the name and surname of the player you are looking for (for example: Lebron James) \n")
        if name in shotsdf['PLAYER_NAME'].values:
            break
        else:
            print ("player not found or wrong format, please retry ")
    
    id = (shotsdf.loc[shotsdf['PLAYER_NAME'] == name, 'PLAYER_ID'].iloc[0])
    return id

def playersfrommatch(gameid, shotsdf):
    game = shotsdf[shotsdf['GAME_ID'] == gameid] 
    players=game['PLAYER_NAME'].unique()
    return players

def find3ptshots(shotsdf):
    while True:
        userinput = input("insert the season you want to see (ex: if you want 2005-06, type in 2006) \n")
        try:
            season = int(userinput)
            if season in shotsdf['SEASON_1'].values:
                break  
            else:
                print(f"season {season} is not valid (go from 2005 to 2025) \n")
        except ValueError:
            print("this value has to be a number(ex 2006), not text, retry \n")
    
    while True:
        player = findplayer(shotsdf)
        seasonshots = shotsdf[
        (shotsdf['SEASON_1'] == season) &
        (shotsdf['PLAYER_ID'] == player) &
        (shotsdf['SHOT_TYPE'] == "3PT Field Goal")
        ]
        if seasonshots.empty:
            print ("that player has never played in that season, retry \n")
        else:
            return seasonshots

def findplayershots(id, shotsdf):

    players=playersfrommatch(id, shotsdf)
    print(f"the available players in that game are: {players}")
    
    playerid = findplayer(shotsdf)

    game = shotsdf[
        (shotsdf['GAME_ID'] == id) &
        (shotsdf['PLAYER_ID'] == playerid)
        ]
    
    if game.empty:
        print("no game was found with this id where that player has played, retry please")
        return 0
    else:
        return game

def viewshots(gameid, df, gmpl):
    
    nbateams = {
        'ATL': 'Atlanta Hawks',
        'BOS': 'Boston Celtics',
        'BKN': 'Brooklyn Nets',
        'CHA': 'Charlotte Hornets',
        'CHI': 'Chicago Bulls',
        'CLE': 'Cleveland Cavaliers',
        'DAL': 'Dallas Mavericks',
        'DEN': 'Denver Nuggets',
        'DET': 'Detroit Pistons',
        'GSW': 'Golden State Warriors',
        'HOU': 'Houston Rockets',
        'IND': 'Indiana Pacers',
        'LAC': 'Los Angeles Clippers',     
        'LAL': 'Los Angeles Lakers',
        'MEM': 'Memphis Grizzlies',
        'MIA': 'Miami Heat',
        'MIL': 'Milwaukee Bucks',
        'MIN': 'Minnesota Timberwolves',
        'NOP': 'New Orleans Pelicans',
        'NYK': 'New York Knicks',
        'OKC': 'Oklahoma City Thunder',
        'ORL': 'Orlando Magic',
        'PHI': 'Philadelphia 76ers',
        'PHX': 'Phoenix Suns',
        'POR': 'Portland Trail Blazers',
        'SAC': 'Sacramento Kings',
        'SAS': 'San Antonio Spurs',
        'TOR': 'Toronto Raptors',
        'UTA': 'Utah Jazz',
        'WAS': 'Washington Wizards',
        'NJN': 'New Jersey Nets',
        'SEA': 'Seattle SuperSonics',
        'NOH': 'New Orleans Hornets',
        'NOK': 'New Orleans/Oklahoma City Hornets',
    }

    if gameid != 0 and gmpl==False:
        shots = df[df['GAME_ID'] == gameid]
        graphtype="game"
    elif gameid != 0 and gmpl==True:
        shots = df[df['GAME_ID'] == gameid]
        graphtype="playershots"
    else:
        shots=df
        graphtype="season"

    # Crea la figura
    fig, ax = plt.subplots(figsize=(12, 11))
    draw_court(ax, outer_lines=True)
    fattore_conversione = 1
    offset=47.5
    team_home = shots['HOME_TEAM'].iloc[0]
    team_away = shots['AWAY_TEAM'].iloc[0]
    made_shots = shots[shots['SHOT_MADE'] == True]
    missed_shots = shots[shots['SHOT_MADE'] == False]
    team_season = shots['SEASON_2'].iloc[0]
    player= shots['PLAYER_NAME'].iloc[0]

    if team_season in ['2019-20', '2020-21']: 
            fattore_conversione = 3.28
            offset=52.5
    
    if graphtype=="game":
        completehome=nbateams.get(team_home, "not found")
        completeaway=nbateams.get(team_away, "not found")

        homemade_shots = shots[(shots['SHOT_MADE'] == True) & (shots['TEAM_NAME']==completehome)]
        homemissed_shots = shots[(shots['SHOT_MADE'] == False) & (shots['TEAM_NAME']==completehome)]
        awaymade_shots = shots[(shots['SHOT_MADE'] == True) & (shots['TEAM_NAME']==completeaway)]
        awaymissed_shots = shots[(shots['SHOT_MADE'] == False) & (shots['TEAM_NAME']==completeaway)]
        
        ax.scatter(homemade_shots['LOC_X'] * -10 *fattore_conversione, homemade_shots['LOC_Y'] * 10*fattore_conversione - offset, 
                color='green', label='Home team Made', s=30)
        ax.scatter(homemissed_shots['LOC_X'] * -10 *fattore_conversione, homemissed_shots['LOC_Y'] * 10*fattore_conversione - offset, 
                color='purple', label='Home team Missed', marker='x', s=30)
        ax.scatter(awaymade_shots['LOC_X'] * -10 *fattore_conversione, awaymade_shots['LOC_Y'] * 10*fattore_conversione - offset, 
                color='blue', label='Away team Made', s=30)
        ax.scatter(awaymissed_shots['LOC_X'] * -10 *fattore_conversione, awaymissed_shots['LOC_Y'] * 10*fattore_conversione - offset, 
                color='orange', label='Away team Missed', marker='x', s=30)
    else:
        ax.scatter(made_shots['LOC_X'] * -10 *fattore_conversione, made_shots['LOC_Y'] * 10*fattore_conversione - offset, 
                color='green', label='Made', alpha=0.7, s=30, edgecolors='white', linewidth=0.5)
        ax.scatter(missed_shots['LOC_X'] * -10 *fattore_conversione, missed_shots['LOC_Y'] * 10*fattore_conversione - offset, 
                color='red', label='Missed', alpha=0.6, marker='x', s=30)

    if graphtype=="game":
        ax.set_title(f"shots in game: {completehome}({team_home}) vs {completeaway}({team_away}) ({team_season})")
    elif graphtype=="season":
        ax.set_title(f"{player}'s 3pt shots from the {team_season} season")
    elif graphtype=="playershots": 
        ax.set_title(f"{player}'s shots from the {team_home} vs {team_away} ({team_season}) game")
    
    # Posiziona la legenda in modo che non copra il campo
    ax.legend(loc='upper right')
    # Mostra il grafico
    plt.show()

def draw_court(ax=None, color='black', lw=2, outer_lines=False, interval=20):
    if ax is None:
        ax = plt.gca()

    # Create the basketball hoop
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                    bottom_free_throw, restricted, corner_three_a,
                    corner_three_b, three_arc, center_outer_arc,
                    center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,color=color, fill=False)
        court_elements.append(outer_lines)

    for element in court_elements:
        ax.add_patch(element)

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 422.5)

    return ax

def main():
    gameid=0
    shots=pd.read_csv(os.path.join("data","shots_all_seasons.csv"), low_memory=False)
    cond=True
    while cond:
        choice=input("Choose an option to continue: \n " \
        "1 to view every shot made/missed in a said game \n " \
        "2 to view every shot of a said player in a said game \n " \
        "3 to view all 3 point shots of a said player in a said season \n " \
        "4 to view all "
        "exit to quit \n ")
        match(choice):
            case "1":
                gameplayer=False
                gameid=findgame(shots)
                if gameid:
                    viewshots(gameid, shots, gameplayer)
            case "2":
                gameplayer=True
                if input("do you want to use the last gameid that was found? yes or no \n") == "yes":
                    print(f"using game id: {gameid}")
                    if gameid==0:
                        print("there was no previous research for a game")
                    else:
                        playershots=findplayershots(gameid, shots)
                        viewshots(gameid, playershots, gameplayer)
                else:
                    gameid=findgame(shots)
                    playershots=findplayershots(gameid, shots)
                    viewshots(gameid, playershots, gameplayer)
            case "3":
                seasonalshots=find3ptshots(shots)
                viewshots(0, seasonalshots, 2)
            case "Change option":
                print(findplayer(shots))
                continue
            case "exit":
                cond=False

if __name__=="__main__":
    main()
        

