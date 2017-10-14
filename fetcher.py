#!/usr/bin/env python
from bs4 import BeautifulSoup
from urllib.request import urlopen
from lxml.html import parse
import sys,os,time,glob,subprocess,re,datetime,hues
import pandas as pd
import csv

ids_real, ids_temp, ids_new = [],[],[]
urls_real, urls_temp, urls_new = [],[],[]
url = 'https://www.sahibinden.com/satilik-daire?viewType=List&pagingSize=50&sorting=date_desc'

Title = None
ID = None
Price = None
Currency = None
LocationCity = None
LocationCounty = None
LocationDistrict = None
LocationLatitude = None
LocationLongitude = None
Date = None
Type = None
m2 = None
RoomCount = None
BuildingAge = None
Floor = None
TotalFloor = None
Heating = None
Bathrooms = None
Furnished = None
Status = None
Residential = None # Site icerisinde 
Dues = None # Aidat
AvailableforLoan = None # Kredi
SalerType = None
Exchange = None

def clearHTML():
	files = glob.glob(os.path.dirname(os.path.realpath(__file__)) + '/html/*.html')
	for file in files:
		os.remove(file)

	files = glob.glob(os.path.dirname(os.path.realpath(__file__)) + '/html/single/*.html')
	for file in files:
		os.remove(file)

