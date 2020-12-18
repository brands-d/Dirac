import h5py

from dirac import __directory__
from .dirac_solver import DiracSolver


class DiracModel:

    def __init__(self, settings):
        self.settings = settings

    def run(self, callback=None):
        import numpy as np
        from dirac.library.spinor import Spinor
        dx, dy, dt = [self.settings[key] for key in ('dt', 'dx', 'dy')]
        M, N = 50, 50
        x, y = np.meshgrid(np.linspace(-1, 1, N), np.linspace(-1, 1, M))
        d = np.sqrt(x**2 + y**2)
        sigma, mu = 0.1, 0.0
        g = np.exp(-((d - mu)**2 / (2.0 * sigma**2)))
        s0 = Spinor(g, np.zeros(g.shape), periodic=True)
        solver = DiracSolver(s0, 1000, delta=(dx, dy, dt))
        result = solver.solve(callback=callback)
        return result

    def save_results(self, results):
        if self.settings['is save']:
            path = __directory__ / '../output' / self.settings['file name']
            with h5py.File(str(path), 'w') as file:
                # file.create_dataset(results)
                pass
