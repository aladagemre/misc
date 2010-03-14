#!/usr/bin/python
# -*- coding: utf-8 -*-

import getpass
import shutil
import os
import sys

#-----/etc/ppp/pppoe.conf-------
print '''#####################################################################
#
#   Linux için Yurt.NET Yapılandırma sihirbazına hoşgeldiniz...
#   Işık Üniversitesi Linux Topluluğu
#   http://isix.isikun.edu.tr
#
#####################################################################


'''
if os.getenv('USER') != 'root':
    sys.exit('Bu aracı lütfen sudo ./yurtnet şeklinde çalıştırın.')
print "pppoe.conf yapılandırması başlıyor."
print "Lütfen Ağ Yöneticisinde yeni bir Ethernet bağlantısı oluşturduğunuzdan ve onu etkinleştirdiğinizden emin olun."
emin_midir_acep = raw_input("Emin misiniz? (e/h)")
if not ('e' in emin_midir_acep or 'E' in emin_midir_acep):
    sys.exit('Lütfen emin olduktan sonra tekrar deneyin.')
    
shutil.copyfile('/etc/resolv.conf', '/etc/resolv.conf-bak')

kullanici = raw_input("Kullanıcı adınız (öğrenci numaranız):")
parola = getpass.getpass("Parolanızı girin:")
icerik = '''ETH='eth0'
USER='%(kullanici)s'
DEMAND=no
DNSTYPE=SERVER
PEERDNS=yes
DNS1=
DNS2=
DEFAULTROUTE=yes
CONNECT_TIMEOUT=30
CONNECT_POLL=2
ACNAME=
SERVICENAME=
PING="."
CF_BASE=`basename $CONFIG`
PIDFILE="/var/run/$CF_BASE-pppoe.pid"
SYNCHRONOUS=no
CLAMPMSS=1412
LCP_INTERVAL=20
LCP_FAILURE=3
PPPOE_TIMEOUT=80
FIREWALL=STANDALONE
LINUX_PLUGIN=
PPPOE_EXTRA=""
PPPD_EXTRA=""
''' % { 'kullanici': kullanici }

shutil.copyfile("/etc/ppp/pppoe.conf", "/etc/ppp/pppoe.conf-bak")
f = open("/etc/ppp/pppoe.conf", "w")
f.write(icerik)
f.close()

print "pppoe.conf dosyası yapılandırıldı."
#---------------------------------



#-----/etc/ppp/pap-secrets--------
print "pap-secrets yapılandırılıyor: /etc/ppp/pap-secrets"
shutil.copyfile("/etc/ppp/pap-secrets", "/etc/ppp/pap-secrets-bak")
f = open("/etc/ppp/pap-secrets","w")
f.write('''
# Secrets for authentication using PAP
# client        server  secret                  IP addresses
"%(kullanici)s"    *       "%(parola)s"
''' % { 'kullanici': kullanici, 'parola'   : parola})
f.close()

#---------------------------------



#----/etc/ppp/chap-secrets--------
print "chap-secrets yapılandırılıyor: /etc/ppp/chap-secrets"
shutil.copyfile("/etc/ppp/chap-secrets", "/etc/ppp/chap-secrets-bak")
f = open("/etc/ppp/chap-secrets","w")
f.write('''
# Secrets for authentication using CHAP
# client        server  secret                  IP addresses
"%(kullanici)s"    *       "%(parola)s"
''' % { 'kullanici': kullanici, 'parola'   : parola})
f.close()

#---------------------------------

#----AUTOSTART-----------------------
print "Açılışta bağlantı kurulması için gereken ayar yapılıyor: /etc/conf.d/local.start"
ek1="br2684ctl -c 0 -b -a 8.35\n"
ek2="adsl-start\n"
f = open("/etc/conf.d/local.start", "r+")
eski_icerik = f.read()
if not ek1 in eski_icerik:
    f.write(ek1)
if not ek2 in eski_icerik:
    f.write(ek2)
f.close()

#-------------------------------------
#-----Starting--------------------------
print "İnternet bağlantısı başlatılıyor: pppoe-start"
os.system("pppoe-start")

#----------------------------------------
print "Bitti..."
print "Şu ana kadar bir hatayla karşılaşmadıysanız (TIMED OUT vs.) geçmiş olsun :)"
print "Eğer bir sorununuz varsa http://isix.isikun.edu.tr adresine girerek bize danışabilirsiniz."
print "Not: Üzerinde değişiklik yapılan dosyaların yedeği aynı dizinde dosyaadi-bak ismiyle saklanmıştır."