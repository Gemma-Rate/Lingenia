"""Initialize the app"""

import flask as fk
import os

from lingenia import phonology_class as pc
from lingenia import ipa_dict_simplified as ip
from lingenia import phonotactics_class as pt
from lingenia import html_dict as htdc

def make_app(test_config=None):
    """Set up the app and configuration"""
    
    app = fk.Flask(__name__, instance_relative_config=True)
    # Create and configure the app.

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # Create the instance folder if it doesn't exist already.

    app.config['TEMPLATES_AUTO_RELOAD']=True 

    @app.route('/lingenia', methods=['GET', 'POST'])
    def main_page():
        """
        Display the main page with phoneme and language generation. Also accept incoming ajax requests from the main page. 
        """
        if fk.request.method == 'POST':
            response = fk.request.get_json()
            keys = response.keys()
            # Get JSON and response keys.

            if list(keys)[0] == 'vowels_and_consonants':
                # Use Vowel and consonant numbers to generate phonology from scratch. 
                vowel_no, consonant_no = response['vowels_and_consonants']
                vowel_json, consonant_json = generate_vowels_and_consonants(vowel_no, consonant_no)
                classified = classify_phonemes(vowel_json, consonant_json)
                return fk.jsonify(vowel_json=vowel_json, consonant_json=consonant_json) 

            elif list(keys)[0] == 'Number_words':
                # Generate a given number of words from the phonemes.
                classified = classify_phonemes(','.join(response['v_list']), ','.join(response['c_list']))
                number_of_words = response['Number_words']
                Syllables = pt.Syllable(classified)
                Syllables.generate_syllables(250)
                # Generate 250 syllables to construct the word from. 
                
                converted = []
                for i in Syllables.all_syllables:
                    converted.append(pt.convert_to_decimal_encoding(i))
                
                if not number_of_words:
                    # If no word number is specified, then generate 5 words.
                    number_of_words = 5

                Words_list = pt.Words(converted)
                Words_list.generate_words(number_of_words)
                   
                return fk.jsonify(generated_words=Words_list.all_words)

            elif list(keys)[0] == 'to_file':
                # Save user generated phonology and words to file.
                save_generated_results(response)

            elif list(keys)[0] == 'from_file':
                vowel_json, consonant_json = load_input_file(response)

                return fk.jsonify(vowel_json=vowel_json, consonant_json=consonant_json) 

            else:
                classified = classify_phonemes(','.join(response['v_list']), ','.join(response['c_list']))

                return fk.render_template('main_page.html')
        else: 
            return fk.render_template('main_page.html')

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

    @app.route('/return-files')
    def return_files():
        try:
            return fk.send_file('lingenia_download.txt', 
                                attachment_filename='lingenia_download.txt', as_attachment=True, cache_timeout=0)
        except Exception as e:
            return str(e)

    def generate_vowels_and_consonants(vowel_no, consonant_no):
        """
        Generate phonology using input vowel and consonant numbers.
        """

        phonology = pc.Phonology(consonant_no, vowel_no)
        phonology.generate_vowels_full()
        phonology.generate_all_consonants()
        # Generate phonology.

        vowel_list = phonology.vowels
        consonant_list = phonology.consonants_list
        # Get vowels and consonants from phonology class. 
        
        vowels_encoded = encode_to_json(vowel_list)
        consonant_encoded = encode_to_json(consonant_list)
        # Get encoded results for JSON.

        return vowels_encoded, consonant_encoded

    def classify_phonemes(vowels, consonants):
        """
        Classify the selected phonemes (back to place and manner of articulation) from the UI.
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
    
    def save_generated_results(json_response):
        """
        Save the generated phonemes and any words to an output file.
        """
        ipa_classed = classify_phonemes(','.join(json_response['v_list']), ','.join(json_response['c_list']))
        words = '\n'.join(json_response['gen_words'])
        ipa_classed = create_ascii_dict(ipa_classed)

        with open('lingenia_download.txt', 'w', encoding='utf-8') as f:
            f.write('Generated phonemes:\n')
            for k,v in zip(ipa_classed.keys(), ipa_classed.values()):
                f.write(k+': '+', '.join(v)+'\n')
            f.write('\nGenerated words:\n')
            f.write(words)

    def create_ascii_dict(classified):
        """
        Convert back to ascii ipa characters from html format.
        """
        new_list = {}
        for k in classified.keys():
            # Iterate through dictionary of classified phonemes.
            key_element = classified[k]
            key_element_list = []
            for c in key_element:
                # Iterate through list of phonemes. 
                key_element_list.append(htdc.convert_to_ascii[c])
            new_list[k] = key_element_list

        return new_list

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

        return phoneme_str

    def load_input_file(json_response):
        """
        Load user submitted phonology to generate more words and highlight phonemes.
        """            
        # Convert the loaded file format to HTML codes for each of the phonemes. 

        file_text = json_response['from_file'].replace('\r', '')
        sep_str = file_text.split('\n')
        # Split on new lines.

        consonants_titles = ['Nasal', 'Stop', 'Fricative', 'Approximant', 'Tap/flap', 
                                'Trill', 'Lateral fricative', 'Lateral approximant']
        vowel_titles = ['Close', 'Near-close', 'Close-mid', 'Mid', 'Open-mid', 
                        'Near-open', 'Open']
        consonants, vowels = [], []
        # Identify vowel and consonants. 
        
        for sp in sep_str:
        # Get each row in the file. 
            split_str = sp.split(':')
            # Get each 'class' of phonemes (for the consonant and vowel titles above).
            try:
                for sp2 in split_str[1]:
                    # Go through the generated phonemes in each class.
                    phonemes = sp2.split(',')
                    if split_str[0] in consonants_titles:
                        consonants.extend(phonemes)
                        # Add to consonants if 'class' title is in consonant title list.
                    elif split_str[0] in vowel_titles:
                        vowels.extend(phonemes)
                        # Add to vowels if 'class' title is in vowels title list.
            except IndexError:
                pass

        if vowels:
            vowels = [v for v in vowels if all([v!='', v!=' '])]
            vowel_encoded = encode_to_json(vowels)

        if consonants:
            consonants = [c for c in consonants if all([c!='', c!=' '])]
            consonant_encoded = encode_to_json(consonants)
        else:
            # Run if empty lists (data file is not in correct format.)
            vowels.append('no result')
            vowel_encoded = encode_to_json(vowels)
            consonants.append('no result')
            consonant_encoded = encode_to_json(consonants)
        
        return vowel_encoded, consonant_encoded


    return app
