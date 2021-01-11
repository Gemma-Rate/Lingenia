"""Class for generating and storing the phonemes of the language"""

import numpy as np
import random as rn
import pandas as pd

from lingenia import phoible_vowels_dict as pv
from lingenia import ipa_dict_simplified as ip


class Phonology(object):
    """
    Container class for generating and storing phonemes.
    """

    def __init__(self, consonant_number, vowel_number):
        print(vowel_number)
        self.vowel_number = int(vowel_number)
        self.consonant_number = int(consonant_number)
        self.phoneme_list = []
        self.vowels = []
        self.consonants = {}

    def generate_phonemes(self):
        """
        Generate a complete set of phonemes for the language.

        :return:
        """
        pass

    def generate_vowel_numbers(self):
        """
        Generate ideal numbers of vowels, based on a weibull distribution.

        :return:
        """
        pass

    def generate_prob_list(self, max_selected, min_percent=5):
        """
        Generate a probability distribution with a min_percent chance
        of returning just one value and an equal chance of returning the
        other numbers, up to the max number of allowed results.
        :return:
        """

        lengthen = int(np.floor(max_selected / (100-min_percent) * 100))
        min_ones = int(np.ceil((min_percent/100) * lengthen))
        prob_list = [t for l in range(lengthen) for t in range(2, max_selected)]
        prob_list.sort()
        prob_list = list(np.ones(min_ones)) + prob_list

        try:
            no_selected = rn.choice(prob_list)
        except IndexError:
            no_selected = 1

        return no_selected


    def generate_vowels_full(self):
        """
        Generate a complete set of phonemes for the language.

        :return:
        """
        total_vowel_no = self.vowel_number
        vowel_phoible_data = pd.DataFrame(pv.phoible_vowels)
        # Load in vowel data from phoible.
        decoded = [bytes(a, 'utf-8').decode("unicode_escape") for a in
                   list(vowel_phoible_data.index.values)]
        vowel_phoible_data.index = decoded
        # Decode \u to unicode from the .csv

        gen_vowel_list = []
        # List to fill with generated vowel phonemes.

        while total_vowel_no > 0:
            # Order sounds by probability:
            probabilities = vowel_phoible_data.sort_values('frequency',
                                                      ascending=False)
            # Cycle through the vowels until x number are selected
            # checking for selection by whether a random number is below
            # the frequency.

            for s in probabilities.index.values:
                if total_vowel_no > 0:
                    vowel_is_selected = self.select_element(s, probabilities)
                    # Select the vowel from the 'yes' or 'no' distribution.

                    if vowel_is_selected:
                        gen_vowel_list.append(s)
                        total_vowel_no -= 1
            print(gen_vowel_list)

        self.vowels.extend(gen_vowel_list)


    def select_element(self, ipa_element, probabilities):
        """

        :param probabilities:
        :param ipa_element:
        :return:
        """
        probability_indiv = probabilities.loc[ipa_element, 'frequency']
        # Get the probability of the individual consonant.
        rnd = rn.random()
        selected = rnd < probability_indiv
        # Select the vowel from the 'yes' or 'no' distribution.
        return selected


    def determing_voiced(self, col, probabilities):
        """
        Randomly choose for voiced data.
        """
        consonant_voice_list = []
        voiceless = col[0]
        try:
            voiced = col[1]
            # select voiced and voiceless elements.
            voiced_is_selected = self.select_element(voiced, probabilities)

            if voiced_is_selected:
                # If voiced selected, then select the voiceless element.
                consonant_voice_list.append(voiceless)
                consonant_voice_list.append(voiced)
            else:
                # Select only voiceless element.
                consonant_voice_list.append(voiceless)
        except:
            consonant_voice_list.append(voiceless)
            # Use this option to append voiceless result if column
            # row only has one consonant.

        return consonant_voice_list

    def generate_consonant_column(self, column_name):
        """
        Generate a column of consonants.

        :return:
        """
        consonant = ip.consonant_df

        # Need voiced resonants (nasal, liquid)
        col_data = consonant.loc[column_name, :]
        col_data = col_data.replace(to_replace='', value=np.nan)
        col_data = col_data.dropna()

        return col_data

    def select_from_column(self, col_data, sel_consonant_number):
        """
        Select from the consonant column.
        :param col_data:
        :return:
        """
        consonant_phoible_data = pd.DataFrame(pc.phoible_consonants)
        decoded = [bytes(a, 'utf-8').decode("unicode_escape") for a in
                   list(consonant_phoible_data.index.values)]
        # Decode \u to unicode from the .csv
        consonant_phoible_data.index = decoded
        probabilities = consonant_phoible_data.sort_values('frequency',
                                                           ascending=False)
        cindex = col_data.index.values
        column_list = []
        for i, s in zip(cindex, col_data):
            print(col_data[i])
            if len(column_list)<sel_consonant_number:
                if (len(s)>1) and (sel_consonant_number>1):
                    # Check for voiced.
                    voiced = self.determing_voiced(s, probabilities)
                    column_list.extend(voiced)
                else:
                    consonant_is_selected = self.select_element(s[0], probabilities)
                    if consonant_is_selected:
                        column_list.extend(s)

        return column_list


    def generate_all_consonants(self):
        """
        Generate the required number of consonants.
        :return:
        """
        all_consonants = []
        total_consonant_no = self.consonant_number

        nasal_col = self.generate_consonant_column('Nasal')

        nasal_num = self.generate_prob_list(len(nasal_col.values))
        while nasal_num<2:
            nasal_num = self.generate_prob_list(len(nasal_col.values)-1)
        print(nasal_col)
        nasal_consonants = self.select_from_column(nasal_col,
                                                   nasal_num)
        print(nasal_consonants)
        # Nasal consonants.

        total_consonant_no = total_consonant_no - len(nasal_consonants)

        liquid_cols = ['Trill', 'Lateral fricative', 'Lateral approximant']
        n_selected = 3 #self.generate_prob_list(len(liquid_cols))
        print(n_selected)
        # Randomly generate the number of liquid columns to select.

        liquid_consonants = []
        liquid_num = self.generate_prob_list(total_consonant_no)
        while (liquid_num > total_consonant_no) or (liquid_num < 2):
            # Enxure the number of liquids is less than the total
            # remaining consonant number and more than 2.
            liquid_num = self.generate_prob_list(len(total_consonant_no))

        try:
            for i in range(n_selected):
                liquid_col = self.select_column(liquid_cols)
                liquid_consonants.extend(self.select_from_column(liquid_col, liquid_num))
                total_consonant_no = total_consonant_no - len(liquid_consonants)
        except TypeError:
            liquid_col = self.select_column(liquid_cols)
            liquid_consonants.extend(self.select_from_column(liquid_col, liquid_num))
            total_consonant_no = total_consonant_no - len(liquid_consonants)
            # Liquid consonants.
        print(liquid_consonants)

        remaining_cols = ['Stop', 'Fricative', 'Approximant', 'Tap/flap']
        rn.shuffle(remaining_cols)
        # Note the remaining columns and shuffle them so selection differs each time.
        for r in remaining_cols:
            new_consonant_list = []
            remaining_col = self.select_column(remaining_cols)
            select_num = self.generate_prob_list(total_consonant_no)
            new_consonant_list.extend(self.select_from_column(remaining_col, select_num))
            total_consonant_no = total_consonant_no - len(new_consonant_list)
            print(new_consonant_list)

    def select_column(self, column_list):
        """
        Randomly choose a column.
        """
        selected_column_name = np.random.choice(column_list, replace=False)
        column_list.remove(selected_column_name)
        # Remove the selected column.
        selected_col = self.generate_consonant_column(selected_column_name)

        return selected_col

