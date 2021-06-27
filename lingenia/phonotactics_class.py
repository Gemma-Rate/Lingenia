"""Class for generating and storing the phonotactics of the language"""

import numpy as np
import random as rn
import pandas as pd

from lingenia import ipa_dict_simplified as ip
from lingenia import phoible_vowels_dict as pv
from lingenia import phoible_consonants_dict as pcs

class Syllable(object):
    """
    phonotactics

    syllable shape:
    possible onset combinations, nucleus combinations and coda combinations.

    onset (consonant beginning the syllable), nucleus-stress (almost always a vowel), coda (consonant ending syllable, must preceede onset of another syllable, or appear at the end of a word)
    open syllable (no coda, occurs in about 1/8 cases), start with generating these!

    fixed stress system?


    Notation system for syllables: C = consonant, V = vowel, other? 
    Include custom notation system for answer. Include optional (). 

    Sonority hierarchy, probability of being in the nucleus higher when further up the list.

    Open vowels
    Mid vowels
    Close vowels and semivowels
    Laterals and rhotics
    Nasals
    Fricatives
    Stops

    define a general syllable structure
    """

    def __init__(self, all_phonemes_classified):

        self.all_phonemes = all_phonemes_classified
        self.onset = ''
        self.sonority_sequence = {'Open':15, 'Near-open':14, 'Open-mid':13, 
                                  'Mid':12, 'Close-mid':11, 'Near-close':10, 
                                  'Close':9, 'Trill':8, 'Approximant':7, 
                                  'Lateral fricative':6, 
                                  'Lateral approximant':5, 'Nasal':4, 
                                  'Fricative':3, 'Stop':2, 'Tap/flap':1}
        #{7:'Open', 6:'Near-open', 5:'Open-mid',  4:'Mid', 3:'Close-mid', 2:'Near-close', 1:'Close', 0:'Trill', -1:'Lateral fricative', -2:'Lateral approximant', -3:'Nasal',  -4:'Fricative', -5:'Plosive'}
        available_phoneme_classes = []
        # Set up a list of available phoneme classes to select.

        for s in all_phonemes_classified.keys():
            if len(all_phonemes_classified[s])>0:
                keynum = self.sonority_sequence[s]
                available_phoneme_classes.append((keynum, s))
        self.available_phoneme_classes = dict(available_phoneme_classes)

    def syllable_structure(self):
        """Generate the basic syllable structure"""
        print(self.available_phoneme_classes.keys())
        phoneme_keys = list(self.available_phoneme_classes.keys())
        self.min_number = np.min(list(self.available_phoneme_classes.keys()))
        self.max_number = np.max(list(self.available_phoneme_classes.keys()))

        self.generate_onset()
        print(self.onset)
        for i in range(3):
            self.generate_nucleus()
            print(self.nucleus)
        self.generate_coda()

        print(self.coda)

    def check_equivalent_afficates(self):
        """
        Check to avoid replicating affricates already in the phoneme 
        list with consonant clusters (e.g 'sh' should not be possible if 
        post-alveolar fricative is a phoneme).
        """
        pass

    def generate_onset(self):
        """Determine which sounds can comprise the onset"""
        # generate start sonority
        self.onset_sonority_number = rn.choice(list(self.available_phoneme_classes.keys()))
        self.onset_sonority = self.available_phoneme_classes[self.onset_sonority_number]
        extracted_keys = self.all_phonemes[self.onset_sonority]
        self.onset = np.random.choice(extracted_keys)
        

    def generate_nucleus(self):
        """Determine which sounds can comprise the nucleus"""
        #generate sonority with higher level at higher probability than the onset sonority
        phoneme_nos = np.array(list(self.available_phoneme_classes.keys()))
        phoneme_nos = phoneme_nos[phoneme_nos>self.onset_sonority_number]
        # Get only phoneme number categories larger than the onset. 
        self.nucleus_sonority_number = rn.choice(list(phoneme_nos))
        self.nucleus_sonority = self.available_phoneme_classes[self.nucleus_sonority_number]
        extracted_keys = self.all_phonemes[self.nucleus_sonority]
        self.nucleus = np.random.choice(extracted_keys)

    def generate_coda(self):
        """Generate the coda"""
        phoneme_nos = np.array(list(self.available_phoneme_classes.keys()))
        phoneme_nos = phoneme_nos[phoneme_nos<self.nucleus_sonority_number]
        # Get only phoneme number categories larger than the onset. 
        self.coda_sonority_number = rn.choice(list(phoneme_nos))
        self.coda_sonority = self.available_phoneme_classes[self.coda_sonority_number]
        extracted_keys = self.all_phonemes[self.coda_sonority]
        self.coda = np.random.choice(extracted_keys)

    def insert_phonemes(self):
        pass

class Words(object):
    """
    Stich syllables together into full words.
    """
    pass
