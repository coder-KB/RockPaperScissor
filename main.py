import sys
import os
from random import randint
import requests
from bs4 import BeautifulSoup


def create_team():
    play1_name = input("Enter your name: ")
    rounds = int(input("Enter number of rounds: "))

    # play1_name = 'bharath'
    # rounds = 5

    api_id = randint(100000, 999999)

    try:

        url = "http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=start&appid=" + str(api_id) + "&pcon1=1&pname1=" + play1_name + "&mround=" + str(rounds)

        req = requests.get(url)

        data = req.json()

    except:
        sys.exit()

    if(data['code'] == '1'):
        print("API id is ", api_id)
        return play1_name, rounds, api_id
    else:
        print("Error in creating team")
        sys.exit()


def join_team():

    api_id = int(input("Enter the api_id to enter the team: "))
    play2_name = input("Enter your name: ")
    play1_name = ''
    # play2_name = 'john'

    try:
        url = "http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=fetchp1&appid=" + str(api_id) + "&pcon2=1&pname2=" + play2_name

        req = requests.get(url)

        data = req.json()

        rounds = data['data'][0]['max_round']

        play1_name = data['data'][0]['player1_name']

    except:
        print("Error in joining the team")
        sys.exit()

    return play1_name, play2_name, int(rounds), api_id


def waiting_for_play2(app_id):

    play2_confirm = False
    play2_name = ''

    while(not play2_confirm):

        url = "http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=fetchp2&appid=" + str(api_id)

        req = requests.get(url)

        data = req.json()

        play2_confirm = (data['data'][0]['player2_confirm'] == '1')
        play2_name = data['data'][0]['player2_name']

    return play2_name


def player_details(play1_name, play2_name, rounds):
    print("\n\tNumber of rounds: ", rounds)
    print("\tPlayer1 name: ", play1_name)
    print("\tPlayer2 name: ", play2_name)
    print()


def choose_winner(opt1, opt2):
    if(opt1 == opt2):
        return 3

    if(opt1 == 1):
        if(opt2 == 2):
            return 2
        else:
            return 1
    elif(opt1 == 2):
        if(opt2 == 1):
            return 1
        else:
            return 2
    else:
        if(opt2 == 1):
            return 2
        else:
            return 1


def convert(opt):
    if(opt == 1):
        return "Rock"
    elif(opt == 2):
        return "Paper"
    else:
        return "Scissor"


def display_winner(api_id):

    print("\n")

    url = f"http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=showall&appid={api_id}"

    req = requests.get(url)

    data = req.json()

    if(data['code'] != '1'):
        print("Error in display_winner")
        sys.exit()

    rounds_det = data['data']

    play1_name = rounds_det[0]['player1_name']
    play2_name = rounds_det[0]['player2_name']

    play1_wins = 0
    play2_wins = 0

    print("-" * (55))

    width = 15
    print("Round".center(10), end="")
    print(play1_name.center(width), end="")
    print(play2_name.center(width), end="")
    print("winner".center(width))

    print("-" * (55))

    for i in range(len(rounds_det)):
        print(str(i + 1).center(10), end="")

        move1 = int(rounds_det[i]["p1_move"])
        print(convert(move1).center(width), end="")

        move2 = int(rounds_det[i]["p2_move"])
        print(convert(move2).center(width), end="")

        winner = choose_winner(move1, move2)

        winner_name = ''

        if(winner == 3):
            winner_name = 'Tie'
        elif(winner == 1):
            play1_wins += 1
            winner_name = play1_name
        else:
            play2_wins += 1
            winner_name = play2_name

        print(winner_name.center(width))

    print("-" * (55))
    print("\n")

    # final winner
    if(play1_wins > play2_wins):
        print("Winner is ", play1_name)
    elif(play1_wins < play2_wins):
        print("Winner is ", play2_name)
    else:
        print("Match is Tie")

    print("\nGame Ends\n")


os.system('cls')

print("\t\tMULTIPLAYER GAME\n")
print("\t\tRock Paper Scissor\n")

print("Option 1: Create team")
print("Option 2: Join team")

print("\n")

try:
    option = int(input("Choose an option: "))
except:
    sys.exit()


if(option == 1):
    play1_name, rounds, api_id = create_team()
    play2_name = waiting_for_play2(api_id)

    player_details(play1_name, play2_name, rounds)

    print("1(Rock), 2(Paper), 3(Scissor)\n")

    round_cnt = 1
    while(round_cnt <= rounds):
        print("Round ", round_cnt)

        opt1 = int(input("Enter your move: "))

        url = f"http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=movep1&appid={api_id}&round={round_cnt}&optp1={opt1}"

        req = requests.get(url)

        data = req.json()

        if(data['code'] != '1'):
            print("Error in round ", round_cnt)
            sys.exit()

        game_completed = False

        while(not game_completed):

            url = f"http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=fetchmove&appid={api_id}&round={round_cnt}"

            req = requests.get(url)

            data = req.json()

            if(data['data'][0]['p2_move'] != "0"):
                game_completed = True

        round_cnt += 1

else:
    play1_name, play2_name, rounds, api_id = join_team()

    player_details(play1_name, play2_name, rounds)

    print("1(Rock), 2(Paper), 3(Scissor)\n")

    round_cnt = 1
    while(round_cnt <= rounds):
        print("Round ", round_cnt)

        opt2 = int(input("Enter your move: "))

        # fetch first player move
        play1_played = False

        while(not play1_played):
            url = f"http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=fetchmove&appid={api_id}&round={round_cnt}"

            req = requests.get(url)

            data = req.json()

            if(data['code'] == '1'):
                play1_played = True

        opt1 = data['data'][0]['p1_move']

        winner = choose_winner(int(opt1), opt2)

        url = f"http://samprit.ml/api/rockpaper/gamecontroller?apiKEY=iwritecode&option=movep2&appid={api_id}&round={round_cnt}&optp2={opt2}&winner={winner}"

        req = requests.get(url)

        data = req.json()

        if(data['code'] != '1'):
            print("Error in round ", round_cnt)
            sys.exit()

        round_cnt += 1


display_winner(api_id)

os.system("pause")
