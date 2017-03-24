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
