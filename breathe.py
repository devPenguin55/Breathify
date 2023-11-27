import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import base64
import io
import math as m
import time as t
import pygame.locals as pglocals
import pygame


# install all necessary features from pygame

LINE = not True
xShift = 10 if LINE else 70

pygame.init()


# Binary data  of the WAV files
# normal sound
inhaleWavData = base64.urlsafe_b64decode(
)
exhaleWavData = base64.urlsafe_b64decode(
)

# new high pitched sound
# inhaleWavData = base64.urlsafe_b64decode(
# )
# exhaleWavData = inhaleWavData

# Convert binary data to file-like objects
inhaleWavFile = io.BytesIO(inhaleWavData)
exhaleWavFile = io.BytesIO(exhaleWavData)
soundNames = {
    0: pygame.mixer.Sound(exhaleWavFile),
    1: pygame.mixer.Sound(inhaleWavFile)
}


def playSound(sound):
    global current
    # get the correct path of the file to avoid any potential errors
    pygame.mixer.Sound.stop(current)
    current = sound
    pygame.mixer.Sound.play(current)


BACKGROUND = (170, 170, 170)
WAVE = (100, 100, 100)
BALL = (50, 50, 50)

DISPLAY_W, DISPLAY_H = (200, 300) if LINE else (600, 600)
xOffset = 55 if LINE else -145
WAVESPEED = 0
SCENE = 0
font = pygame.font.SysFont(None, 30)
if not LINE:
    inhaleBox = pygame.Rect(DISPLAY_W/3, DISPLAY_H/3+0, 200, 30)
    exhaleBox = pygame.Rect(DISPLAY_W/3, DISPLAY_H/3+85, 200, 30)
    volText = pygame.Rect(DISPLAY_W/3+10, DISPLAY_H/3+0, 200, 40)
else:
    inhaleBox = pygame.Rect(DISPLAY_W/3+xShift, DISPLAY_H/3-30, 50, 30)
    exhaleBox = pygame.Rect(DISPLAY_W/3+xShift, DISPLAY_H/3+55, 50, 30)
    volText = pygame.Rect(DISPLAY_W/3+xShift, DISPLAY_H/3+0, 200, 40)

DISPLAY = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
pygame.display.set_caption("Breathify")
CLOCK = pygame.time.Clock()

inhaleInput = "5"
exhaleInput = "5"
inhaleActive = False
exhaleActive = False
SCENE = 0
step = 0
lastTrough = True
VOLUME = 80
record = t.time()
deltaVol = 0


