#!/usr/bin/env python

'''
Update: 2010
    Added extra unnessary comments (that should be self explantory) so
    that it is understandle by new commers

A simple connect 4 game on terminal for 'proof of concept'
Initially wrote to familarize myself with Python - list manipulation exercise
But more importantly, it was meant to be a client-server architect but enthusiasm
dropped after completing the game and some over project took over

Not compatible with Py3 although it should be possible to port it
Just needs to add parenthesis for 'print' and change 'raw_input' to just 'input'
Hopefully, the rest are okay!

Features and Cons:
    Connect 4 game style
    User interface based on command line
    Okay~ish bot AI
    Save the current game state in a file to restart later
    NOT MEANT to be highly efficient
    Incomplete future features :(
    Realised I didn't follow the DRY guidlines properly

Future:
    Client-server architect for playing the game
    GUI
    OO style

author: garbu
'''

from time import sleep
from random import randint
import cPickle, copy

def create_board():
    '''
    This function is just for creating a board which is a 2D list.
    '''
    board = [] #initialize an empty

    #ask user for required size of the board, but can't be less than 4
    #asking for the width size
    width = raw_input("Enter the width of the board: ")
    while width.isdigit() is False or int(width) < 4:
        # endless loop if the user input is not correct
        if width.isdigit() is False:
            print "Invalid input"
        else:
            print "Size less than 4"
        width = raw_input("Enter the width of the board: ")
    print

    # same as the above, asking for the length size
    length = raw_input("Enter the heigth of the board: ")
    while length.isdigit() is False or int(length) < 4:
        if length.isdigit() is False:
            print "Invalid input"
        else:
            print "Size less than 4"
        length = raw_input("Enter the width of the board: ")

    # using the width and length, 2d list is recreated using a for-loop
    for x in range(int(length)):
        board.append(["~"]*int(width))
        # "~" meaning nothing, at least for this game

    #return the board
    return board

def display_board(board):
    '''
    This function displays the 2D list, "board" in a bit nice style
    '''
    width = len(board[0])
    print "\n\t Column number" #tabing the "Column number" text
    print "  |", # add bars next to the numbers ...
    
    #[print "%-2s" % num + "|" for num in range(1, width+1)]
    
    for num in range(1, width+1):
        print ('%-2s') % (num) + "|",
    # using the width of the board, I am adding numbers at the top of the board
                                    # that represents the column no.
    # using '%', I am referencing the 'num' to use 2 spaces from the left,
                                    # indicated by "%-2s", "-" meaning from the left
    
    print
    print " ","="*(int(width*4.2))
    # heading separator, the "width*4.2" is just about ideal for this ...
    
    for row in range(len(board)):
        print ('%-2s') % (str(row+1)) + "|",
        for column in range(len(board[0])):
            print ('%-2s') % (board[row][column]) + "|",
        print
    #this print formatting is the same as above for,
    # "%" is used to reference the space which the corresponding variable may occupy
    # again, "-2s", two spaces from the left
    
def game_draw(board):
    '''
    This function checks whether is game is draw or not, and return a Boolean Value
    accordingly. True meaning game is draw, or False otherwise.
    For connect4 board, only the top row needs to be checked if it is empty or not.
    '''

    check = "~" in board[0]
    if check:
        return False
    else:
        return True
    #so just a simple check,
        #if "~" is still on the top row, then the game is not draw

def get_row(col_no, board):
    '''
    This function returns the row number for the given column no. by the user.
    It checks each row of same column from the bottom. If the coulumn has an empty
    space whether token can be placed, it returns that row number, (index of board)
    '''
    if int(col_no) <= len(board[0]):
        col_no = int(col_no) #since col_no is a string
        row = len(board)-1 #like a loop_counter
        while row >= 0:
            check = board[row][col_no-1] == "~"
            if check:
                return row # if empty row (index position) is found, then no need to
                           # run the loop, so return the row and break it
                break
            row -= 1 #decrease the row (counter) by 1

    return None #return none, if the column is full.

