import json
from pprint import pprint
from build_fsa import file_to_tokens, build_vocab


def build_tprobs(corpus_fpath):
    # read lines from file
    toklines = file_to_tokens(corpus_fpath)

    # empty dictionary of transition counts
    # key is word, value is dictionary of preceding words
    vocab = build_vocab(toklines)
    tdict = { word:dict() for word in vocab }
    tdict['END'] = dict()

    # probability P( word | START )
    # probability P( END  | word  )
    for line in toklines:
        if len(line) < 2: continue
        tdict[line[0]]['START'] = 1
        tdict['END'][line[-1]] = 1

    # populate tdict
    for line in toklines:
        if len(line) < 2: continue
        for idx, word in enumerate(line[1:]):
            prev = line[idx]
            if prev in tdict[word]:
                tdict[word][prev] += 1
            else:
                tdict[word][prev] = 1

    # normalize each count by total preceding counts
    for word, prevs in tdict.items():
        total_count = sum(prevs.values())
        for prev in prevs.keys():
            prevs[prev] = prevs[prev] / total_count

    #pprint(tdict)
    # write to file
    with open('transition_probs.json', 'w') as fp:
        json.dump(tdict, fp, indent=2)


#build_tprobs('../test_poem.txt')
