# %%
import pygame as pg
import numpy as np
import copy

def getUp(myPosition):
	return [myPosition[0] - 1, myPosition[1]]
def getDown(myPosition):
	return [myPosition[0] + 1, myPosition[1]]
def getRight(myPosition):
	return [myPosition[0], myPosition[1] + 1]
def getLeft(myPosition):
	return [myPosition[0], myPosition[1] - 1]
def getUpLeft(myPosition):
	return [myPosition[0] - 1, myPosition[1] - 1]
def getUpRight(myPosition):
	return [myPosition[0] - 1, myPosition[1] + 1]
def getDownLeft(myPosition):
	return [myPosition[0] + 1, myPosition[1] - 1]
def getDownRight(myPosition):
	return [myPosition[0] + 1, myPosition[1] + 1]
def negate(board_position):
    for row in board_position:
        for i in range(len(row)):
            row[i] = -1 * row[i]
    return board_position

class Board():
	def __init__(self, current_player):
		#self.screen_resolution = 400
		self.size = 8
		#Initialize images against corresponding key
		self.board_images = dict()
		self.initialize_dictionary()
		#Initialize the board
		self.board_position = np.zeros((8, 8))
		self.initialize_position()
		self.player_color = current_player
		self.human_player = "White"
		self.selected_piece = None
		self.selected_piece_moves = None
		self.weightage = {1: 1000, 2: 9, 5: 5, 3: 3, 4: 3, 6: 1}

	def initialize_dictionary(self):
		self.board_images[1] = "White_Pieces\wK.png"
		self.board_images[2] = "White_Pieces\wQ.png"
		self.board_images[3] = "White_Pieces\wB.png"
		self.board_images[4] = "White_Pieces\wN.png"
		self.board_images[5] = "White_Pieces\wR.png"
		self.board_images[6] = "White_Pieces\wp.png"

		self.board_images[-1] = "Black_Pieces\\bK.png"
		self.board_images[-2] = "Black_Pieces\\bQ.png"
		self.board_images[-3] = "Black_Pieces\\bB.png"
		self.board_images[-4] = "Black_Pieces\\bN.png"
		self.board_images[-5] = "Black_Pieces\\bR.png"
		self.board_images[-6] = "Black_Pieces\\bp.png"
	def initialize_position(self):
		board_position=[[-5,-4,-3,-2,-1,-3,-4,-5],
						[-6,-6,-6,-6,-6,-6,-6,-6],
					  	[0,0,0,0,0,0,0,0],
					  	[0,0,0,0,0,0,0,0],
					  	[0,0,0,0,0,0,0,0],
					  	[0,0,0,0,0,0,0,0],
					  	[6,6,6,6,6,6,6,6],
					  	[5,4,3,2,1,3,4,5]]
		self.board_position = np.array(board_position)
	
	#Checks validity of cell (True, 0), check if enemy lies there (True, -1)
	def valid_path(self, position):
		if ( position[0] < 0 or position[0] > self.size - 1 ):
			return False,0
		elif ( position[1] < 0 or position[1] > self.size - 1 ):
			return False,0
		elif (self.board_position[position[0]][position[1]] == 0 ):
			return True,0
		if self.player_color == "White":
			if (self.board_position[position[0]][position[1]] > 0 ):
				return False,0
			else:
				return True,-1
		else:
			if (self.board_position[position[0]][position[1]] < 0 ):
				return False,0
			else:
				return True,-1	

	def generate_bishop_moves(self, current_position):
		moves = []

		#Checking all possible movies in UpLeft direction
		temp_position = current_position
		possible = True
		value = 0
		while possible == True and value == 0:
			temp_position = getUpLeft(temp_position)
			possible, value = self.valid_path(temp_position)
			if possible == True:
				moves.append(temp_position)
		
		#Checking all possible movies in UpRight direction
		temp_position = current_position
		possible = True
		value = 0
		while possible == True and value == 0:
			temp_position = getUpRight(temp_position)
			possible, value = self.valid_path(temp_position)
			if possible == True:
				moves.append(temp_position)

		#Checking all possible movies in DownLeft direction
		temp_position = current_position
		possible = True
		value = 0
		while possible == True and value == 0:
			temp_position = getDownLeft(temp_position)
			possible, value = self.valid_path(temp_position)
			if possible == True:
				moves.append(temp_position)

		#Checking all possible movies in DownRight direction
		temp_position = current_position
		possible = True
		value = 0
		while possible == True and value == 0:
			temp_position = getDownRight(temp_position)
			possible, value = self.valid_path(temp_position)
			if possible == True:
				moves.append(temp_position)
				
		return moves

	def generate_rook_moves(self, current_position):
		moves = []
		#Checking all possible movies in upper direction
		temp_position = current_position
		possible = True
		value = 0
		while possible == True and value == 0:
			temp_position = getUp(temp_position)
			possible, value = self.valid_path(temp_position)
			if possible == True:
				moves.append(temp_position)

		#Checking all possible movies in lower direction
		temp_position = current_position
		possible = True
		value = 0
		while possible == True and value == 0:
			temp_position = getDown(temp_position)
			possible, value = self.valid_path(temp_position)
			if possible == True:
				moves.append(temp_position)

		#Checking all possible movies in right direction
		temp_position = current_position
		possible = True
		value = 0
		while possible == True and value == 0:
			temp_position = getRight(temp_position)
			possible, value = self.valid_path(temp_position)
			if possible == True:
				moves.append(temp_position)

		#Checking all possible movies in left direction
		temp_position = current_position
		possible = True
		value = 0
		while possible == True and value == 0:
			temp_position = getLeft(temp_position)
			possible, value = self.valid_path(temp_position)
			if possible == True:
				moves.append(temp_position)
		return moves

	def generate_king_moves(self, current_position):
		moves = []

		possible, value = self.valid_path( getUp(current_position))
		if possible == True:
			moves.append(getUp(current_position))
		possible, value = self.valid_path(getDown(current_position))
		if possible == True:
			moves.append(getDown(current_position))
		possible, value = self.valid_path(getLeft(current_position))
		if possible == True:
			moves.append(getLeft(current_position))
		possible, value = self.valid_path(getRight(current_position))
		if possible == True:
			moves.append(getRight(current_position))

		possible, value = self.valid_path(getUpLeft(current_position))
		if possible == True:
			moves.append(getUpLeft(current_position))
		possible, value = self.valid_path(getUpRight(current_position))
		if possible == True:
			moves.append(getUpRight(current_position))
		possible, value = self.valid_path(getDownLeft(current_position))
		if possible == True:
			moves.append(getDownLeft(current_position))
		possible, value = self.valid_path( getDownRight(current_position))
		if possible == True:
			moves.append(getDownRight(current_position))
		
		return moves
	
	def generate_queen_moves(self, current_position ):
		moves_diagonal = self.generate_bishop_moves(current_position)
		moves_straight = self.generate_rook_moves(current_position)
		return moves_diagonal + moves_straight

	def in_bounds(self, position):
		if ( position[0] < 0 or position[0] > self.size - 1 ):
			return False
		elif ( position[1] < 0 or position[1] > self.size - 1 ):
			return False
		return True
	def generate_pawn_moves(self, current_position,):
		moves = []
		if self.player_color == "White":
			#Check up left
			temp_position = getUpLeft(current_position)
			if self.in_bounds(temp_position) and self.board_position[temp_position[0]][temp_position[1]] < 0:
				moves.append(temp_position)
			#Check up right
			temp_position = getUpRight(current_position)
			if self.in_bounds(temp_position) and self.board_position[temp_position[0]][temp_position[1]] < 0:
				moves.append(temp_position)
			#Front position is empty
			temp_position = getUp(current_position)
			if self.in_bounds(temp_position) and self.board_position[temp_position[0]][temp_position[1]] == 0:	
				possible, value = self.valid_path(getUp(current_position))
				if possible == True:
					moves.append(getUp(current_position))
					if value == -1:
						return moves
				if current_position[0] == 6:
					current_position = getUp(current_position)
					#print(getUp(current_position))
					possible, value = self.valid_path(getUp(current_position))
					if possible == True:
						moves.append(getUp(current_position))
		else:
			#Check up left
			temp_position = getDownLeft(current_position)
			if self.in_bounds(temp_position) and self.board_position[temp_position[0]][temp_position[1]] > 0:
				moves.append(temp_position)
			#Check up right
			temp_position = getDownRight(current_position)
			if self.in_bounds(temp_position) and self.board_position[temp_position[0]][temp_position[1]] > 0:
				moves.append(temp_position)
			#Front position is empty
			temp_position = getDown(current_position)
			if self.in_bounds(temp_position) and self.board_position[temp_position[0]][temp_position[1]] == 0:
				#print(getUp(current_position))
				possible, value = self.valid_path(getDown(current_position))
				if possible == True:
					moves.append(getDown(current_position))
					if value == -1:
						return moves
				if current_position[0] == 1:
					current_position = getDown(current_position)
					#print(getUp(current_position))
					possible, value = self.valid_path(getDown(current_position))
					if possible == True:
						moves.append(getDown(current_position))
		return moves
	
	def generate_knight_moves(self, current_position):
		moves = []

		#Up
		possible, value = self.valid_path(getLeft(getUp(getUp(current_position))) )
		if possible == True:
			moves.append(getLeft(getUp(getUp(current_position))))
		possible, value = self.valid_path(getRight(getUp(getUp(current_position))))
		if possible == True:
			moves.append(getRight(getUp(getUp(current_position))))
		#Left
		possible, value = self.valid_path(getUp(getLeft(getLeft(current_position))))
		if possible == True:
			moves.append(getUp(getLeft(getLeft(current_position))))
		possible, value = self.valid_path(getDown(getLeft(getLeft(current_position))))
		if possible == True:
			moves.append(getDown(getLeft(getLeft(current_position))))
		#Right
		possible, value = self.valid_path(getUp(getRight(getRight(current_position))))
		if possible == True:
			moves.append(getUp(getRight(getRight(current_position))))
		possible, value = self.valid_path(getDown(getRight(getRight(current_position))))
		if possible == True:
			moves.append(getDown(getRight(getRight(current_position))))
		#Down
		possible, value = self.valid_path(getLeft(getDown(getDown(current_position))))
		if possible == True:
			moves.append(getLeft(getDown(getDown(current_position))))
		possible, value = self.valid_path(getRight(getDown(getDown(current_position))))
		if possible == True:
			moves.append(getRight(getDown(getDown(current_position))))

		return moves

	"""Takes the coordiante as input, checks if coordinate piece 
	matches the current player color value, that is if 
	player_color is Black, then checks if piece is negative, then
	generates its move, vice versa for white player, 
	-----player_color is crucial here----------------""" 
	def generate_valid_path_list(self, current_position):
		#"White" represents positive number
		#"Black" represents negative number
		moves = []
		#find the current position piece
		piece = self.board_position[current_position[0]][current_position[1]]
		if self.player_color == "Black":
			if piece == -1:
				moves = self.generate_king_moves(current_position)
			elif piece == -2:
				moves = self.generate_queen_moves(current_position)
			elif piece == -3:
				moves = self.generate_bishop_moves(current_position)
			elif piece == -4:
				moves = self.generate_knight_moves(current_position)
			elif piece == -5:
				moves = self.generate_rook_moves(current_position)
			elif piece == -6:
				moves = self.generate_pawn_moves(current_position)
			
		else:
			if piece == 1:
				moves = self.generate_king_moves(current_position)
			elif piece == 2:
				moves = self.generate_queen_moves( current_position)
			elif piece == 3:
				moves = self.generate_bishop_moves(current_position)
			elif piece == 4:
				moves = self.generate_knight_moves(current_position)
			elif piece == 5:
				moves = self.generate_rook_moves(current_position)
			elif piece == 6:
				moves = self.generate_pawn_moves( current_position)
		return moves

	#Takes the move list as input, check if any coordinate in move will cause check state, remove that coordinate and return the new moves list, needs to be called after we are generating move for any individual piece		
	def remove_check_moves(self,current_position,moves):
		for move in reversed(moves):
			if self.bad_move(current_position, move) == True:
				moves.remove(move)
		return moves
	#Takes the current position and new position as input, checks
	#if movement from current position to new position causes our player to be in check state
	#This function is called by remove check moves
	#player_color dxetermines for which player we are checking check state
	def bad_move(self, current, new):
		current_piece = self.board_position[current[0]][current[1]]
		new_piece = self.board_position[new[0]][new[1]]

		#print(f"New position is : {new}")
		check_move = False
		self.move_piece(new, current)

		check_move = self.evaluate_check()
		self.board_position[current[0]][current[1]] = current_piece
		self.board_position[new[0]][new[1]] = new_piece

		return check_move

	#Returns the corrdinate of specific color king
	def find_king(self, color):
		if color == "Black":
			for i in range (0, 8):
				for j in range(0, 8):
					if self.board_position[i][j] == -1:
						return [i, j]
		else:
			for i in range (0, 8):
				for j in range(0, 8):
					if self.board_position[i][j] == 1:
						return [i, j]
	
	#Returns all the possible moves for current player - White or Black
	def get_all_moves(self):
		moves = []
		if self.player_color == "White":
			for i in range(0, 8):
				for j in range(0, 8):
					if self.board_position[i][j] > 0:
						moves += self.generate_valid_path_list([i,j])
		else:
			for i in range(0, 8):
				for j in range(0, 8):
					if self.board_position[i][j] < 0:
						moves += self.generate_valid_path_list([i,j])
		return moves
	
	#Check condition movement---If we have check condition that means if our king is in danger this function checks whether we can make any move to save our king or not
	#Returns true if we can
	#Return false if we can't save our king, that is checkmate from enemy
	#It only checks for valid king move, not for other pieces
	def check_movement(self) ->bool:
		if self.player_color == "Black":
			#Find black player king
			#Check for its possible moves
			King = self.find_king("Black")
			KingMoves = self.generate_valid_path_list(King)
			#print(f"All king moves are : {KingMoves}")
			#Now iterate all enemy pieces and get their moves and check if any of the king move is countered by those moves, then remove that move from king move, if none move is left, then its checkmate from enemy
			self.player_color = "White"
			all_enemy_moves = self.get_all_moves()

			for moves in reversed(KingMoves):
				if moves in all_enemy_moves:
					KingMoves.remove(moves)
			self.player_color = "Black"
			#if there is move left then player can move on that place only, change the selected piece to king and 
			if len(KingMoves) > 0:
				self.selected_piece = King
				#print(f"King moves are {KingMoves}")
				self.selected_piece_moves = KingMoves
				return True
		else:
			#Find black player king
			#Check for its possible moves
			King = self.find_king("White")
			KingMoves = self.generate_valid_path_list(King)
			#Now iterate all enemy pieces and get their moves and check if any of the king move is countered by those moves, then remove that move from king move, if none move is left, then its checkmate from enemy
			self.player_color = "Black"
			all_enemy_moves = self.get_all_moves()

			for moves in reversed(KingMoves):
				if moves in all_enemy_moves:
					KingMoves.remove(moves)
			self.player_color = "White"
			#if there is move left then player can move on that place only, change the selected piece to king and 
			if len(KingMoves) > 0:
				self.selected_piece = King
				self.selected_piece_moves = KingMoves
				return True
		return False
	
	#Check if there is enemy king on parameter position
	#Return trues if there is
	#Returns false if there isn't
	def enemy_king(self, position):
		if self.player_color == "White":
			if self.board_position[position[0]][position[1]] == -1: 
				return True
		else:
			if self.board_position[position[0]][position[1]] == 1: 
				return True
		return False
	#Updates the player_color
	def next_turn(self):
		if self.player_color == "White":
			return "Black"
		return "White"
	#Check - selection --- This function only allows those movement which are anti-checks
	#Inputs the user click coordinate
	#if coordinate is of only allowed movement of kings (from check movement function then updates the position and set the turn to next player, else ignores the click)
	def check_selection(self):
		pos = pg.mouse.get_pos()
		#Human clicked while Ai is making its move
		#Ignore the click
		#if self.human_player != self.player_color:
			#return False
		
		#Getting current box positions
		#self.previous_selected_piece = self.selected_piece
		selected_box = [-1, -1]
		selected_box[1] = int(pos[0]/ 50)
		selected_box[0] = int(pos[1]/ 50)

		print(f"Pieces are {self.selected_piece_moves}")
		if selected_box in self.selected_piece_moves:
			#Move the piece
			self.move_piece(selected_box, self.selected_piece)
			#Reset the click
			self.selected_piece = None
			self.selected_piece_moves = None
			self.player_color = self.next_turn()
	#Piece movement operation
	#This function is of user movement in board, check if user can made a valid move, we can remove else part code when bot is implemented, since we will be manually sticking to white color for human player, also uncomment the human """
	# #if self.human_player != self.player_color:
			#return False"""
	#This will ignore any click from user
	def selection_and_movement(self):

		pos = pg.mouse.get_pos()
		#Human clicked while Ai is making its move
		#Ignore the click
		#if self.human_player != self.player_color:
			#return False
		
		#Getting current box positions
		#self.previous_selected_piece = self.selected_piece
		selected_box = [-1, -1]
		selected_box[1] = int(pos[0]/ 50)
		selected_box[0] = int(pos[1]/ 50)
		
		if self.player_color == "White":
			#This code is for white piece
			#New clicked, generate all possible moves from current position
			#if self.previous_selected_piece == None:
			if self.selected_piece == None and self.board_position[selected_box[0]][selected_box[1]] > 0:
				self.selected_piece_moves = self.generate_valid_path_list(selected_box)
				self.selected_piece = selected_box
				self.selected_piece_moves = self.remove_check_moves(self.selected_piece , self.selected_piece_moves)
			#Previously selected piece and Newly selected piece is a valid move
			elif self.selected_piece != None and selected_box in self.selected_piece_moves:
				#Check for checkmate
				print(f"Selected box is {selected_box}")
				if ( self.enemy_king(selected_box) == True):
					print("Game ended, Black king died")
					return True
				#Move the piece
				self.move_piece(selected_box, self.selected_piece)
				#Reset the click
				self.selected_piece = None
				self.selected_piece_moves = None
				#Update the player turn here, since one user has made the move
				self.player_color = "Black"
			else:
				#Reset the click
				self.selected_piece = None
				self.selected_piece_moves = None
		else:
			#This code is for black piece
			#New clicked, generate all possible moves from current position
			#if self.previous_selected_piece == None:
			if self.selected_piece == None and self.board_position[selected_box[0]][selected_box[1]] < 0:
				self.selected_piece_moves = self.generate_valid_path_list(selected_box)
				self.selected_piece = selected_box
				self.selected_piece_moves = self.remove_check_moves(self.selected_piece , self.selected_piece_moves)
			#Previously selected piece and Newly selected piece is a valid move
			elif self.selected_piece != None and selected_box in self.selected_piece_moves:
				#Check for checkmate
				print(f"Selected box is {selected_box}")
				if ( self.enemy_king(selected_box) == True):
					print("Game ended, White king died")
					return True
				#Move the piece
				self.move_piece(selected_box, self.selected_piece)
				#Reset the click
				self.selected_piece = None
				self.selected_piece_moves = None
				#Update the player turn here, since one user has made the move
				self.player_color = "White"
			else:
				#Reset the click
				self.selected_piece = None
				self.selected_piece_moves = None
		return False	
	#Moves the piece from old_position to new positions, sets the old psoition to 0, perform any calculation if required here, since this function will overwrite the enemy piece in case
	#Also pawn updation needs to be implemented here
	def move_piece(self, new_position, old_position):
		self.board_position[new_position[0]][new_position[1]] = self.board_position[old_position[0]][old_position[1]]
		self.board_position[old_position[0]][old_position[1]] = 0

		#Check here if the movement was of pawn, if it was pawn, did it move to the other possible least row, make the pawn queen
		if self.board_position[new_position[0]][new_position[1]] == 6 and self.player_color == "White" and new_position[0] == 0:
			self.board_position[new_position[0]][new_position[1]] = 2
		elif self.board_position[new_position[0]][new_position[1]] == -6 and self.player_color == "Black" and new_position[0] == 7:
			self.board_position[new_position[0]][new_position[1]] = -2
	#Creates the copy of the board, will be required for bot
	def copy_board(self):
		new_board = Board(self.player_color)
		for i in range (0, 8):
			for j in range(0, 8):
				new_board.board_position[i][j] = self.board_position[i][j]
		new_board.selected_piece = self.selected_piece
		new_board.selected_piece_moves = self.selected_piece_moves
		return new_board
	#Returns the white king position
	def get_king_position(self):
		for i in range(0, 8):
			for j in range(0, 8):
				if self.board_position[i][j] == 1:
					return [i,j]
		return [-1,-1]

	#Calculates the total score of the specified color pieces
	def evaluation_score(self, color):
		score = 0

		if color == "Black":
			negate(self.board_position)

		for i in range(0, 8):
			for j in range(0, 8):
				if self.board_position[i][j] > 0:
					score += self.weightage[self.board_position[i][j]]
		
		if color == "Black":
			negate(self.board_position)
		
		return score
	#Check if we are in check state, that is our king can be attacked by one of the enemy piece
	def evaluate_check(self):
		check = False
		if self.player_color == "Black":
			King = self.find_king("Black")
			self.player_color = "White"
			all_enemy_moves = self.get_all_moves()
			if King in all_enemy_moves:
				check = True
			self.player_color = "Black"
		else:
			King = self.find_king("White")
			self.player_color = "Black"
			all_enemy_moves = self.get_all_moves()
			if King in all_enemy_moves:
				check = True
			self.player_color = "White"
		return check
	#Function that draws the screen
	def draw_board(self, main_screen):

		#Colors
		Black = (0,0,0)
		White = (255,255,255)
		Cyan = (0,255,255)
		Red = (255,0,0)
		rectangle_outline_size = 53
		main_screen.fill(White)

		#Draw the current selected box outline
		#Since the rectangle of board are transparent they will not overwrite this outline
		if self.selected_piece != None:
			for x in range(4):
				pg.draw.rect(main_screen, Cyan, ((self.selected_piece[1] * 50)-x,(self.selected_piece[0] * 50)-x,rectangle_outline_size,rectangle_outline_size), 1)
			#Print all the valid moves of current box piece here
			for i in range(len(self.selected_piece_moves)):
				for x in range(4):
					pg.draw.rect(main_screen, Red, ((self.selected_piece_moves[i][1] * 50)-x,(self.selected_piece_moves[i][0] * 50)-x,rectangle_outline_size,rectangle_outline_size), 1)
		for i in range(0,8):
			for j in range(0,8):
				if i % 2 == 0 and j % 2 == 0:
					#Drawing a transparent triangle, can make a single function
					rectangle = pg.Rect(j * 50, i * 50, 50, 50)
					shape_surf = pg.Surface(rectangle.size, pg.SRCALPHA)
					shape_surf.set_alpha(128)
					pg.draw.rect(shape_surf, White, shape_surf.get_rect())
					main_screen.blit(shape_surf, rectangle)
					#Rectangle borders
					#for x in range(4):
						#pg.draw.rect(main_screen, Cyan, ((j * 50)-x,(j * 50)-x,53,53), 1)
					#Drawing the piece
					if self.board_position[i][j] != 0:
						piece = pg.image.load(self.board_images[self.board_position[i][j]])
						main_screen.blit(piece, ((j * 50) - 5, (i * 50) - 5))
				elif i % 2 != 0 and j % 2 != 0:
					#Drawing a transparent triangle, can make a single function
					#main_screen.fill(White,pg.Rect(j * 50, i * 50, 50, 50))
					rectangle = pg.Rect(j * 50, i * 50, 50, 50)
					shape_surf = pg.Surface(rectangle.size, pg.SRCALPHA)
					shape_surf.set_alpha(128)
					pg.draw.rect(shape_surf, White, shape_surf.get_rect())
					main_screen.blit(shape_surf, rectangle)

					#Drawing the piece
					if self.board_position[i][j] != 0:
						piece = pg.image.load(self.board_images[self.board_position[i][j]])
						main_screen.blit(piece, ((j * 50) - 5, (i * 50) - 5))
				else:
					#Drawing a transparent triangle, can make a single function
					#main_screen.fill(Black,pg.Rect(j * 50, i * 50, 50, 50))
					rectangle = pg.Rect(j * 50, i * 50, 50, 50)
					shape_surf = pg.Surface(rectangle.size, pg.SRCALPHA)
					shape_surf.set_alpha(128)
					pg.draw.rect(shape_surf, Black, shape_surf.get_rect())
					main_screen.blit(shape_surf, rectangle)

					#Drawing the piece
					if self.board_position[i][j] != 0:
						piece = pg.image.load(self.board_images[self.board_position[i][j]])
						main_screen.blit(piece, ((j * 50) - 5, (i * 50) - 5))	
def main():

	#Pygame variables
	screen_resolution = 400
	pg.init()
	main_screen = pg.display.set_mode((screen_resolution, screen_resolution))
	#Setting caption
	pg.display.set_caption("Chess-AI")
	#Setting icons
	icon = pg.image.load('Others/Icon.png')
	pg.display.set_icon(icon)
	board = Board("White")
	while True:
		event = pg.event.poll()
		if event.type == pg.QUIT:
			break
		if event.type == pg.MOUSEBUTTONUP:
				
			score = board.evaluation_score("Black")
			print(f"Black score is : {score}")
			score = board.evaluation_score("White")
			print(f"White score is : {score}")
			#Checks if it's a ----check---- move
			#So we can restrict current user movement
			if board.evaluate_check() == True:
				if board.check_movement() == False:
					print(f"{board.player_color} got checkmate, {board.player_color} lost!!!!")
					break
				else:
					board.check_selection()
			#Simple move
			elif board.selection_and_movement() == True:
				break
		board.draw_board(main_screen)
		pg.display.flip()
	pg.quit()
main()
# %%
