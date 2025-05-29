from compas_fea2.model import TieConstraint


class OpenseesTieConstraint(TieConstraint):
    def __init__(self, master, slave, **kwargs):
        super(OpenseesTieConstraint, self).__init__(master, slave, tol=None, **kwargs)
        raise NotImplementedError