def path():
    global xOffset
    global wave_points
    AMPLITUDE = 100
    FREQUENCY = 0.01
    VERTICAL_SHIFT = DISPLAY_H // 2
    thickness = 3
    if not LINE:
        for yOff in range(-thickness, thickness):
            for x in range(DISPLAY_W):
                y = AMPLITUDE * \
                    m.sin(FREQUENCY * (x + xOffset)) + VERTICAL_SHIFT
                pygame.draw.circle(DISPLAY, WAVE, (x, int(y)+yOff), 1)
    else:
        # line if not having the wave
        pygame.draw.line(DISPLAY, WAVE, (DISPLAY_W // 2, -AMPLITUDE + VERTICAL_SHIFT),
                         (DISPLAY_W // 2, AMPLITUDE + VERTICAL_SHIFT), thickness)
    xOffset += WAVESPEED


def ball():
    global xOffset
    global trough
    AMPLITUDE = 100
    FREQUENCY = 0.01
    VERTICAL_SHIFT = DISPLAY_H // 2
    y = AMPLITUDE * m.sin(FREQUENCY * (DISPLAY_W/2 + xOffset)) + VERTICAL_SHIFT
    pygame.draw.circle(DISPLAY, BALL, (DISPLAY_W/2, y), 15)
    nextY = AMPLITUDE * \
        m.sin(FREQUENCY * (DISPLAY_W/2 + xOffset+WAVESPEED)) + VERTICAL_SHIFT
    if y < nextY:
        trough = True
    else:
        trough = False


def setSpeed(inhale, exhale, step):
    global WAVESPEED
    if step == 1:
        val = inhale
    else:
        val = exhale
    WAVESPEED = 10.55/val  # single formula that makes it look visually appealing


def handleEvents():
    global SCENE
    global inhaleActive
    global exhaleActive
    global LINE
    global inhaleBox
    global exhaleBox
    global inhaleInput
    global exhaleInput
    global deltaVol
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll Up
                deltaVol += 5
            elif event.button == 5:  # Scroll Down
                deltaVol -= 5
        if event.type == pglocals.MOUSEBUTTONDOWN and event.button == 3:
            if SCENE == 0:
                SCENE = 1
            else:
                SCENE = 0
            inhaleActive = False
            exhaleActive = False
        if SCENE == 1:
            MAX = 13
            if LINE:
                MAX = 2
            if event.type == pglocals.MOUSEBUTTONDOWN:
                if inhaleBox.collidepoint(event.pos):
                    inhaleActive = not inhaleActive
                else:
                    inhaleActive = False
            if event.type == pglocals.MOUSEBUTTONDOWN:
                if exhaleBox.collidepoint(event.pos):
                    exhaleActive = not exhaleActive
                else:
                    exhaleActive = False
            if event.type == pglocals.KEYDOWN:
                if inhaleActive:
                    if event.key == pglocals.K_RETURN:
                        inhaleActive = not inhaleActive
                    elif event.key == pglocals.K_BACKSPACE:
                        inhaleInput = inhaleInput[:-1]
                    else:
                        if len(inhaleInput) <= MAX:
                            if event.unicode.isnumeric() or (event.unicode == '.' and '.' not in inhaleInput):
                                inhaleInput += event.unicode
                if exhaleActive:
                    if event.key == pglocals.K_RETURN:
                        exhaleActive = not exhaleActive
                    elif event.key == pglocals.K_BACKSPACE:
                        exhaleInput = exhaleInput[:-1]
                    else:
                        if len(exhaleInput) <= MAX:
                            if event.unicode.isnumeric() or (event.unicode == '.' and '.' not in exhaleInput):
                                exhaleInput += event.unicode
        if event.type == pygame.QUIT:
            pygame.quit()
            return True
    return False


def renderScene():
    global SCENE
    global inhaleActive
    global exhaleActive
    global LINE
    global inhaleBox
    global exhaleBox
    global step
    global inhaleInput
    global exhaleInput
    global check
    global check2
    global VOLUME

    DISPLAY.fill(BACKGROUND)
    if SCENE == 0:
        pygame.mixer.unpause()
        path()
        ball()
    else:
        pygame.mixer.pause()
        # inhale duration
        if inhaleActive:
            pygame.draw.rect(DISPLAY, pygame.Color(
                'lightgray'), inhaleBox, border_radius=5)
        else:
            pygame.draw.rect(DISPLAY, pygame.Color(
                'gray'), inhaleBox, border_radius=5)

        surface = font.render(inhaleInput, True, WAVE)
        DISPLAY.blit(surface, (inhaleBox.x + 5, inhaleBox.y + 5))
        surface = font.render("in(s)", True, WAVE)
        if not LINE:
            DISPLAY.blit(surface, (inhaleBox.x + xShift+5, inhaleBox.y - 27))
        else:
            DISPLAY.blit(surface, (inhaleBox.x + xShift-5, inhaleBox.y - 27))
        # exhale duration
        if exhaleActive:
            pygame.draw.rect(DISPLAY, pygame.Color(
                'lightgray'), exhaleBox, border_radius=5)
        else:
            pygame.draw.rect(DISPLAY, pygame.Color(
                'gray'), exhaleBox, border_radius=5)

        surface = font.render(exhaleInput, True, WAVE)
        DISPLAY.blit(surface, (inhaleBox.x + 5, inhaleBox.y + 93))
        surface = font.render("out(s)", True, WAVE)
        if not LINE:
            DISPLAY.blit(surface, (inhaleBox.x + xShift, inhaleBox.y + 60))
        else:
            DISPLAY.blit(surface, (inhaleBox.x + xShift-10, inhaleBox.y + 60))
        surface = font.render(f"vol: {VOLUME}%", True, WAVE)
        DISPLAY.blit(surface, (volText.x - 20 + xShift, volText.y + 153))
    # set speed and cap seconds
    if SCENE == 0:
        setSpeed(float(inhaleInput), float(exhaleInput), step)
    else:
        if not inhaleActive:
            if float(inhaleInput) < 3:
                inhaleInput = "3"
            if float(inhaleInput) > 12:
                inhaleInput = "12"
        if not exhaleActive:
            if float(exhaleInput) < 3:
                exhaleInput = "3"
            if float(exhaleInput) > 12:
                exhaleInput = "3"


def handleAudio():
    global trough
    global lastTrough
    global step
    global VOLUME
    global deltaVol
    # handle switch of sounds and troughs
    if trough != lastTrough:
        # print(f"{t.time()-record}/{check}/{check2}") # uncomment to see time between oscillations
        # current.stop()
        if step == 1:
            step = 0
        else:
            step = 1
        playSound(soundNames[step])
    lastTrough = trough

    newVol = VOLUME + deltaVol
    if newVol > 100:
        VOLUME = 100
    elif newVol < 0:
        VOLUME = 0
    else:
        VOLUME = newVol
    deltaVol = 0

    current.set_volume(VOLUME/100)


# main loop
current = soundNames[step]
while True:
    stop = handleEvents()
    if stop:
        break
    renderScene()
    handleAudio()
    pygame.display.update()
    CLOCK.tick(30)