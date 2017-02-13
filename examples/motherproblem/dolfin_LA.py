import ROL


class dolfinLA(ROL.CustomLA):
    def __init__(self, vec, inner):
        ROL.CustomLA.__init__(self)
        self.vec = vec
        self.inner = inner

    def plus(self, x):
        self.vec += x.vec

    def scale(self, alpha):
        self.vec *= alpha

    def __getitem__(self, i):
        return self.vec[i][0]

    def __setitem__(self, i, v):
        self.vec[i] = v

    def dot(self, xx):
        if self.inner is not None:
            return self.inner.eval(self.vec, xx.vec)
        else:
            return self.vec.inner(xx.vec)

    def dimension(self):
        return self.vec.size()

    def basis(self, i):
        res = dolfinLA(self.vec.copy(), self.inner)
        res.scale(0.0)
        res[i] = 1.0
        return res

    def clone(self):
        res = dolfinLA(self.vec.copy(), self.inner)
        return res