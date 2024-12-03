'''
AMMM P2 Instance Generator v2.0
Instance Generator class.
Copyright 2020 Luis Velasco.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os, random
import numpy as np
from AMMMGlobals import AMMMException


class InstanceGenerator(object):
    # Generate instances based on read configuration.

    def __init__(self, config):
        self.config = config

    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances

        N = self.config.N

        if not os.path.isdir(instancesDirectory):
            raise AMMMException('Directory(%s) does not exist' % instancesDirectory)

        for i in range(numInstances):
            instancePath = os.path.join(instancesDirectory, '%s%d_%d.%s' % (fileNamePrefix, N, i, fileNameExtension))
            fInstance = open(instancePath, 'w')

            D = random.randint(2, max(2, N // 2))
            
            C = random.randint(D, N - 1)
            
            partitions = [0] + sorted(random.sample(range(1, C), D - 1)) + [C]
            n = [partitions[i+1] - partitions[i] for i in range(D)]
            
            # Create department assignments
            d = []
            for p in range(D):
                d.extend([p + 1] * (n[p]))  # Assign initial members equally to departments
            d += [random.randint(1, D) for _ in range(N - C)]  # Distribute remaining members randomly
            
            m = np.random.uniform(0.0, 1.0, (N, N)).round(2)
            m = (m + m.T) / 2
            np.fill_diagonal(m, 1.0)

            fInstance.write(f"D = {D};\n")
            fInstance.write(f"n = [ {' '.join(map(str, n))} ];\n\n")
            fInstance.write(f"N = {N};\n")
            fInstance.write(f"d = [ {' '.join(map(str, sorted(d)))} ];\n\n")
            fInstance.write("m = [\n")
            for row in m:
                fInstance.write(f"    [ {' '.join(f'{value:.2f}' for value in row)} ]\n")
            fInstance.write("];\n")


            fInstance.close()
