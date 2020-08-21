from Levenshtein import *
import time
import json
from os import listdir
from pylcs import *
import codecs

def read(path):
	with open(path, 'r',encoding="utf8") as file:
		content = file.read()
		ret = content.split('\n')
		return ret

religion = read('target_data/tongiao.txt')
folk = read('target_data/dantoc.txt')
province = read('target_data/tinh.txt')
data = json.load(open("target_data/local.json","r"))

def religion_correction(religion_str):
	maxx = 0
	ret = None
	tmp = None
	for i in range(8):
		tmp = ratio(religion[i], religion_str)
		if tmp > maxx:
			maxx = tmp
			ret = i
	return religion[ret] if ret != None else None

def folk_correction(folk_str):
	maxx = 0
	ret = None
	tmp = None
	for i in range(54):
		tmp = ratio(folk[i], folk_str)
		if tmp > maxx:
			print(tmp)
			maxx = tmp
			ret = i
			print(ret)
	return folk[ret] if ret != None else None

def province_correction(province_str):
	print('Input: {}'.format(province_str))
	maxx = 0
	ret = None
	tmp = None
	for i in range(64):
		tmp = ratio(province[i], province_str)
		if tmp > maxx:
			maxx = tmp
			ret = i
	return province[ret] if ret != None else None

def get_all_addresses(data):
		all_addresses = []
		for province in data:
				raw_province_name = province['name']
				raw_province_id = province['id']

				for district in province['districts']:
						raw_district_name = district['name']
						raw_district_id = district['id']

						for ward in district['wards']:
								raw_ward_name = ward['name']
								raw_ward_id = ward['id']

								address = [ 
									(raw_province_name, raw_province_id),
									(raw_district_name, raw_district_id),
									(raw_ward_name, raw_ward_id)
								]
								all_addresses.append(address)

		return all_addresses

def gen_pattern_addresses(address):

		pattern_addresses = []

		pattern_cities = address[0][0]
		pattern_districts = address[1][0]
		pattern_wards = address[2][0]

		result = [(pattern_wards + ',' + pattern_districts + ',' \
			+ pattern_cities).upper()]
		return result

all_addresses = get_all_addresses(data)
noise_string = {'TT', 'TP', 'TX', 'XÃ', 'PHƯỜNG', 'HUYỆN', 'QUẬN', 'TỈNH', 
				'THÀNH PHỐ', 'Q.', 'T.', 'X.', 'P.', 'CỤM', 'THỊ XÃ', 
				'THỊ TRẤN'}
district_replace = {'Q1':'1', 'Q2':'2', 'Q3':'3','Q4':'4', 'Q5':'5', 'Q6':'6', 
					'Q7':'7', 'Q8':'8', 'Q9':'9', 'Q10':'10', 'Q11':'11', 
					'Q12': '12'}

def clean_raw_address(raw_address):
	ret = raw_address.upper()
	for noise in noise_string:
		ret = ret.replace(noise,'')
	for key in district_replace:
		ret = ret.replace(key,district_replace[key])
	for i in range(65,91):
		tmp = ' ' + chr(i) + ' '
		ret = ret.replace(tmp,'')
	if len(ret)>1 and ret[1] == ' ':
		ret = ret.replace(ret[:2],'')
	if len(ret)>1 and ret[-2] == ' ':
		ret = ret.replace(ret[-2:],'')
	i = 1
	while i < len(ret):
		if ret[i] >= '0' and ret[i] <= '9' and (ret[i-1] < '0' or ret[i-1] > \
			'9'):
			ret = ret[:i] + ' ' + ret[i:]
			i += 1
		i += 1 
	return ret

def address_correction(input_address):
		input_address = input_address.strip()

		print("Input address: ",input_address.strip())


		pattern_address = clean_raw_address(input_address)

		total = []
		prefix_res = None
		maxx = 0
		ret = None
		for i in range(len(all_addresses)):
				pattern_addresses = gen_pattern_addresses(all_addresses[i])
				for y in pattern_addresses:
						tmp = ratio(y, pattern_address)
						total.append((tmp, i))

		total.sort(reverse = True)
		for i in range(3):
				index = 0
				pattern_addresses = clean_raw_address(gen_pattern_addresses(\
					all_addresses[total[i][1]])[0])
				current_dis = lcs(pattern_address,pattern_addresses)
				while (lcs(pattern_addresses, pattern_address[index + 1:]) == \
					current_dis):
						index += 1
				tmp = ratio(pattern_addresses, pattern_address[index:])
				if tmp > maxx:
					maxx = tmp
					ret = total[i][1]
					prefix_res = pattern_address[:index]

		prefix_res = clean_raw_address(prefix_res)
		prefix_res = prefix_res.lower() + ',' if len(prefix_res) > 1 else ''

		ret = [all_addresses[ret][j][0] for j in range(2, -1, -1)]
		current_dis = lcs(pattern_address,' '.join(ret).upper())
		if lcs(pattern_address,' '.join(ret[2:]).upper()) == current_dis:
			ret = ret[2:]
		if lcs(pattern_address,' '.join(ret[1:]).upper()) == current_dis:
			ret = ret[1:]
		
		# if len(pattern_address.split()) < len((' '.join(ret)).split()):
		# 	index = len(ret)-1
		# 	low = 0
		# 	high = len(clean_raw_address(pattern_address).split()) - 1
		# 	while low < high:
		# 		low += ret[index].count(' ') + 1
		# 		index -= 1
		# 	ret = ret[index+1:]
		
		ret = prefix_res.capitalize() + ','.join(ret)
		return ret