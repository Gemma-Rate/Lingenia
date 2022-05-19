"""
Utilities for converting back and forth from the generated results
"""

from lingenia import phonology_class as pc
from lingenia import ipa_dict_simplified as ip
from lingenia import phonotactics_class as pt
from lingenia import html_dict as htdc

def generate_vowels_and_consonants(vowel_no, consonant_no):
    """
    Generate phonology using input vowel and consonant numbers.
    """

    phonology = pc.Phonology(consonant_no, vowel_no)
    phonology.generate_vowels_full()
    phonology.generate_all_consonants()
    # Generate phonology.
    
    vowels_encoded = phonology.encode_to_json(phonology.vowels)
    consonant_encoded = phonology.encode_to_json(phonology.consonants_list)
    # Get encoded results for JSON.

    return vowels_encoded, consonant_encoded

def classified_to_dictionary(phoneme_dict):
    """
    Convert the classified data into a dictionary that maps each vowel or 
    consonant to manner of articulation.
    """

    df_class = {}
    # Create storage dictionary.

    for index, row in phoneme_dict.iterrows():
        # Cycle through dictionary rows to get vowels and consonants.
        rowlist = row.to_numpy().tolist()
        flattened = [pc.Phonology.encode_to_json(item) for slist in rowlist for item in slist]
        # Get all possible vowels or consonants with a given manner of articulation.
        for f in flattened:
            df_class[f] = index
            # Create a dictionary that maps each vowel or consonant to the manner of articulation
            # by assigning it to the index of the row iteration.
    
    return df_class

def classify_phonemes(vowels, consonants):
    """
    Classify the selected phonemes (back to manner of articulation) from the UI.
    """
    
    vowels = vowels.split(',')
    consonants = consonants.split(',')
    keys = vowels + consonants
    # Get all vowels and consonants.

    vowel_keys = ip.vowel_df.index.values
    consonant_keys = ip.consonant_df.index.values
    # Get manner of articulation from vowel or consonant dictionary indices.

    classified_vowel_df = classified_to_dictionary(ip.vowel_df)
    classified_consonant_df = classified_to_dictionary(ip.consonant_df)
    classified_all_df = {**classified_vowel_df, **classified_consonant_df}
    # Create dictionary mapping for each possible vowel and consonant back to manner of articulation.
    
    all_keys = list(consonant_keys) + list(vowel_keys)
    df_keys = {ak:[] for ak in all_keys} 
    # Create empty lists for each manner of articulation to fill for each type of phonemes. 

    for k in keys:
        try:
            key_for_all = classified_all_df[k]
            df_keys[key_for_all].append(k)
        except KeyError:
            pass

    return df_keys

def save_generated_results(json_response):
    """
    Save the generated phonemes and any words to an output file.
    """
    ipa_classed = classify_phonemes(','.join(json_response['v_list']), ','.join(json_response['c_list']))
    ipa_classed = create_ascii_dict(ipa_classed)
    # Classified phonemes back to manner of articulation.
    words = '\n'.join(json_response['gen_words'])
    
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
    ascii_list = {}
    for k in classified.keys():
        # Iterate through dictionary of classified phonemes to get all phonemes in a specific manner of articulation.
        key_element = classified[k]
        ascii_list[k] = [htdc.convert_to_ascii[c] for c in key_element]
        
    return ascii_list

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
    # Get manners of articulation for vowels and consonants. 

    consonants, vowels = [], []
    
    for sp in sep_str:
    # Get each row in the file. 
        split_str = sp.split(':')
        # Get each manner of articulation for phonemes (for the consonant and vowel titles above).
        try:
            for sp2 in split_str[1]:
                # Cycle through the generated phonemes in each manner of articulation.
                phonemes = sp2.split(',')
                if split_str[0] in consonants_titles:
                    consonants.extend(phonemes)
                    # Add to consonants if manner of articulation is in consonant title list.
                elif split_str[0] in vowel_titles:
                    vowels.extend(phonemes)
                    # Add to vowels if manner of articulation is in vowels title list.
        except IndexError:
            pass

    if vowels:
        vowels = [v for v in vowels if all([v!='', v!=' '])]
        vowel_encoded = pc.Phonology.encode_to_json(vowels)

    if consonants:
        consonants = [c for c in consonants if all([c!='', c!=' '])]
        consonant_encoded = pc.Phonology.encode_to_json(consonants)
    else:
        # Run if empty lists (data file is not in correct format.)
        vowels.append('no result')
        vowel_encoded = pc.Phonology.encode_to_json(vowels)
        consonants.append('no result')
        consonant_encoded = pc.Phonology.encode_to_json(consonants)
    
    return vowel_encoded, consonant_encoded
