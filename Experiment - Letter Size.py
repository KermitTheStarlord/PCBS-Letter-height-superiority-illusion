#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Last updated on :
# Time-stamp: <2023-22-05 16:54:42 arthur.bert@hec.edu>
# PCBS - Prog201 Cogmaster ENS-PSL 2023

##############################################################################
# 0. Experiments and experimental constants
##############################################################################

# This is a reproduction of the Letter Height Superiority Illusion, as done
# in the 2014 paper "The letter height superiority Illusion - brief report",
# by Boris New, Karie Doré-Mazars, Céline Cavézian, Christophe Pallier,
# Julien Barra.
# DOI 10.3758/s13423-014-075308

# # Set constants
# distanceFromScreen = 0.64 #In meters
# smallVerticalSize = 0.28 #In visual angle degree
# # smallHorizontalSize is "de facto" from imported letters
# tallVerticalSize = 0.30 #In visual angle degree
# # tallHorizontalSize is "de facto" from imported letters
# distanceBetweenStimuli = 2.75 #In visual angle degree
# typesOfStimuli = ("letters","mirror letters","pseudoletters")
screenHeight = 768 #in pixels
screenLength = 1024 #in pixels
# fontExperiment = "timesNewRoman.ttf"


##############################################################################
# I. Constants, libraries, and set-up.
##############################################################################

# Import libraries
import random
import math
import expyriment
import os
abspath = os.path.abspath('') # String containing absolute path to the script file
os.chdir(abspath) # Setting up working directory

# Interface constants, as used by Expyriment
SAME_SIZE_RESPONSE_KEY = 'f'
DIFFERENT_SIZE_RESPONSE_KEY = 'j'
MAX_RESPONSE_DELAY = 5000

# Constants of the experiment, as stated in the paper
timeFixationCross = 200 #in miliseconds
timeAfterCross = 500 #in milisenconds
timeStimuli = 700 #in miliseconds
timeBetweenTrials = 750 #in miliseconds

minNumberTrainingExp = 1 #no unit
maxNumberTrainingExp = 100 #no unit
numberOfTrialsBySession = 2 #no unit
numberOfSession = 2 #no unit
totalNumberOfTrials = numberOfTrialsBySession * numberOfSession #no unit
trainingThreshold = 0.5 #no unit


##############################################################################
# II. Pathing and LetterList
##############################################################################

# Get the abosulte path to the letter files
letterPath = abspath+"/lettresPseudolettres"

# Core objects in this scripts are the LetterLists. These list are constructed
# for each stimuli used in the experiment. They are constructed as such :
# [ letter used for the stimuli, as a single caracter string,
#   the type os stinmuli, either letter, switched letter, or pseudoletter, as
#   a string,
#   the size of the stimulo, either normal or big, as a string,
#   the path to the image file, as a string.]

# They are named as a concatanation of :
#   Type of experiment : training or stimuli
#   Size of letter : Small or Big
#   Type of letter : Normal, Pseudo, or Reversed
#   The string : LetterList

# Create LetterList for the training experiment
trainingPath = letterPath + "/stimtraining"
trainingLetter = ["n","u","x"]
trainingSmallNormalLetterList = [[letter, "letter", "small", trainingPath + "/"+ letter + "100.bmp"] for letter in trainingLetter]
trainingBigNormalLetterList = [[letter, "letter", "big", trainingPath + "/"+ letter + "110.bmp"] for letter in trainingLetter]
trainingSmallPseudoLetterList = [[letter, "pseudoletter", "small", trainingPath + "/"+ letter + "p100.bmp"] for letter in trainingLetter]
trainingBigPseudoLetterList = [[letter, "pseudoletter", "big", trainingPath + "/"+ letter + "p110.bmp"] for letter in trainingLetter]

# Create concatenated list for the training experiment, containing
# respectively only letter stimuli and all possible stimuli
trainingSmallbigNormalLetterList = trainingSmallNormalLetterList + trainingBigNormalLetterList
trainingLetterList = trainingSmallNormalLetterList + trainingBigNormalLetterList + trainingSmallPseudoLetterList + trainingBigPseudoLetterList

# Create LetterList for the recorded experiment
stimuliPath = letterPath + "/stimuli/lettres"
stimuliLetter = ["a","c","e","m","r","s","v","w","z"]
stimuliSmallNormalLetterList = [[letter, "letter", "small", stimuliPath + "/" + letter + "100.bmp"] for letter in stimuliLetter]
stimuliBigNormalLetterList = [[letter, "letter", "big", stimuliPath + "/" + letter + "110.bmp"] for letter in stimuliLetter]
stimuliSmallReversedLetterList = [[letter, "switched letter", "small", stimuliPath + "/" + letter + "s100.bmp"] for letter in stimuliLetter]
stimuliBigReversedLetterList = [[letter, "switched letter", "big", stimuliPath + "/" + letter + "s110.bmp"] for letter in stimuliLetter]
stimuliSmallPseudoLetterList = [[letter, "pseudoletter", "small", stimuliPath + "/" + letter + "p100.bmp"] for letter in stimuliLetter]
stimuliBigPseudoLetterList = [[letter, "pseudoletter", "big", stimuliPath + "/" + letter + "p110.bmp"] for letter in stimuliLetter]