def start_game(players,board,tokens):
    '''
    This is the function where the game is set to run. The 'tokens', containing 'X'
    and 'O', 'players' as a list of two playeres and the 'board' is passed.
    This function is created in this way, so that to play a new game and resuming from
    previous saved game, this same function can be called again and again.

    Here, I am assinging the token 'X' to player1 and 'O' to player2. Player2 can be
    both human or bot, depending on how this function is called.
    '''
    while True: #Continus loop for each player, unless player wins, draw or pause/save.
        
        current_token = tokens[0] #current token is set to the first item on 'token' list
        current_player = players[0]
        #current player is set to the fist element of the 'players' list

        
        display_board(board) #display the board, before playing
        print
        print current_player,"'s turn. The token is '",current_token,"'"
        # telling the user who is the current player and what the token is.

        if current_player == "Computer":
            sleep(1)
            row_no, col_no = computer_move(board) #AI, co-ordinates
            sleep(1)
            print
            print "Computer placed its token in column no.", col_no
            # this 'if' condtional statement is if the player is a bot.
            
        else: #if not bot then:
            print "Enter 'pause' to save this game, anytime!"
            row_no = None
            col_no = raw_input("Enter the column number: ")
            int_check = col_no.isdigit() #check if input is number
            if col_no == "pause":
                # if input is 'pause' then save the current game and end.
                # pause_save(a,b,c,d)
                pause_save(board,current_player,current_token,players)
                print "The game details have been saved\n"
                break #break the top "While Loop itself"
            
            elif int_check: #if user input is number
                row_no = get_row(col_no, board)
                #get the correct row no. on the board to insert the token,
                    # if the column is full, "row_no" gets 'None'

            # while loop for validation.
                #loop if row_no = False
                #loop if int_check = False
                #loop if input is not in range
            while (int_check is False) or row_no is None or (int(col_no)>= len(board)+1) or (int(col_no) <= 0):
                print "Invalid input detected!\n"
                # display some appropriate error messages
                
                # repeat the above again
                print "Enter 'pause' to save this game, anytime!"
                col_no = raw_input("Enter the column number: ")
                int_check = col_no.isdigit()
                if col_no == "pause":
                    pause_save(board,current_player,current_token,players)
                    print current_player,current_token
                    print "The game details have been saved\n"
                    break
                elif int_check:
                    row_no = get_row(col_no, board)
                    
            
            if col_no == "pause":
                break #break the top level, "While Loop itself"

        # now that both indices for the board, (row and column no)
            # has been calculated, it is time to put it into the board

        # int(col_no) because 'col_no' is a string,
            # and '-1' because index starts from 0, but the user is using the
                                            # column no. at the top to reference
        board[row_no][int(col_no) - 1] = current_token
        
        draw = game_draw(board)
        winner,coordinates = check_winner(board)
        # each time a token is inserted, the board is checked if it is draw
                                            # or if there is any winner

        #'game_draw(?) returns a Boolean value to indicated draw or not
        #'check_winner(?) returns a Boolean value, and the 4 matched coordinates
                                 # to indicated win if there is,
                                 # else 'None'
                                            
        
        if draw or winner:
            # if there is either one of them then, display the board for the last time.
            display_board(board)
            print
            if winner:
                print current_player, "won this game"
                print 'with the following 4 matched co-ordinates'
                print coordinates
            elif draw:
                print "Game draw"

            break #break the top level While loop if draw or win found.

        # Each the player token has been inserted,
                    # items in 'tokens' and 'players' list are swaped.
        tokens[0],tokens[1] = tokens[1],tokens[0]
        players[0],players[1] = players[1],players[0]

    # if the while loop is broken:
    print
    print "-"*40
    print "Game ended"
    print "-"*40, "\n"

def pause_save(board,current_player,token,players):
    '''
    This function saves the game details so that the game can be resumed or
    restarted next time. A dictionary is created that contains the 'board' itself,
    'players' list, 'current_player' and 'current_player'
    '''
    game_details = {"board":board, "playerTurn": current_player, "token":token, "bothPlayers": players}

    # any files that had a game saved before is over written.
    f = open("saved-game.dat", "wb")
    cPickle.dump(game_details,f)
    f.close()
    
        
