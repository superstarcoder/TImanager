import os
import time
import sys
from datetime import datetime
# python -m pip install win10toast
from win10toast import ToastNotifier

# One-time initialization
toaster = ToastNotifier()

# Show notification whenever needed
#toaster.show_toast("Notification!", "Alert!", threaded=True,
#                  icon_path=None, duration=3)  # 3 seconds

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

import pygame
from pygame.locals import *
import random

pygame.init()

#800x600 is minimum recommended
#screen = pygame.display.set_mode((0,0), pygame.RESIZABLE)	
infoObject = pygame.display.Info()
width = 1280
height = 720
size = (width, height) #1920, 1080
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("pygame")
#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)	
clock = pygame.time.Clock()

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (209, 41, 41)
BLUE = (1, 38, 249)
GREEN = (3, 252, 19)
ORANGE = (252, 128, 3)
YELLOW = (238, 255, 0)

done = False

fps = 700
now = datetime.now()
minuteNow = int(now.strftime("%M"))
lastMinute = minuteNow


song1S = pygame.mixer.Sound('song1.wav')
song2S = pygame.mixer.Sound('song2.wav')
song3S = pygame.mixer.Sound('song3.wav')
songsS = [song1S, song2S, song3S]
homeB = pygame.image.load('homeB.png')
exitB = pygame.image.load('exitB.png')
addB = pygame.image.load('addB.png')
scheduleB = pygame.image.load('scheduleB.png')
background = pygame.image.load('background.png')
background2 = pygame.image.load('background2.png')
exitB = pygame.transform.scale(exitB, (200, 200))
homeB = pygame.transform.scale(homeB, (100, 100))
addB = pygame.transform.scale(addB, (200, 200))
scheduleB = pygame.transform.scale(scheduleB, (200, 200))
homeS = homeB.get_rect().size
homeR = pygame.Rect([0,0,100,100])
exitR = pygame.Rect([width/2+200,height/2-100,200,200])
addR = pygame.Rect([width/2-100,height/2-100,200,200])
scheduleR = pygame.Rect([width/2-400,height/2-100,200,200])

loadingR = [200, 500, 0, 100] #880 is the max width

def thing(a, sh, sm, eh, em, ls, imp):
	ls.append([a, sh.zfill(2)+":"+sm.zfill(2), eh.zfill(2)+":"+em.zfill(2),importance])
	ls.sort(key=lambda x: x[1])
	#print(ls)
	return ls
"""
a = input("what event would you like to add? (type done if done): ")
	if a == "done":
		break
	st = input("start time [00:00]: ")
	et = input("end time  [00:00]:")
	thing(a,st,et,ls)
"""
def renderText(text, yd, s, b=True, c=True, cx=True,fontName="lucidaconsole", xpos=-1, ypos=-1, color=(209, 41, 41)):
	WHITE = (255,255,255)
	BLUE = (107, 129, 255)
	font = pygame.font.SysFont(fontName, s)
	if b:
		text = font.render(text, True, color)
	else:
		text = font.render(text, True, color)
	if c:
		height2 = 0.5 * text.get_rect().height
		y = (height/2-height2)+yd
		#screen.blit(text, (width/2-width2, (height/2-height2)+yd))
	if cx:
		width2 = 0.5 * text.get_rect().width
		x = width/2-width2

	if xpos != -1:
		x = xpos
	if ypos != -1:
		x = ypos
	screen.blit(text, (x, y))

def normalRenderText(text, xpos=0, ypos=0, s=50, color=RED):
	font = pygame.font.SysFont("lemonmilk", s)
	text = font.render(text, True, color)
	screen.blit(text, (xpos, ypos))


def getTotalTime(ls, index):
	startTime = ls[index][1].split(":")
	endTime = ls[index][2].split(":")
	hd = abs(int(startTime[0])-int(endTime[0])) #hour difference
	md = -(int(startTime[1])-int(endTime[1])) #minute difference
	totalTime = (hd*60)+md
	#print(totalTime)
	return totalTime

def timeDifference(ls, eh, em):
	sh = int(ls[0][1].split(":")[0])
	sm = int(ls[0][1].split(":")[1])
	hd = abs(sh-eh) #hour difference
	md = -(sm-em) #minute difference
	totalTime = (hd*60)+md
	#print("yeah:",totalTime)
	return totalTime

def getTotalTimes(ls):
	times = []
	for x in range(len(ls)):
		times.append(getTotalTime(ls,x))
	return times
		

