"""Initialize the app"""

import flask as fk
import os
import json

from flask import g
from lingenia import phonology_class as pc
from lingenia import ipa_dict_simplified as ip
from lingenia import phonotactics_class as pt

def make_app(test_config=None):

    app = fk.Flask(__name__, instance_relative_config=True)
    # Create and configure the app.

    app.config['TEMPLATES_AUTO_RELOAD']=True 

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # Create the instance folder if it doesn't exist already.

    def encode_to_json(phoneme_list):
        """
        Encode list contents and convert to a json for passing to ajax.
        """
        encoded = [str(a.encode('unicode_escape', 'backslashreplace')) for a in
                   list(phoneme_list)]
        phoneme_code = [s.replace("b'\\\\u'", '') for s in encoded]
        phoneme_code = [s.replace("\\\\u", '') for s in phoneme_code]
        phoneme_code = [s.replace("'", '').upper() for s in phoneme_code]
        phoneme_str = ','.join(phoneme_code)
        # Single string with all the vowels, to pass to ajax.

        #phoneme_json = {phoneme_name: phoneme_str}
        #print(phoneme_str)
        return phoneme_str

    @app.route('/lingenia', methods=['GET', 'POST'])
    def main_page():
        """
        Display the main page with phoneme and language generation. Also accept incoming ajax requests from the main page. 
        """
        if fk.request.method == 'POST':
            response = fk.request.get_json()
            keys = response.keys()
            print(keys)

            if list(keys)[0] == 'vowels_and_consonants':
                vowel_no, consonant_no = response['vowels_and_consonants']
                vowel_json, consonant_json = forms(vowel_no, consonant_no)
                g.vowels = vowel_json
                g.consonants = consonant_json
                classified = classify_phonemes(vowel_json, consonant_json)
                return fk.jsonify(vowel_json=vowel_json, consonant_json=consonant_json) 

            elif list(keys)[0] == 'Number_words':
                classified = classify_phonemes(','.join(response['v_list']), ','.join(response['c_list']))
                Syllables = pt.Syllable(classified)
                output_word_list = Syllables.syllable_structure() 
                   
                return fk.render_template('main_page.html')

            else:
                classified = classify_phonemes(','.join(response['v_list']), ','.join(response['c_list']))

                return fk.render_template('main_page.html')
        else: 
            return fk.render_template('main_page.html')

         #, vowel_json=vowel_json, consonant_json=consonant_json)

    @app.route('/about')
    def about():
        """
        Display the about page.
        """
        return fk.render_template('about.html')

    @app.route('/contact')
    def contact():
        """
        Display the contact page.
        """
        return fk.render_template('contact.html')

    def forms(vowel_no, consonant_no):

        if not vowel_no:
            # Replace with constant if no vowel is specified.
            vowel_no = 5
        if not consonant_no:
            # Do the same with consonants.
            consonant_no = 20

        phonology = pc.Phonology(consonant_no, vowel_no)
        phonology.generate_vowels_full()
        phonology.generate_all_consonants()
        # Generate phonology.

        vowel_list = phonology.vowels
        consonant_list = phonology.consonants_list
        # Get vowels and consonants from phonology class. 
        print(vowel_list, consonant_list)
        
        vowel_json = encode_to_json(vowel_list)
        consonant_json = encode_to_json(consonant_list)
        # Get encoded results for JSON.

        return vowel_json, consonant_json
        # return vowel_json

    def classify_phonemes(vowels, consonants):
        """
        Classify the selected phonemes from the UI.
        """
        df_class = {}
        vowels = vowels.split(',')
        consonants = consonants.split(',')
        keys = vowels+consonants

        ip_vowels = ip.vowel_df
        vowel_keys = ip_vowels.index.values
        for index, row in ip_vowels.iterrows():
            rowlist = row.to_numpy().tolist()
            flattened = [encode_to_json(item) for slist in rowlist for item in slist]
            for f in flattened:
                df_class[f] = index

        ip_consonants = ip.consonant_df
        consonant_keys = ip_consonants.index.values
        for index, row in ip_consonants.iterrows():
            rowlist = row.to_numpy().tolist()
            flattened = [encode_to_json(item) for slist in rowlist for item in slist]
            for f in flattened:
                df_class[f] = index
        
        all_keys = list(consonant_keys)+list(vowel_keys)

        df_keys = {ak:[] for ak in all_keys} 
        # Create empty lists to fill for each type of phonemes. 

        for k in keys:
            try:
                key_for_all = df_class[k]
                df_keys[key_for_all].append(k)
            except KeyError:
                pass

        return df_keys

    return app
