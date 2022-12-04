# beam search

import json
from random import randint
from pprint import pprint


# read in fsa and create dictionary mapping
# dict : (current state, next state) -> set of words
def get_transitions(fsa_fpath):
    transitions = dict()
    with open(fsa_fpath, 'r') as fp:
        for line in fp.readlines():
            [word, curr, next] = line.rstrip().split(',')
            if (curr,next) not in transitions.keys():
                transitions[(curr,next)] = { word }
            else:
                transitions[(curr,next)].add(word)
    return transitions


# retrieve transitions leading up to current
def retrieve_last(backptrs, curr):
    ts = []
    for t in backptrs.keys():
        if t[1] == curr:
            ts.append(t)
    return ts


# compute transition probability P(a | b)
def get_tprob(a, b, tprobs, oov):
    if b in tprobs[a].keys():
        return tprobs[a][b]
    else:
        return oov


# given dictionary {str : float}, return top 3
def get_top_3(d, used):
    top_3 = dict()
    s = sorted(list(d.items()), key=lambda i:i[1], reverse=True)

    count = 0
    for word, prob in s:
        if word not in used and randint(0, 10) > 3:
            top_3[word] = prob
            count += 1
        if count == 3: break

    return top_3


# given current top paths and candidates, compute new top paths
def get_new_top_paths(top_paths, candidates, t, tprobs, oov, used):
    new_paths = dict()
    for path, path_prob in top_paths.items():
        for cand in candidates[t]:
            prob = path_prob * get_tprob(cand, path, tprobs, oov)

            # penalty for repeated words
            if cand in used:
                #used[cand] *= 0.1
                prob *= 0.01

            new_paths[cand] = prob
            #print(f'P({cand}|{path}) = {prob}')

    # eliminate all but top 3
    top_3 = get_top_3(new_paths, used)
    return top_3


# perform beam search
def beam_search(num_states, fsa_fpath, tprob_fpath, used):
    # read fsa
    transitions = get_transitions(fsa_fpath)

    # read transition probabilities
    with open(tprob_fpath, 'r') as fp:
        tprobs = json.load(fp)

    # backpointers
    # { transition : { word : prob of path up to that point } }
    backptrs = { key:dict() for key in transitions.keys() }

    oov_prob = 0.00001
    for t in transitions.keys():
        if t[0] == '0':
            for word in transitions[t]:
                # OOV check
                if 'START' not in tprobs[word].keys():
                    backptrs[t][word] = oov_prob
                else:
                    backptrs[t][word] = tprobs[word]['START']

    #pprint(backptrs)
    
    for state in range(1, num_states):
        # retrieve candidate words at current step
        # { next_state : set of words }
        candidates = dict()
        for t in transitions.keys():
            if str(state) == t[0]:
                candidates[t] = transitions[t]

        # for each transition out of current state
        for t in candidates.keys():
            # get previous transitions
            prevs = retrieve_last(backptrs, t[0])

            # retrieve top paths up to current point
            for prev in prevs:
                top_paths = backptrs[prev]

                # compute P( candidates[t] | word in top_paths )
                new = get_new_top_paths(top_paths, candidates, t, tprobs, oov_prob, used)
                backptrs[t] = new

    #pprint(backptrs)
    return backptrs


def decode(backptrs, num_states, dupl):
    final_state = str(num_states)
    line = []
    #dupl = set()

    # recover final transition
    last_t = ('_', '-1')
    best_pair = ('_', 0)
    for t in reversed(backptrs.keys()):
        if t[1] == final_state:
            for word, prob in backptrs[t].items():
                if prob > best_pair[1] and word not in dupl:
                    best_pair = (word, prob)
                    last_t = t
    line.append(best_pair[0])
    dupl.add(best_pair[0])
    #print(best_pair, last_t)


    # recover rest of transitions
    for i in range(num_states):
        best_pair = ('_', 0)

        # get previous transitions
        prevs = retrieve_last(backptrs, last_t[0])
        if len(prevs) == 0:
            break

        # compute new best
        for t in reversed(prevs):
            for word, prob in backptrs[t].items():
                if prob > best_pair[1] and word not in dupl:
                    best_pair = (word, prob)
                    last_t = t
        dupl.add(best_pair[0])
        #print(best_pair, last_t)

        # add to output
        line.append(best_pair[0])

    return ' '.join(reversed(line))


def generate(num_lines, num_states):
    used, dupl = set(), set()
    for _ in range(num_lines):
        backptrs = beam_search(num_states, 'fsa.txt', 'transition_probs.json', used)
        #pprint(backptrs)
        line = decode(backptrs, num_states, dupl)
        backptrs.clear()
        print(line)

#generate(5, 8)

