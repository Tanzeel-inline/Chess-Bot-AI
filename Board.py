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
            row[i] = -row[i]
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
		self.weightage = {'King': 1000, 'Queen': 9, 'Rook': 5, 'Bishop': 3, 'Knight': 3, 'Pawn': 1}

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
					  	[5,4,3,1,2,3,4,5]]
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

	def generate_pawn_moves(self, current_position,):
		moves = []
		if self.player_color == "White":
			#print(getUp(current_position))
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
	
	def enemy_king(self, position):
		if self.player_color == "White":
			if self.board_position[position[0]][position[1]] == -1: 
				return True
		else:
			if self.board_position[position[0]][position[1]] == 1: 
				return True
		return False
	#Piece movement operation
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
			#Evaluate for check move here
			#So if king is in danger generate its valid move and allow user to only move in one of the selected piece


			#This code is for white piece
			#New clicked, generate all possible moves from current position
			#if self.previous_selected_piece == None:
			if self.selected_piece == None and self.board_position[selected_box[0]][selected_box[1]] > 0:
				self.selected_piece_moves = self.generate_valid_path_list(selected_box)
				self.selected_piece = selected_box
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
			#Evaluate for check move here
			#So if king is in danger generate its valid move and allow user to only move in one of the selected piece


			#This code is for black piece
			#New clicked, generate all possible moves from current position
			#if self.previous_selected_piece == None:
			if self.selected_piece == None and self.board_position[selected_box[0]][selected_box[1]] < 0:
				self.selected_piece_moves = self.generate_valid_path_list(selected_box)
				self.selected_piece = selected_box
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
	def move_piece(self, new_position, old_position):
		self.board_position[new_position[0]][new_position[1]] = self.board_position[old_position[0]][old_position[1]]
		self.board_position[old_position[0]][old_position[1]] = 0
	def copy_board(self):
		new_board = Board(self.player_color)
		for i in range (0, 8):
			for j in range(0, 8):
				new_board.board_position[i][j] = self.board_position[i][j]
		new_board.selected_piece = self.selected_piece
		new_board.selected_piece_moves = self.selected_piece_moves

	def get_king_position(self):
		for i in range(0, 8):
			for j in range(0, 8):
				if self.board_position[i][j] == 1:
					return [i,j]
		return [-1,-1]
	def evaluate_check(self):
		#This functions checks if current player king is under attack then only allow king movement
		check = False
		if self.player_color == "Black":
			negate(self.board_position)

		king_position = self.get_king_position()
		
		for i in range(0, 8):
			for j in range(0, 8):
				if self.board_position[i][j] >= 0 :
					continue
				moves = self.generate_valid_path_list([i, j])
				if king_position in moves:
					check = True
					break
		
		if self.player_color == "Black":
			negate(self.board_position)
		return check
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
		#main_screen.fill(White)
		event = pg.event.poll()
		if event.type == pg.QUIT:
			break
		if event.type == pg.MOUSEBUTTONUP:
			if board.selection_and_movement() == True:
				break
			"""#Evaluating check for enemy
			board.player_color = "Black"
			if board.evaluate_check() == True:
				print("Black king is in danger")
			board.player_color = "White"
			"""
		board.draw_board(main_screen)
		pg.display.flip()
	pg.quit()
main()
# %%
