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

    def __init__(self, consonants, vowels):

        self.available_consonants = consonants
        self.available_vowels = vowels
        self.onset = ''

    def syllable_structure(self):
        """Generate the basic syllable structure"""

        if consonant:
            pass

        if optional:
            pass

        pass

    def sonority_hierarchy(self):
        pass

    def generate_onsets(self):
        """Determine which sounds can comprise the onset"""
        self.onset = np.random.choice(self.available_consonants)
        

    def generate_nuclei(self):
        """Determine which sounds can comprise the nucleus"""
        self.nucleus = np.random.choice(self.available_vowels)

    def generate_codas(self):
        """Generate the coda"""
        pass

    def insert_phonemes(self):
        pass

class Words(object):
    """
    Stich syllables together into full words.
    """
