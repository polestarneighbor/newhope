# ######################################################################################################################
# Imports
# ######################################################################################################################
from collections import defaultdict
import numpy
import operator
import random
from scipy import stats


# ######################################################################################################################
# Class Definitions
# ######################################################################################################################
def invert(num):
    if num %12289==0:
        return 0
    mod=12289
    x=num
    inv=num
    for i in range(12):
        x=x**2%mod
        inv*=x
        inv%=12289
    x=x**2%12289
    x=x**2%12289
    inv*=x
    return inv%12289


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

        if coeffs is None:
            for index in range(len(self.__coeffs)):
                self.__coeffs[index] %= mod
        self.mod = mod
        self.degree = degree

    def __repr__(self):
        return str(self)

    def __str__(self):
        coeff_strings = []
        for coeff_number in range(len(self.coeffs)):
            if self.coeffs[coeff_number]!=0:
                coeff_strings.append(str(self.coeffs[coeff_number]) + "X^" + str(coeff_number))
        if len(coeff_strings)==0:
            return "0"
        return " + ".join(coeff_strings)

    @property
    def gaussian(self):
        samples = []
        for sample_input in numpy.arange(0, self.mod, step=self.mod / 4000):
            samples.append(self.as_function(sample_input))
        test_statistic, p_value = stats.shapiro(samples)
        return p_value > 0.05

    def as_function(self, input_value):
        output_value = 0
        for coeff_number in range(len(self.coeffs)):
            output_value += self.coeffs[coeff_number] * pow(input_value, coeff_number)
        return output_value

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

    def __neg__(self):
        c = [-i for i in self.coeffs]
        return Polynomial(c, degree=self.degree, mod=self.mod)

    def __sub__(self, other):
        return self + (-other)

    def __truediv__(self,scalar):
        c = [(self.__coeffs[i]/scalar) % self.mod for i in range(self.degree)]
        return Polynomial(coeffs=c, mod=self.mod, degree=self.degree)
    def first_nonzero(self,lst=None):
        if lst==None:
            lst=self.coeffs
        i=self.degree-1
        while lst[i]==0 and i>0:
            i-=1
        return i
    def __floordiv__(self,other):
        rem=Polynomial(coeffs=self.coeffs,mod=self.mod,degree=self.degree)
        quot=[]
        done=False
        i=0
        while not done and i<1024:
            i+=1
            pos=rem.first_nonzero()
            o_pos=other.first_nonzero()
            if i==1024:
                print("hit end")
            if pos<o_pos:
                done=True
                continue
            div=rem.coeffs[pos]*invert(other.coeffs[o_pos])%self.mod
            part_quot=other*div
            part_quot*=Polynomial(coeffs=[1 if i==pos-o_pos else 0 for i in range(self.degree)],mod=self.mod, degree=self.degree)
            rem -= part_quot
            quot+=[div]
        return Polynomial(coeffs=quot, sizelimit=0,mod=self.mod, degree=self.degree), rem
        #implement long division here
    def __eq__(self,other):
        if self.mod!=other.mod:
            return False
        if self.degree!=other.degree:
            return False
        for i in range(self.degree):
            if self.coeffs[i]!=other.coeffs[i]:
                return False
        return True
    def __lt__(self,other):
        #based on most significant digit only
        #THIS IS ONLY A PARTIAL ORDERING
        if self.mod!=other.mod:
            return False
        if self.degree!=other.degree:
            return self.degree<other.degree
        i=self.degree
        while i>=0:
            if self.degree!=0 and other.degree==0:
                return False
            if self.degree==0 and other.degree!=0:
                return True
            i-=1
        return False

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
            c = []
            for i in range(len(self.__coeffs)):
                c.append((self.__coeffs[i] * other) % self.mod)
            return Polynomial(coeffs=c, mod=self.mod, degree=self.degree)

    def signal(self):
        info_bits = []
        for coeff in self.__coeffs:
            if abs(coeff)-1 > self.mod//4:
                info_bits += [1]
            else:
                info_bits += [0]
        return Polynomial(coeffs=info_bits, degree=self.degree, mod=self.mod)

    def mod2(self, sig):
        return [(self.__coeffs[i]+sig.__coeffs[i]*sig.mod/2) % self.mod % 2 for i in range(self.degree)]


