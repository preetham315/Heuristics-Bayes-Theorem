import sys
import time
import copy
import math

def board_to_string(board,N):
    converted_string = ""
    for i in range(0,len(board),N):
        converted_string = converted_string+'\n'+ board[i:i+N]
    return converted_string

def board_conversion(board,N):
    list_board = []
    for i in range(0,len(board),N):
        list_board.append([ char for char in board[i:i+N]])
    return list_board

def finding_successor_function(board):
    successor_list = []
    for row_value in range(len(board)):
        for column_value in range(len(board[0])):
            if board[row_value][column_value] == '$' or  board[row_value][column_value] == '@':
                successor_list = successor_list + successor_of_raichu(board,board[row_value][column_value], row_value, column_value)
            elif board[row_value][column_value] in 'B' or board[row_value][column_value] in 'W':
                successor_list = successor_list + successor_of_pikachu(board,board[row_value][column_value], row_value, column_value)
            elif board[row_value][column_value] in 'b' or board[row_value][column_value] in 'w':
                successor_list = successor_list + successor_of_pichu(board,board[row_value][column_value], row_value, column_value)
    return successor_list

def pichu_count(board, pichu, row_value, column_value):
    top_right, top_left, bottom_right,bottom_left = [0,0,0,0]

    if pichu =='w':
        kill_flag = False
        move_count = 0
        for i,j in zip(range(row_value+1,len(board)),range(column_value+1,len(board[0]))): # bottom-right diagonal
            if move_count == 2:
                break
            else:
                if (board[i][j] in 'BwW@$'):
                    break
                elif (board[i][j] == 'b'):
                    kill_flag = True
                    move_count +=1
                elif(board[i][j] == '.' and kill_flag == False):
                    bottom_right += 1
                    break
                elif (board[i][j] == '.' and kill_flag == True):
                    bottom_right +=2
                    move_count +=1
                    
        kill_flag = False
        move_count = 0
        for i,j in zip(range(row_value+1,len(board)),range(column_value-1, -1, -1)): #bottom-left diagonal
            if move_count == 2:
                break
            else:
                if (board[i][j] in 'BwW@$'):
                    break
                elif (board[i][j] == 'b'):
                    kill_flag = True
                    move_count +=1
                if(board[i][j] == '.' and kill_flag == False):
                    bottom_left += 1
                    break
                elif (board[i][j] == '.' and kill_flag == True):
                    bottom_left +=2
                    move_count +=1
        
        return  bottom_left + bottom_right 

    if pichu == 'b':
        kill_flag = False
        move_count = 0
        for i,j in zip(range(row_value-1, -1, -1),range(column_value-1, -1, -1)):  # top-left diagonal
            if move_count == 2:
                break
            else:
                if (board[i][j] in 'WbB@$'):
                    break
                elif (board[i][j] == 'w'):
                    kill_flag = True
                    move_count +=1
                elif(board[i][j] == '.' and kill_flag == False):
                    top_left += 1
                    break
                elif (board[i][j] == '.' and kill_flag == True):
                    top_left +=2
                    move_count +=1

        kill_flag = False
        move_count = 0
        for i,j in zip(range(row_value-1, -1, -1),range(column_value+1,len(board[0]))): # top-right diagonal
            if move_count == 2:
                break
            else:
                if (board[i][j] in 'WbB@$'):
                    break
                elif (board[i][j] == 'w'):
                    kill_flag = True
                    move_count +=1
                if(board[i][j] == '.' and kill_flag == False):
                    top_right += 1
                    break
                elif (board[i][j] == '.' and kill_flag == True):
                    top_right +=2
                    move_count +=1

        return top_left + top_right

