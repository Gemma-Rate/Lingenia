"""Initialize the app"""

import flask as fk
import os

from lingenia import phonotactics_class as pt
from lingenia import utils as ut


def make_app(test_config=None):
    """Set up the app and configuration"""
    
    app = fk.Flask(__name__, instance_relative_config=True)
    # Create and configure the app.

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # Create the instance folder if it doesn't exist already.

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
                vowel_json, consonant_json = ut.generate_vowels_and_consonants(vowel_no, consonant_no)
                classified = ut.classify_phonemes(vowel_json, consonant_json)
                return fk.jsonify(vowel_json=vowel_json, consonant_json=consonant_json) 

            elif list(keys)[0] == 'Number_words':
                # Generate a given number of words from the phonemes.
                classified = ut.classify_phonemes(','.join(response['v_list']), ','.join(response['c_list']))
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
                ut.save_generated_results(response)

            elif list(keys)[0] == 'from_file':
                vowel_json, consonant_json = ut.load_input_file(response)

                return fk.jsonify(vowel_json=vowel_json, consonant_json=consonant_json) 

            else:
                classified = ut.classify_phonemes(','.join(response['v_list']), ','.join(response['c_list']))

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


    return app
