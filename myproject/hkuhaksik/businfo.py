from bs4 import BeautifulSoup
import requests, sys
sys.path.append('/home/ubuntu/Djangojh/myproject/hkuhaksik/key')
import keys

def get_station_pyeog():
	pyeng_url = 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey='
	pyeng_url += keys.data + '&stationId=231000322'
	pyeng_res = requests.get(pyeng_url)
	pyeng_soup = BeautifulSoup(pyeng_res.text, 'html.parser')
	pyeng_ret = ''
	pyeng_rat = ''

	pyeng_routeid = {'231000007' : '1번',  '231000018' : '1-1번', '231000019' : '1-2번',
					'231000011' : '1-3번', '231000020' : '1-4번' ,'231000126' : '1-5번', 
					'231000021' : '1-6번', '231000024' : '1-8번','231000023' : '1-9번',
					'231000122' : '10-8번' ,'231000131' : '11번' ,'231000014' : '2-2번',
					'231000015' : '2-3번' ,'228000013' : '22-1번' ,'231000005' : '370번' ,
					'231000118' : '380번' ,'214000022' : '50번' ,'214000246' : '50-9번' ,
					'231000033' : '60번' ,'231000035' : '60-1번' ,'231000034' : '60-3번',
					'231000025' : '7번' ,'231000016' : '7-1번' ,'231000026' : '7-2번' ,
					'231000028' : '7-3번' ,'231000027' : '7-4번' ,'231000006' : '70번' ,
					'241001590' : '8435번','241004370' : '8455번','241002170' : '8456번'}

	pyeng_arrivalList = list()
	pyeng_busidList = list()
	
	for pyeng_arrival in pyeng_soup.find_all('busarrivallist'):
		pyeng_ele = pyeng_arrival.find('routeid').get_text()
		#pyeng_arrivalList.append(pyeng_ele)
		pyeng_rat = pyeng_routeid[pyeng_ele]
		pyeng_busidList.append(pyeng_rat)
	
	for pyeng_bus_num,pyeng_time1,pyeng_left1 in zip(pyeng_busidList,pyeng_soup.select('predicttime1'),pyeng_soup.select('locationno1')):
		pyeng_ret += "-------------------------\n◆{0:<7}\n{1:<2}분 후 도착\n{2:<2}번째 정거장 전\n".format(pyeng_bus_num,pyeng_time1.string,pyeng_left1.string)
	
	return pyeng_ret


def get_station_an():
	an_url = 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey='
	an_url += keys.data + '&stationId=231000312'

	an_res = requests.get(an_url)
	an_soup = BeautifulSoup(an_res.text, 'html.parser')
	an_ret = ''
	an_rat = ''

	an_routeid = {'231000007' : '1번',  '231000018' : '1-1번', '231000019' : '1-2번',
					'231000011' : '1-3번', '231000020' : '1-4번' ,'231000126' : '1-5번',
					'231000021' : '1-6번', '231000024' : '1-8번','231000023' : '1-9번',
					'231000122' : '10-8번' ,'231000131' : '11번' ,'228000013' : '22-1번',
					'231000005' : '370번' ,'231000118' : '380번' ,'231000105' : '5-5번',
					'214000022' : '50번' ,'214000246' : '50-9번' ,'231000033' : '60번' ,
					'231000035' : '60-1번' ,'231000034' : '60-3번','231000025' : '7번' ,
					'231000016' : '7-1번' ,'231000026' : '7-2번' ,'231000028' : '7-3번' ,
					'231000027' : '7-4번' ,'231000006' : '70번' ,'241001590' : '8435번',
					'241004370' : '8455번','241002170' : '8456번'}

	an_arrivalList = list()
	an_busidList = list()
	
	for an_arrival in an_soup.find_all('busarrivallist'):
		an_ele = an_arrival.find('routeid').get_text()
		an_arrivalList.append(an_ele)
		an_rat = an_routeid[an_ele]
		an_busidList.append(an_rat)
	
	for an_bus_num,an_time1,an_left1 in zip(an_busidList,an_soup.select('predicttime1'),an_soup.select('locationno1')):
		an_ret += "-------------------------\n◆{0:<7}\n{1:<2}분 후 도착\n{2:<2}번째 정거장 전\n".format(an_bus_num,an_time1.string,an_left1.string)
	
	return an_ret

