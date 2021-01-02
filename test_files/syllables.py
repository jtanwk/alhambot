# syllables.py

import re

# Setup
filename = 'cmudict-0.7b.txt'
syllable_dict = {}

# Initialize dictionary
for line in open(filename, encoding='latin-1'):
    if line[0] == ';':
        continue
    else:
        word, entry = line.strip('\n').split('  ')
        syllable_dict[word] = entry

# Create function to take a string and count all syllables across words
def matches_al_ham(text):
    '''Returns True if provided string input matches syllable count and stress
    pattern for "Alexander Hamilton" phrase.'''

    def get_syllables(word):
        '''Checks input word against syllable dictionary and returns the number
        of syllables in the word. If the word is not in the dictionary, raises
        a KeyError.'''

        if word.upper() in syllable_dict.keys():
            syllable_wts = re.sub(r'[^0-9]', '', syllable_dict[word.upper()])
            return syllable_wts
        else:
            raise KeyError('Word is not recognized')

    def get_structure(text):
        '''Returns True if stresses are on 1st and 4th syllables, 1st syllable
        begins with "A", and 4th syllable begins with "H".'''

        # Remove all non-alphanumeric and non-space characters
        text = re.sub(r'[^0-9a-zA-Z ]', '', text)

        # Check if 1st and 4th syllables are primary or secondary stresses
        pattern = ''.join(list(map(get_syllables, text.split(' '))))
        if len(pattern) == 7:
            correct_stresses = int(pattern[0]) > 0 and int(pattern[4]) > 0
        else:
            correct_stresses = False

        # Segment text by syllables
        word_list = text.split(' ')

        segmented = []
        for i in word_list:
            if len(get_syllables(i)) == 1:
                segmented.append(syllable_dict[i.upper()].replace(' ', ''))
            else:
                temp = []
                buffer = ''

                for j in syllable_dict[i.upper()].split(' '):
                    buffer += j
                    if re.search(r'[0-9]', j):
                        temp.append(buffer)
                        buffer = ''
                    else:
                        continue

                segmented.extend(temp)

        print(segmented)

        correct_structure = segmented[0][0] == 'A' and segmented[4][0] == 'H'

        return correct_stresses and correct_structure

    return get_structure(text)

# Test
print(matches_al_ham('Andover is Hungary'))
