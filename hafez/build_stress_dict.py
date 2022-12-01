import cmudict

# words to stress pattern
stress_dict = dict()
pdict = cmudict.dict()
for word, prons in pdict.items():
    # get the most common pronunciation
    pron = prons[0]

    # compute stress pattern
    stress = ''
    for phoneme in pron:
        if phoneme[-1] == '0':
            stress += '0'
        elif phoneme[-1] == '1' or phoneme[-1] == '2':
            stress += '1'

    # add to dictionary
    stress_dict[word] = stress
 
# write to file
with open('stresses.txt', 'w') as fp:
    for word, stress in stress_dict.items():
        fp.write(f'{word},{stress}\n')

