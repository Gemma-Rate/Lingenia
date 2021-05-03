"""Initialize the app"""

import flask as fk
import os
import json
from lingenia import phonology_class as pc
from lingenia import ipa_dict_simplified as ip
from lingenia import phonotactics_class as pt

def make_app(test_config=None):

    app = fk.Flask(__name__, instance_relative_config=True)
    # Create and configure the app.
    app.config.from_mapping(
        SECRET_KEY='dev')

    if test_config is None:
        # load the instance config, if it exists, when not testing.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # Create the instance folder if it doesn't exist already.

    def encode_to_json(phoneme_list, phoneme_name):
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

        phoneme_json = {phoneme_name: phoneme_str}
        print(phoneme_str)
        
        return phoneme_json

    @app.route('/lingenia', methods=['GET', 'POST'])
    def main_page():
        """
        Display the main page with phoneme and language generation. Also accept incoming ajax requests from the main page. 
        """
        if fk.request.method == 'POST':
            print('Incoming..')
            print(fk.request.get_json())  
            
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

   # @app.route('/lingenia', methods = ['POST'])
    #def listener():
    #    if fk.request.method == 'POST':
    #        print('Incoming..')
    #        print(fk.request.get_json())
   #         return '', 200 
   # def get_post_javascript_data():
    #    jsdata = fk.request.form['javascript_data']
     #   return json.loads(jsdata)[0]

    @app.route('/lingenia', methods=['GET', 'POST'])
    def forms():

        vowel_no = fk.request.get_json('vowel_no')
        consonant_no = fk.request.get_json('consonant_no')
        # Get vowel and consnants form. 

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
        # Get vowels and consonants from phonology class. w
        
        vowel_json = encode_to_json(vowel_list, "vowels")
        consonant_json = encode_to_json(consonant_list, "consonants")
        # Get encoded results for JSON.

        phonotactics = pt.Syllable(consonant_list, vowel_list)

        return fk.render_template('main_page.html', vowel_json=vowel_json, consonant_json=consonant_json)
        # return vowel_json

    return app
#<script src="{{ url_for('static', filename='main_script.js') }}"></script>
