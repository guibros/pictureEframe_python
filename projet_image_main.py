import pygame
from datetime import datetime,timedelta
import time
import yaml
import os
import random
from PIL import Image
from enum import Enum
from projet_image_preparation import *

from RPiSim import GPIO  # Import GPIO Library

#configuration du board raspberry
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


#bloc declaration des variables de gpio pin
BTN_ALBUM_PIN = 22
BTN_PHOTO_PIN = 17
BTN_VEILLE_PIN = 6


#initiation des pin du board
GPIO.setup(BTN_ALBUM_PIN, GPIO.MODE_IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_PHOTO_PIN, GPIO.MODE_IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_VEILLE_PIN, GPIO.MODE_IN, pull_up_down=GPIO.PUD_UP)

#bloc-config de la fonction d'evenements en provenance du raspberry
def getEvent():
    global mode
    if GPIO.input(BTN_ALBUM_PIN) == False:
        print ('getEvent ALBUM')
        time.sleep(0.2)
        switchAlbum()
    if GPIO.input(BTN_PHOTO_PIN) == False:
        print ('getEvent PHOTO')
        time.sleep(0.2)
        switchPhoto()
    if GPIO.input(BTN_VEILLE_PIN) == False:
        print ('getEvent VEILLE')
        time.sleep(0.2)
        if mode == Veille.OFF:
            mode = Veille.ON
            print(mode)
        else:
            mode = Veille.OFF
            print(mode)
        return mode

class Veille(Enum):
    ON = 0
    OFF = 1

#bloc config couleur
BLEU = (0, 0, 255)
ROUGE = (100, 0, 0)
JAUNE = (200, 200, 0)
VERT = (0, 100, 0)
BLANC = (255, 255, 255)
GRIS = (50, 50, 50)
NOIR = (0, 0, 0)

#importation du document config et de ses variables
try:
    fichier = open("config.yaml", "r")
    config = yaml.load(fichier, yaml.Loader)
    hourOFF = config['hourOFF']
    hourON = config['hourON']
    path = config['path']
    delay = config['delay']
except:
    print("error config")

#config des parametres x/y de l'affichage
ecranX = 800
ecranY = 550

#classe pour preparation des fichiers photos pour l'affichages
dataPhoto = prepImg(path,ecranX,ecranY)
dataPhoto.set()

#declaration des differents variables pour l'articulation des path
choixPhoto = 0
choixAlbum = 0
dossiers = os.listdir(path)
nbDossiers = len(dossiers)
numeroDossiers = range(nbDossiers-1)
fichiers = os.listdir(path + dossiers[choixAlbum])
nbFichiers = len(fichiers)
numeroFichiers = range(nbFichiers-1)
photo = path + dossiers[choixAlbum] + "/" + fichiers[choixPhoto]

#fonction pour le mode de veille
def clockVeille(houroff, houron):
    global modeVeille
    global mode
    heure = datetime.now().time()
    preminuit = datetime.strptime("23:59:59", "%H:%M:%S").time()
    postminuit = datetime.strptime("00:00", "%H:%M").time()
    timeOFF=datetime.strptime(str(houroff), "%H:%M").time()
    timeON=datetime.strptime(str(houron), "%H:%M").time()
    if timeOFF>timeON:
        if heure < preminuit and heure > timeOFF:
            modeVeille = "on"
            mode = Veille.ON
        elif heure > postminuit and heure < timeON:
            mode = Veille.ON
    else:
        if heure > timeOFF and heure < timeON:
            mode = Veille.ON
    return mode

#fonction pour appeler le bon path pour les fichiers photo
def getPhoto(choixalbum,choixphoto):
    dossiers = os.listdir(path)
    fichiers = os.listdir(path + dossiers[choixalbum])
    photo = path + dossiers[choixalbum] + "/" + fichiers[choixphoto]
    return photo

#fonction pour changer la photo
def switchPhoto():
    global choixPhoto
    fichiers = os.listdir(path + dossiers[choixAlbum])
    nbFichiers = len(fichiers)
    choixPhoto = choixPhoto + 1
    if choixPhoto > nbFichiers-1:
        choixPhoto = 0
    print(nbFichiers)
    print(choixPhoto)
    print(datetime.now())
    return choixPhoto

#fonction pour changer l'album
def switchAlbum():
    global choixAlbum
    dossiers = os.listdir(path)
    nbDossiers = len(dossiers)
    choixAlbum = choixAlbum + 1
    if choixAlbum > nbDossiers-1:
        choixAlbum = 0
    print(choixAlbum)
    print(datetime.now())
    return choixAlbum

#initialisation des variables d'affichage
screen = pygame.display.set_mode([ecranX, ecranY])
image = pygame.image.load(photo)
rect = image.get_rect()
rect.center = (ecranX/2,ecranY/2)


#initiation des variables d'entreposages pour les fonctions de temps
now = 0
delta = datetime.now()+ timedelta(seconds=delay)
delta = delta.strftime('%H:%M:%S')

#initialisation de l'etat modeVeille a off
mode = Veille.OFF

#initiation du premier choix d'album au hasard
choixAlbum = random.randint(0,nbDossiers-1)

#initiation de la variable de roulement de la boucle
running = True
while running:
    getEvent()
    
    pygame.init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                switchAlbum()
            if event.key == pygame.K_RIGHT:
                switchPhoto()
            if event.key == pygame.K_BACKSPACE:
                print(mode)
                #print(modeVeille)
                if mode == Veille.ON:
                    mode = Veille.OFF
                elif mode == Veille.OFF:
                    mode = Veille.ON
               


    #declaration du fond de l'ecran
    screen.fill(NOIR)

    #declaration des boucles temporel
    now = datetime.now()
    now = now.strftime('%H:%M:%S')
    if delta == now:
        delta = datetime.now()+ timedelta(seconds=delay)
        delta = delta.strftime('%H:%M:%S')
        switchPhoto()
    clockVeille(hourOFF,hourON)

    #declaration de path pour fichier photo
    photo = getPhoto(choixAlbum, choixPhoto)
    #chargement de l'image
    image = pygame.image.load(photo)
    #decclaration des variables d'ajustement d'affichage
    rect = image.get_rect()
    rect.center = (ecranX / 2, ecranY / 2)
    #declaration d'affichage selon l'etat modeVeille
    if mode == Veille.OFF:
        screen.blit(image, rect)

    pygame.display.flip()


pygame.quit()
print("Fin du test")