"""Command line version of lingenia, using argparse"""

import argparse
from lingenia import phonology_class as pc

parser = argparse.ArgumentParser()


parser.add_argument('-vn', help='Number of vowels for language.', action='store', dest='vnum',
                    type=int)
parser.add_argument('-cn', help='Number of consonants for language.', action='store', dest='cnum',
                           type=int)

args = parser.parse_args()

if not args.vnum:
    pass
    # Generate number of vowels.

if not args.cnum:
    pass
    # Generate number of consonants.

phonology_lists = pc.Phonology(args.cnum, args.vnum)

phonology_lists.generate_vowels_full()
print(phonology_lists.vowels)
phonology_lists.generate_all_consonants()
