"""Initialize the app"""

import flask as fk
import os
from lingenia import phonology_class as pc
from lingenia import ipa_dict_simplified as ip

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

    @app.route('/lingenia')
    def main_page():
        """
        Display the main page with phoneme and language generation.
        """
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

    @app.route('/lingenia', methods=['GET', 'POST'])
    def forms():

        vowel_no = fk.request.form.get('vowel_no')

        phonology = pc.Phonology(5, vowel_no)
        phonology.generate_vowels_full()

        vowel_list = phonology.vowels
        print(vowel_list)
        encoded = [str(a.encode('unicode_escape', 'backslashreplace')) for a in
                   list(vowel_list)]
        vowel_code = [s.replace("b'\\\\u'", '') for s in encoded]
        vowel_code = [s.replace("\\\\u", '') for s in vowel_code]
        vowel_code = [s.replace("'", '').upper() for s in vowel_code]
        vowel_str = ','.join(vowel_code)
        # Single string with all the vowels, to pass to ajax.

        print(vowel_str)

        vowel_json = {"vowels": vowel_str}
        print(vowel_json)

        return fk.render_template('main_page.html', vowel_json=vowel_json)
       # return vowel_json

    return app
#<script src="{{ url_for('static', filename='main_script.js') }}"></script>
