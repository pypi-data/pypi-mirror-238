from testbook import testbook

import os
from os import makedirs
from os.path import exists
assert len(set(['interpretable','examples','tests']) - set(os.listdir('.')))==0
assert exists('./examples/inputs')
makedirs('./examples/outputs',exist_ok=True)

@testbook('examples/interpretable_01_preprocess.ipynb', execute=True)
def test_interpretable_01_preprocess(tb):
    pass # execute only because tests are present in the notebook itself
    return

@testbook('examples/interpretable_02_learn.ipynb', execute=True)
def test_interpretable_02_learn(tb):
    pass # execute only because tests are present in the notebook itself
    return

@testbook('examples/interpretable_03_evaluate.ipynb', execute=True)
def test_interpretable_03_evaluate(tb):
    pass # execute only because tests are present in the notebook itself
    return

@testbook('examples/interpretable_04_interpret.ipynb', execute=True)
def test_interpretable_04_interpret(tb):
    pass # execute only because tests are present in the notebook itself
    return