"""
Created on Fri Mar 22 2019

@author: Eidan

Description: A script to explore the game tree of ultimate tic-tac-toe.
"""
# Initialize empty board
board = [[[[0 for i in range(3)] for j in range(3)] for k in range(3)] for l in range(3)]
# Find Legal Moves and Add to Stack
newMoveStack = [[i, j, k, l, 1, 1] for i in range(3) for j in range(3) for k in range(3) for l in range(3)]
# Stack of moves to roll back
oldMoveStack = []
# Depth
t = 0
# Current Player
player = 1
# Miniboard wins
miniVictories = [[None for i in range(3)] for j in range(3)]
# Dictionary saves the possible values for the state at depth x in the current search tree. 
# When it is time to rollback from depth t to t-1: 
# # find the max or min value of that state as appropriate and save it as a possible value for its parent state (t-1)
# # then reset the list of possible values for depth t
values = {x: [] for x in range(81)}

while True:
    # Pop move from stack
    currentMove = newMoveStack.pop()
    # print(str(currentMove) + " popped from new stack")
    # If popped move is the next turn
    if currentMove[4] == t+1:
        [X, Y, x, y, t, player] = currentMove[:]
        wonMini = False
        board[X][Y][x][y] = player
        # print(str(currentMove) + " marked")
        # input("ok?")
        # Push move to stack (for possible future rollback)
        oldMoveStack.append(currentMove)
        # print(str(currentMove) + " pushed to old stack")
        # Check if latest move won the mini board
        if miniVictories[X][Y] is None:
            # Check rows
            for row in range(3):
                equal = True
                for col in range(2):
                    if(board[X][Y][row][col] == 0):
                        equal = False
                        break
                    else:
                        equal = equal and board[X][Y][row][col] == board[X][Y][row][col+1]
                        
                if(equal):
                    miniVictories[X][Y] = currentMove
                    # print(str(currentMove) + " won mini board " + str([X, Y]))
                    # input("ok?")
                    wonMini = True

        if miniVictories[X][Y] is None:            
            # Check cols
            for col in range(3):
                equal = True
                for row in range(2):
                    if(board[X][Y][row][col] == 0):
                        equal = False
                        break
                    else:
                        equal = equal and board[X][Y][row][col] == board[X][Y][row+1][col]
                        
                if(equal):
                    miniVictories[X][Y] = currentMove
                    # print(str(currentMove) + " won mini board " + str([X, Y]))
                    # input("ok?")
                    wonMini = True

        if miniVictories[X][Y] is None:        
            # Check diagonals
            if board[X][Y][1][1] == player:
                if (board[X][Y][0][0] == player and board[X][Y][2][2] == player) or (board[X][Y][2][0] == player and board[X][Y][0][2] == player):
                    miniVictories[X][Y] = currentMove
                    # print(str(currentMove) + " won mini board " + str([X, Y]))
                    # input("ok?")
                    wonMini = True

        wonMega = False
        # If the latest move won a miniboard, and there are at least 3 miniVictories, check to see if the game has been won.
        if wonMini and sum( [sum([victory is not None for victory in miniVictories[i]]) for i in range(3)]):
            # Check Rows
            for row in range(3):
                equal = True
                for col in range(2):
                    if(miniVictories[row][col] is None):
                        equal = False
                        break
                    else:
                        equal = equal and miniVictories[row][col][5] == player
                        
                if(equal):
                    # print(str(currentMove) + " won mega board ")
                    # input("ok?")
                    wonMega = True

            if not wonMega:            
                # Check cols
                for col in range(3):
                    equal = True
                    for row in range(3):
                        if(miniVictories[row][col] is None):
                            equal = False
                            break
                        else:
                            if not miniVictories[row][col][5] == player:
                                equal = False
                                break
                            
                    if equal:
                        # print(str(currentMove) + " won mega board ")
                        # input("ok?")
                        wonMega = True

            if not wonMega:        
                # Check diagonals: Upper left to lower right
                wonMega = True
                for a in range(3):
                    if miniVictories[a][a] is None:
                        wonMega = False
                        break
                    else:
                        if not miniVictories[a][a][5] == player:
                            wonMega = False
                            break

            if not wonMega:        
                # Check diagonals: Lower left to upper right
                wonMega = True
                for a in range(3):
                    if miniVictories[2-a][a] is None:
                        wonMega = False
                        break
                    else:
                        if not miniVictories[2-a][a][5] == player:
                            wonMega = False
                            break

        if wonMega or t == 81:
            lastMove = oldMoveStack.pop()
            [X, Y, x, y, t, player] = lastMove[:]
            values[t-1].append(int(wonMega)*player)
            # Undo last move
            board[X][Y][x][y] = 0
            # print(str(lastMove) + " unmarked")
            # input("ok?")
            t = t-1
            for i in range(3):
                for j in range(3):
                    if miniVictories[i][j] == lastMove:
                        miniVictories[i][j] = None
                        # print("miniboard " + str([i,j]) + " unwon")
                        break
        else:
            # Go deeper
            nextMiniFull = True
            for i in range(3):
                for j in range(3):
                    if board[x][y][i][j] == 0:
                        nextMiniFull = False
                        newmove = [x, y, i, j, t+1, -1 * player]
                        newMoveStack.append(newmove)
                        # print(str(newmove) + " pushed to new stack")
            
            if nextMiniFull:
                for a in range(3):
                    for b in range(3):
                        for c in range(3):
                            for d in range(3):
                                if board[a][b][c][d] == 0:
                                    newmove = [a, b, c, d, t+1, -1 * player]
                                    newMoveStack.append(newmove)
                                    # print(str(newmove) + " pushed to new stack")
    else:
        # Roll back further!
        if t % 2 == 0:
            # It is now min's turn. The value of t is the minimum value of all possible t+1. Append this to list of values for t-1
            values[t-1].append(min(values[t]))
        else:
            values[t-1].append(max(values[t]))

        if(t < 50):
            print(t)

        values[t] = []
        lastMove = oldMoveStack.pop()
        [X, Y, x, y, t, player] = lastMove[:]
        # Undo last move
        # print(str(lastMove) + " unmarked")
        # input("ok?")
        # if not board[X][Y][x][y] == player:
        #     print("OH NO")
        board[X][Y][x][y] = 0
        t = t-1
        for i in range(3):
            for j in range(3):
                if miniVictories[i][j] == lastMove:
                    miniVictories[i][j] = None
                    # print("miniboard " + str([i,j]) + " unwon")
                    break


print(max(values[0]))