def pikachu_count(board, pikachu,row_value, column_value):
    top,bottom,right,left = [0,0,0,0]
    kill_flag = False
    move_count = 0

    if pikachu == 'B':
        kill_flag = False
        move_count = 0
        
        for i in range(row_value-1,-1,-1): # top direction
            if ((kill_flag == True and move_count ==3) or (kill_flag == False and move_count==2) or (kill_flag == True and top ==0 and move_count ==2) ):
                break
            else:
                if (board[i][column_value] in 'B@$'):
                    break
                elif (board[i][column_value] in 'wW'):
                    if kill_flag == False: 
                        kill_flag = True
                    move_count += 1
                elif (board[i][column_value] == '.' and kill_flag == False):
                    top +=1
                    move_count +=1
                elif (board[i][column_value] == '.' and kill_flag == True):
                    if top == 0:
                        top += 2
                    elif top == 2:
                        top +=1 
                    move_count +=1
       

    if pikachu == 'W':
        kill_flag = False
        move_count = 0
        for i in range(row_value+1,len(board)): # bottom direction
            if ((kill_flag == True and move_count ==3) or (kill_flag == False and move_count==2) or (kill_flag == True and top ==0 and move_count ==2) ):
                break
            else:
                if (board[i][column_value] in 'W@$'):
                    break
                elif (board[i][column_value] in 'bB'):
                    if kill_flag == False: 
                        kill_flag = True
                    move_count += 1
                elif (board[i][column_value] == '.' and kill_flag == False):
                    bottom +=1
                    move_count +=1
                elif (board[i][column_value] == '.' and kill_flag == True):
                    if bottom == 0:
                        bottom += 2
                    elif bottom == 2:
                        bottom +=1
                    move_count +=1

    kill_flag = False
    move_count = 0
    for i in range(column_value-1,-1,-1): # left direction
        if ((kill_flag == True and move_count ==3) or (kill_flag == False and move_count==2) or (kill_flag == True and top ==0 and move_count ==2) ):
                break
        else:
            if (pikachu =='W' and board[row_value][i] in 'W@$') or (pikachu =='B' and board[row_value][i] in 'B@$'):
                    break
            elif (pikachu =='W' and board[row_value][i] in 'bB') or (pikachu =='B' and board[row_value][i] in 'wW') :
                if kill_flag == False: 
                    kill_flag = True
                move_count += 1
            elif (board[row_value][i] == '.' and kill_flag == False):
                left +=1
                move_count +=1
            elif (board[row_value][i] == '.' and kill_flag == True):
                if left == 0:
                    left += 2
                elif left == 2:
                    left +=1 
                move_count +=1
            

    kill_flag = False
    move_count = 0
    for i in range(column_value+1,len(board[0])): # right direction
        if (kill_flag == False and move_count==2):
                break
        if (kill_flag == True and  move_count ==3):
            break
        if (kill_flag == True and right ==0 and move_count ==2):
                break

        if (board[row_value][i] == '.' and kill_flag == False):
            right +=1
            move_count +=1
        elif (board[row_value][i] == '.' and kill_flag == True):
            if right == 0:
                right += 2
            elif right == 2:
                right +=1 
            move_count +=1
        elif (pikachu =='W' and board[row_value][i] in 'bB') or (pikachu =='B' and board[row_value][i] in 'wW') :
            if kill_flag == False: 
                kill_flag = True
            move_count += 1
        elif (pikachu =='W' and board[row_value][i] in 'W@$') or (pikachu =='B' and board[row_value][i] in 'B@$'):
                break
    
    if pikachu == 'B':
        return top + left + right
    elif pikachu == 'W':
        return bottom +left + right