def checkTime(ls, hour, minute):
	for x in range(len(ls)):
		sh = int(ls[x][2].split(":")[0])
		sm = int(ls[x][2].split(":")[1])
		#print("hour, minute",sh, sm)
		if hour == sh and minute == sm:
			toaster.show_toast(ls[x][0], "Timanager Alert!", threaded=True,
                   icon_path="https://media.discordapp.net/attachments/553435367080984576/648028458630381579/tmanage1.png?width=375&height=375", duration=20)
			songsS[random.randint(0,2)].play()

notificationShown = False
times = []
schedule = []
totalTimes = 0
timePassed = 0
place = "loading"
while not done:
	screen.fill(BLACK)
	if place == "loading":
		timePassed += 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					done = True

		screen.blit(background, (0,0))
		loadingR[2] = timePassed*10
		pygame.draw.rect(screen, BLUE, loadingR)

		if loadingR[2] > 880:
			place = "home"

	elif place == "home":
		#screen.blit(addB, (addR[0],addR[1]))
		screen.blit(background2, (0,0))
		screen.blit(addB, (addR[0],addR[1]))
		#print(scheduleR[0],scheduleR[1])
		screen.blit(scheduleB, (scheduleR[0],scheduleR[1]))
		screen.blit(exitB, (exitR[0],exitR[1]))
		#print(addR[0], addR[1])

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					done = True

			mpos = pygame.mouse.get_pos() # Get mouse position
			if event.type == pygame.MOUSEBUTTONDOWN:
				if addR.collidepoint(mpos): # Check if position is in the rect
					place = "addEventName"
					eventName = ""
				if scheduleR.collidepoint(mpos): # Check if position is in the rect
					place = "schedule"
					eventName = ""
				if exitR.collidepoint(mpos):
					done = True

	elif place == "schedule":
		screen.blit(homeB, (0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					done = True
			mpos = pygame.mouse.get_pos() # Get mouse position
			if event.type == pygame.MOUSEBUTTONDOWN:
				if homeR.collidepoint(mpos): # Check if position is in the rect
					place = "home"

		screenSize = height-100
		currentY = 100
		if schedule != []:
			for x in range(len(schedule)):
				scheduleR2 = [0, currentY, width, (times[x]/totalTimes)*screenSize]
				#color = (random.randint(40, 255), random.randint(40, 255), random.randint(40, 255))
				if schedule[x][3] == "1":
					pygame.draw.rect(screen, GREEN, scheduleR2)
				elif schedule[x][3] == "2":
					pygame.draw.rect(screen, ORANGE, scheduleR2)
				elif schedule[x][3] == "3":
					pygame.draw.rect(screen, RED, scheduleR2)
				#print("so im rendering: "+schedule[x][0])
				#renderText(schedule[x][0], 0, 50, True, False, currentY)
				textSize = int(((times[x]/totalTimes)*screenSize)/7)
				if textSize < 70:
					textSize = 70
				normalRenderText(schedule[x][0], 100, currentY, textSize, color=WHITE)
				normalRenderText(schedule[x][1], 500, currentY, textSize, color=WHITE)
				normalRenderText(schedule[x][2], 1000, currentY, textSize, color=WHITE)
				currentY += (times[x]/totalTimes)*screenSize
			lastMinute = minuteNow
			now = datetime.now()
			hourNow = int(now.strftime("%H"))
			minuteNow = int(now.strftime("%M"))
			#print(hourNow)
			scheduleR2 = [0, 100, 10, (timeDifference(schedule, hourNow, minuteNow)/totalTimes)*screenSize]
			pygame.draw.rect(screen, YELLOW, scheduleR2)
			
	elif place == "addEventName":
		screen.blit(homeB, (0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					done = True
				if event.key == pygame.K_BACKSPACE:
					eventName = eventName[:-1]
				if event.unicode.isalpha() or event.unicode == " ":
					eventName += event.unicode
				if event.key == pygame.K_RETURN:
					place = "addEventImportance"
					importance = ""
			mpos = pygame.mouse.get_pos() # Get mouse position
			if event.type == pygame.MOUSEBUTTONDOWN:
				if homeR.collidepoint(mpos): # Check if position is in the rect
					place = "home"
		renderText("EVENT NAME:", 0, 100, xpos=100)
		renderText(eventName, 0, 80, xpos=800, color=BLUE)
		#key = pygame.key.get_pressed()
		#print(key)

	elif place == "addEventImportance":
		screen.blit(homeB, (0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					done = True
				if event.key == pygame.K_BACKSPACE:
					importance = importance[:-1]
				if event.unicode.isnumeric():
					importance += event.unicode
				if event.key == pygame.K_RETURN:
					place = "addEventHour"
					hour = ""
			mpos = pygame.mouse.get_pos() # Get mouse position
			if event.type == pygame.MOUSEBUTTONDOWN:
				if homeR.collidepoint(mpos): # Check if position is in the rect
					place = "home"
		renderText("Importance Level (1-3):", 0, 70, xpos=100)
		renderText(importance, 0, 80, xpos=1125, color=BLUE)


	elif place == "addEventHour":
		screen.blit(homeB, (0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					done = True
				if event.key == pygame.K_BACKSPACE:
					hour = hour[:-1]
				if event.unicode.isnumeric():
					hour += event.unicode
				if event.key == pygame.K_RETURN:
					place = "addEventMinute"
					minute = ""
			mpos = pygame.mouse.get_pos() # Get mouse position
			if event.type == pygame.MOUSEBUTTONDOWN:
				if homeR.collidepoint(mpos): # Check if position is in the rect
					place = "home"
		renderText("START TIME", -300, 100, True, color=WHITE)
		renderText("Hour (0-23):", -100, 50, True)
		renderText(hour, -50, 50, True, color=BLUE)
		renderText("Minute:", 0, 50, True)
		#key = pygame.key.get_pressed()
	
	elif place == "addEventMinute":
		screen.blit(homeB, (0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					done = True
				if event.key == pygame.K_BACKSPACE:
					minute = minute[:-1]
				if event.unicode.isnumeric():
					minute += event.unicode
				if event.key == pygame.K_RETURN:
					place = "addEndEventHour"
					endHour = ""
			mpos = pygame.mouse.get_pos() # Get mouse position
			if event.type == pygame.MOUSEBUTTONDOWN:
				if homeR.collidepoint(mpos): # Check if position is in the rect
					place = "home"
		renderText("START TIME", -300, 100, True, color=WHITE)
		renderText("Hour (0-23):", -100, 50, True)
		renderText(hour, -50, 50, True, color=BLUE)
		renderText("Minute:", 0, 50, True)
		renderText(minute, 50, 50, True, color=BLUE)

	elif place == "addEndEventHour":
		screen.blit(homeB, (0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					done = True
				if event.key == pygame.K_BACKSPACE:
					endHour = endHour[:-1]
				if event.unicode.isnumeric():
					endHour += event.unicode
				if event.key == pygame.K_RETURN:
					place = "addEndEventMinute"
					endMinute = ""
			mpos = pygame.mouse.get_pos() # Get mouse position
			if event.type == pygame.MOUSEBUTTONDOWN:
				if homeR.collidepoint(mpos): # Check if position is in the rect
					place = "home"
		renderText("END TIME", -300, 100, True, color=WHITE)
		renderText("Hour (0-23):", -100, 50, True)
		renderText(endHour, -50, 50, True, color=BLUE)
		renderText("Minute:", 0, 50, True)
		#key = pygame.key.get_pressed()

	elif place == "addEndEventMinute":
		screen.blit(homeB, (0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					done = True
				if event.key == pygame.K_BACKSPACE:
					endMinute = endMinute[:-1]
				if event.unicode.isnumeric():
					endMinute += event.unicode
				if event.key == pygame.K_RETURN:
					schedule = thing(eventName, hour, minute, endHour, endMinute, schedule, importance)
					place = "home"
					print(schedule)
					#print(schedule)
					times = getTotalTimes(schedule)
					#print(times)
					totalTimes = sum(times)
					#print(sum(times))
			mpos = pygame.mouse.get_pos() # Get mouse position
			if event.type == pygame.MOUSEBUTTONDOWN:
				if homeR.collidepoint(mpos): # Check if position is in the rect
					place = "home"

		renderText("END TIME", -300, 100, True, color=WHITE)
		renderText("Hour (0-23):", -100, 50, True)
		renderText(endHour, -50, 50, True, color=BLUE)
		renderText("Minute:", 0, 50, True)
		renderText(endMinute, 50, 50, True, color=BLUE)

	#lastMinute = minuteNow
	#if notificationShown and lastMinute != minuteNow:
	#	notificationShown = False
	now = datetime.now()
	hourNow = int(now.strftime("%H"))
	minuteNow = int(now.strftime("%M"))
	#print("now:", hourNow, minuteNow)
	if lastMinute != minuteNow:
		#print("break: ",lastMinute,minuteNow)
		checkTime(schedule, hourNow, minuteNow)
	#	notificationShown = True
		
	clock.tick(fps)
	pygame.display.update()


