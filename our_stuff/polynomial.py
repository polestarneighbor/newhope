import random
class Polynomial:
    def __init__(self, coeffs=None, sizelimit=None, degree=1024, mod=12289):
        if coeffs is None:
            coeffs=[]
        self.__coeffs=coeffs

        if sizelimit is None:
            sizelimit = mod//2

        if sizelimit == 0:
            while len(self.__coeffs)<degree:
                self.__coeffs.append(0)
        else:
            while len(self.__coeffs)<degree:
                self.__coeffs.append(random.randint(-sizelimit,sizelimit)%mod)

        for index  in range(len(self.__coeffs)):
            self.__coeffs[index] %=mod
        self.mod=mod
        self.degree=degree
    def __repr__(self):
        print(self.__coeffs)
    def coeff_to_byte(x):
        firstbyte=x//256
        secondbyte=x%256
        return firstbyte,secondbyte

    def to_bits(self):
        sequence=()
        for coeff in self.__coeffs:
            sequence+=Polynomial.coeff_to_byte(coeff)
        return bytes(sequence)
    def __add__(self,other):
        c=[(self.__coeffs[i]+other.__coeffs[i])%self.mod for i in range(self.degree)]
        return Polynomial(coeffs=c,mod=self.mod,degree=self.degree)
    def __mul__(self,other):
        #FIXME implement this please
        return Polynomial()
    def signal(self):
        info_bits=[]
        for coeff in self.__coeffs:
            if abs(coeff)-1>self.mod//4:
                info_bits+=[1]
            else:
                info_bits+=[0]
        return Polynomial(coeffs=info_bits,degree=self.degree,mod=self.mod)

    def mod2(self,sig):
        return [ (self.__coeffs[i]+sig.__coeffs[i]*sig.mod/2)%self.mod %2 for i in range(self.degree)]

    def reconcile(v,w):
        v+=(w*(q-1)/2).mod2()

class Authority():
    def __init__(self, clientA=None, clientB=None):
        self.a=Polynomial()
        if clientA is None:
            self.clientA=KeyExchanger()
        else:
            self.clientA=clientA
        if clientB is None:
            self.clientB=KeyExchanger()
        else:
            self.clientB=clientB
    def runExchange(self):
        pA=self.clientA.sendP(self.a)
        sig, pB = self.clientB.key_and_signal(self.a,pA)
        self.clientA.key_and_signal(self.a,pB)
    def checkExchange(self):
        print(self.clientA.key)
        print(self.clientB.key)

class KeyExchanger():
    def __init__(self):
        self.secret=Polynomial(sizelimit=12889//4)
        self.error=Polynomial(sizelimit=12889//4)
        self.key=None
    def sendP(self,a):
         return self.secret*a+self.error

    def key_and_signal(self,a,p,signal=None):
        poly=self.secret*p
        if signal is None:
            signal=poly.signal()
        self.key=poly.mod2(signal)
        return poly.signal(), self.secret*a+self.error