def raichu_count(board, raichu, row_value, column_value):
    top = bottom = left = right = top_left = top_right = bottom_left = bottom_right = 0

    kill_flag = False
    kill_count = 0
    for i in range(row_value-1,-1,-1):  # top direction
        if (board[i][column_value] == '.'):
            if (kill_flag == False and kill_count == 0):
                top += 1
            elif (kill_flag == True and kill_count == 0):
                top += 2
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                top += 1
        elif (raichu == '@' and board[i][column_value] in 'bB$') or (raichu == '$' and board[i][column_value] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[i][column_value] in '@wW') or (raichu == '$' and board[i][column_value] in '$bB')):
            break

    kill_flag = False
    kill_count = 0
    for i in range(row_value+1,len(board)): # bottom direction
        if (board[i][column_value] == '.'):
            if (kill_flag == False and kill_count == 0):
                bottom += 1
            elif (kill_flag == True and kill_count == 0):
                bottom += 2
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                bottom += 1
        elif (raichu == '@' and board[i][column_value] in 'bB$') or (raichu == '$' and board[i][column_value] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[i][column_value] in '@wW') or (raichu == '$' and board[i][column_value] in '$bB')):
            break
    
    kill_flag = False
    kill_count = 0
    for i in range(column_value-1,-1,-1): # left direction
        if (board[row_value][i] == '.'):
            if (kill_flag == False and kill_count == 0):
                left += 1
            elif (kill_flag == True and kill_count == 0):
                left += 2
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                left += 1
        elif (raichu == '@' and board[row_value][i] in 'bB$') or (raichu == '$' and board[row_value][i] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[row_value][i] in '@wW') or (raichu == '$' and board[row_value][i] in '$bB')):
            break

        
    kill_flag = False
    kill_count = 0
    for i in range(column_value+1,len(board[0])): #right direction
        if (board[row_value][i] == '.'):
            if (kill_flag == False and kill_count == 0):
                right += 1
            elif (kill_flag == True and kill_count == 0):
                right += 2
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                right += 1
        elif (raichu == '@' and board[row_value][i] in 'bB$') or (raichu == '$' and board[row_value][i] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[row_value][i] in '@wW') or (raichu == '$' and board[row_value][i] in '$bB')):
            break
    
    kill_flag = False
    kill_count = 0
    for i,j in zip(range(row_value-1, -1, -1),range(column_value-1, -1, -1)): # top-left diagonal
        if (board[i][j] == '.'):
            if (kill_flag == False and kill_count == 0):
                top_left += 1
            elif (kill_flag == True and kill_count == 0):
                top_left += 2
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                top_left += 1
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    kill_flag = False
    kill_count = 0
    for i,j in zip(range(row_value-1, -1, -1),range(column_value+1,len(board[0]))): # top-right diagonal
        if (board[i][j] == '.'):
            if (kill_flag == False and kill_count == 0):
                top_right += 1
            elif (kill_flag == True and kill_count == 0):
                top_right += 2
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                top_right += 1
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    kill_flag = False
    kill_count = 0
    for i,j in zip(range(row_value+1,len(board)),range(column_value-1, -1, -1)): # bottom-left diagonal
        if (board[i][j] == '.'):
            if (kill_flag == False and kill_count == 0):
                bottom_left += 1
            elif (kill_flag == True and kill_count == 0):
                bottom_left += 2
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                bottom_left += 1
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    kill_flag = False
    kill_count = 0
    for i,j in zip(range(row_value+1,len(board)),range(column_value+1,len(board[0]))): # bottom-right diagonal
        if (board[i][j] == '.'):
            if (kill_flag == False and kill_count == 0):
                bottom_right += 1
            elif (kill_flag == True and kill_count == 0):
                bottom_right += 2
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                bottom_right += 1
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    return top + bottom + left + right + top_left + top_right + bottom_left + bottom_right

