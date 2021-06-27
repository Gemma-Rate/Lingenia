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

    def syllable_structure(self, nuclei_no=3):
        """Generate the basic syllable structure"""
        phoneme_keys = list(self.available_phoneme_classes.keys())
        self.min_number = np.min(list(self.available_phoneme_classes.keys()))
        self.max_number = np.max(list(self.available_phoneme_classes.keys()))

        output_word_list = []
        
        onset, onset_sonority_number = self.generate_onset()
        output_word_list.append(onset)
        for i in range(nuclei_no):
            nucleus, nucleus_sonority_number = self.generate_nucleus(onset_sonority_number)
            output_word_list.append(nucleus_sonority_number)
        output_word_list.append(self.generate_coda(nucleus_sonority_number))

        return output_word_list

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
        onset_sonority_number = rn.choice(list(self.available_phoneme_classes.keys()))
        onset_sonority = self.available_phoneme_classes[onset_sonority_number]
        extracted_keys = self.all_phonemes[onset_sonority]
        onset = np.random.choice(extracted_keys)

        return onset, onset_sonority_number
        

    def generate_nucleus(self, onset_sonority_number):
        """Determine which sounds can comprise the nucleus"""
        #generate sonority with higher level at higher probability than the onset sonority
        phoneme_nos = np.array(list(self.available_phoneme_classes.keys()))
        phoneme_nos = phoneme_nos[phoneme_nos>onset_sonority_number]
        # Get only phoneme number categories larger than the onset. 
        nucleus_sonority_number = rn.choice(list(phoneme_nos))
        nucleus_sonority = self.available_phoneme_classes[nucleus_sonority_number]
        extracted_keys = self.all_phonemes[nucleus_sonority]
        nucleus = np.random.choice(extracted_keys)

        return nucleus, nucleus_sonority_number

    def generate_coda(self, nucleus_sonority_number):
        """Generate the coda"""
        phoneme_nos = np.array(list(self.available_phoneme_classes.keys()))
        phoneme_nos = phoneme_nos[phoneme_nos<nucleus_sonority_number]
        # Get only phoneme number categories larger than the onset. 
        coda_sonority_number = rn.choice(list(phoneme_nos))
        coda_sonority = self.available_phoneme_classes[coda_sonority_number]
        extracted_keys = self.all_phonemes[coda_sonority]
        coda = np.random.choice(extracted_keys)

        return coda

    def insert_phonemes(self):
        pass

    def convert_to_decimal_encoding(syllable_list):
        """
        Convert the html selected and reordered 
        values to html decimals for display
        """
        convert_decimal = {"BI":"&#x0069", "BY":"&#x0079",
                           "B0268":"&#x0268", "B0289":"&#x0289",
                           "B026F":"&#x026F", "BU":"&#x0075",
                           "B026A":"&#x026A", "B028F":"&#x028F",
                           "B028A":"&#x028A", "BE":"&#x0065",
                           "B\\XF8":"&#x00F8", "B0258":"&#x0258",
                           "B0275":"&#x0275", "B0264":"&#x0264",
                           "BO":"&#x006F", "B\\X65031E":"&#x0065;&#x031E",
                           "B\\XF8031E":"&#x00F8;&#x031E", "B0259":"&#x0259",
                           "B0264\\U031E":"&#x0264;&#x031E", "BO031E":"&#x006F;&#x031E",
                           "B025B":"&#x025B", "B0153":"&#x0153",
                           "B025C":"&#x025C", "B025E":"&#x025E",
                           "B028C":"&#x028C", "B0254":"&#x0254",
                           "B\\XE6":"&#x00E6", "B0250":"&#x0250",
                           "BA":"&#x0061", "B0276":"&#x0276",
                           "BA0308":"&#x0061;&#x0308", "B0251":"&#x0251",
                           "B0252":"&#x0252"}
        converted_syllable_list = []
        for s in syllable_list:
            converted_syllable_list.append(s)
        joined = ';'.join(converted_syllable_list)

        return joined


class Words(object):
    """
    Stich syllables together into full words.
    """
    pass
