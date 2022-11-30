from pprint import pprint
import nltk
import functools
from itertools import product


# check if token is a punctuation marker
def is_punct(token):
    for c in token:
        if c.isalpha(): return False
        return True


# remove punctuation and set to lowercase for list of tokens
def clean(tokens):
    return [token.lower() for token in tokens if not is_punct(token)]


# tokenize poem in file
def file_to_tokens(filepath):
    # read in poem from file
    with open(filepath, 'r') as fp:
        poem_lines = fp.readlines()

    if len(poem_lines) < 4: return 0

    # remove byte order marker
    if ord(poem_lines[0][0]) == 65279:
        poem_lines[0] = poem_lines[0][1:]

    # tokenize each line
    return [clean(nltk.tokenize.word_tokenize(line)) for line in poem_lines]


# extract unique words from token as list of lists
def build_vocab(toklines):
    vocab = functools.reduce(lambda x, y : set(x).union(set(y)), toklines)
    return vocab


# get possible stress combinations given a target pattern
# e.g. iambic4 has pattern 010101, and a possible comb. is 01 010 1
def get_stress_combinations(target_pattern, stress_to_words):
    # restrict available patterns to ones used in the target
    patterns = list(filter(lambda p : p in target_pattern, stress_to_words.keys()))
    #pattern_indices = list(range(len(patterns)))
    #print(pattern_indices)
    # enumerate all possible combinations within the length restriction
    all_poss = []
    for i in range(1, 8):
        poss = product(patterns, repeat=i)
        for item in poss:
            if ''.join(item) == target_pattern:
                all_poss.append(item)
    return all_poss


# build fsa for a SINGLE LINE
def build_fsa(pattern, vocab, stress_to_words):
    transitions = []
    for idx, syll in enumerate(pattern):
        for stress, words in stress_to_words.items():
            if stress == pattern[idx : idx + len(stress)]:
                # add transitions
                for word in words:
                    transitions.append((word, idx, idx + len(stress)))
    return transitions


toklines = file_to_tokens('../test_poem.txt')
vocab = build_vocab(toklines)


# build dict of stress pattern to sets of words w/ that stress pattern
stress_to_words = dict()
with open('stresses.txt', 'r') as fp:
    lines = fp.readlines()
    for line in lines:
        pair = line.rstrip().split(',')
        word, stress = pair[0], pair[1]
        if word not in vocab: continue
        if stress not in stress_to_words.keys():
            stress_to_words[stress] = { word }
        else:
            stress_to_words[stress].add(word)

pprint(stress_to_words)
#combs = get_stress_combinations('01010101', stress_to_words)
#pprint(combs)

fsa = build_fsa('01010101', vocab, stress_to_words)
#pprint(fsa)

# write fsa to file
with open('fsa.txt', 'w') as fp:
    for word, curr, next in fsa:
        fp.write(f'{word},{curr},{next}\n')

