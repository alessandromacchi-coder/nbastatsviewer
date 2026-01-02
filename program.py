import pandas as pd 
import os
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
datadir="data"

def findgame(shotsdf):
    hometeam = input("Insert the home team name:\n")
    awayteam = input("Insert the away team name:\n")
    season = input("Insert the season (e.g. 2022-23):\n")

    possiblegames = (
        shotsdf[
            (shotsdf['SEASON_2'] == season) &
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
        try:
            choice = int(input("\n insert the number of the game you want to select "))

            if 0 <= choice < len(possiblegames):
                return possiblegames.loc[choice, 'GAME_ID']
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please insert a valid integer.")

def findplayer(shotsdf):
    name = input("insert the name and surname of the player you are looking for (for example: Lebron James) \n")
    id = (
        shotsdf.loc[shotsdf['PLAYER_NAME'] == name, 'PLAYER_ID']
        .iloc[0])
    
    if id==0:
        print("player not found, retry")

    return id

def playersfrommatch(gameid, shotsdf):
    
    game = shotsdf[shotsdf['GAME_ID'] == gameid]
    
    if game.empty:
        print("no game found ")
        return 0
    
    players=game['PLAYER_NAME'].unique()
    
    return players

def find3ptshots(shotsdf):
    season = int(input("insert the season you want to see (ex: if you want 2005-06, type in 2006) \n"))
    player = findplayer(shotsdf)

    seasonshots = shotsdf[
        (shotsdf['SEASON_1'] == season) &
        (shotsdf['PLAYER_ID'] == player) &
        (shotsdf['SHOT_TYPE'] == "3PT Field Goal")
        ]
    
    if seasonshots.empty:
        print ("that player has never played in that season \n")
        return 0
    else:
        return seasonshots

def findplayershots(id, shotsdf):

    players=playersfrommatch(id, shotsdf)
    print(f"the available players in that game are: {players}")
    

    playerid = findplayer(shotsdf)

    print (f"this i player id {playerid} and this is game id {id}")

    game = shotsdf[
        (shotsdf['GAME_ID'] == id) &
        (shotsdf['PLAYER_ID'] == playerid)
        ]
    
    if game.empty:
        print("no game was found with this id where that player has played, retry please")
        return 0
    else:
        return game

def viewshots(gameid, df):
    
    if gameid != 0:
        shots = df[df['GAME_ID'] == gameid]
        graphtype="game"
    else:
        shots=df
        graphtype="season"

    # Crea la figura
    fig, ax = plt.subplots(figsize=(12, 11))

    # Separa i tiri segnati da quelli sbagliati
    made_shots = shots[shots['SHOT_MADE'] == True]
    missed_shots = shots[shots['SHOT_MADE'] == False]

    # Prendi i dati per il titolo (usando .iloc[0] per prendere il primo valore)
    team_home = shots['HOME_TEAM'].iloc[0]
    team_away = shots['AWAY_TEAM'].iloc[0]
    team_season = shots['SEASON_2'].iloc[0]

    # 1. Disegna PRIMA il campo (così i tiri vanno sopra le linee)
    draw_court(ax, outer_lines=True)
    
    # 2. Plotta i tiri SEGNATI (Green)
    # LOC_X * -10: inverte l'asse X e scala in decimi
    # LOC_Y * 10 - 47.5: scala in decimi e allinea alla linea di fondo
    ax.scatter(made_shots['LOC_X'] * -10, (made_shots['LOC_Y'] * 10) - 47.5, 
               color='green', label='Made', alpha=0.7, s=30, edgecolors='white', linewidth=0.5)

    # 3. Plotta i tiri SBAGLIATI (Red)
    ax.scatter(missed_shots['LOC_X'] * -10, (missed_shots['LOC_Y'] * 10) - 47.5, 
               color='red', label='Missed', alpha=0.6, marker='x', s=30)

    # Titolo e Legenda
    if graphtype=="game":
        ax.set_title(f"Game selected: {team_home} vs {team_away} ({team_season})", fontsize=15)
    elif graphtype=="season":
        player= shots['PLAYER_NAME'].iloc[0]
        ax.set_title(f"{player}'s shots from the {team_season} season")
    
    # Posiziona la legenda in modo che non copra il campo
    ax.legend(loc='upper right')

    # Rimuovi gli assi numerici per pulizia (opzionale)
    ax.set_xticks([])
    ax.set_yticks([])

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

gameid=0
shots=pd.read_csv(os.path.join("data","shots_all_seasons.csv"))
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
            gameid=findgame(shots)
            viewshots(gameid, shots)
        case "2":
            print("")
            if input("do you want to use the last gameid that was found? yes or no \n") == "yes":
                print(f"using game id: {gameid}")
                if gameid==0:
                    print("there was no previous research for a game")
                else:
                    playershots=findplayershots(gameid, shots)
                    viewshots(gameid, shots)
            else:
                gameid=findgame(shots)
                playershots=findplayershots(gameid, shots)
                viewshots(gameid, playershots)
        case "3":
            seasonalshots=find3ptshots(shots)
            viewshots(0, seasonalshots)
        case "Change option":
            print(findplayer(shots))
            continue
        case "exit":
            cond=False

    
        

