import random
class Polynomial:
    degree=1024
    mod=12289
    def __init__(self, sizelimit=mod//2):
        self.__coeffs=[random.randint(-b,b)%mod for x in range(degree)]
    def __init__(self, coeffs=None)
        if coeffs is None:
            coeffs=[]
        self.__coeffs=coeffs
        while len(self.__coeffs)<degree:
            self.__coeffs.append(0)
        i=0
        while i<len(self.__coeffs):
            self.__coeffs[i] %=mod
    def coeff_to_byte(x):
        firstbyte=x//256
        secondbyte=x%256
        return firstbyte,secondbyte
    def to_bits(self):
        sequence=()
        for coeff in self.__coeffs:
            sequence+=Polynomial.coeff_to_byte(coeff)
        return bytes(sequence)
    def signal(self):
        info_bits=''
        random=random.randint(0,1)
        for coeff in self.__coeffs:
            if abs(coeff)-1>q//4:
                info_bits+='1'
            else:
                info_bits+='0'
        info_list=b''
        while len(info_bits)>3:
            byte=info_bits[0:3]
            info_bits=info_bits[3:]
            info_list+=bytes([int(byte,2)])
        return info_list
    def mod2(self):
        return [ x%2 for x in self.__coeffs]
    def reconcile(v,w):
        v+=(w*(q-1)/2).mod2()
