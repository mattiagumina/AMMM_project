import os, random
import numpy as np
import math
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

            D = random.randint(min(math.ceil(math.sqrt(N)), N // 4), max(math.ceil(math.sqrt(N)), N // 4))

            d = []
            for p in range(D):
                d.extend([p + 1] * (N // D))
            d += [random.randint(1, D) for _ in range(N % D)]

            n = [] 
            for p in range(D):
                M = 0
                for j in range(N):
                    if d[j] == p + 1:
                        M += 1
                n += [random.randint(1, M - 1)]
            
            m = [[0.00] * N for _ in range(N)]
            for j in range(N):
                for k in range(j, N):
                    if j == k:
                        m[j][k] = 1.00
                    else:
                        c = np.random.normal(0.50, 0.15)
                        c = np.clip(c, 0.00, 1.00)
                        m[j][k] = c
                        m[k][j] = c

            fInstance.write(f"D = {D};\n")
            fInstance.write(f"n = [ {' '.join(map(str, n))} ];\n\n")
            fInstance.write(f"N = {N};\n")
            fInstance.write(f"d = [ {' '.join(map(str, sorted(d)))} ];\n\n")
            fInstance.write("m = [\n")
            for row in m:
                fInstance.write(f"    [ {' '.join(f'{value:.2f}' for value in row)} ]\n")
            fInstance.write("];\n")


            fInstance.close()
