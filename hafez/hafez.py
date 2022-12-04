from build_tprobs import build_tprobs
from build_fsa import corpus_to_fsa
from beam_search import generate


def hafez(corpus_fpath, stress_pattern, num_lines, num_states):
    corpus_to_fsa(corpus_fpath, stress_pattern)
    build_tprobs(corpus_fpath)
    generate(num_lines, num_states)


hafez('../StylusPoems1977,2015,2022.csv' , '01010101', 8, 8)

