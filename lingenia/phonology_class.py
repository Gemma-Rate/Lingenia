"""Class for generating and storing the phonemes of the language"""

import numpy as np
import random as rn
import pandas as pd

from lingenia import ipa_dict_simplified as ip
from lingenia import phoible_vowels_dict as pv
from lingenia import phoible_consonants_dict as pcs


class Phonology(object):
    """
    Container class for generating and storing phonemes.
    """

    def __init__(self, consonant_number, vowel_number):
        self.vowel_number = int(vowel_number)
        self.consonant_number = int(consonant_number)
        self.phoneme_list = []
        self.vowels = []
        self.consonants = {}
        self.consonants_list = []

    def generate_phonemes(self):
        """
        Generate a complete set of phonemes for the language.
        """
        pass

    def generate_vowel_numbers(self):
        """
        Generate ideal numbers of vowels, based on a weibull distribution.
        """
        pass

    def generate_prob_list(self, max_selected, min_percent=5):
        """
        Generate a probability distribution with a min_percent chance
        of returning just one value and an equal chance of returning the
        other numbers, up to the max number of allowed results.
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

        probabilities = vowel_phoible_data.sort_values('frequency',
                                                    ascending=False)
        # Cycle through the vowels until x number are selected
        # checking for selection by whether a random number is below
        # the frequency.

        while total_vowel_no > 0:
            # Order sounds by probability:

            for s in probabilities.index.values:
                if total_vowel_no > 0:
                    vowel_is_selected = self.select_element(s, probabilities)
                    # Select the vowel from the 'yes' or 'no' distribution.

                    if vowel_is_selected:
                        gen_vowel_list.append(s)
                        total_vowel_no -= 1
                        probabilities = probabilities.drop(index=s)

        self.vowels.extend(gen_vowel_list)


    def select_element(self, ipa_element, probabilities):
        """
        Select an individual consonant depending on the probability of occurance.
        """
        probability_indiv = probabilities.loc[ipa_element, 'frequency']
        # Get the probability of the individual consonant.
        rnd = rn.random()
        selected = rnd < probability_indiv
        # Select the vowel from the 'yes' or 'no' distribution.
        return selected


    def determing_voiced(self, col, probabilities):
        """
        Randomly choose voiced data.
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

    def generate_consonant_row(self, row_name):
        """
        Generate a row of consonants.
        """
        consonant = ip.consonant_df
        row_data = consonant.loc[row_name, :]
        row_data = row_data.replace(to_replace='', value=np.nan)
        row_data = row_data.dropna()
        # Remove empty gaps from the ipa table. 

        return row_data

    def select_from_column(self, col_data, sel_consonant_number):
        """
        Select from the consonant column.
        """
        consonant_phoible_data = pd.DataFrame(pcs.phoible_consonants)
        decoded = [bytes(a, 'utf-8').decode("unicode_escape") for a in
                   list(consonant_phoible_data.index.values)]
        # Decode \u to unicode from the .csv
        consonant_phoible_data.index = decoded
        probabilities = consonant_phoible_data.sort_values('frequency',
                                                           ascending=False)

        column_list, clist_len = [], 0

        if len(col_data) <= sel_consonant_number:
            # Reset length of the consonants to be selected. Include column -2.
            sel_consonant_number = len(col_data)-2
            # Include some flexibility in the column length, to avoid trying to 
            # select phonemes with very low probabilities.

        while clist_len < sel_consonant_number:
            consonants_to_drop = []
            for i, s in zip(col_data.index.values, col_data):
                if (len(s)>2) and (clist_len < sel_consonant_number-2):
                    # Check for voiced.
                    voiced = self.determing_voiced(s, probabilities)
                    column_list.extend(voiced)
                    consonants_to_drop.append(i)
                    # Drop consonants from chosen column to prevent them from being selected twice.
                    clist_len = len(column_list)
                elif clist_len < sel_consonant_number:
                    try:
                        # Account for empty values.
                        consonant_is_selected = self.select_element(s[0], probabilities)
                        if consonant_is_selected:
                            column_list.extend(s)
                            consonants_to_drop.append(i)
                            # Drop consonants from chosen column to prevent them from being selected twice.
                            clist_len = len(column_list)
                    except IndexError:
                        pass
                elif clist_len >= sel_consonant_number:
                    clist_len = len(column_list)
                    break
            col_data = col_data.drop(labels=consonants_to_drop)
            # Drop any selected consonants from the column.

        return column_list


    def generate_all_consonants(self):
        """
        Generate the required number of consonants.
        :return:
        """
        total_consonant_no_remaining = self.consonant_number
        nasal_col = self.generate_consonant_row('Nasal')

        # Currently, the code can get 'stuck' on some selections, so we use a 

        nasal_num = self.generate_prob_list(len(nasal_col.values))
        while (nasal_num < 2) and (nasal_num > (total_consonant_no_remaining -2)):
            # Minimum available nasal consonants and maximum possible 
            # nasal consonants without losing liquid columns. 
            nasal_num = self.generate_prob_list(len(nasal_col.values)-1)
        nasal_consonants = self.select_from_column(nasal_col,
                                                   nasal_num)
        # Nasal consonants.
        total_consonant_no_remaining = total_consonant_no_remaining  - len(nasal_consonants)

        liquid_cols = ['Trill', 'Lateral fricative', 'Lateral approximant']
        # Randomly generate the number of liquid columns to select.
        
        total_liquid_col_nos = 0
        for col in liquid_cols:
            total_liquid_col_nos = total_liquid_col_nos + len(self.generate_consonant_row(col).values)
            # Get total numbers of liquids available. 

        liquid_consonants = {}
        liquid_num = self.generate_prob_list(total_liquid_col_nos)
        while (liquid_num > total_consonant_no_remaining) or (liquid_num < 2):
            # Ensure the number of liquids is less than the total
            # remaining consonant number and more than 2.
            liquid_num = self.generate_prob_list(total_liquid_col_nos)

        for i in range(len(liquid_cols)):
            if liquid_num > 2: 
                liquid_col = self.select_column(liquid_cols)
                selected_liquids = self.select_from_column(liquid_col, liquid_num)
                liquid_consonants.update({liquid_col.name : selected_liquids})
                liquid_num = liquid_num - len(selected_liquids)
        
        total_consonant_no_remaining = total_consonant_no_remaining - len(liquid_consonants)
        # Liquid consonants.

        # Remove the liquid and nasal from the ipa dictionary. 
        all_consonants = ip.consonant_df
        drop_cols = liquid_cols + ['Nasal']
        all_consonants = all_consonants.drop(labels=drop_cols)

        self.consonants = {}
        while total_consonant_no_remaining > 0:
            # Only run remaining columns if 'spare' consonants are left.
            remaining_cols = list(all_consonants.columns.values)
            rn.shuffle(remaining_cols)
            # Note the remaining columns and shuffle them so selection differs each time.
            
            for r in remaining_cols:
                if total_consonant_no_remaining > 0:
                    remaining_col = all_consonants[r]
                    remaining_col = remaining_col.replace(to_replace='', value=np.nan)
                    remaining_col = remaining_col.dropna()
                    
                    select_num = self.generate_prob_list(total_consonant_no_remaining)
                    new_consonants = self.select_from_column(remaining_col, select_num)
                    # Select new consonants from the chosen column.
                    self.consonants.update({r : new_consonants})
                    total_consonant_no_remaining = total_consonant_no_remaining - len(new_consonants)
                
        self.consonants.update(liquid_consonants)
        self.consonants.update({'Nasal': nasal_consonants})
        self.consonants_list = [item for sublist in self.consonants.values() for item in sublist]


    def select_column(self, column_list):
        """
        Randomly choose a column from a dataframe.
        """
        selected_column_name = np.random.choice(column_list, replace=False)
        #column_list.remove(selected_column_name)
        # Remove the selected column.
        selected_col = self.generate_consonant_row(selected_column_name)

        return selected_col

        