def successor_of_pichu(board, pichu, row_value, column_value):
    print("in pichu dsjknf")
    newboard = copy.deepcopy(board)
    successor_pichu = []
    
    if pichu == 'b':
        kill_flag = False
        move_count = 0
        k,m = 1000, 1000
        for i,j in zip(range(row_value-1, -1, -1),range(column_value-1, -1, -1)): #top-left diagonal
            k = i
            m = j
            if move_count == 2:
                break
            if(board[i][j] == '.' and kill_flag == False):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[i+1][j+1] = '.'
                if (k == 0 and newboard[k][m]=='b'):
                    newboard[k][m] = '$'
                successor_pichu.append(newboard)
                newboard = copy.deepcopy(board)
                break
            elif (board[i][j] == '.' and kill_flag == True):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[i+1][j+1] = '.'
                if (k == 0 and newboard[k][m]=='b'):
                    newboard[k][m] = '$'
                successor_pichu.append(newboard)
                newboard = copy.deepcopy(board)
                move_count +=1
            elif (board[i][j] == 'w'):
                kill_flag = True
                move_count +=1
            elif (board[i][j] in 'WbB@$'):
                break
        

        kill_flag = False
        move_count = 0
        k,m = 1000, 1000
        for i,j in zip(range(row_value-1, -1, -1),range(column_value+1,len(board[0]))): #top-right diagonal
            k = i
            m = j
            if move_count == 2:
                break
            if (board[i][j] == 'w'):
                kill_flag = True
                move_count +=1
            elif (board[i][j] in 'WbB@$'):
                break
            if(board[i][j] == '.' and kill_flag == False):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[i+1][j-1] = '.'
                if (k == 0 and newboard[k][m]=='b'):
                    newboard[k][m] = '$'
                successor_pichu.append(newboard)
                newboard = copy.deepcopy(board)
                break
            elif (board[i][j] == '.' and kill_flag == True):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[i+1][j-1] = '.'
                if (k == 0 and newboard[k][m]=='b'):
                    newboard[k][m] = '$'
                successor_pichu.append(newboard)
                newboard = copy.deepcopy(board)
                move_count +=1

        return successor_pichu

            
    if pichu =='w':
        kill_flag = False
        move_count = 0
        k = 0
        m = 0
        for i,j in zip(range(row_value+1,len(board)),range(column_value-1, -1, -1)): #bottom-left diagonal
            k = i
            m = j
            if move_count == 2:
                break
            if(board[i][j] == '.' and kill_flag == False):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[i-1][j+1] = '.'
                if (k == len(board)-1 and newboard[k][m]=='w'):
                    newboard[k][m] = '@'
                successor_pichu.append(newboard)
                newboard = copy.deepcopy(board)
                break
            elif (board[i][j] == '.' and kill_flag == True):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[i-1][j+1] = '.'
                if (k == len(board)-1 and newboard[k][m]=='w'):
                    newboard[k][m] = '@'
                successor_pichu.append(newboard)
                newboard = copy.deepcopy(board)
                move_count +=1
            elif (board[i][j] == 'b'):
                kill_flag = True
                move_count +=1
            elif (board[i][j] in 'BwW@$'):
                break
        
            
        kill_flag = False
        move_count = 0
        k = 0
        m = 0
        for i,j in zip(range(row_value+1,len(board)),range(column_value+1,len(board[0]))): #bottom-right
            k = i
            m = j
            if move_count == 2:
                break
            if (board[i][j] == 'b'):
                kill_flag = True
                move_count +=1
            elif (board[i][j] in 'BwW@$'):
                break
            elif(board[i][j] == '.' and kill_flag == False):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[i-1][j-1] = '.'
                if (k == len(board)-1 and newboard[k][m]=='w'):
                    newboard[k][m] = '@'
                successor_pichu.append(newboard)
                newboard = copy.deepcopy(board)
                break
            elif (board[i][j] == '.' and kill_flag == True):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[i-1][j-1] = '.'
                if (k == len(board)-1 and newboard[k][m]=='w'):
                    newboard[k][m] = '@'
                successor_pichu.append(newboard)
                newboard = copy.deepcopy(board)
                move_count +=1

        return  successor_pichu        


