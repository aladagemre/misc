# -*- coding: iso-8859-9 -*-
import urllib
from BeautifulSoup import BeautifulSoup
import re

class Hat:
	def __init__(self, hatkodu):
		'''URL belirler, saat tablosunu indirir, bunu parcalar, gerekli saatleri liste'nin icine aktarir.'''
		url = "http://www.iett.gov.tr/saat/orer.php?hatcode=%s&hid=hat&BtnSaatler" % self.trKodla(hatkodu) #URL'yi hazirlar.
		html = urllib.urlopen(url).read() #HTML kodlarini bulur.
		
		#-------KALKIS MERKEZLERININ BULUNMASI-----------------------
		#--"<td colspan=1><center>ŞAHİNBEY <br>Kalkış</center></td>"--
		
		#ILK MERKEZ
		baslangic = html.find("<td colspan=1><center>") + len("<td colspan=1><center>") #Kalkis metninin basi
		bitis = html.find("<br>Kalkış</center></td>") #Kalkis metninin sonu
		
		self.kalkisA=html[baslangic:bitis] #temiz metni bulduk.
		
		baslangic2 = html.find("<td colspan=1><center>",bitis) + len("<td colspan=1><center>") #Ikinci Kalkis metninin basi
		bitis2 = html.find("<br>Kalkış</center></td>", bitis+1) #ikinci kalkis metninin sonu
		
		self.kalkisB=html[baslangic2:bitis2] #temiz metni bulduk
				
		
		corba = BeautifulSoup(html) #saatleri bulmak icin corbaya kasik daldiriyoruz.
		self.liste = [[],[],[],[],[],[]] #bos saat listeleri olusturuyoruz: haftaiciA, haftaiciB, cmtA,cmtB,pazA,pazB...
		
		i=0 #listeler arasinda donebilmek icin. Bir ona bir ona saat yazabilmek icin. (ayni satirda 6 veri var)
		for fontEtiketi in corba.findAll('font'): #Tï¿½m font etiketi iceren etiketleri bul
			temizSaat = self.saatCek(fontEtiketi) #Saf saat cikar.
			#if temizSaat!='': #Eger dolu gelmisse, saat gecerli demektir.
			self.liste[i].append(temizSaat) #Bu saati i. listeye ekle.
			i+=1 #i'yi arttir ki bir diger listeye yazalim.
			if i==6: #Eger i=6 olursa(pazarB), bir alt satira geciyoruz demektir.
				i = 0 #en basa donduk (haftaiciA)


   	def satirSayisi(self):
        	return max(len(self.liste[0]), len(self.liste[1]), len(self.liste[2]), len(self.liste[3]), len(self.liste[4]), len(self.liste[5]))
        
    	def tumListe(self):
        	return self.liste
        
	def haftaiciA(self):
	        '''Haftaicinde birinci kalkis merkezinden kalkan otobus listesi'''		
        	return self.liste[0]
    	def haftaiciB(self):
		'''Haftaicinde ikinci kalkis merkezinden kalkan otobus listesi'''		
		return self.liste[1]
    	def cumartesiA(self):
        	'''Cumartesi gunu birinci kalkis merkezinden kalkan otobus listesi'''		
        	return self.liste[2]
    	def cumartesiB(self):
	        '''Cumartesi ikinci kalkis merkezinden kalkan otobus listesi'''		
	        return self.liste[3]
    	def pazarA(self):
	        '''Pazar gunu birinci kalkis merkezinden kalkan otobus listesi'''	
	        return self.liste[4]
    	def pazarB(self):
        	'''Pazar ikinci kalkis merkezinden kalkan otobus listesi'''	
        	return self.liste[5]
	    
    	def merkezA(self):
	        '''Birinci kalkis merkezinin ismini verir.'''
	        return unicode(self.kalkisA, encoding="iso-8859-9")
    	def merkezB(self):
	        '''Ikinci kalkis merkezinin ismini verir.'''
	        return unicode(self.kalkisB, encoding="iso-8859-9")
	            
	
	def trKodla(self, hatkodu):
		''' Verilen bir hat kodunu URL'ye uygun sekilde kodlar'''
		print hatkodu
		sonuc = ""
		for harf in hatkodu:
			if harf == 'Ü':
				sonuc += "3%DC"
			elif harf == 'Ç':
				sonuc += "%C7"
			elif harf == 'Ş':
				sonuc += "%DE"
			elif harf == 'İ':
				sonuc += "%DD"
			else:
				sonuc += harf
		return sonuc

	def saatCek(self, fontEtiketi):
		'''Verilen <font color="...">12:20</font> seklindeki etiketin icindeki saati cikarir'''
		fontEtiketi = str(fontEtiketi)
		baslangic = fontEtiketi.find(">") + 1
		bitis = fontEtiketi.find("</font>")
		sonuc = fontEtiketi[baslangic:bitis]
		if re.match("(20|21|22|23|[01]\d|\d)(([:][0-5]\d){1,2})", sonuc):
			return sonuc
		else:
			return ''
		

#a = Hat("122M")
#print a.merkezA()