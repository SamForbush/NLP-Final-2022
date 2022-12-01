# beam search

import json


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

    # TODO populate backpointers for initial state

    oov_prob = 0.00001
    for state in range(num_states):
        # retrieve candidate words at current step
        # { next_state : set of words }
        candidates = dict()
        for t in transitions.keys():
            if str(state) == t[0]:
                candidates[t] = transitions[t]

        # retrieve top paths up to current point
        for t in candidates.keys():
            top_paths = backptrs[t]

        # TODO compute new top paths


#beam_search(8, 'transition_probs.json')
print(get_transitions('fsa.txt'))

