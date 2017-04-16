import pygame
from backEnd import *
from time import sleep

#############################
#VARIABLES
#############################

#RGB colors for pygame to read
BLACK = (0,0,0)
WHITE = (255,255, 255)
BLUE = (66, 134, 244) #It's like a nice relaxing blue.

ticks = pygame.time.get_ticks #because I dont want to type all that

#self-explanatory
PlayerOneScore = 0
PlayerTwoScore = 0

screen_x = 400
screen_y = 400

############################
#FUNCTIONS
############################

#If the user wants to quit, let em.
def quitCheck():
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4):
			return True
	return False		
 
def deleteSongFiles():
	import os
	for x in os.listdir("Songs"):
		try:
			os.remove("Songs/"+x) #This causes an error if pygame played the song in question last. Solution unknown.
		except PermissionError:
			pass #Just leave the file. its ok.

#defines what happens for a song guess. (5 of these happen for each player each round, grand total of 30.)
def songGuess(playerNum, songNum):
	currentPlayerScore = PlayerOneScore if playerNum == 1 else PlayerTwoScore
	currentScore = font.render("Your Score: "+str(currentPlayerScore), 1, BLACK)
	screen.blit(currentScore, (1, 50))
	pygame.display.update()

	while(1): #This loop simply gets a song. Not a game mechanic loop.
		try:
			index = random_index()
			jsonData = get_track_data(index)
			download_mp3(jsonData)
			break
		except TypeError: #if the song lacks an mp3 url
			pass
		except OSError: # if the song name has quotes in it...
			pass
		except ValueError: #if the son lacks a spotify link (I think)
			pass	
	song_name = jsonData["name"]
	
	#When the timer runs out OR a button is clicked,
	#Give them a brief respite and then let the loop continue.


	while(1): #This loop plays
		screen.fill(BLUE)
		
		screen.blit(currentScore, (1, 50))
		currentPlayer = font.render("Player "+str(playerNum), 1, BLACK)
		screen.blit(currentPlayer, (1,1))
		pygame.display.update()
		pygame.mixer.init()
		pygame.mixer.music.load("Songs/"+song_name+".mp3")
		pygame.mixer.music.play()
		start_time = ticks()
		
		while(1):
		
			curr_time = ticks()
			print(curr_time, start_time)

			toUpdate = pygame.Rect(1, 100, screen_x, 50)#left, top, width, height
			timeLeft = font.render("Time Left: "+str(10-int((curr_time - start_time)/1000)), 1, BLACK)
			screen.fill(BLUE, toUpdate)
			screen.blit(timeLeft, (1, 100))
			pygame.display.update(toUpdate)
		
			if curr_time - start_time >= 10000:
				break
			

			#Code to take input via buttons goes here	
			

			if quitCheck():
				deleteSongFiles()
				exit()
		pygame.mixer.stop()
		pygame.mixer.quit()
		break
		sleep(1)
	


#This function occurs for a player's turn, AKA their 5 songs in a given round.
def playerTurn(playerNum):
	screen.fill(BLUE)
	currentPlayer = font.render("Player "+str(playerNum)+"'s Turn", 1, BLACK)
	screen.blit(currentPlayer, (1,1))
	pygame.display.update()

	for songNum in range(5):
		songGuess(playerNum, songNum)

		

######################################################
#STUFF THAT ACTUALLY HAPPENS
######################################################

pygame.init()
font = pygame.font.SysFont("trebuchetms", 40)

screen = pygame.display.set_mode((screen_x, screen_y))
screen.fill(BLUE)

for rounds in range(3):
	playerTurn(1)
	playerTurn(2)


while(1):
	screen.fill(BLUE)
	WhoWon = "One" if PlayerOneScore>PlayerTwoScore else "Two"
	if(PlayerTwoScore == PlayerOneScore):
		final = font.render("It's a tie!", 1, WHITE)
		screen.blit(final, (1,1))
		pygame.display.update()
	else:	
		final = font.render("Player " + WhoWon +" Wins!", 1, WHITE)
		screen.blit(final, (1,1))
		pygame.display.update()
	if quitCheck():
		deleteSongFiles()
		exit()