def successor_of_pikachu(board, pikachu, row_value, column_value):
    top,bottom,left,right = [0,0,0,0]
    pikachu_succ_list = []
    newboard = copy.deepcopy(board)

    kill_flag = False
    move_count = 0

    if pikachu == 'B':
        kill_flag = False
        move_count = 0
        k = 10000
        opp_i = 1000
        opp_j = 1000
        for i in range(row_value-1,-1,-1): # top direction
            k=i
            if (kill_flag == False and move_count==2):
                break
            if (kill_flag == True and  move_count ==3):
                break

            if (kill_flag == True and top ==0 and move_count ==2): #
                break

            if (board[i][column_value] == '.' and kill_flag == False):
                newboard[i][column_value], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][column_value]
                newboard[i+1][column_value] = '.'
                if (k==0 and newboard[k][column_value] == 'B'):
                    newboard[k][column_value] = '$'
                pikachu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                top += 1
                move_count +=1
            elif (board[i][column_value] == '.' and kill_flag == True):
                newboard[i][column_value], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][column_value]
                newboard[opp_i][opp_j] = '.'
                if (k==0 and newboard[k][column_value] == 'B'):
                    newboard[k][column_value] = '$'
                pikachu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                if top == 0:
                    top += 2
                elif top == 2:
                    top +=1 
                move_count +=1
            elif (board[i][column_value] in 'wW'):
                if kill_flag == False: 
                    kill_flag = True
                opp_i = i
                opp_j = column_value
                move_count += 1
            elif (board[i][column_value] in 'bB@$'):
                break
        

    if pikachu == 'W':
        kill_flag = False
        move_count = 0
        k=0
        opp_i = 1000
        opp_j = 1000
        for i in range(row_value+1,len(board)): # bottom direction
            k=i
            if (kill_flag == False and move_count==2):
                break
            if (kill_flag == True and  move_count ==3):
                break
            if (kill_flag == True and bottom ==0 and move_count ==2):
                break
            

            if (board[i][column_value] == '.' and kill_flag == False):
                newboard[i][column_value], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][column_value]
                newboard[i-1][column_value] = '.'
                if (k==len(board)-1 and newboard[k][column_value] == 'W'):
                    newboard[k][column_value] = '@'
                pikachu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                bottom +=1
                move_count +=1
            elif (board[i][column_value] == '.' and kill_flag == True):
                newboard[i][column_value], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][column_value]
                newboard[opp_i][opp_j] = '.'
                if (k==len(board)-1 and newboard[k][column_value] == 'W'):
                    newboard[k][column_value] = '@'
                pikachu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                if bottom == 0:
                    bottom += 2
                elif bottom == 2:
                    bottom +=1 
                move_count +=1
            elif (board[i][column_value] in 'bB'):
                if kill_flag == False: 
                    kill_flag = True
                opp_i = i
                opp_j = column_value
                move_count += 1
            elif (board[i][column_value] in 'wW@$'):
                break
        
    

    kill_flag = False
    move_count = 0
    opp_i = 1000
    opp_j = 1000
    for i in range(column_value-1,-1,-1): # left direction
        if ((kill_flag == False and move_count==2)or (kill_flag == True and move_count ==3) or(kill_flag == True and left ==0 and move_count ==2)):
                break
        if (board[row_value][i] == '.' and kill_flag == False):
            newboard[row_value][i], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[row_value][i]
            newboard[row_value][i+1] = '.'
            pikachu_succ_list.append(newboard)
            newboard = copy.deepcopy(board)
            left +=1
            move_count +=1
        elif (board[row_value][i] == '.' and kill_flag == True):
            newboard[row_value][i], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[row_value][i]
            newboard[opp_i][opp_j] = '.'
            pikachu_succ_list.append(newboard)
            newboard = copy.deepcopy(board)
            if left == 0:
                left += 2
            elif left == 2:
                left +=1 
            move_count +=1
        elif (pikachu =='W' and board[row_value][i] in 'bB') or (pikachu =='B' and board[row_value][i] in 'wW') :
            if kill_flag == False: 
                kill_flag = True
            opp_i = row_value
            opp_j = i
            move_count += 1
        elif (pikachu =='W' and board[row_value][i] in 'wW@$') or (pikachu =='B' and board[row_value][i] in 'bB@$'):
                break

    kill_flag = False
    move_count = 0
    opp_i = 1000
    opp_j = 1000
    for i in range(column_value+1,len(board[0])): # right direction
        if ((kill_flag == False and move_count==2)or (kill_flag == True and move_count ==3) or(kill_flag == True and left ==0 and move_count ==2)):
                break
        if (board[row_value][i] == '.' and kill_flag == False):
            newboard[row_value][i], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[row_value][i]
            newboard[row_value][i-1] = '.'
            pikachu_succ_list.append(newboard)
            newboard = copy.deepcopy(board)
            right +=1
            move_count +=1
        elif (board[row_value][i] == '.' and kill_flag == True):
            newboard[row_value][i], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[row_value][i]
            newboard[opp_i][opp_j] = '.'
            pikachu_succ_list.append(newboard)
            newboard = copy.deepcopy(board)
            if right == 0:
                right += 2
            elif right == 2:
                right +=1 
            move_count +=1
        elif (pikachu =='W' and board[row_value][i] in 'bB') or (pikachu =='B' and board[row_value][i] in 'wW') :
            if kill_flag == False: 
                kill_flag = True
            opp_i = row_value
            opp_j = i
            move_count += 1
        elif (pikachu =='W' and board[row_value][i] in 'wW@$') or (pikachu =='B' and board[row_value][i] in 'bB@$'):
                break
    
    return pikachu_succ_list


