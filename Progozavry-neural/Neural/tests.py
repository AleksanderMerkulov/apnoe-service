# some_file.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../Progozavry/')
from Neural.net import Network
from Neural.dataset import Dataset

size = 10
print('Loading dataset')
d1 = Dataset()
d1.load('../', 3)
d2 = Dataset()
d2.load('../', 6)
print('Dataset loaded')
#d = Dataset()
#d.load('../', size)
n1 = Network(size)
n2 = Network(size)
try:
    n1.loadWeights('1.weights.h5')
    n2.loadWeights('2.weights.h5')
except:
    pass
n1.train(d1, 14)
n2.train(d2, 14)
n1.saveWeights('1.weights.h5')
n2.saveWeights('2.weights.h5')