# Create concatenated list for the recorded experiment, containing
# respectively only letter stimuli and all possible stimuli
stimuliSmallbigNormalLetterList = stimuliSmallNormalLetterList + stimuliBigNormalLetterList
stimuliLetterList = stimuliSmallNormalLetterList + stimuliBigNormalLetterList + stimuliSmallReversedLetterList + stimuliBigReversedLetterList + stimuliSmallPseudoLetterList + stimuliBigPseudoLetterList

##############################################################################
# III. Training Experiment
##############################################################################

# This part of the script is composed of two blocks. The first for the
# initial set-up, the second for the running of the training experiment.

# III.A. Set-up ##############################################################

# We create a trainingExperiments list of list. Each entry of this list
# represent an stimuli of two letters. Each entry is a list, composed of the
# two LetterList of the corresponding stimuli, the expyriment stimuli of the
# two picture stimuli, a string stating the type of coupling formed, and a 
# caracter string corresponding to the correct response expected of the
# participant.

# The coupling string is formed as :
#   "Type of letter of stimuli 1" + " "
#   "Size of letter of stimuli 1" + " "
#   " vs " +
#   "Type of letter of stimuli 2" + " "
#   "Size of letter of stimuli 2" 

# To do this, we use a fonction shuffle_and_pair_list and a function
# create_dual_stimuli, that are to be reused in the second part of the
# experiment.
# - shuffle_and_pair_list creates the list of list from the two LetterList,
# by shuffling them and zipping the two list together. It also adds some
# trivial strings, as stated above.
# - create_dual_stimuli is a function specialized in creating a dual stimuli
# from the two pictures linked in the LetterList.

def shuffle_and_pair_list(list1,list2,maxLength=100):
    # This function inputs two list and a string, and returns a list.
    # This function requires that floor from the math library is imported.
    # This function requires that shuffle from the random library is imported.
    # This function uses system variable used in the Expyriment library. These
    # variables are SAME_SIZE_RESPONSE_KEY and DIFFERENT_SIZE_RESPONSE_KEY.
    
    # This allows for a random shuffle, but with minimal variance in
    # stimuli occurences.

    list1 = list1 * math.floor(maxLength / len(list1)+1)
    list2 = list2 * math.floor(maxLength / len(list2)+1)
    random.shuffle(list1)
    random.shuffle(list2)
    
    shuffledPair = []
    for index in range(maxLength):
        shuffledPair.append([
            list1[index],list2[index],
            # Starting here, the rest of the function is only compatible with
            # this exact script ; modify accordingly when reusing.
            None,
            list1[index][2]+" "+list1[index][1] + " vs " + list2[index][2] + " " + list2[index][1],
            ""])
        if shuffledPair[index][0][2] == shuffledPair[index][1][2]:
            shuffledPair[index][4] = SAME_SIZE_RESPONSE_KEY
        else:
            shuffledPair[index][4] = DIFFERENT_SIZE_RESPONSE_KEY

    return shuffledPair

# Why did we multiply the LetterList instead of using modulos on the index
# in the for loop ? Because when using modulos on the index in the 
# loop, the same couples would be formed over and over again. Shuffling
# random LetterList before iterating over them allows for all couples to
# be random, while keeping individual stimuli occurences in check.

def create_dual_stimuli(list):
    # This functoin inputs a list and returns a list.
    # This inputed list needs to be a list of list, of the shape :
    # list = [LetterList1,LetterList2,None,...]
    
    compList = list
    for index in range(len(list)):
        # We create a global canva on which to plot the stimulus
        canva = expyriment.stimuli.Canvas(size=(screenLength,screenHeight),colour=(255,255,255))
        
        # The two letter stims
        Stim1 = expyriment.stimuli.Picture(
                                compList[index][0][3],position=(10,0))
        Stim2 = expyriment.stimuli.Picture(
                                compList[index][1][3],position=(-10,0))
        
        # Plotting the letter stims on the canva
        Stim1.plot(canva)
        Stim2.plot(canva)
        compList[index][2] = canva

        # For a detailled example on how to use Canva on expyriment, see
        # https://github.com/expyriment/expyriment-stash/tree/master/examples/behavioural/mental_logic_card_game

    return compList
    
