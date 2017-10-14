#!/usr/bin/env python
import pandas as pd
import os, shutil

id_1, id_2 = [],[]

def removeVal():
	global id_1
	global id_2

	id_1.clear()
	id_2.clear()

def clearDuplicates(file):
	# Create Backup
	filepath = os.path.dirname(os.path.realpath(__file__)) + '/inc/' + file
	shutil.copy(filepath, filepath + '_backup')

	# Remove Duplicates
	df = pd.read_csv(filepath, encoding = 'utf-8')
	df.drop_duplicates(subset=None, inplace=True)
	print('DUPLICATED IDs DELETED')

	# Remove original file and backup
	os.remove(filepath + '_backup')
	os.remove(filepath)
	df.to_csv(filepath, index=False, encoding = 'utf-8')

def compareCSV(file1, file2):
	global id_1
	global id_2

	df_1 = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/inc/' + file1, names=['id','url'])
	for x in df_1.id:
		id_1.append(int(x))

	df_2 = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/inc/' + file2, names=['title','id','price','currency','city','county','district ','lat','lon','date','type','m2','room','age','floor','total_floor','heating','bathroom','furnished','status','residental','dues','loan','saler','exchange'])
	for x in df_2.id:
		id_2.append(int(x))

	for x in id_1:
		if not x in id_2:
			print(str(x) + ' DELETED')
			print(id_1.index(x))
			df_1 = df_1.drop(id_1.index(x))

	os.remove(os.path.dirname(os.path.realpath(__file__)) + '/inc/' + file1)
	df_1.to_csv(os.path.dirname(os.path.realpath(__file__)) + '/inc/' + file1, index=False, header=False, encoding='utf-8')

def compareCSV2(file1, file2):
	global id_1
	global id_2

	df_1 = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/inc/' + file1, names=['title','id','price','currency','city','county','district ','lat','lon','date','type','m2','room','age','floor','total_floor','heating','bathroom','furnished','status','residental','dues','loan','saler','exchange'])
	for x in df_1.id:
		id_1.append(int(x))

	df_2 = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/inc/' + file2, names=['id','url'])
	for x in df_2.id:
		id_2.append(int(x))

	for x in id_1:
		if not x in id_2:
			print(str(x) + ' DELETED')
			df_1 = df_1.drop(id_1.index(x))
	
	os.remove(os.path.dirname(os.path.realpath(__file__)) + '/inc/' + file1)
	df_1.to_csv(os.path.dirname(os.path.realpath(__file__)) + '/inc/' + file1, index=False, header=False, encoding='utf-8')


if __name__ == '__main__':
	clearDuplicates('real_estate_data.csv')
	clearDuplicates('id_url.csv')
	compareCSV('id_url.csv','real_estate_data.csv')
	removeVal()
	compareCSV2('real_estate_data.csv','id_url.csv')

