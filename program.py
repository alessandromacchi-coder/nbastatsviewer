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
        return possiblegames.iloc[0, 'GAME_ID']

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
    
    #if id.empty:
       # print("player not found, retry")

    return id


def findplayershots(id, shotsdf):

    playerid = findplayer(shotsdf)

    game = shotsdf[
        (shotsdf['GAME_ID'] == id) &
        (shotsdf['PLAYER_ID'] == playerid)
        ]
    
    if game.empty:
        print("no game was found with this id where that player has played, retry please")
        return None
    else:
        return game.iloc[0, 'GAME_ID']


def viewshots(gameid, df):
    shots = df[(df['GAME_ID']) == (gameid)]
    fig, ax = plt.subplots(figsize=(10, 7))

   

    made_shots = shots[shots['SHOT_MADE'] == True]
    missed_shots = shots[shots['SHOT_MADE'] == False]

    # Take the right things for the title of the plot
    team_home = (shots['HOME_TEAM']).iloc[0]
    team_away = (shots['AWAY_TEAM']).iloc[0]
    team_season = (shots['SEASON_2']).iloc[0]


     # Draw the lines field
    draw_court(ax)
    
    # Draw the made (green) and the failed (red)
    #non so farlo !!!!!!


    # Title of the plot
    ax.set_title(f"Game selected: {team_home} - {team_away} {team_season}")
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2)

    # Save the figure and show it
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
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                                color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
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
    choice=input("Choose an option to continue: \n 1 to view every shot made/missed in a said game \n 2 to view every shot of a said player in a said game \n 3 to view ")
    match(choice):
        case "1":
            gameid=findgame(shots)
            viewshots(gameid, shots)
        case "2":
            print("")
            if input("do you want to use the last gameid that was found? Y or N") == "Y":
                if gameid==0:
                    print("there was no previous research for a game")
                else:
                    playershots=findplayershots(gameid, shots)
                    viewshots(gameid, shots)
            else:
                gameid=findgame(shots)
                playershots=findplayershots(gameid, shots)
                viewshots(gameid, shots)
        case "Change option":
            continue
        case "Exit":
            cond=False

    
        

