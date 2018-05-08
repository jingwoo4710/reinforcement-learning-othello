#This is Alpha Beta Pruning for Othello, using
#https://github.com/hylbyj/Alpha-Beta-Pruning-for-Othello-Game/blob/master/othello.py
#ply is the depth

import math
import numpy as np
from othelloBoard import Board
from copy import deepcopy

path = "/Users/student36/reinforcement-learning-othello/"
#path = "/home/oliver/git/othello/reinforcement-learning-othello/"

def process(array):
    new_array = []
    pieces = [0, 1, -1]
    
    for i in range(3):
        board = []
        for j in range(8):
            row = []
            for k in range(8):
                row.append(int(array[j][k] == pieces[i]))
            board.append(row)
        new_array.append(board)

    return new_array

def reverse(board):
    newBoard = [[0 for i in range(8)] for j in range(8)]
    d = {0:0, 1:-1, -1:1}
    for i in range(8):
        for j in range(8):
            newBoard[i][j] = d[board[i][j]]

    return newBoard


class AlphaBeta():
    def __init__(self, controller):
        self.controller = controller
    
    def policy(self, board, color, index):
        if(color == -1):
            board = reverse(board)
        processedBoard = process(board)
        processedBoard = np.array([processedBoard])
        return self.controller.population[index].model.predict(processedBoard)[0][0]

    #How I implement minimax algorithm:
    #I separated minimax into three functions, the first one is minimax which is
    #the general function acting like get the min or the max value based on the
    #depth it currently explores:
    def _minmax(self, board, color, ply, index):
        #need to get all the legal moves
        moves = board.get_legal_moves(color)

        print("legal move " + str(moves))
        if not isinstance(moves, list):
           score = self.policy(board, color)
           return score,None
        print(ply)
        return_move = moves[0]
        bestscore = - math.inf
        print("using minmax best score: "+ str(bestscore))
        #ply = 4
        #will define ply later;
        for move in moves:
            newboard = deepcopy(board)
            newboard.execute_move(move,color)

            score = self.min_score(newboard, -color, ply, index)
            if score > bestscore:
                bestscore = score
                return_move = move
                print("return move " + str(return_move) + "bestscore " + str(bestscore))
        #newboard = deepcopy(board)
        #return max((value(newboard.execute_move(m, color)),m) for m in moves)
        return (bestscore,return_move)

    #function max_score is aimed to maximize the score of player and function min_score is aimed to minimize the score of opponent. They all only return the value.
    def max_score(self, board, color, ply, index):
        moves = board.get_legal_moves(color)
        #if not isinstance(moves, list):
        #   return board.count(color)
        if ply == 0:
           return self.policy(board, color, index)
        bestscore = -math.inf
        for move in moves:
            newboard = deepcopy(board)
            newboard.execute_move(move,color)
            score = self.min_score(newboard, -color, ply-1, index)
            if score > bestscore:
                bestscore = score
        return bestscore

    def min_score(self, board, color, ply, index):
        moves = board.get_legal_moves(color)
        #if not isinstance(moves, list):
        #   return board.count(color)
        if ply == 0:
           return self.policy(board, color, index)
        bestscore = math.inf
        for move in moves:
            newboard = deepcopy(board)
            newboard.execute_move(move,color)
            score = self.max_score(newboard, -color, ply-1, index)
            if score < bestscore:
                bestscore = score
        return bestscore

#=========================================================================
  
    #2) Alpha-beta Othello player
    #I modify the three functions and initially set alpha, beta as +infinity and -infinity. The functions are listed:
    def _minmax_with_alpha_beta(self, board, color, ply, index):
        if ply == 0:
            return self.policy(board, color, index)
        
        #print(board.pieces)
        moves = board.get_legal_moves(color)
        #print(board.pieces)
        if len(moves) == 0:
            return [0, (-1, -1)]

        #print ply
        return_move = moves[0]
        bestscore = - math.inf
        #print "using alpha_beta best score:"+ str(bestscore)
        #ply = 4
        #will define ply later;
        for move in moves:
            newboard = deepcopy(board)
            newboard.execute_move(move,color)

            score = self.min_score_alpha_beta(newboard, -color, ply, math.inf, -math.inf, index)
            print(move)
            print(score)
            print("")
            
            if score > bestscore:
               bestscore = score
               return_move = move
               #print "return move" + str(return_move) + "best score" + str(bestscore)

        return (bestscore,return_move)

    #Also the max and min value function:
    def max_score_alpha_beta(self, board, color, ply, alpha, beta, index):
        if ply == 0:
            print("")
            print(color)
            return self.policy(board, color, index)
        
        bestscore = -math.inf

        moves = board.get_legal_moves(color)
        if len(moves) == 0:
            return self.policy(board, color, index)

        for move in moves:
            newboard = deepcopy(board)
            newboard.execute_move(move,color)
            score = self.min_score_alpha_beta(newboard, -color, ply-1, alpha, beta, index)
            #print("Max")
            #print(move)
            #print(score)
            #print("")
            
            if score > bestscore:
                bestscore = score
            if bestscore >= beta:
                return bestscore
            alpha = max (alpha,bestscore)
        return bestscore

    def min_score_alpha_beta(self, board, color, ply, alpha, beta, index):
          if ply == 0:
              print("")
              print(color)
              return self.policy(board, color, index)
          bestscore = math.inf

          moves = board.get_legal_moves(color)
          if len(moves) == 0:
              return self.policy(board, color, index)
  
          for move in moves:
              newboard = deepcopy(board)
              newboard.execute_move(move,color)
              score = self.max_score_alpha_beta(newboard, -color, ply-1, alpha, beta, index)
              #print("Min")
              #print(move)
              #print(score)
              #print("")

              if score < bestscore:
                 bestscore = score
              if bestscore <= alpha:
                 return bestscore
              beta = min(beta,bestscore)
          return bestscore