def check_winner(board):
    '''
    This is the function that check if the board has a winner and returns the
    4 matched coordinates on the board. If there is none so far, a Boolean value
    "False" and "None" value coordinates is passed to which ever function has called it.

    The simple conditional statements can tell how it is checking from winnners.
    It first checks for any winner, horizontally for all rows.
    If it fails, then it checks all the columns vertically.
    If that also fails, it checks for any diagonal wins.
    If all the above check fails, then that means there is no winner so far.
    '''
    coordinates = None #initializing coordinates as fails, at the start.

    # all the funcitons:
            #horizontal_check(board)
            #vertical_check(board)
            #diagonal_check(board)
        # returns a tuple.
            # the first item in that tuple is 'Boolean Value' True/False
                #to indicated winner, and
            # the other is list of 4 matched coordinates, if there is any winner

    # step by step check
    horizontal_win = horizontal_check(board)
    if horizontal_win[0]:
        coordinates = horizontal_win[1]
    else:
        vertical_win = vertical_check(board)
        if vertical_win[0]:
            coordinates = vertical_win[1]
        else:
            diagonal_win = diagonal_checks(board)
            if diagonal_win[0]:
                coordinates = diagonal_win[1]

    # if either checks calculated a winner, then return "True" and its coordinates.
    if horizontal_win[0] or vertical_win[0] or diagonal_win[0]:
        return True, coordinates

    # return False and None if there is no winners so far.
    else:
        return False, coordinates
    
def horizontal_check(board):
    coordinates = None #initialize coordinates to False
    tokens = ['X','O']
    row = 0 #initialize 'row' (loop counter) to zero
    while row < len(board):
        column = 0 #initialize 'column' (loop counter) to zero
        while column < len(board[0]):
            try:
                #each time I am incrementing the next four columns for a matched token
                #the check could go out-of-bound,
                    # so 'try' is used to error handle
                
                #very long statement
                check = (board[row][column] in tokens) \
                    and (board[row][column] == board[row][column+1]) \
                    and (board[row][column+1] == board[row][column+2]) \
                    and (board[row][column+2] == board[row][column+3])
                # if match is found then break, no need to run the loop anymore
                if check:
                    break

            # If there check went out-of-bound, then let the loop run again
                    #with next incremented loop counter.
            except IndexError:
                pass #do nothing

            column += 1 #increment
            
        if check:
            # if match found, break and store the current indices of the board
            # here, '+1' is added to row
                # and '+1,+2,+3,+4' is added to coulmn so the user can see it clearly.
            coordinates = [(row+1,column+1),(row+1,column+2),(row+1,column+3),(row+1,column+4)]
            break
        
        row += 1 #increment
        
    return check, coordinates #return the results
    
def vertical_check(board):
    #This function is exactly the same as "horizontal_check"
                    # just in opposite way

    coordinates = None
    #vertical check
    tokens = ['X','O']
    row = 0
    while row < len(board[0]):
        column = 0
        while column < len(board):
            try:
                #check for 4 matched indices vertically.
                check = (board[row][column] in tokens) \
                    and (board[row][column] == board[row+1][column]) \
                    and (board[row+1][column] == board[row+2][column]) \
                    and (board[row+2][column] == board[row+3][column])
                if check:
                    break
            except IndexError:
                pass #do nothing and continue the loop
            column += 1
        if check:
            coordinates = [(row+1,column+1),(row+2,column+1),(row+3,column+1),(row+4,column+1)]
            break
        row += 1

    return check, coordinates

def diagonal_checks(board):
    '''
    This function checks for any diagonal winners. It checks diagionally from left-to-right
    first. If it fails, then it does any diagonal check, from right-to-left.
    If both fail, it return 'False' and 'None' to indicate winner and coordinates respectively.
    '''

    # step by step check
    win_1 = diagonal_1(board)
    if not win_1[0]:
        win_2 = diagonal_2(board)
        
    if win_1[0] or win_2[0]:
        if win_1[0]:
            return win_1
        else:
            return win_2

    # if both checks fails ...
    else:
        return False,None

    
def diagonal_1(board):
    '''
    This function checks for winner diagonally from left-to-right.
    The loop and check structure is similar to every checks.
    '''
    
    coordinates = None
    tokens = ['X','O']
    row = 0
    while row < len(board):
        column = 0
        while column < len(board[0]):
            try:
                check = (board[row][column] in tokens) \
                    and (board[row][column] == board[row+1][column+1]) \
                    and (board[row+1][column+1] == board[row+2][column+2]) \
                    and (board[row+2][column+2] == board[row+3][column+3])
                if check:
                    break
            except IndexError:
                pass
            column += 1
        if check:
            coordinates = [(row+1,column+1),(row+2,column+2),(row+3,column+3),(row+4,column+4)]
            break
        row += 1

    return check, coordinates

