import random, re, datetime
from queue import PriorityQueue
#import numpy as np
#import numba as nb

class Agent(object):
    def __init__(self, game):
        self.game = game

    def getAction(self, state):
        raise Exception("Not implemented yet")


class RandomAgent(Agent):
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)


class SimpleGreedyAgent(Agent):
    # a one-step-lookahead greedy agent that returns action with max vertical advance
    def getAction(self, state):
        legal_actions = self.game.actions(state)

        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        if player == 1:
            max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[0][0] - action[1][0] == max_vertical_advance_one_step]
        else:
            max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[1][0] - action[0][0] == max_vertical_advance_one_step]
        self.action = random.choice(max_actions)

class MyAgent(Agent):
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        
        
        self.abpruningAction(state, 0, -10000, 10000, 2)

            
    def abpruningAction(self, state, depth, a, b, DEPTH):
        player = state[0]
        if player == 1:
            self.max_value(state, depth, a, b, DEPTH)
        else: self.min_value(state, depth, a, b, DEPTH)

    def max_value(self, state, depth, a, b, DEPTH):
        if depth >= DEPTH: 
            return self.evaluate(state)
        v = -float('inf')
        legal_actions = self.game.actions(state)
        random.shuffle(legal_actions)
        for action in legal_actions:
            v = max(v, self.min_value(self.game.succ(state, action), depth+1, a, b, DEPTH))
            if v >= b:
                return v
            if v > a:
                a = v
                if depth == 0:
                    self.action = action
        return v

    def min_value(self, state, depth, a, b, DEPTH):
        if depth >= DEPTH: return self.evaluate(state)
        v = float('inf')

        legal_actions = self.game.actions(state)
        random.shuffle(legal_actions)
        for action in legal_actions:
            v = min(v, self.max_value(self.game.succ(state, action), depth+1, a, b, DEPTH))
            if v <= a:
                return v
            if v < b:
                b = v
                if depth == 0:
                    self.action = action
        return v

    def evaluate(self, state):
        board = state[1]
        player1_status = board.getPlayerPiecePositions(1)    
        player2_status = board.getPlayerPiecePositions(2)
        location1 = [(2, 1), (2, 2), (3, 2)]
        location1_bad = [(1, 1), (4, 1), (4, 4)]
        location2 = [(18, 1), (18, 2), (17, 2)]
        location2_bad = [(19, 1), (16, 1), (16, 4)]

        player1_vertical_count = 0
        player2_vertical_count = 0
        player1_horizontal_count = 0
        player2_horizontal_count = 0

        for position in player1_status:
            player1_vertical_count += 20-position[0]
            player1_horizontal_count += abs(position[1] - (11-abs(position[0]-10))/2)
            if position in location1:
                if board.board_status[position] == 3:
                    player1_vertical_count += 5
                else:
                    player1_vertical_count -= 5
            if  (position in location1_bad) & (board.board_status[position] == 3):
                player1_vertical_count -= 5
        player1_horizontal_count = -player1_horizontal_count


        for position in player2_status:
            player2_vertical_count += position[0]
            player2_horizontal_count += abs(position[1] - (11-abs(position[0]-10))/2)
            if position in location2:
                if board.board_status[position] == 4:
                    player2_vertical_count += 5
                else:
                    player2_vertical_count -=5
            if (position in location2_bad) & (board.board_status[position] == 4):
                player2_vertical_count -= 5
        player2_vertical_count = -player2_vertical_count
 
        if player1_vertical_count == 185: return 1000 #player1 wins
        if player2_vertical_count == -185: return -1000 #player2 wins

        return 0.5*(player1_horizontal_count+player2_horizontal_count)+player1_vertical_count+player2_vertical_count


