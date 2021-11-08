"""Initialize the app"""

import flask as fk
import os
import json

from lingenia import phonology_class as pc
from lingenia import ipa_dict_simplified as ip
from lingenia import phonotactics_class as pt
from lingenia import html_dict as htdc
from werkzeug.utils import secure_filename

def make_app(test_config=None):

    app = fk.Flask(__name__, instance_relative_config=True)
    # Create and configure the app.

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # Create the instance folder if it doesn't exist already.

    try: 
        cwd = os.getcwd()
        os.makedirs(cwd+'/uploads')
    except OSError:
        pass
    
    ALLOWED_EXTENSIONS = {'txt'}
    app.config['TEMPLATES_AUTO_RELOAD']=True 
    app.config['UPLOAD_FOLDER'] = '/uploads'

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

    @app.route('/return-files/')
    def return_files():
        try:
            return fk.send_file('/home/gemma/Documents/Python_projects/Lingenia/lingenia/output.txt', 
                                attachment_filename='test.txt', as_attachment=True, cache_timeout=0)
        except Exception as e:
            return str(e)

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
                # Vowel and consonant numbers. 
                vowel_no, consonant_no = response['vowels_and_consonants']
                vowel_json, consonant_json = forms(vowel_no, consonant_no)
                classified = classify_phonemes(vowel_json, consonant_json)
                return fk.jsonify(vowel_json=vowel_json, consonant_json=consonant_json) 

            elif list(keys)[0] == 'Number_words':
                # Number of words to generates, maximum and minimum length.
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
                classified = classify_phonemes(','.join(response['v_list']), ','.join(response['c_list']))
                words = '\n'.join(response['gen_words'])

                new_list = {}
                for k in classified.keys():
                    # Iterate through dictionary of classified phonemes.
                    key_element = classified[k]
                    key_element_list = []
                    for c in key_element:
                        # Iterate through list of phonemes. 
                        key_element_list.append(htdc.convert_to_ascii[c])
                    new_list[k] = key_element_list

                with open('output.txt', 'w') as f:
                    f.write('Generated phonemes:\n')
                    for k,v in zip(new_list.keys(), new_list.values()):
                        f.write(k+': '+', '.join(v)+'\n')
                    f.write('\nGenerated words:\n')
                    f.write(words)

            elif list(keys)[0] == 'from_file':
                # Convert the loaded file format to HTML codes for each of the phonemes. 

                file_text = response['from_file']
                sep_str = file_text.split('\n')

                consonants_titles = ['Nasal', 'Stop', 'Fricative', 'Approximant', 'Tap/flap', 
                                     'Trill', 'Lateral fricative', 'Lateral approximant']
                vowel_titles = ['Close', 'Near-close', 'Close-mid', 'Mid', 'Open-mid', 
                                'Near-open', 'Open']
                consonants, vowels = [], []
                # Identify vowel and consonants. 
                
                for sp in sep_str:
                # Get each phoneme element. 
                    split_str = sp.split(':')
                    try:
                        for sp2 in split_str[1]:
                            # Go through the generated phonemes.
                            phonemes = sp2.split(',')
                            if split_str[0] in consonants_titles:
                                consonants.extend(phonemes)
                            elif split_str[0] in vowel_titles:
                                vowels.extend(phonemes)
                    except IndexError:
                        pass

                vowels = [v for v in vowels if all([v!='', v!=' '])]
                consonants = [c for c in consonants if all([c!='', c!=' '])]

                vowel_json = encode_to_json(vowels)
                consonant_json = encode_to_json(consonants)
                
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

    def forms(vowel_no, consonant_no):
        """
        Generate phonology using input vowel and consonant numbers.
        """

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

    def check_allowed_filename(filename):
        """Check filename is of the allowed type."""
        split_files = filename.split('.')
        split_files = split_files[1]
        
        if split_files in ALLOWED_EXTENSIONS:
            return True
        else:
            return False

    @app.route('/upload-files/', methods=['GET', 'POST'])
    def upload_files():
        if fk.request.method == 'POST':
            print('file received')
            file = fk.request.files['file']

            if file.filename == '':
                return redirect(request.url)

            if file and check_allowed_filename(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return fk.jsonify(vowel_json=vowel_json, consonant_json=consonant_json) 
    return app