def fetchSinglePage(url):
	now = datetime.datetime.now()
	filename = 'single-' + str(now.hour) + str(now.minute) + str(now.second) + str(now.microsecond) + '.html'
	filepath = os.path.dirname(os.path.realpath(__file__)) + '/html/single/' + filename
	command = 'wget -O ' + filepath + ' \"' + url + '\"'
	subprocess.Popen(command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()
	if os.stat(filepath).st_size == 0:
		hues.error(filename + ' IS NOT DOWNLOADED')
	else:
		pass
		#hues.success(filename + ' DOWNLOADED')
	return

def fetchArchivePage(url):
	now = datetime.datetime.now()
	filename = 'archive-' + str(now.hour) + str(now.minute) + str(now.second) + str(now.microsecond) + '.html'
	filepath = os.path.dirname(os.path.realpath(__file__)) + '/html/' + filename
	#page = urlopen(url).read()
	#soup = BeautifulSoup(page, 'lxml')
	#print(soup)
	command = 'wget -O ' + filepath + ' \"' + url + '\"'
	subprocess.Popen(command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()
	if os.stat(filepath).st_size == 0:
		hues.error(filename + ' IS NOT DOWNLOADED')
	else:
		pass
		#hues.success(filename + ' DOWNLOADED')
	return

def searchSingle(filepath):
	global Title
	global ID
	global Price
	global LocationCity
	global LocationCounty
	global LocationDistrict
	global LocationLatitude
	global LocationLongitude
	global Date
	global Type
	global m2
	global RoomCount
	global BuildingAge
	global Floor
	global TotalFloor
	global Heating
	global Bathrooms
	global Furnished
	global Status
	global Residential
	global Dues
	global AvailableforLoan
	global SalerType
	global Exchange

	#files = glob.glob('html/single/*.html')
	#soup = BeautifulSoup(open(files[0],encoding="utf-8"), 'lxml')
	soup = BeautifulSoup(open(filepath,encoding="utf-8"), 'lxml')

	#soup = BeautifulSoup(urlopen(url), 'lxml')
	# Title Div
	rows = soup.findAll("div", { "class" : "classifiedDetailTitle" })
	rows_string = str(rows).split('\n')

	# Data Table
	rows2 = soup.findAll("div", { "class" : "classifiedInfo" })
	rows_string2 = str(rows2).split('\n')

	# Location
	rows3 = soup.find("div", { "id" : "gmap" })
	if rows3:
		LocationLatitude, LocationLongitude = rows3.attrs['data-lat'], rows3.attrs['data-lon']
	else:
		LocationLatitude = 'Unknown'
		LocationLongitude = 'Unknown'

	#Title = soup.title.string
	Title = rows_string[1]
	Price = rows_string2[2]
	LocationCity = rows_string2[6]
	LocationCounty = rows_string2[9]
	LocationDistrict = rows_string2[12]
	ID = rows_string2[16]
	Date = rows_string2[22]
	Type = rows_string2[26]
	m2 = rows_string2[31]
	RoomCount = rows_string2[36]
	BuildingAge = rows_string2[41]
	Floor = rows_string2[46]
	TotalFloor = rows_string2[51]
	Heating = rows_string2[56]
	Bathrooms = rows_string2[61]
	Furnished = rows_string2[66]
	Status = rows_string2[71]
	Residential = rows_string2[76]
	Dues = rows_string2[81]
	AvailableforLoan = rows_string2[86]
	SalerType = rows_string2[91]
	Exchange = rows_string2[96]

	#hues.info(filepath + ' DELETED')
	#os.remove(filepath)

def searchArchive():
	global ids_temp
	global urls_temp

	hues.info('SCANNING ARCHIVE')

	files = glob.glob(os.path.dirname(os.path.realpath(__file__)) + '/html/*.html')
	soup = BeautifulSoup(open(files[0],encoding="utf-8"), 'lxml')
	rows = soup.findAll("tr", attrs={"class":"searchResultsItem"})

	for row in rows:
		rows_string = str(row).split('\n')

		# Find the ID of the Ad
		id = re.findall('data-id=\"(.*?)\">', rows_string[0], re.DOTALL) 
		ids_cleaned = str(id).replace('[\'', '')
		ids_cleaned = ids_cleaned.replace('\']', '')
		ids_temp.append(int(ids_cleaned))

		# Find & Clear the URL
		url = re.findall('/ilan/(.*?)/detay', rows_string[2], re.DOTALL)
		url_string = str(url[0]).replace('[', '')
		url_string = str(url[0]).replace(']', '')
		#urls = 'https://www.sahibinden.com/ilan/' + url_string + '/detay'
		urls_temp.append('https://www.sahibinden.com/ilan/' + url_string + '/detay')

def clearData():
	global Title
	global ID
	global Price
	global Currency
	global LocationCity
	global LocationCounty
	global LocationDistrict
	global LocationLatitude
	global LocationLongitude
	global Date
	global Type
	global m2
	global RoomCount
	global BuildingAge
	global Floor
	global TotalFloor
	global Heating
	global Bathrooms
	global Furnished
	global Status
	global Residential
	global Dues
	global AvailableforLoan
	global SalerType
	global Exchange

	Title = Title.replace(',',' ')
	Title = Title.replace('<h1>', '')
	Title = Title.replace('</h1>', '')
	if '&amp;' in Title:
		Title = Title.replace('&amp;', '&')
	if '\"' in Title:
		Title = Title.replace('\"', ' ')

	ID = ID.replace('<span class="classifiedId" id="classifiedId">', '')
	ID = ID.strip('</span>')
	ID = int(ID.lstrip())

	Price = Price.replace('<a class="emlak-endeksi-link trackClick trackId_emlak-endeksi-link" href="javascript:;" id="emlakEndeksiLink" style="cursor:pointer">Emlak Endeksi</a>', '')
	Price = Price.lstrip()

	if 'TL' in Price:
		Currency = 'Turkish Lira'
	elif '$' in Price:
		Currency = 'US Dollar'
	elif '€' in Price:
		Currency = 'Euro'
	elif '₤' in Price:
		Currency = 'British Pound'

	Price = list(filter(str.isdigit, Price))
	Price = ''.join(Price)

	LocationCity = LocationCity.replace('</a>', '')
	LocationCity = LocationCity.lstrip()

	LocationCounty = LocationCounty.replace('</a>', '')
	LocationCounty = LocationCounty.lstrip()

	LocationDistrict = LocationDistrict.replace('</a>', '')
	LocationDistrict = LocationDistrict.lstrip()

	Date = Date.replace('</span>', '')
	Date = Date.lstrip()
	date_dump = str(Date).split(' ')
	if 'Ocak' in date_dump[1]:
		date_month = '01'
	elif 'Şubat' in date_dump[1]:
		date_month = '02'
	elif 'Mart' in date_dump[1]:
		date_month = '03'
	elif 'Nisan' in date_dump[1]:
		date_month = '04'
	elif 'Mayis' in date_dump[1]:
		date_month = '05'
	elif 'Haziran' in date_dump[1]:
		date_month = '06'
	elif 'Temmuz' in date_dump[1]:
		date_month = '07'
	elif 'Ağustos' in date_dump[1]:
		date_month = '08'
	elif 'Eylül' in date_dump[1]:
		date_month = '09'
	elif 'Ekim' in date_dump[1]:
		date_month = '10'
	elif 'Kasim' in date_dump[1]:
		date_month = '11'
	elif 'Aralik' in date_dump[1]:
		date_month = '12'
	Date = date_dump[2] + '-' + date_month + '-' + date_dump[0]

	Type = Type.replace('<span>', '')
	Type = Type.replace('</span>', '')
	Type = Type.lstrip()
	if 'Daire' in Type:
		Type = 'Flat'
	elif 'Villa' in Type:
		Type = 'Villa'
	elif 'Residence' in Type:
		Type = 'Residence'
	elif 'Müstakil Ev' in Type:
		Type = 'Detached House'
	elif 'Çiftlik Evi' in Type:
		Type = 'Farm House'
	elif 'Köşk & Konak' in Type:
		Type = 'Mansion'
	elif 'Yalı' in Type:
		Type = 'Waterside'
	elif 'Yalı Dairesi' in Type:
		Type = 'Waterside Apartment'
	elif 'Yazlık' in Type:
		Type = 'Summerhouse'
	elif 'Prefabrik Ev' in Type:
		Type = 'Prefabric Home'
	elif 'Kooperatif' in Type:
		Type = 'Cooperative'

	m2 = m2.replace('</span>', '')
	if 'Belirtilmemiş' in m2:
		m2 = 'Unknown'
	else:
		m2 = m2.lstrip()
		m2 = list(filter(str.isdigit, m2))
		m2 = int(''.join(m2))

	RoomCount = RoomCount.replace('</span>', '')
	if 'Stüdyo (1+0)' in RoomCount:
		RoomCount = '1+0 (Studio)'
	elif '10 Üzeri' in RoomCount:
		RoomCount = '10+'
	elif 'Belirtilmemiş' in RoomCount:
		RoomCount = 'Unknown'
	else:
		RoomCount = RoomCount.lstrip()

	BuildingAge = BuildingAge.strip('</span>')
	if '5-10 arası' in BuildingAge:
		BuildingAge = '5-10'
	elif '11-15 arası' in BuildingAge:
		BuildingAge = '11-15'
	elif '16-20 arası' in BuildingAge:
		BuildingAge = '16-20'
	elif '21-25 arası' in BuildingAge:
		BuildingAge = '21-25'
	elif '26-30 arası' in BuildingAge:
		BuildingAge = '26-30'
	elif '31 ve üzeri' in BuildingAge:
		BuildingAge = '31+'
	else:
		BuildingAge = int(BuildingAge.lstrip())

	if 'Villa Tipi' in Floor:
		Floor = 'Villa Type'
	elif 'Kot 4' in Floor:
		Floor = 'Rise 4'
	elif 'Kot 3' in Floor:
		Floor = 'Rise 3'
	elif 'Kot 2' in Floor:
		Floor = 'Rise 2'
	elif 'Kot 1' in Floor:
		Floor = 'Rise 1'
	elif 'Bodrum Kat' in Floor:
		Floor = 'Basement'
	elif 'Zemin Kat' in Floor:
		Floor = 'Ground Floor'
	elif 'Bahçe Katı' in Floor:
		Floor = 'Garden Floor'
	elif 'Giriş Katı' in Floor:
		Floor = 'Ground Floor'
	elif 'Yüksek Giriş' in Floor:
		Floor = 'High Entrance'
	elif 'Müstakil' in Floor:
		Floor = 'Seperate'
	elif 'Çatı Katı' in Floor:
		Floor = 'Penthouse'
	elif '30 ve üzeri' in Floor:
		Floor = '30+'
	else:
		Floor = Floor.strip('</span>')
		Floor = int(Floor.lstrip())

	TotalFloor = TotalFloor.replace('</span>', '')
	if '30 ve üzeri' in TotalFloor:
		TotalFloor = '30+'
	else:
		TotalFloor = int(TotalFloor.lstrip())

	if 'Yerden Isıtma' in Heating:
		Heating = 'Floor'
	elif 'Merkezi' in Heating:
		Heating = 'Central'
	elif 'Doğalgaz (Kombi)' in Heating:
		Heating = 'Combi'
	elif 'Yok' in Heating:
		Heating = 'None'
	elif 'Soba' in Heating:
		Heating = 'Stove'
	elif 'Doğalgaz Sobası' in Heating:
		Heating = 'Natural Gas Stove'
	elif 'Kat Kaloriferi' in Heating:
		Heating = 'Floor Calorie'
	elif 'Merkezi (Pay Ölçer)' in Heating:
		Heating = 'Center (Pay Meter)'
	elif 'Klima' in Heating:
		Heating = 'Air Conditioning'
	elif 'Fancoil Ünitesi' in Heating:
		Heating = 'Fancoil Unit'
	elif 'Güneş Enerjisi' in Heating:
		Heating = 'Solar Energy'
	elif 'Jeotermal' in Heating:
		Heating = 'Geothermal'
	elif 'Şömine' in Heating:
		Heating = 'Fireplace'
	elif 'VRV' in Heating:
		Heating = 'VRV'
	elif 'Isı Pompası' in Heating:
		Heating = 'Heat Pump'

	Bathrooms = Bathrooms.replace('</span>', '')
	if 'Yok' in Bathrooms:
		Bathrooms = 'None'
	elif '6 Üzeri' in Bathrooms:
		Bathrooms = '6+'
	else:
		Bathrooms = int(Bathrooms.lstrip())

	if 'Hayır' in Furnished:
		Furnished = False
	elif 'Evet' in Furnished:
		Furnished = True
	elif 'Belirtilmemiş' in Furnished:
		Furnished = 'Unknown'

	if 'Boş' in Status:
		Status = 'Empty'
	elif 'Kiracılı' in Status:
		Status = 'Tenant'
	elif 'Mülk Sahibi' in Status:
		Status = 'Owner'
	elif 'Belirtilmemiş' in Status:
		Status = 'Unknown'

	if 'Hayır' in Residential:
		Residential = False
	elif 'Evet' in Residential:
		Residential = True
	elif 'Belirtilmemiş' in Residential:
		Residential = 'Unknown'

	if 'Belirtilmemiş' in Dues:
		Dues = 'Unknown'
	else:
		Dues = Dues.strip('</span>')
		Dues = list(filter(str.isdigit, Dues))
		Dues = int(''.join(Dues))
		#Dues = int(Dues.lstrip())

	if 'Hayır' in AvailableforLoan:
		AvailableforLoan = False
	elif 'Evet' in AvailableforLoan:
		AvailableforLoan = True
	elif 'Belirtilmemiş' in AvailableforLoan:
		AvailableforLoan = 'Unknown'

	if 'Sahibinden' in SalerType:
		SalerType = 'Owner'
	elif 'İnşaat Firması' in SalerType:
		SalerType = 'Construction Company'
	elif 'Bankadan' in SalerType:
		SalerType = 'Bank'	
	elif 'Emlak Ofisinden' in SalerType:
		SalerType = 'Real Estate Office'

	if 'Hayır' in Exchange:
		Exchange = False
	elif 'Evet' in Exchange:
		Exchange = True

def showData():
	print('Title: ' + Title)
	print('ID: ' + str(ID))
	print('Price: ' + str(Price))
	print('Currency: ' + str(Currency))
	print('City: ' + LocationCity)
	print('County: ' + LocationCounty)
	print('District: ' + LocationDistrict)
	print('Latitude: ' + str(LocationLatitude))
	print('Longitude: ' + str(LocationLongitude))
	print('Date: ' + Date)
	print('Type: ' + Type)
	print('m2: ' + str(m2))
	print('Rooms: ' + RoomCount)
	print('Building Age: ' + str(BuildingAge))
	print('Floor: ' + str(Floor))
	print('Total Floor: ' + str(TotalFloor))
	print('Heating: ' + Heating)
	print('Bathrooms: ' + str(Bathrooms))
	print('Furnished: ' + str(Furnished))
	print('Status: ' + str(Status))
	print('Residential: ' + str(Residential))
	print('Dues: ' + str(Dues))
	print('Available for Loan: ' + str(AvailableforLoan))
	print('Saler: '+ SalerType)
	print('Exchange: ' + str(Exchange))

def loadCSV():
	global ids_real
	global urls_real

	# Load real data from id_url
	data_real = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/inc/id_url.csv', names=['id','url'])
	for x in data_real.id:
		ids_real.append(x)
	for x in data_real.url:
		urls_real.append(x)

	#hues.info('REAL DATA LOADED')

def compareCSV():
	global ids_new
	global urls_new
	global ids_temp
	global urls_temp
	global ids_real
	global urls_real

	# Compare _temp and _real
	ids_new = [x for x in ids_temp if x not in ids_real]
	urls_new = [x for x in urls_temp if x not in urls_real]
	if ids_new:
		hues.info('NEW ID COUNT: ' + str(len(ids_new)))
	elif not ids_new:
		hues.warn('NO NEW ID')

def writeToCSV():
	global Title
	global ID
	global Price
	global Currency
	global LocationCity
	global LocationCounty
	global LocationDistrict
	global LocationLatitude
	global LocationLongitude
	global Date
	global Type
	global m2
	global RoomCount
	global BuildingAge
	global Floor
	global TotalFloor
	global Heating
	global Bathrooms
	global Furnished
	global Status
	global Residential
	global Dues
	global AvailableforLoan
	global SalerType
	global Exchange

	Title_temp = Title.replace(',', '')
	WriteMe = Title + ',' + str(ID) + ',' + str(Price) + ',' + str(Currency) + ',' + LocationCity + ',' + LocationCounty + ',' + LocationDistrict + ',' + str(LocationLatitude) + ',' + str(LocationLongitude) + ',' + Date + ',' + Type + ',' + str(m2) + ',' + str(RoomCount) + ',' + str(BuildingAge) + ',' + str(Floor) + ',' + str(TotalFloor) + ',' + Heating + ',' + str(Bathrooms) + ',' + str(Furnished) + ',' + str(Status) + ',' + str(Residential) + ',' + str(Dues) + ',' + str(AvailableforLoan) + ',' + SalerType + ',' + str(Exchange)
	File = open(os.path.dirname(os.path.realpath(__file__)) + '/inc/real_estate_data.csv','a', encoding="utf-8") # 'a' parameter for append, 'w' for overwrite
	File.write(WriteMe + '\n')
	File.close()

	hues.success('REAL ESTATE DATA HAS BEEN WRITTEN to inc/real_estate_data.csv')

def writeNew():
	global ids_new
	global urls_new

	if ids_new:
		f = open(os.path.dirname(os.path.realpath(__file__)) + '/inc/id_url.csv', 'a')
		for i in range(0,len(ids_new)):
 	  		f.write("{},{}\n".format(ids_new[i], urls_new[i]))
		f.close()
		hues.success('ID URL DATA HAS BEEN WRITTEN to inc/id_url.csv')

def returnNotMatches(a, b):
	#return [[x for x in a if x not in b], [x for x in b if x not in a]]
	return [x for x in a if x not in b]

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ''()

def real_estate_data():
	files = glob.glob(os.path.dirname(os.path.realpath(__file__)) + '/html/single/*.html')
	for file in files:
		if os.stat(file).st_size == 0:
			#print(file + ' IS NOT DOWNLOADED')
			pass
		else:
			searchSingle(file)
			clearData()
			showData()
			writeToCSV()

def clearSYSTEM():
	global ids_new
	global ids_temp
	global ids_real
	global urls_new
	global urls_temp
	global urls_real

	clearHTML()
	ids_new.clear()
	ids_temp.clear()
	ids_real.clear()
	urls_new.clear()
	urls_temp.clear()
	urls_real.clear()
	#hues.info('SYSTEM CLEANED')

def automator(url):
	# 0 - Clear html files
	clearHTML()

	# 1 - Load CSV to _real
	loadCSV()

	# 2 - Download archive.html
	fetchArchivePage(url)

	# 3 - Load IDs & URLs to _temp
	searchArchive()

	# 4 - Compare _temp & _real, write new ones to _new
	compareCSV()

	# 5 - Fetch new single pages
	#hues.info('AD PAGES DOWNLOADING')
	for urls in urls_new:
		fetchSinglePage(urls)
		#print('New Ad ID: ' + str(row_temp))
		#print('URL: ' + urls_temp[x])
	
	# 5.1 - IDs & URLs to real_estate_data.csv
	real_estate_data()

	# 5.2 - Write _new to id_url.csv
	writeNew()

	# 6 - Delete archive.html & single.html, Clear _new and _temp
	clearSYSTEM()

if __name__ == '__main__':
	while True:
		#automator(url)
		for x in range(1,951):
			if float(x % 50) == 0:
				hues.info('PAGE: ' + str(int(x / 50)))
				automator('https://www.sahibinden.com/satilik-daire?viewType=List&pagingOffset=' + str(x) + '&pagingSize=50&sorting=date_desc')
		hues.info('SLEEPING')
		time.sleep(900) # 15 min
