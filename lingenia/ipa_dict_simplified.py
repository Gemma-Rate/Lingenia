"""Grid of International Phonetics Alphabet symbols"""

import pandas as pd

vowels = {'Front':[['\u0069','\u0079'], ['\u026A','\u028F'], ['\u0065','\u00F8'], ['\u00F8\u031E'],
                   ['\u025B','\u0153'], ['\u00E6'], ['\u0061','\u0276']],
          'Central':[['\u0268','\u0289'], '', ['\u0258','\u0275'], ['\u0259'],
                     ['\u025C','\u025E'], ['\u0250'], ['\u0061\u0308']],
          'Back':[['\u026F','\u0075'], ['\u028A'], ['\u0264','\u006F'], ['\u006F\u031E'],
                 ['\u028C','\u0254'], '', ['\u0251','\u0252']]}

vindex = ['Close','Near-close','Close-mid','Mid','Open-mid','Near-open','Open']

vowel_df = pd.DataFrame(vowels, index=vindex)

pulmonic_consonants = {'Bi­labial':[['\u006D'], ['\u0070','\u0062'],
                                    ['\u0278', '\u03B2'], '', '',
                                    ['\u0299'], '', ''],
                       'Labiodental':[['\u0271'], '',
                                      ['\u0066','\u0076'], ['\u028B'],
                                      ['\u2C71'], '', '', ''],
                       'Dental':['', '', ['\u03B8', '\u00F0'], '', '', '', '', ''],
                       'Alveolar':[['\u006E'], ['\u0074'],
                                   ['\u0073', '\u007A'],
                                   ['\u0279'], ['\u027E'],
                                   ['\u0072'], ['\u026C', '\u026E'],
                                   ['\u006C']],
                       'Post-alveolar':['','', ['\u0283', '\u0292'],
                                        '', '', '', '', ''],
                       'Retroflex':[['\u0273'], ['\u0288', '\u0256'],
                                    ['\u0282','\u0290'],
                                    ['\u027B'], ['\u027D'],
                                    '', '', ['\u026D']],
                       'Palatal':[['\u0272'], ['\u0063', '\u025F'],
                                  ['\u00E7', '\u029D'], ['\u006A'],
                                  '', '', '',
                                  ['\u028E']],
                       'Velar':[['\u014B'], ['\u006B', '\u0261'],
                                ['\u0078', '\u0263'], ['\u0270'], '', '',
                                '', ['\u029F']],
                       'Uvelar':[['\u0274'], ['\u0071', '\u0262'], ['\u03C7', '\u0281'], '',
                                 '', ['\u0280'], '',['\u029F\u0331']],
                       'Pharyngeal':['', ['\u02A1'], ['\u0127', '\u0295'], '', ['\u0306\u02A1'],
                                     '', '', ''],
                       'Glottal':['', ['\u0294'], ['\u0068', '\u0266'], '', '', '',
                                  '','']}
cindex = ['Nasal', 'Stop', 'Fricative', 'Approximant',
          'Tap/flap', 'Trill', 'Lateral fricative', 'Lateral approximant']

consonant_df = pd.DataFrame(pulmonic_consonants, index=cindex)
