# beam search

import json
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
def get_top_3(d):
    s = sorted(list(d.items()), key=lambda i:i[1])
    #print(sorted(d.items(), key=lambda i:i[1]))
    #print(s[-3:])
    return dict(s[-3:])


# given current top paths and candidates, compute new top paths
def get_new_top_paths(top_paths, candidates, t, tprobs, oov):
    new_paths = dict()
    for path, path_prob in top_paths.items():
        for cand in candidates[t]:
            prob = path_prob * get_tprob(cand, path, tprobs, oov)
            new_paths[cand] = prob
            #print(f'P({cand}|{path}) = {prob}')

    # eliminate all but top 3
    return get_top_3(new_paths)


# perform beam search
def beam_search(num_states, fsa_fpath, tprob_fpath):
    # read fsa
    transitions = get_transitions(fsa_fpath)

    # read transition probabilities
    with open(tprob_fpath, 'r') as fp:
        tprobs = json.load(fp)

    # backpointers
    # { transition : { word : prob of path up to that point } }
    backptrs = { key:dict() for key in transitions.keys() }

    oov_prob = 0.00001
    # TODO populate backpointers for initial state
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
            #print(t, prevs, candidates[t])

            # retrieve top paths up to current point
            for prev in prevs:
                top_paths = backptrs[prev]
                #print('top paths: ', end='')
                #pprint(top_paths)

                # compute P( candidates[t] | word in top_paths )
                new = get_new_top_paths(top_paths, candidates, t, tprobs, oov_prob)
                backptrs[t] = new
                #print(new)

        #print('\n')
    pprint(backptrs)
    return backptrs


def decode(backptrs, num_states):
    final_state = str(num_states)

    # recover final transition
    last_t = ('_', '-1')
    best_prob = 0
    for t in backptrs.keys():
        if t[1] == final_state:
            best = pick_max(backptrs[t])

beam_search(8, 'fsa.txt', 'transition_probs.json')
#print(get_transitions('fsa.txt'))