def diagonal_2(board):
    '''
    This function checks for winner diagonally from right-to-left.
    Very is similar to every other checks ...
    '''
    
    coordinates = None
    # diagonal from left to right
    tokens = ['X','O']
    row = 0
    while row < len(board):
        column = len(board[0])-1
        while column >= 0:
            try:
                check = (board[row][column] in tokens) \
                    and(board[row][column]==board[row+1][column-1]) \
                    and (board[row+1][column-1]==board[row+2][column-2]) \
                    and (board[row+2][column-2]==board[row+3][column-3]) \
                    and (column-3) >= 0
                if check:
                    break
            except:
                pass
            column -= 1
        if check:
            coordinates =[(row+1,column+1),(row+2,column),(row+3,column-1),(row+4,column-2)]
            break
        row += 1
    
    return check, coordinates

def initialize_game(value):
    '''
    This is the function that runs before the start of the game. It has a parameter,
    which is an integer it receives from the option of the 'menu' displayed at the very start
    of the game.
    This parameter is used to specify how to run the game, "start_game(a,b,c)".
    '''

    tokens = ["X","O"]
    answer = ""
    expected_ans = ["Y","N","y","n"]
    while answer not in expected_ans: #top level while loop

        # if value is 3, then it means the game needs to be restarted.
        if value == 3:
            try: #try reading an existiing file,
                    # if possible, then get the details and run the game.
                f = open("saved-game.dat", "rb")
                game_details = cPickle.load(f)
                f.close()

                # game_details is a dictionary type.

                # retrieve every values this dictionary has.
                board = game_details["board"]
                current_player = game_details["playerTurn"]
                current_token = game_details["token"]
                players = game_details["bothPlayers"]

                # since the game always, starts with 'token[0]'
                    # so there is a need to check if the saved token is at
                    # token[0]. If not then swap.
            
                if tokens[1] == current_token:
                    tokens[0],tokens[1] = tokens[1],tokens[0]
                # this swap is very issential, so to restart the game in the way
                        # it was left off before.

                start_game(players,board,tokens) #and run the game...

            # error handling, if there is no file in the game directory.
            except IOError:
                print "No saved game file"
                # display some error message to the user"

        # if the value is not 3, then
        # game is going to be played.
        else:
            player_one = get_PlayerOne()
            print
            player_two = get_PlayerTwo(value)
            # get names of player1 and player2.
                #get_PlayerTwo(a), has a same 'value', integer parameter.
                # now, this is used here, to check whether the player2 should
                                            # be human or a bot.
            
            print "\nPlayer1'", player_one, "' is given 'X' token"
            print "and"
            print "Player2 '", player_two, "' is given 'O' token\n"
            # display what players are assigned what tokens
            sleep(1) #pause a second so that the user can see what their tokens are.
            board = create_board() #create the board.

            # create playerlist and pass to the 'start_game(?,?,?)'.
            players = [player_one,player_two]

            start_game(players,board,tokens) #and run the game...

        # These lines are for check whether the user wants to start a new game or not,
                #so to either continue the loop each the game is finished,
                        # or break it if the user wants to end the game.

        print
        print "Start a new game: ?"
        answer = raw_input("Enter 'y' for yes and 'n' for no: ")
        # ask user for an input.
        
        while answer not in expected_ans:
            # expected_ans has ["Y","N","y","n"]
            # keep looping if the input is not in the 'expected_ans' list
            
            print answer, "not recognised"
            answer = raw_input("Enter 'y' for yes and 'n' for no: ")
            # display an error message and ask again.
            
        if answer == "N" or answer == "n":
            # if the answer is not then break the top level while loop.
            break
        elif answer == "Y" or answer == "y":
            main() #run the first main function again, if the user wants to
                   #play a new game.

def next_move(board, token):
    '''
    This is the (AI part) function that computer uses to check the possible next moves
    (of the player or for itself) and see if the predicted next move
    can win the game.
    Therefore, 'token' also passed here as a parameter along with the 'board'
    to check for next possible move of the token.
    '''
    
    column = 0
    while column < len(board[0]):
        # each time I run a loop, I am copying the original board
        # to a temporary board.

        # and I am using the temporary to check for possible moves without affecting
        # the original board.
        #temp_board = list(board)
        temp_board = copy.deepcopy(board) # do a deep copy to study

        # I repeat just to clarify:
            #'get_row' returns the index position on the board that is empty (from the bottom)
                    #of the given 'column' parameter.
        
            # 'column+1' is passed here, because the 'get_row' function was initially
                #designed to handle the user column no. which is always +1 more.
        row_no = get_row(column+1,temp_board)#return False, row

        if row_no is None:
            # the row of the column in the board can be full, so row_no is None,
                # do nothing and just let loop continue.
            pass

        else:

            # put the 'token' into the temporary board and check if the
                # it can win...
            temp_board[row_no][column] = token
            win = check_winner(temp_board)[0]

            if win:
                # if it is possible to win from the predicted move, break the loop.
                break
            else:
                pass
        column += 1
        
    if win:
        # so if it possible to win, get the coordinates of the board that can win.
        return True, (row_no,column+1)
    
    else:
        # if all the possible next move produces no win, at all
                # return False and None.
        return False, None

