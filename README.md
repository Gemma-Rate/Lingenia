# Lingenia

This small flask app allows you to generate individual words for a naming language. The words are generated by selecting common phonemes (or a user selected combination of phonemes), then combining these into syllables and finally combining the syllables into words. 

This app makes use of data from the Phoible database (Moran, Steven & McCloy, Daniel (eds.) 2019., PHOIBLE 2.0., Jena: Max Planck Institute for the Science of Human History), see attribution section below.

## How to use this app
![Screenshot of the main Lingenia web interface page, showing features outlined below](images/main_page_view.png?raw=true "Main Lingenia web interface page")

Select the number of vowels and consonants to generate by entering them into the text boxes. You can then click 'generate' to produce a set of phonemes, based on how common they are in real world languages and a set of other common rules. Alternatively, you can click on individual phonemes to add them to the list. Selected phonemes (either those generated by entering the number of vowels and consonants or manually selected by the user) will be highlighted in red.

You can then generate words using the highlighted phoneme selection, by clicking 'Generate words'. Like the vowels and consonants, you can also choose to generate a set number of words.

The output phoneme list and generated words can be downloaded by clicking the 'download' button at the top of the screen. Uploading this file (using the 'upload' button) will return the same phoneme selection so that you can generate more words.

## Running on Windows

To run Lingenia with a development environment on Windows:
1. Clone this repository
2. Ensure that your version of Python has the modules in the 'Requirements' sections below installed (making a Python virtual environment may be helpful).
3. Open Windows cmd
4. Go to the 'Lingenia' folder in the location of the cloned repository (by using the 'change directory' command 'cd', or by opening cmd in the folder location of Lingenia).
5. Start the flask app by entering the following:
```
set FLASK_APP=lingenia
set FLASK_ENV=development
flask run
```
6. Open a browser window and go to http://127.0.0.1:5000/lingenia

You should see the main Lingenia page as shown above.

## Requirements

Lingenia was constructed using Python 3 and requires the following packages:

- Flask 
- Numpy
- Pandas
- Random

## Details and rules for word generation

Phonemes, the distinct sounds in the language, are selected first. These are then compiled into syllables and the syllables are compiled into words.

### Phoneme selection

Phonemes are selected using a series of rules to emulate a natural language. The Phoible database is used to select the phonemes based on how many languages they occur in. This ensures that a language is not filled with large numbers of unusual sounds by default. Unfortunately, only a selection of the most common phonemes (down to those that occur in 0.2% of all languages) are included at the moment. Each phoneme is included if the Phoible probability is below a randomly selected value. If a voiced consonant is selected, the unvoiced version is included by default.

Sounds tend to occur in places of similar articulation, which form columns down the IPA table. New phonemes are therefore chosen depending on whether a phoneme with a given articulatory place is already in the selected list. 

### Syllable generation

Syllables are generated using the basic construction of syllable components:

Onset - Nucleus - Coda

There is a random probability (currently 50% true or false, this may be modified to be more realistic in future) for a syllable to have no coda (be an 'open syllable').

The choice of which phoneme to use as each component is governed by sonority rules, which are based on place of articulation:
- Open vowels
- Mid vowels
- Close vowels and semivowels
- Laterals and rhotics
- Nasals
- Fricatives
- Stops

Each level of sonority is mapped to a number. The onset sonority is randomly chosen (such that it is less than the maximum sonority) and the nucleus sonority will be randomly selected so that it is higher than the onset. If a coda is being generated, it will have a sonority lower than the nucleus.

Phonemes with the designated sonority are then selected for each component of the syllable. The final output is a list of the syllable onset, nucleus and (if required) coda in order.

### Word construction

Words are currently set up to be constructed from between 1 and 4 syllables. The number of syllables to be used are chosen randomly, using the probability distribution 
```
[0.2, 0.5, 0.2, 0.1]
```
Each syllable is selected randomly (with replacement) from the overall pool generated at the syllable construction step. This does mean that words consisting of the same syllable repeated multiple times may be generated.

## Possible future features and bug fixes

- Due to the rule that unvoiced consonants are included by default if a voiced consonant is selected, sometimes the number of consonants selected will be larger than the number specified by the user. This is a known bug I hope to fix in the future.
- The word construction syllable number is currently somewhat arbitrary. I hope to make this more evidence based in future. 

## Attributions 

The files containing probabilities of phonemes (both vowels and consonants) are modified from the Phoible database: Moran, Steven & McCloy, Daniel (eds.) 2019., PHOIBLE 2.0., Jena: Max Planck Institute for the Science of Human History. (Available online at http://phoible.org, Accessed on 2020-07 and 2020-08).

Some of the processes and rules I have used for Phonology generation are based on the excellent 'How to make a Language' series from Biblaridion on Youtube (found [here](https://www.youtube.com/channel/UCMjTcpv56G_W0FRIdPHBn4A)).

Word generation is inspired by the original Awkwords (created by Petr Mejzlík), whilst the sonority hierarchy information and general IPA grid Phonemes were taken from Wikipedia.

