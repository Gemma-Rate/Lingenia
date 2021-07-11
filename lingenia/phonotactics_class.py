"""Class for generating and storing the phonotactics of the language"""

import numpy as np
import random as rn
import pandas as pd
from numpy.random import choice

from lingenia import ipa_dict_simplified as ip
from lingenia import phoible_vowels_dict as pv
from lingenia import phoible_consonants_dict as pcs
from lingenia import html_dict as htm

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
        self.all_syllables = []

        self.sonority_sequence = {'Open':15, 'Near-open':14, 'Open-mid':13, 
                                  'Mid':12, 'Close-mid':11, 'Near-close':10, 
                                  'Close':9, 'Trill':8, 'Approximant':7, 
                                  'Lateral fricative':6, 
                                  'Lateral approximant':5, 'Nasal':4, 
                                  'Fricative':3, 'Stop':2, 'Tap/flap':1}
        available_phoneme_classes = []
        # Set up a list of available phonemes to select.

        for s in all_phonemes_classified.keys():
            if len(all_phonemes_classified[s])>0:
                keynum = self.sonority_sequence[s]
                available_phoneme_classes.append((keynum, s))
        self.available_phoneme_classes = dict(available_phoneme_classes)
        # Mapping between generated phonemes and numbers.

    def generate_syllables(self, number_of_syllables_to_gen):
        """Generate a number of syllables to use for constructing words"""
        for i in range(number_of_syllables_to_gen):
            coda_or_not = rn.choice([True, False])
            syllable_generated = self.syllable_structure(open_syllable=coda_or_not)
            self.all_syllables.append(syllable_generated)

    def syllable_structure(self, open_syllable=False):
        """Generate a basic syllable structure"""
        phoneme_keys = list(self.available_phoneme_classes.keys())
        self.min_number = np.min(list(self.available_phoneme_classes.keys()))
        self.max_number = np.max(list(self.available_phoneme_classes.keys()))

        output_syllable = []
        
        onset, onset_sonority_number = self.generate_onset()
        output_syllable.append(onset)
        nucleus, nucleus_sonority_number = self.generate_nucleus(onset_sonority_number)
        output_syllable.append(nucleus)

        if open_syllable:
            output_syllable.append(self.generate_coda(nucleus_sonority_number))

        return output_syllable

    def check_equivalent_afficates(self):
        """
        Check to avoid replicating affricates already in the phoneme 
        list with consonant clusters (e.g 'sh' should not be possible if 
        post-alveolar fricative is a phoneme).
        """
        pass

    def generate_onset(self):
        """Determine which sounds can comprise the onset"""
        phoneme_list = list(self.available_phoneme_classes.keys())[:-2]
        # Select to almost end of list (to prevent errors from needing 
        # to select higher sonority).
        onset_sonority_number = rn.choice(phoneme_list)
        onset_sonority = self.available_phoneme_classes[onset_sonority_number]
        extracted_keys = self.all_phonemes[onset_sonority]
        onset = rn.choice(extracted_keys)

        return onset, onset_sonority_number
        
    def generate_nucleus(self, onset_sonority_number):
        """Determine which sounds can comprise the nucleus"""
        #generate sonority with higher level at higher probability than the onset sonority
        phoneme_nos = np.array(list(self.available_phoneme_classes.keys()))
        phoneme_nos = phoneme_nos[phoneme_nos>onset_sonority_number]
        # Get only phoneme number categories larger than the onset. 

        if onset_sonority_number<9:
        # Additionally, get vowels only if current selection <9.
            phoneme_nos = phoneme_nos[phoneme_nos>9]

        nucleus_sonority_number = rn.choice(list(phoneme_nos))
        nucleus_sonority = self.available_phoneme_classes[nucleus_sonority_number]
        extracted_keys = self.all_phonemes[nucleus_sonority]
        nucleus = rn.choice(extracted_keys)

        return nucleus, nucleus_sonority_number

    def generate_coda(self, nucleus_sonority_number):
        """Generate the coda"""
        phoneme_nos = np.array(list(self.available_phoneme_classes.keys()))
        phoneme_nos = phoneme_nos[phoneme_nos<nucleus_sonority_number]
        # Get only phoneme number categories larger than the onset.

        coda_sonority_number = rn.choice(list(phoneme_nos))
        coda_sonority = self.available_phoneme_classes[coda_sonority_number]
        extracted_keys = self.all_phonemes[coda_sonority]
        coda = rn.choice(extracted_keys)

        return coda

class Words(object):
    """
    Stich syllables together into full words.
    """
    def __init__(self, all_syllables):

        self.syllables = all_syllables
        self.all_words = []

        self.sprobability_distribution = [0.2, 0.5, 0.2, 0.1]
        # Syllable number probability distribution.

    def generate_words(self, number_of_words):
        """Generate a list of words"""

        for n in number_of_words:
            self.generate_word()

    def generate_word(self):
        """Generate a single word """
        total_syllable_no = np.random.choice(list(range(1, 5)), 1,
                            p=self.sprobability_distribution)
        total_syllable_no = total_syllable_no[0]

        word_list = []

        for t in range(total_syllable_no+1):
            chosen_syllable = rn.choice(self.syllables)
            word_list.append(chosen_syllable)

        joined_word = ''.join(word_list)

        self.all_words.append(joined_word)


def convert_to_decimal_encoding(syllable_list):
    """
    Convert the html selected and reordered 
    values to html decimals for display
    """
    convert_decimal = htm.convert_to_decimal
    converted_syllable_list = []
    for s in syllable_list:
        converted_syllable_list.append(convert_decimal[s])

    converted_syllables = ''.join(converted_syllable_list)

    return converted_syllables
