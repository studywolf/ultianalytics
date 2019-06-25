"""Note: Some touches numbers are off ... not sure where though, as goals,
catches, callahans all seem to be correct. Could be pickup calculations
missing some instances."""

import matplotlib.pyplot as plt
import numpy as np

def basic_stats(filename):
    data = []

    # set up dictionaries for recording stats
    assists = {}
    catches = {}
    completions = {}
    ds = {}
    drops = {}
    games = {}
    games_roster = {}
    goals = {}
    throwaways = {}
    touches = {}
    pickups = {}
    points = {}
    points_roster = {}

    with open(filename, 'r') as f:

        # first line of the file is the name of the data in each column
        names = f.readline().split(',')
        # get the indices of the columns of interest
        action_idx = names.index('Action')
        datetime_idx = names.index('Date/Time')
        defender_idx = names.index('Defender')
        event_type_idx = names.index('Event Type')
        opponent_idx = names.index('Opponent')
        passer_idx = names.index('Passer')
        player0_idx = names.index('Player 0')
        player7_idx = names.index('Player 7')
        linenumber_idx = names.index('Line')
        ourscore_idx = names.index('Our Score - End of Point')
        receiver_idx = names.index('Receiver')
        theirscore_idx = names.index('Their Score - End of Point')

        # load the rest of the file into a list
        data = [row.split(',') for row in f.readlines()]
        for ii in range(len(data)):
            row = data[ii]


            # what kind of action was performed in this entry
            action = row[action_idx]
            # get the name of the player performing each action for this entry
            passer = row[passer_idx]
            receiver = row[receiver_idx]
            defender = row[defender_idx]

            datetime = row[datetime_idx]
            opponent = row[opponent_idx]
            linenumber = row[linenumber_idx]
            game_name = '%s - %s' % (opponent, datetime)
            linenumber_name = '%s - %s - %s:% s' % (
                opponent, datetime, row[ourscore_idx], row[theirscore_idx])
            line = row[player0_idx:player7_idx]

            # calculate number of games player has played in
            for player in line:
                game = games_roster.get(game_name, [])
                if player not in game:
                    games[player] = games.get(player, 0) + 1
                    games_roster[game_name] = game + [player]
                player_points = points_roster.get(player, [])
                if linenumber_name not in player_points:
                    points_roster[player] = player_points + [linenumber_name]

            if action == 'Callahan':
                ds[defender] = ds.get(defender, 0) + 1
                goals[defender] = goals.get(defender, 0) + 1
                touches[defender] = touches.get(defender, 0) + 1

            elif action == 'Catch':
                completions[passer] = completions.get(passer, 0) + 1

                catches[receiver] = catches.get(receiver, 0) + 1
                touches[receiver] = touches.get(receiver, 0) + 1

            elif action == 'D':
                ds[defender] = ds.get(defender, 0) + 1

            elif action == 'Drop':
                drops[receiver] = drops.get(receiver, 0) + 1

            elif action == 'Goal':
                assists[passer] = assists.get(passer, 0) + 1
                completions[passer] = completions.get(passer, 0) + 1

                goals[receiver] = goals.get(receiver, 0) + 1
                catches[receiver] = catches.get(receiver, 0) + 1
                touches[receiver] = touches.get(receiver, 0) + 1

            elif action == 'Throwaway':
                throwaways[passer] = throwaways.get(passer, 0) + 1

        # calculate how many points each player played
        for name in points_roster.keys():
            points[name] = len(points_roster[name])

        for name in sorted(points.keys()):
            print('%s %s' % (name.ljust(10), points[name]))

        # handle case where first entry in data file was a pickup
        if data[0][event_type_idx] == 'Offense':
            pickups[data[0][passer_idx]] = 1
        # calculate number of pickups of each player by looking for
        # turns from defense to offense
        for ii in range(len(data)):
            row = data[ii]
            passer = row[passer_idx]
            # find the first offense passer of each possession
            if (row[event_type_idx] == 'Offense' and
                data[ii-1][event_type_idx] == 'Defense'):
                    pickups[passer] = pickups.get(passer, 0) + 1
                    touches[passer] = touches.get(passer, 0) + 1

        # print('----------------- GAMES ROSTER')
        # for opponent in games_roster.keys():
        #     print(opponent)
        #     print(games_roster[opponent])

        return {
            'Assists':assists,
            'Catches':catches,
            'Completions':completions,
            'Ds':ds,
            'Drops':drops,
            'Goals':goals,
            'Throwaways':throwaways,
            'Touches':touches,
            'Pickups':pickups,
            'Points':points,
            'Games':games,
            }


def setup_stats(filename, plot_weighting=False):
    data = []

    # set up dictionaries to record player scores
    scores = {
        'Goal':{},
        'Throwaway':{},
    }

    # assign weights to setting up different actions, the player at index
    # [action - ii] gets weight ** (ii + 1) added to their score
    weights = {
        'Goal':0.8,
        'Throwaway':0.5,
    }

    if plot_weighting:
        x = np.arange(20)
        for key in weights.keys():
            plt.plot(x, weights[key]**x, label=key)
        plt.legend()
        plt.ylabel('Reward / blame weighting for event')
        plt.xlabel('Number of throws before event')
        plt.tight_layout()
        plt.show()

    with open(filename, 'r') as f:

        # first line of the file is the name of the data in each column
        names = f.readline().split(',')
        # get the indices of the columns of interest
        action_idx = names.index('Action')
        event_type_idx = names.index('Event Type')
        passer_idx = names.index('Passer')

        data = [row.split(',') for row in f.readlines()]
        for ii in range(len(data)):
            row = data[ii]

            # what kind of action was performed in this entry
            action = row[action_idx]
            event = row[event_type_idx]

            # check if it's an action we're looking for
            if event == 'Offense' and action in weights.keys():

                dict = scores[action]
                weight = weights[action]

                # start walking backwards to see the set up of this action
                jj = 1
                # check to see if the previous action was part of the
                # offensive possession that lead to the action of interest
                while data[ii - jj][event_type_idx] == 'Offense':
                    # find out who was involved
                    passer = data[ii - jj][passer_idx]
                    # add to their score based on how far removed from the
                    # action of interest they are
                    dict[passer] = dict.get(passer, 0) + weight ** (jj + 1)
                    jj += 1

        # go through data and calculate involvement in goal / throwaway ratio
        ratio = {}
        for name in scores['Goal'].keys():
            goal_score = scores['Goal'][name]
            throwaway_score = scores['Throwaway'].get(name, None)
            if throwaway_score is not None:
                ratio[name] = goal_score / throwaway_score - 1
        scores['Ratio'] = ratio

        return scores


if __name__ == '__main__':

    basic_stats('Zen-stats.csv')
