
from compas_fea2.model import Concrete
from compas_fea2.model import ConcreteDamagedPlasticity
from compas_fea2.model import ConcreteSmearedCrack

# ==============================================================================
# non-linear concrete
# ==============================================================================


class OpenseesConcrete(Concrete):
    """"""

    __doc__ += Concrete.__doc__

    def __init__(self, *, fck, v=0.2, density=2400, fr=None, **kwargs):
        super(OpenseesConcrete, self).__init__(fck=fck, v=v, density=density, fr=fr, **kwargs)

    def jobdata(self):
        # FIXME: This is a standard material, not a concrete material
        self.notension = False
        if not self.notension:
            line = [
                "uniaxialMaterial Elastic {} {}\n".format(self.key, self.E),
                "nDMaterial ElasticIsotropic {} {} {} {}".format(self.key + 1000, self.E, self.v, self.density),
            ]  # FIXME Remove one of the two
        else:
            line = ["uniaxialMaterial ENT {} {}\n".format(self.key, self.E)]
        return "".join(line)


class OpenseesConcreteSmearedCrack(ConcreteSmearedCrack):
    """"""

    __doc__ += ConcreteSmearedCrack.__doc__

    def __init__(self, *, E, v, density, fc, ec, ft, et, fr=[1.16, 0.0836], **kwargs):
        super(OpenseesConcreteSmearedCrack, self).__init__(E=E, v=v, density=density, fc=fc, ec=ec, ft=ft, et=et, fr=fr, **kwargs)
        raise NotImplementedError


class OpenseesConcreteDamagedPlasticity(ConcreteDamagedPlasticity):
    """"""

    __doc__ += ConcreteDamagedPlasticity.__doc__

    def __init__(self, *, E, v, density, damage, hardening, stiffening, **kwargs):
        super(OpenseesConcreteDamagedPlasticity, self).__init__(E=E, v=v, density=density, damage=damage, hardening=hardening, stiffening=stiffening, **kwargs)
        raise NotImplementedError
