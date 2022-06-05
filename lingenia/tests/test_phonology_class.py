"""Unit tests for phonology generation"""

import pandas as pd
import phonology_class as pc
import unittest as ut

class TestPhonology(ut.TestCase):

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

        test_consonants_frequency = {'frequency': {'\\u006D': 0.915488533, '\\u0070': 0.814954445,
                                                   '\\u0062': 0.5988061579999999, 
                                                   '\\u0278': 0.048067860999999996,
                                                   '\\u03B2': 0.011624253999999999, 
                                                   '\\u0299': 0.000628338,'\\u0271': 0.005655042,
                                                   '\\u0066': 0.41753063100000004, 
                                                   '\\u0076': 0.256361923,
                                                   '\\u028B': 0.022306001000000002,
                                                   '\\u2C71': 0.009110901999999999}}

        test_instance = pc.Phonology(3, 3)

        test_instance.vowels_probabilities = test_vowels_frequency
        test_instance.consonants_probabilities = test_consonants_frequency
        # Update the instance with only the probabilities defined above. 

        return test_instance


    def test_generate_vowels_full(self):
        
        """
        Tests that vowels are selected and that the selection consists of the right number of vowels.
        """
        pass

    def test_update_probability(self):
        """
        Test changing the probability of a vowel or consonant. 
        """
        pass