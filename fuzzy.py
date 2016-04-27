import itertools
from random import *

with open("data_training.csv", "r") as ins:
    data_training = []
    for line in ins:
        a = (line.replace("\n","").replace("_","").lower()).split(',')
        a[0] = float(a[0])
        a[1] = float(a[1])
        a[2] = float(a[2])
        a[3] = int(a[3])
        data_training.append(a)

class keanggotaan:
    def __init__(self, data, _min, _max):
        self.anggota = []
        self._min = _min
        self._max = _max
        for a in data:
            if a.b < _min:
                a.b = _min
            if a.c > _max:
                a.c = _max
            self.anggota.append(a)
    def countDerajat(self, data):
        score = []
        for i in self.anggota:
            if(data >= i.a and data <= i.d):
                if(data >= i.b and data <= i.c):
                    score.append({i.nama:1})
                elif(data > i.a and data < i.b):
                    score.append({i.nama:((data - i.a) / (i.b - i.a))})
                elif(data > i.c and data < i.d):
                    score.append({i.nama:(-(data - i.d) / (i.d - i.c))})
        return score

class trapesium:
    def __init__(self,a,b,c,d,nama):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.nama = nama

class fuzzy:
    def __init__(self, data, uns):
        self.data = data
        anggotastg = ["kurang","cukup","berlebihan"]
        anggotascg = ["kurang","cukup","berlebihan"]
        anggotapeg = ["kurang","cukup","baik"]
        self.stg = keanggotaan(
            [
                trapesium(0, 0, 0.16, 0.27, anggotastg[0]),
                trapesium(0.16, 0.27, 0.4, 0.5, anggotastg[1]),
                trapesium(0.4, 0.5, 1, 1, anggotastg[2])
            ],0,1
        )
        self.scg = keanggotaan(
            [
                trapesium(0, 0, 0.15, 0.29, anggotascg[0]),
                trapesium(0.15, 0.29, 0.5, 0.6, anggotascg[1]),
                trapesium(0.5, 0.6, 1, 1, anggotascg[2])
            ],0,1
        )
        self.peg = keanggotaan(
            [
                trapesium(0, 0, 0.1, 0.4, anggotapeg[0]),
                trapesium(0.1, 0.4, 0.7, 0.8, anggotapeg[1]),
                trapesium(0.7, 0.8, 1, 1, anggotapeg[2])
            ],0,1
        )
        self.fuzzyrule = {}
        anggota = [anggotastg,anggotascg,anggotapeg]
        urutan = 0
        for t in itertools.product(*anggota):
            self.fuzzyrule[t[0]+"|"+t[1]+"|"+t[2]] = uns[urutan]
            urutan += 1
        self.fuzifikasi()
        self.inferensi()
        self.defuzifikasi()
        self.koreksi()

    def fuzifikasi(self):
        self.hasil = []
        for data in self.data:
            self.hasil.append([self.stg.countDerajat(data[0]),self.scg.countDerajat(data[1]),self.peg.countDerajat(data[2])])

    def inferensi(self):
        self.iResult = []
        for data in self.hasil:
            inf = []
            hasil = {}
            for i in range(4):
                hasil[i] = 0
            for t in itertools.product(*data):
                kombinasi = t[0].keys()[0]+"|"+t[1].keys()[0]+"|"+t[2].keys()[0]
                if not (kombinasi in inf):
                    inf.append(self.fuzzyrule[kombinasi])
                    hasil[self.fuzzyrule[kombinasi]] = min(t).values()[0]
                else:
                    hasil[self.fuzzyrule[kombinasi]] = max([hasil[self.fuzzyrule[kombinasi]],min(t).values()[0]])[0]
            self.iResult.append(hasil)
    def defuzifikasi(self):
        self.endresult = []
        for data in self.iResult:
            result = 0
            jml = 0
            for i in range(4):
                result += data[i]*i
                jml += data[i]
            result = round(result/jml)
            self.endresult.append(int(result))
    def koreksi(self):
        self.akurasi = 0.0
        for a in xrange(len(self.endresult)):
            if self.endresult[a] == self.data[a][3]: self.akurasi += 1
        self.akurasi = self.akurasi/len(self.data)

aasd = [0, 2, 3, 0, 2, 3, 0, 2, 3, 0, 2, 3, 0, 2, 3, 1, 2, 3, 0, 2, 3, 0, 2, 3, 0, 2, 3]
fuzz = fuzzy(data_training,aasd)
print fuzz.akurasi