class Authority:
    def __init__(self, clientA=None, clientB=None, degree=1024, mod=12289, a=None):
        if a is None:
            self.a = Polynomial(mod=mod, degree=degree)
        else:
            self.a = a
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
    def __init__(self, secret=None, degree=1024, mod=12289):
        if secret is None:
            self.secret = Polynomial(sizelimit=mod//4, degree=degree, mod=mod)
        else:
            self.secret = secret
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


class StatsAdversary:
    def __init__(self,degree=1024,mod=12889):
        self.mod=mod
        self.degree=degree
        self.error = Polynomial(coeffs=[1]*degree,degree=degree,mod=mod)
        self.oppo_est=Polynomial(coeffs=[0]*degree,degree=degree,mod=mod)
        self.tries=0
        self.secret=0
        self.a=0

    def sendP(self, a):
        self.a=a
        return self.error

    def key_and_signal(self, a, p, signal=None):
        self.a=a
        self.oppo_est+=p
        self.tries+=1
        return p.signal(), self.error
    def guess(self):
        a_times_s=self.oppo_est/self.tries
        return (a_times_s,self.a)
        secret_est, remainder=a_times_s//self.a
        print( secret_est, remainder)

class Adversary:
    def __init__(self, degree=1024, mod=12289, accounting_for_errors=False):
        self._mod = mod
        self._degree = degree
        self._accounting_for_errors = accounting_for_errors
        self._secret = Polynomial(sizelimit=mod // 4, degree=degree, mod=12289)
        self._error = Polynomial(coeffs=[1] * degree, degree=degree, mod=mod)
        self._private_key = None
        self._public_key = None
        self._a = None
        self._signal_values = defaultdict(lambda: [])
        self._coefficients_step1 = None
        self._coefficients_step2 = None
        self._same_signs_step3 = None
        self._attack_steps = self._attack_steps()
        self._attack_complete = False
        self._guess = None

    @property
    def guess(self):
        return self._guess

    def sendP(self, a):
        self._a = a
        try:
            return self._attack_steps.__next__()
        except StopIteration:
            self._attack_complete = True
            raise StopIteration

    def _attack_steps(self):
        for p in self._attack_step_1():
            yield p
        self._coefficients_step1 = self._interpret_signal_changes()
        for p in self._attack_step_2():
            yield p
        self._coefficients_step2 = self._interpret_signal_changes()
        self._attack_step_3()
        # Step 4 is just step 3, but for all coefficients, so step 3 was simplified to everything
        # Step 5 should check the distribution to see if it is right, but whatever for now.
        self._guess = self._attack_step_5()
        raise StopIteration

    def _interpret_signal_changes(self):
        def basic_logic(list_of_changes):
            if len(list_of_changes) == 0:
                return 0
            value = list_of_changes[0]
            number_of_changes = 0
            for change in list_of_changes[1:]:
                if value != change:
                    value = change
                    number_of_changes += 1
            # Check wrap around
            if list_of_changes[0] != list_of_changes[-1]:
                number_of_changes += 1

            return number_of_changes // 2

        def error_accounting_logic(list_of_changes):
            if len(list_of_changes) == 0:
                return 0
            value = list_of_changes[0]
            number_of_changes = 0
            changes_in_a_row = 0
            for change in list_of_changes[1:]:
                if value != change:
                    value = change
                    changes_in_a_row += 1
                    if changes_in_a_row == 3:
                        number_of_changes += 1
                        changes_in_a_row = 0
                else:
                    if changes_in_a_row == 1:
                        number_of_changes += 1
                        changes_in_a_row = 0
                    elif changes_in_a_row == 2:
                        changes_in_a_row = 0

                return number_of_changes // 2

        results = []
        cooeficients = list(self._signal_values.keys())
        cooeficients.sort()
        for cooeficient in cooeficients:
            if not self._accounting_for_errors:
                results.append(basic_logic(self._signal_values[cooeficient]))
            else:
                results.append(error_accounting_logic(self._signal_values[cooeficient]))
        self._signal_values = defaultdict(lambda: [])
        return results

    def _attack_step_1(self):
        for k in range(self._mod):
            yield k

    def _attack_step_2(self):
        poly_const = Polynomial([1, 1], sizelimit=0, degree=self._degree, mod=self._mod)
        for k in range(self._mod):
            yield poly_const * k

    # Determine if things have the same or different sign
    def _attack_step_3(self):
        self._same_signs_step3 = [True] * self._degree
        # First pair
        self._same_signs_step3[0] = True if self._coefficients_step2[0] == \
                                            self._coefficients_step1[0] + self._coefficients_step1[-1] else False

        # Remaining pairs
        for i in range(0, len(self._coefficients_step1)-1):
            self._same_signs_step3[i+1] = True if self._coefficients_step1[i] == \
                                                  self._coefficients_step1[i] + self._coefficients_step1[i+1] else False

    def _attack_step_5(self):
        def create_guess():
            coefficients = []
            for coefficient_number in range(len(self._coefficients_step1)):
                coefficients.append(self._coefficients_step1[coefficient_number])

            for coefficient_number in range(len(self._coefficients_step1)):
                # Set prior coefficient
                if self._same_signs_step3[coefficient_number]:
                    comparison = operator.lt
                else:
                    comparison = operator.gt

                if comparison(coefficients[coefficient_number], 0):
                    coefficients[coefficient_number-1] = -self._coefficients_step1[coefficient_number-1]
                else:
                    coefficients[coefficient_number-1] = self._coefficients_step1[coefficient_number-1]

                # Set next coefficient
                index = (coefficient_number + 1) % len(self._coefficients_step1)
                if self._same_signs_step3[index]:
                    comparison = operator.lt
                else:
                    comparison = operator.gt

                if comparison(coefficients[coefficient_number], 0):
                    coefficients[index] = -self._coefficients_step1[index]
                else:
                    coefficients[index] = self._coefficients_step1[index]
            return coefficients

        coefficients = create_guess()
        guess = Polynomial(coeffs=coefficients, degree=self._degree, mod=self._mod)
        test = self._public_key - (self._a * guess)
        if test.gaussian:
            return guess
        else:
            for coefficient_number in range(len(coefficients)):
                coefficients[coefficient_number] = -coefficients[coefficient_number]
            guess = Polynomial(coeffs=coefficients, degree=self._degree, mod=self._mod)
            test = self._public_key - (self._a * guess)
            if test.gaussian:
                return guess
            else:
                raise RuntimeError("Unable to find solution!")

    def key_and_signal(self, a, p, signal=None):
        self._public_key = p
        if signal is not None:
            for coeff_index in range(len(signal.coeffs)):
                self._signal_values[coeff_index].append(signal.coeffs[coeff_index])

        poly = self._secret * p
        if signal is None:
            signal = poly.signal()
        self._private_key = poly.mod2(signal)
        return poly.signal(), self._secret * a + self._error