def computer_move(board):
    '''
    This returns the coordinate of token, the bot places on the board.
    Each time this function is called, it tries to check if it can win. If it is possible
    to win then it will return the corresponding coordinates for the board.

    If there is no way for the bot to win, it tries to check if the human can win, using the
    same algorithm as above, 'next_move(?,?)' for the next possible moves.
    If the human player has possible way of winning,
        then return the corresponding coordinates to block to win.
    This doesn't mean that the bot is impossible to defeat. If the human has two or more
        ways to winn the game, the bot will block the first possible way.

    If the above both fails (no winner produces), it inserts a random number into the board.

    This is for the bot for this game.
    '''
    
    # since player2/computer is always asign with 'O' token
        # this token can be passed to 'next_move() to see if this token can win.
    win_check = next_move(board, 'O')
    if win_check[0]:
        print "The computer has found out a way of winning!"
        row_no, col_no = win_check[1]

        # return the coordinate that allow computer to win.
        return row_no, col_no
    else:
        # if no win for computer then, check if player can win.
        # player1 is always asign with 'X' token
        # so 'O' is passed to 'next_move() to see if this token can win.
        block_check = next_move(board, 'X')
        if block_check[0]:
            print "The bot blocked one of the way for you to win!"
            row_no, col_no = block_check[1]

            # return the coordinate that computer can block the player from winning.
            return row_no, col_no

        # if the above fails, insert token into a random column.
        else:
            total_column = len(board[0])
            col_no = randint(0,total_column-1)
            # generate a random number.
            print "Bot selected a %d column!" % col_no
            
            check = "~" in board[0][col_no]
            # check if the the random column no is full or not.
            # if it full, try with another random
            while check == False:
                col_no = randint(0,total_column-1)
                check = "~" in board[0][col_no]

            # get the correct row no. of the current column number.
            # with this loop
            row_no = len(board)-1
            while row_no >= 0:
                check2 = board[row_no][col_no] == "~"
                if check2:
                    break
                row_no -= 1

        # return the bot coordinates.
        return row_no, col_no+1

def get_PlayerOne():
    '''
    This gets the player1 name and returns it.
    '''
    print "Player 1"
    PlayerOne = raw_input("Enter your name: ")
    # if invalid, ask again and again using while loop
    while PlayerOne == "" or PlayerOne.isalpha() is False:
        print "Empty or invalid name"
        PlayerOne = raw_input("Enter your name: ")
    return PlayerOne

def get_PlayerTwo(value):
    '''
    This function gets the player2 name and returns it.
    Using the value as an integer parameter, it
        can assign player2 as computer of 'value' = 2
    '''
    if value == 2:
        PlayerTwo = "Computer"
    else:
        print "Player 2"
        PlayerTwo = raw_input("Enter your name: ")
        while PlayerTwo == "" or PlayerTwo.isalpha() is False:
            # if invalid, ask again and again using while loop
            print "Empty or invalid name"
            PlayerTwo = raw_input("Enter your name: ")

    # return PlayerTwo name,
        #which is either "Computer" or some name given by the human
    return PlayerTwo

def menu():
    '''
    This is the menu that starts right at the start of the program.
    '''
    print"""
                            CONNECT4
                    ---------------------------
                    Select Options
                    ---------------------------
                    >>(1) Play with your friend
                    >>(2) Play with a bot
                    >>(3) Resume . . . from last saved game?
                    ............................
                    >>(4) Exit the game
    """
 
def main():
    '''
    This is function nagivates the user to correct places in the program
    by the option provided by the user.
    '''
    menu()
    option = raw_input('Enter option >> ')
    while (option.isdigit() == False) or (int(option) > 4) or (int(option) <= 0):
        # loop if invalid user input is detected ! ! !
        if option.isdigit() is False:
            print "Invalid characters"
        else:
            print "Option not in range"
        print
        option = raw_input('Enter option >>')

    if int(option) == 4:
        # '4' means to exit so do nothing.
        pass
    else:
        initialize_game(int(option))

if __name__ == "__main__":
    main() #run the main function that needs to run first
