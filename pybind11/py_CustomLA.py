import ROL
class MyObj(ROL.Objective):
    def __init__(self):
        ROL.Objective.__init__(self)

    def value(self, x, tol):
        return (x[0] - 1)**2 + x[1]**2

    def gradient(self, g, x, tol):
        g[0] = 2 * (x[0] - 1)
        g[1] = 2 * x[1]
obj = MyObj()

params = """
<ParameterList>
  <ParameterList name="Step">
    <ParameterList name="Line Search">
      <ParameterList name="Descent Method">
        <Parameter name="Type" type="string" value="Quasi-Newton Method"/>
      </ParameterList>
    </ParameterList>
  </ParameterList>
  <ParameterList name="Status Test">
    <Parameter name="Gradient Tolerance" type="double" value="1e-12"/>
    <Parameter name="Step Tolerance" type="double" value="1e-16"/>
    <Parameter name="Iteration Limit" type="int" value="10"/>
  </ParameterList>
</ParameterList>
"""

algo = ROL.Algorithm("Line Search", params)

import numpy as np
class NPBasedLA(ROL.CustomLA):
    def __init__(self, size):
        ROL.CustomLA.__init__(self)
        self.data = np.zeros(size)
        self.size = size

    def plus(self, xx):
        self.data += xx.data

    def scale(self, alpha):
        self.data *= alpha

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, i, v):
        self.data[i] = v

    def dot(self, xx):
        return np.inner(self.data, xx.data)

    def dimension(self):
        return self.size

    def basis(self, i):
        res = NPBasedLA(self.size)
        res[i] = 1.0
        return res

    def clone(self):
        res = NPBasedLA(self.size)
        res.data = np.copy(self.data)
        return res

x = NPBasedLA(2)
y = NPBasedLA(2)
z = NPBasedLA(2)
x.data[0] = 1.0
x.data[1] = 1.5

x.checkVector(y, z)

algo.run(x, obj)
print x.data