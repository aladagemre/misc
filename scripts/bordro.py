#encoding: utf-8
import math

ay = 1

BM = {}
EK = {}
AGI = {}

SM = {}
SK = {}
SKI = {}
IS = {}
ISI = {}
KVSP = {}
HY = {}
KES = {}
BES = {}

VM = {}
KVM = {0: 0.0}
GV = {0: 0.0}
VO = {}
DV = {}
NET = {}
MALIYET = {}

def hesapla(i, brut=None):
    # SGK Tavan Ocak - Haziran
    SGKT1 = 10705.50
    # SGK Tavan Temmuz - Aralık
    SGKT2 = 10705.50

    # Vergi dilimi %15 <
    VD15 = 12600.00
    # Vergi dilimi %20 <
    VD20 = 30000.00
    # Vergi dilimi %27 <
    VD27 = 110000.00

    # Brüt Maaş
    if brut:
        BM[i] = brut
    else:
        BM[i] = 1647.00
    # İkramiye, prim, fazla mesai
    EK[i] = 0.00
    # Asgari geçim indirimi
    AGI[i] = 123.53

    # SGK Matrahı
    if i < 7:
        SGKT = SGKT1
    else:
        SGKT = SGKT2

    SM[i] = min(BM[i] + EK[i], SGKT)

    # SGK Kesintisi (sigorta primi işçi payı)
    SK[i] = SM[i] * 0.14

    # SGK Kesintisi (işveren payı)
    SKI[i] = SM[i] * 0.185

    # İşsizlik Sigortası (işçi payı)
    IS[i] = SM[i] * 0.01

    # İşsizlik Sigortası (işveren payı)
    ISI[i] = SM[i] * 0.02

    # Kısa Vadeli Sigorta Primi (sadece işveren)
    KVSP[i] = SM[i] * 0.02

    # Hazine Yardımı (sadece işverenden düşüyor)
    HY[i] = SM[i] * 0.05

    # Bireysel Emeklilik Sigortası Kesintisi
    BES[i] = BM[i] * 0.02

    # Diğer kesintiler
    KES[i] = 0.0

    # Vergi Matrahı
    VM[i] = BM[i] + EK[i] - SK[i] - IS[i]

    # Kümüle Vergi Matrahı
    KVM[i] = KVM[i-1] + VM[i]

    # Gelir Vergisi
    # TODO %35 dilim
    GV1 = max((KVM[i]-VD27)*0.08, 0) + max((KVM[i]-VD20)*0.07, 0) + max((KVM[i]-VD15)*0.05, 0) + KVM[i]*0.15
    GV0 = max((KVM[i-1]-VD27)*0.08, 0) + max((KVM[i-1]-VD20)*0.07, 0) + max((KVM[i-1]-VD15)*0.05, 0) + KVM[i-1]*0.15
    GV[i] = (GV1 - GV0)

    # Ortalama gelir vergisi oranı
    VO[i] = GV[i] / VM[i]

    # Damga vergisi
    DV[i] = (BM[i] + EK[i]) * 0.00759

    kesintiler = SK[i] + IS[i] + GV[i] + DV[i] # + BES + KES
    #print "Kesintiler=", kesintiler
    NET[i] = BM[i] + EK[i] + AGI[i] - kesintiler

    MALIYET[i] = SM[i] + SKI[i] + KVSP[i] + ISI[i] - HY[i]
    print "NET=", NET[i]
    print "İşveren Maliyet=", MALIYET[i]


BRUT_MAAS = 10000
for ay in xrange(1, 13):
    hesapla(ay, BRUT_MAAS)

print "Gelir Vergisi:"
print GV