trainingExperiments = shuffle_and_pair_list(
    trainingSmallbigNormalLetterList,
    trainingLetterList,
    maxNumberTrainingExp)

# III.B. Training Experiment #################################################

exp = expyriment.design.Experiment(name="SizeOfletters")
expyriment.control.defaults.window_mode
expyriment.control.initialize(exp)

cue = expyriment.stimuli.FixCross(size=(50, 50), line_width=4)
blankscreen = expyriment.stimuli.BlankScreen()
instructions = expyriment.stimuli.TextScreen("Instructions",
    f"""À l'écran vont s'afficher deux lettres, vraie ou fausse, à l'endroit ou à l'envers.

    Si les deux stimulis font la même taille, appuyez sur '{SAME_SIZE_RESPONSE_KEY.upper()}'

    Si les deux stimulis sont de taille différente, appuez sur '{DIFFERENT_SIZE_RESPONSE_KEY.upper()}'

    Appuyez sur la barre d'espace pour commencer l'expérience.""")

expyriment.control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait_char(" ")
blankscreen.present()

trainingExperiments = create_dual_stimuli(trainingExperiments)

exp.clock.wait(timeBetweenTrials)

sucessRate = 0
successes = 0
index = 0

while sucessRate<trainingThreshold or index<minNumberTrainingExp:
    
    cue.present()
    exp.clock.wait(timeFixationCross)
    blankscreen.present()
    exp.clock.wait(timeAfterCross)
    trainingExperiments[index][2].present()
    key, rt = exp.keyboard.wait_char([SAME_SIZE_RESPONSE_KEY,
                                      DIFFERENT_SIZE_RESPONSE_KEY],
                                     duration=MAX_RESPONSE_DELAY)
    index += 1
    if key == trainingExperiments[index][4]:
        successes += 1
    sucessRate = successes/index
    blankscreen.present()
    exp.clock.wait(timeBetweenTrials)

##############################################################################
# IV. Recorded Experiment
##############################################################################

# This part of the script is composed of two blocks. The first for the
# initial set-up, the second for the running of the recorded experiment.

# IV.A. Set-up ###############################################################

# The set-up is the same as was done in the training part (III). The same
# function is used, on the LetterList created in the setup part (II).

sessions = []
for i in range(numberOfSession):
    sessions.append(
        shuffle_and_pair_list(
            stimuliSmallbigNormalLetterList,
            stimuliLetterList,
            numberOfTrialsBySession))

for i in range(numberOfSession):
    sessions[i] = create_dual_stimuli(sessions[i])

# IV.B. Real Experiment ######################################################

blankscreen = expyriment.stimuli.BlankScreen()
instructions = expyriment.stimuli.TextScreen("Instructions",
    f"""Vous avez terminé l'entrainement ! L'expérience va commencer.
    
    À l'écran vont s'afficher deux lettres, vraie ou fausse, à l'endroit ou à l'envers.

    Si les deux stimulis font la même taille, appuyez sur '{SAME_SIZE_RESPONSE_KEY.upper()}'

    Si les deux stimulis sont de taille différente, appuez sur '{DIFFERENT_SIZE_RESPONSE_KEY.upper()}'

    Appuyez sur la barre d'espace pour commencer l'expérience.""")

exp.add_data_variable_names(['Session','Type', 'ExpectedAnswer', 'Answer', 'RT'])

instructions.present()
exp.keyboard.wait_char(" ")

for sessionNumber in range(numberOfSession):
    prompt = expyriment.stimuli.TextScreen("Session",
        f""" Session '{sessionNumber+1}'
        
        Appuyez sur espace pour continuer...""")
    prompt.present()
    exp.keyboard.wait_char(" ")
    
    for index in range(numberOfTrialsBySession):
    
        blankscreen.present()
        exp.clock.wait(timeBetweenTrials)
        cue.present()
        exp.clock.wait(timeFixationCross)
        blankscreen.present()
        exp.clock.wait(timeAfterCross)
        sessions[sessionNumber][index][2].present()
        key, rt = exp.keyboard.wait_char([SAME_SIZE_RESPONSE_KEY,
                                          DIFFERENT_SIZE_RESPONSE_KEY],
                                          duration=MAX_RESPONSE_DELAY)
        blankscreen.present()
        exp.clock.wait(timeBetweenTrials)
        exp.data.add([sessionNumber+1,
                      sessions[sessionNumber][index][3],
                      sessions[sessionNumber][index][4],
                      key,
                      rt])

expyriment.control.end()

##############################################################################
# V. Data formating, analysis, and saving.
##############################################################################

# See second file, DataAnalysis.py