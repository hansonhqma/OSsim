class rand48:
    def __init__(self, seed:int) -> None:
        self.__a = 0x5DEECE66D
        self.__c = 0xB
        self.__n = int(bin(seed)[2:].zfill(32) + bin(0x330E)[2:].zfill(16), 2)
        self.__m = 2**48

    def __next(self) -> int:
        self.__n = (self.__a * self.__n + self.__c) & (self.__m - 1)
        return self.__n
    
    def drand48(self) -> int:
        return self.__next() / self.__m

    def seed(self) -> int:
        return self.__n
