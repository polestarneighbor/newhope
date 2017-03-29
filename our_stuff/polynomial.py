# ######################################################################################################################
# Imports
# ######################################################################################################################
from collections import defaultdict
import random


# ######################################################################################################################
# Class Definitions
# ######################################################################################################################
class Polynomial:
    def __init__(self, coeffs=None, sizelimit=None, degree=1024, mod=12289):
        if coeffs is None:
            coeffs = []
        self.__coeffs = coeffs

        if sizelimit is None:
            sizelimit = mod//2

        if sizelimit == 0:
            while len(self.__coeffs) < degree:
                self.__coeffs.append(0)
        else:
            while len(self.__coeffs) < degree:
                self.__coeffs.append(random.randint(-sizelimit, sizelimit) % mod)

        for index in range(len(self.__coeffs)):
            self.__coeffs[index] %= mod
        self.mod = mod
        self.degree = degree

    def __repr__(self):
        return self.__coeffs

    @property
    def coeffs(self):
        return self.__coeffs

    def coeff_to_byte(self, x):
        firstbyte = x//256
        secondbyte = x % 256
        return firstbyte,secondbyte

    def to_bits(self):
        sequence = ()
        for coeff in self.__coeffs:
            sequence += Polynomial.coeff_to_byte(coeff)
        return bytes(sequence)

    def __add__(self, other):
        c = [(self.__coeffs[i]+other.__coeffs[i]) % self.mod for i in range(self.degree)]
        return Polynomial(coeffs=c, mod=self.mod, degree=self.degree)

    def __mul__(self, other):
        if type(other) == Polynomial:
            c = [0]*(self.degree+other.degree-1)  # least significant on the left
            for i in range(len(other.__coeffs)):
                x = [0]*i+[y*other.__coeffs[i] for y in self.__coeffs]
                for xi in range(len(x)):
                    c[xi] += x[xi]
            if len(c)>=self.degree:
                for j in range(len(c)-1, -1, self.degree-1):
                    c[j-self.degree] += c[j]
                del c[self.degree:len(c)]
            truncate = None  # Marks the start of the leading zeros
            for i in range(len(c)):
                c[i] %= self.mod  # mods each coefficent by modulus
                if c[i] == 0:
                    truncate = i
                elif c[i] != 0:
                    truncate = None
            if truncate is not None:
                c = c[:truncate]
            return Polynomial(coeffs=c, mod=self.mod, degree=self.degree)
        else:
            for i in range(len(self.__coeffs)):
                self.__coeffs[i] *= other
                self.__coeffs[i] % self.mod
            return Polynomial(coeffs=self.__coeffs, mod=self.mod, degree=self.degree)        

    def signal(self):
        info_bits = []
        for coeff in self.__coeffs:
            if abs(coeff)-1>self.mod//4:
                info_bits += [1]
            else:
                info_bits += [0]
        return Polynomial(coeffs=info_bits, degree=self.degree, mod=self.mod)

    def mod2(self, sig):
        return [(self.__coeffs[i]+sig.__coeffs[i]*sig.mod/2) % self.mod % 2 for i in range(self.degree)]


class Authority:
    def __init__(self, clientA=None, clientB=None, degree=1024, mod=12289):
        self.a=Polynomial()
        if clientA is None:
            self.clientA=KeyExchanger(degree=degree, mod=mod)
        else:
            self.clientA=clientA
        if clientB is None:
            self.clientB=KeyExchanger(degree=degree, mod=mod)
        else:
            self.clientB=clientB

    def runExchange(self):
        pA=self.clientA.sendP(self.a)
        sig, pB = self.clientB.key_and_signal(self.a, pA)
        self.clientA.key_and_signal(self.a, pB, sig)

    def checkExchange(self):
        print(self.clientA.key)
        print(self.clientB.key)


class KeyExchanger:
    def __init__(self, degree=1024, mod=12289):
        self.secret = Polynomial(sizelimit=mod//4, degree=degree, mod=mod)
        self.error = Polynomial(sizelimit=mod//4, degree=degree, mod=mod)
        self.key = None

    def sendP(self, a):
        return self.secret*a+self.error

    def key_and_signal(self, a, p, signal=None):
        poly = self.secret*p
        if signal is None:
            signal = poly.signal()
        self.key = poly.mod2(signal)
        return signal, self.secret*a+self.error


class Adversary:
    def __init__(self, degree=1024, mod=12289):
        self.mod = mod
        self.degree = degree
        self.secret = Polynomial(sizelimit=mod // 4, degree=degree, mod=12289)
        self.error = Polynomial(coeffs=[1]*degree, degree=degree, mod=1)
        self.key = None
        self.signal_values = defaultdict(lambda: None)
        self.signal_changes = defaultdict(lambda: 0)
        self.preys_key = None
        self._attack_steps = self._attack_steps()
        self._attack_complete = False

    def sendP(self, a):
        try:
            return self._attack_steps.__next__()
        except StopIteration:
            self._attack_complete = True
            return self._normal_sendP(a)

    def _attack_steps(self):
        step1 = self._attack_step_1()
        try:
            return step1.__next__()
        except StopIteration:
            raise StopIteration

    def _attack_step_1(self):
        for k in range(self.mod):
            yield self.error * k

    def _normal_sendP(self, a):
        self.secret * a + self.error

    def _interpret_signal_changes(self):
        self.preys_key = []
        keys = list(self.signal_values.keys())
        keys.sort()
        for key in keys:
            self.preys_key.append(self.signal_changes[key]//2)

    def key_and_signal(self, a, p, signal=None):
        if signal is not None:
            for coeff_index in range(len(signal.coeffs)):
                if self.signal_values[coeff_index] is None:
                    self.signal_values[coeff_index] = signal.coeffs[coeff_index]
                else:
                    if self.signal_values[coeff_index] != signal.coeffs[coeff_index]:
                        self.signal_values[coeff_index] = signal.coeffs[coeff_index]
                        self.signal_changes[coeff_index] += 1

        poly = self.secret*p
        if signal is None:
            signal = poly.signal()
        self.key = poly.mod2(signal)
        return poly.signal(), self.secret*a+self.error
