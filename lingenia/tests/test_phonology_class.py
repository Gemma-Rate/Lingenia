"""Unit tests for phonology generation"""

import pandas as pd
import unittest as ut


class TestPhonology(unittest.TestCase):

    def initialize_test_data(self):
        """
        Create the test data to use in phonology. 
        """

        test_vowels = {'test':[['\u0069','\u0079'], ['\u026A','\u028F'], ['\u0065','\u00F8'], ['\u00F8\u031E'],
                               ['\u025B','\u0153'], ['\u00E6'], ['\u0061','\u0276']],
                       'test 2':[['\u0268','\u0289'], '', ['\u0258','\u0275'], ['\u0259'],
                                ['\u025C','\u025E'], ['\u0250'], ['\u0061\u0308']]}

        test_vowels_frequency = {'frequency': {'\\u0069': 0.873075715, '\\u0079': 0.054979579,
                                 '\\u028F': 0.008796733000000001, '\\u026A': 0.139491046,
                                '\\u0065': 0.578385171,'\\u00F8': 0.029531888,
                                '\\u00F8\\u031E': 0.005026704, '\\u025B': 0.35469682700000005,
                                '\\u0153':0.027961042999999998, '\\u00E6': 0.070059692,
                                '\\u0061': 0.81683946, '\\u0276':0.000314169022934339,
                                '\\u0268': 0.15425699, '\\u0289': 0.021049325, 
                                '\\u0258': 0.013509268, '\\u0275': 0.011310085,
                                '\\u0259': 0.21206409, '\\u025C': 0.010995916000000001,
                                '\\u025E': 0.001885014, '\\u0250': 0.023562677,
                                '\\u0061\\u0308':0.025133522000000002}}

        test_consonants = {'test':[['\u006D'], ['\u0070','\u0062'],
                                    ['\u0278', '\u03B2'], '', '',
                                    ['\u0299'], '', ''],
                       'test 2':[['\u0271'], '',
                                      ['\u0066','\u0076'], ['\u028B'],
                                      ['\u2C71'], '', '', '']}
        cindex = ['test row 1', 'test row 2', 'test row 3', 'test row 4',
                'test row 5', 'test row 6', 'test row 7', 'test row 8']

        consonant_df = pd.DataFrame(test_consonants, index=cindex)



    def test_vowel_creation(self):
        
        """
        Tests that vowels are selected and that the selection consists of the right number of vowels.
        """