def successor_of_raichu(board, raichu, row_value, column_value):
    print("in raichuuu")
    raichu_succ_list = []
    newboard = copy.deepcopy(board)

    kill_flag = False
    kill_count = 0
    opp_i = 1000
    opp_j = 1000
    for i in range(row_value-1,-1,-1): # top direction
        if (board[i][column_value] == '.'):
            if (kill_flag == False and kill_count == 0):
                newboard[i][column_value], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][column_value]
                newboard[i+1][column_value] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
            elif (kill_flag == True and kill_count == 0):
                newboard[i][column_value], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][column_value]
                newboard[i+1][column_value] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                newboard[i][column_value], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][column_value]
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][column_value] in 'bB$') or (raichu == '$' and board[i][column_value] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
                opp_i = i
                opp_j = column_value
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[i][column_value] in '@wW') or (raichu == '$' and board[i][column_value] in '$bB')):
            break

    kill_flag = False
    kill_count = 0
    opp_i = 1000
    opp_j = 1000
    for i in range(row_value+1,len(board)): # bottom direction
        if (board[i][column_value] == '.'):
            if (kill_flag == False and kill_count == 0):
                newboard[i][column_value], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][column_value]
                newboard[i-1][column_value] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
            elif (kill_flag == True and kill_count == 0):
                newboard[i][column_value], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][column_value]
                newboard[i-1][column_value] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                newboard[i][column_value], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][column_value]
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][column_value] in 'bB$') or (raichu == '$' and board[i][column_value] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
                opp_i = i
                opp_j = column_value
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[i][column_value] in '@wW') or (raichu == '$' and board[i][column_value] in '$bB')):
            break
    
    kill_flag = False
    kill_count = 0
    opp_i = 1000
    opp_j = 1000
    for i in range(column_value-1,-1,-1): # left direction
        if (board[row_value][i] == '.'):
            if (kill_flag == False and kill_count == 0):
                newboard[row_value][i], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[row_value][i]
                newboard[row_value][i+1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
            elif (kill_flag == True and kill_count == 0):
                newboard[row_value][i], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[row_value][i]
                newboard[row_value][i+1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                newboard[row_value][i], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[row_value][i]
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
        elif (raichu == '@' and board[row_value][i] in 'bB$') or (raichu == '$' and board[row_value][i] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
                opp_i = row_value
                opp_j = i
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[row_value][i] in '@wW') or (raichu == '$' and board[row_value][i] in '$bB')):
            break

        
    kill_flag = False
    kill_count = 0
    opp_i = 1000
    opp_j = 1000
    for i in range(column_value+1,len(board[0])): # right direction
        if (board[row_value][i] == '.'):
            if (kill_flag == False and kill_count == 0):
                newboard[row_value][i], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[row_value][i]
                newboard[row_value][i-1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
            elif (kill_flag == True and kill_count == 0):
                newboard[row_value][i], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[row_value][i]
                newboard[row_value][i-1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                newboard[row_value][i], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[row_value][i]
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
        elif (raichu == '@' and board[row_value][i] in 'bB$') or (raichu == '$' and board[row_value][i] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
                opp_i = row_value
                opp_j = i
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[row_value][i] in '@wW') or (raichu == '$' and board[row_value][i] in '$bB')):
            break
    
    kill_flag = False
    kill_count = 0
    opp_i = 1000
    opp_j = 1000
    for i,j in zip(range(row_value-1, -1, -1),range(column_value-1, -1, -1)): # top-left diagonal
        if (board[i][j] == '.'):
            if (kill_flag == False and kill_count == 0):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[i+1][j+1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
            elif (kill_flag == True and kill_count == 0):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[i+1][j+1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
                opp_i = i
                opp_j = j
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    kill_flag = False
    kill_count = 0
    opp_i = 1000
    opp_j = 1000
    for i,j in zip(range(row_value-1, -1, -1),range(column_value+1,len(board[0]))): # top-right diagonal
        if (board[i][j] == '.'):
            if (kill_flag == False and kill_count == 0):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[i+1][j-1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
            elif (kill_flag == True and kill_count == 0):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[i+1][j-1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
                opp_i = i
                opp_j = j
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    kill_flag = False
    kill_count = 0
    opp_i = 1000
    opp_j = 1000
    for i,j in zip(range(row_value+1,len(board)),range(column_value-1, -1, -1)): # bottom-left diagonal
        if (board[i][j] == '.'):
            if (kill_flag == False and kill_count == 0):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[i-1][j+1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
            elif (kill_flag == True and kill_count == 0):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[i-1][j+1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
                opp_i = i
                opp_j = j
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    kill_flag = False
    kill_count = 0
    opp_i = 1000
    opp_j = 1000
    for i,j in zip(range(row_value+1,len(board)),range(column_value+1,len(board[0]))): # nottom-right diagonal
        if (board[i][j] == '.'):
            if (kill_flag == False and kill_count == 0):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[i-1][j-1] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
            elif (kill_flag == True and kill_count == 0):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                kill_count = 1
            elif (kill_flag == True and kill_count == 1):
                newboard[i][j], newboard[row_value][column_value] = newboard[row_value][column_value], newboard[i][j] 
                newboard[opp_i][opp_j] = '.'
                raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (kill_flag == False):
                kill_flag = True
                opp_i = i
                opp_j = j
            elif (kill_flag == True):
                break
        elif ((raichu == '@' and board[i][j] in '@wW') or (raichu == '$' and board[i][j] in '$bB')):
            break

    return raichu_succ_list

def white_count(board,row_value,column_value):
    if board[row_value][column_value] == 'w':
                return pichu_count(board,board[row_value][column_value], row_value, column_value)
    elif board[row_value][column_value] == 'W':
                return pikachu_count(board,board[row_value][column_value], row_value, column_value)
    elif board[row_value][column_value] == '@':
                return raichu_count(board,board[row_value][column_value], row_value, column_value)

def black_count(board,row_value,column_value):

    if board[row_value][column_value] == 'b':
                return pichu_count(board,board[row_value][column_value], row_value, column_value)
    elif board[row_value][column_value] == 'B':
                return pikachu_count(board,board[row_value][column_value], row_value, column_value)
    elif board[row_value][column_value] == '$':
                return raichu_count(board,board[row_value][column_value], row_value, column_value)

def symbol_count(board, symbol):
    move_count = 0
    for row_value in range(len(board)):
        for column_value in range(len(board[0])):
            if board[row_value][column_value] == symbol:
                move_count += 1
    return move_count

def heuristic_function_1(board):
    nw = symbol_count(board,'w')
    nb = symbol_count(board,'b')
    nW = symbol_count(board,'W')
    nB = symbol_count(board,'B')
    nWR = symbol_count(board,'@')
    nBR = symbol_count(board,'$')
    return (0.4*(nw - nb) + 0.7*(nW - nB) + 1.5*(nWR - nBR))

            
def heuristic_function_2(board):
    #[black move_count, white move_count]
    color_count = [0,0]
    for row_value in range(len(board)):
        for column_value in range(len(board[0])):
            if board[row_value][column_value] == 'w' or board[row_value][column_value] == 'W' or board[row_value][column_value] == '@':
                color_count[1]+= white_count(board, row_value, column_value)
            if board[row_value][column_value] == 'b' or board[row_value][column_value] == 'B' or board[row_value][column_value] == '$':
                color_count[1]+= black_count(board,row_value,column_value)
    
    return color_count

def max_alpha_value(successor,alpha,beta,heuristic_count):
    if heuristic_count==2:
            heuristic_1  = heuristic_function_1(successor)
            heuristic_3 = heuristic_function_2(successor)
            total_heuristic  = heuristic_1 +((heuristic_3[0] - heuristic_3[1])/200)
            return total_heuristic
    else:
        for temp_successor in finding_successor_function(successor):
            alpha = max(alpha,max_alpha_value(temp_successor,alpha,beta,heuristic_count+1))
            if alpha>=beta:
                return alpha
        return alpha

def min_beta_value(successor,alpha,beta,heuristic_count):
    if heuristic_count==2:
            heuristic_1  = heuristic_function_1(successor)
            heuristic_3 = heuristic_function_2(successor)
            total_heuristic  = heuristic_1  +((heuristic_3[0] - heuristic_3[1])/200)
            return total_heuristic
    else:
        for temp_successor in finding_successor_function(successor):
            beta = min(beta,min_beta_value(temp_successor,alpha,beta,heuristic_count+1))
            if alpha>=beta:
                return beta
        return beta

def find_best_move(board,N,player,timelimit):
    alpha = -1 * pow(10,6)
    beta = pow(10,6)
    heuristic_count = 0
    heuristic_values = []

    if player =='b':
        for successor in finding_successor_function(board):
            heuristic_count=0
            heuristic_values.append(max_alpha_value(successor,alpha,beta,heuristic_count))
        return finding_successor_function(board)[heuristic_values.index(min(heuristic_values))]

    if player =='w':
        for successor in finding_successor_function(board):
            heuristic_count=0
            heuristic_values.append(min_beta_value(successor,alpha,beta,heuristic_count))
        return finding_successor_function(board)[heuristic_values.index(max(heuristic_values))]



if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    new_board = board_conversion(board,N)
    for row_value in new_board:
        print(*row_value)
    print("")
    board = find_best_move(new_board, N, player, timelimit)
    for row_value in board:
        print(*row_value)
    print("")
