import numpy as np

class ComplexHello():
    def __init__(self, complexity) -> None:
        self.complextiy = complexity

    def hello_world(self):
        s = ''.join([str(_) for _ in np.random.rand(self.complextiy).flatten().tolist()])
        print("hello, {:s}, world!".format(s))