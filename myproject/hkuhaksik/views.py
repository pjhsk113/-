import sys
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from hkuhaksik.models import HakMenu, KyoMenu
from bs4 import BeautifulSoup
import json, datetime, requests
sys.path.append('/home/ubuntu/Djangojh/myproject/hkuhaksik')
from businfo import get_station_pyeog, get_station_an

yoill = ['월요일', '화요일', '수요일','목요일', '금요일', '토요일', '일요일']
today_yoill= datetime.datetime.today().weekday()
date_info = yoill[today_yoill]

def keyboard(request):

	return JsonResponse({
		'type' : 'buttons',
		'buttons' : ['학생회관식당','교직원식당', '열람실조회','버스']
	})

@csrf_exempt
def message(request):
	button_list = ['학생회관식당','교직원식당', '열람실조회','버스']
	bus_button = ['평택 > 한경대 방향','한경대 > 평택 방향', '취소하기']
	message = (request.body).decode('utf-8')
	received_json_data = json.loads(message)
	content_name = received_json_data['content']
	today = datetime.date.today()
	today_date = today.strftime("(%Y.%m.%d)")

	if content_name =="학생회관식당":
		return JsonResponse({
			'message': {
				'text' : today_date + date_info +'\n\n' + get_menu(content_name)
			},
			'keyboard' : {
				'type' :'buttons',
				'buttons' : button_list
			}

		})
	elif content_name =="교직원식당" :
		return JsonResponse({
			'message': {
				'text' :  today_date + date_info +'\n\n' + get_menu(content_name)
			},
			'keyboard' : {
				'type' :'buttons',
				'buttons' : button_list
			}
		})
	elif content_name =="열람실조회":
		return JsonResponse({
			"message": {
    			"text": "열람실 현황입니다.",
				'message_button':{
					"label": "좌석 확인하기",
					"url": "http://220.66.22.33/EZ5500/SEAT/RoomStatus.aspx"
				}
			},
			'keyboard' : {
				'type' :'buttons',
				'buttons' : button_list
			}
		})
	elif content_name =="버스" :
		return JsonResponse({
			'message': {
				'text' :  "가실방향을 정해주세요.",
			},
			'keyboard' : {
				'type' :'buttons',
				'buttons' : bus_button
			}
		})
	if content_name =="평택 > 한경대 방향":
		return JsonResponse({
			'message': {
				'text' :  "평택 > 한경대 방향\n\n" + get_station_an()
			},
			'keyboard' : {
				'type' :'buttons',
				'buttons' : button_list				
			}
		})
	elif content_name =="한경대 > 평택 방향":
		return JsonResponse({
			'message': {
				'text' :  '한경대 > 평택 방향\n\n' + get_station_pyeog()
			},
			'keyboard' : {
				'type' :'buttons',
				'buttons' : button_list
			}
		})
	elif content_name =="취소하기":
		return JsonResponse({
			'message': {
				'text' :  '취소되었습니다.'
			},
			'keyboard' : {
				'type' :'buttons',
				'buttons' : button_list
			}
		})
					
def get_menu(content_name):
	if content_name =='학생회관식당':
		if date_info == ('토요일'):
			return "===========\n학생회관식당메뉴\n============\n토요일은 쉽니다!"
		elif date_info == ('일요일'):
			return "===========\n학생회관식당메뉴\n===========\n일요일은 쉽니다!"
		else:
			hak_yang = HakMenu.objects.get(cafe_name='양식').menu
			hak_ill	= HakMenu.objects.get(cafe_name='일품').menu
			hak_bek = HakMenu.objects.get(cafe_name='백반').menu
			hak_bun = HakMenu.objects.get(cafe_name='분식').menu

			return "===========\n학생회관식당메뉴\n===========\n" \
				+ hak_yang \
				+ "--------------------\n" + hak_ill \
				+ "--------------------\n" + hak_bek \
				+ "--------------------\n" + hak_bun \

	elif content_name =="교직원식당":
		if date_info == ('토요일'):
			return "==========\n교직원식당메뉴\n==========\n토요일은 쉽니다!"
		elif date_info == ('일요일'):
			return "==========\n교직원식당메뉴\n==========\n일요일은 쉽니다!"
		else:
			kyo_menu = KyoMenu.objects.get(cafe_name='교직원').menu

			return "==========\n교직원식당메뉴\n==========" \
				+ "\n" + kyo_menu \

def hakcrawl(request):
	flush_hak_menu_db()

	#학생식당메뉴 테이블 추출 	
	hak_res = requests.get('http://www.hknu.ac.kr/web/kor/l_05_06_01')
	hak_res.close()
	hak_soup = BeautifulSoup(hak_res.content, 'html.parser', from_encoding='utf-8')	
	hak_table_find = hak_soup.find(class_='table-basic') #전체 테이블 추출
	hak_menu_table = hak_table_find.find_all('tr')[1:6]
	
	hak_mon_tr = hak_menu_table[0]
	hak_tue_tr = hak_menu_table[1]
	hak_wed_tr = hak_menu_table[2]
	hak_thu_tr = hak_menu_table[3]
	hak_fri_tr = hak_menu_table[4]

	#요일별 열정보(요일,날짜 정보)
	hak_mon_td = hak_mon_tr.find('td')
	hak_tue_td = hak_tue_tr.find('td')
	hak_wed_td = hak_wed_tr.find('td')
	hak_thu_td = hak_thu_tr.find('td')
	hak_fri_td = hak_fri_tr.find('td')
	
	#요일별 양식메뉴 
	hak_mon_yang = hak_mon_tr.find_all('td')[1]
	hak_tue_yang = hak_tue_tr.find_all('td')[1]
	hak_wed_yang = hak_wed_tr.find_all('td')[1]
	hak_thu_yang = hak_thu_tr.find_all('td')[1]
	hak_fri_yang = hak_fri_tr.find_all('td')[1]
	yang_col = [hak_mon_yang, hak_tue_yang, hak_wed_yang, hak_thu_yang, hak_fri_yang]

	#요일별 일품메뉴
	hak_mon_ill = hak_mon_tr.find_all('td')[2]	
	hak_tue_ill = hak_tue_tr.find_all('td')[2] 
	hak_wed_ill = hak_wed_tr.find_all('td')[2]	
	hak_thu_ill = hak_thu_tr.find_all('td')[2]
	hak_fri_ill = hak_fri_tr.find_all('td')[2]
	ill_col = [hak_mon_ill, hak_tue_ill, hak_wed_ill, hak_thu_ill, hak_fri_ill]	

	#요일별 백반메뉴
	hak_mon_bek = hak_mon_tr.find_all('td')[3]	
	hak_tue_bek = hak_tue_tr.find_all('td')[3]
	hak_wed_bek = hak_wed_tr.find_all('td')[3]	
	hak_thu_bek = hak_thu_tr.find_all('td')[3]
	hak_fri_bek = hak_fri_tr.find_all('td')[3]
	bek_col = [hak_mon_bek, hak_tue_bek, hak_wed_bek, hak_thu_bek, hak_fri_bek] 

	#요일별 분식메뉴
	hak_mon_bun = hak_mon_tr.find_all('td')[4]
	hak_tue_bun = hak_tue_tr.find_all('td')[4]
	hak_wed_bun = hak_wed_tr.find_all('td')[4]	
	hak_thu_bun = hak_thu_tr.find_all('td')[4]
	hak_fri_bun = hak_fri_tr.find_all('td')[4]
	bun_col = [hak_mon_bun, hak_tue_bun, hak_wed_bun, hak_thu_bun, hak_fri_bun]

	for i in range(0,5):
		yang_col[i] = str(yang_col[i]).replace("<td>","★").replace("&amp;","&").replace("<br/>"," \n").replace("</td>","\n")
		ill_col[i] = str(ill_col[i]).replace("<td>","★").replace("&amp;","&").replace("<br/>"," \n").replace("</td>","\n")
		bek_col[i] = str(bek_col[i]).replace("<td>","★").replace("&amp;","&").replace("<br/>"," \n").replace("</td>","")
		bun_col[i] = str(bun_col[i]).replace("<td>","★").replace("&amp;","&").replace("<br/>"," \n").replace("</td>","")

	if hak_mon_td.find(text='월요일') == date_info:
		create_hak_menu_db('양식', yang_col[0])
		create_hak_menu_db('일품', ill_col[0])
		create_hak_menu_db('백반', bek_col[0])
		create_hak_menu_db('분식', bun_col[0])
	elif hak_tue_td.find(text='화요일') == date_info:
		create_hak_menu_db('양식', yang_col[1])
		create_hak_menu_db('일품', ill_col[1])
		create_hak_menu_db('백반', bek_col[1])
		create_hak_menu_db('분식', bun_col[1])
	elif hak_wed_td.find(text='수요일') == date_info:
		create_hak_menu_db('양식', yang_col[2])
		create_hak_menu_db('일품', ill_col[2])
		create_hak_menu_db('백반', bek_col[2])
		create_hak_menu_db('분식', bun_col[2])
	elif hak_thu_td.find(text='목요일') == date_info:
		create_hak_menu_db('양식', yang_col[3])
		create_hak_menu_db('일품', ill_col[3])
		create_hak_menu_db('백반', bek_col[3])
		create_hak_menu_db('분식', bun_col[3])
	elif hak_fri_td.find(text='금요일') == date_info:
		create_hak_menu_db('양식', yang_col[4])
		create_hak_menu_db('일품', ill_col[4])
		create_hak_menu_db('백반', bek_col[4])
		create_hak_menu_db('분식', bun_col[4])

	return JsonResponse({'status': 'crawled'})

def kyocrawl(request):
	flush_kyo_menu_db()

	kyo_res = requests.get('http://www.hknu.ac.kr/web/kor/l_05_06_02')
	kyo_res.close()
	kyo_soup = BeautifulSoup(kyo_res.content, 'html.parser', from_encoding='utf-8')	
	kyo_table_find = kyo_soup.find(class_='table-basic') #전체 테이블 추출
	kyo_menu_table = kyo_table_find.find_all('tr')[1:6]

	kyo_mon_tr = kyo_menu_table[0]
	kyo_tue_tr = kyo_menu_table[1]
	kyo_wed_tr = kyo_menu_table[2]
	kyo_thu_tr = kyo_menu_table[3]
	kyo_fri_tr = kyo_menu_table[4]

	#요일별 열정보(요일,날짜 정보)
	kyo_mon_td = kyo_mon_tr.find('td')
	kyo_tue_td = kyo_tue_tr.find('td')
	kyo_wed_td = kyo_wed_tr.find('td')
	kyo_thu_td = kyo_thu_tr.find('td')
	kyo_fri_td = kyo_fri_tr.find('td')

	#요일별 양식메뉴 
	kyo_mon_kyo = kyo_mon_tr.find_all('td')[1]
	kyo_tue_kyo = kyo_tue_tr.find_all('td')[1]
	kyo_wed_kyo = kyo_wed_tr.find_all('td')[1]
	kyo_thu_kyo = kyo_thu_tr.find_all('td')[1]
	kyo_fri_kyo = kyo_fri_tr.find_all('td')[1]
	kyo_col = [kyo_mon_kyo, kyo_tue_kyo, kyo_wed_kyo, kyo_thu_kyo, kyo_fri_kyo]
		
	for i in range(0,5):
		kyo_col[i] = str(kyo_col[i]).replace("<td>","★").replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("<br/>","\n").replace("</td>","")

	if kyo_mon_td.find(text='월요일') == date_info:
		create_kyo_menu_db('교직원', kyo_col[0])
			
	elif kyo_tue_td.find(text='화요일') == date_info:
		create_kyo_menu_db('교직원', kyo_col[1])
		
	elif kyo_wed_td.find(text='수요일') == date_info:
		create_kyo_menu_db('교직원', kyo_col[2])
		
	elif kyo_thu_td.find(text='목요일') == date_info:
		create_kyo_menu_db('교직원', kyo_col[3])
			
	elif kyo_fri_td.find(text='금요일') == date_info:
		create_kyo_menu_db('교직원', kyo_col[4])

	return JsonResponse({'status': 'crawled'})

def create_hak_menu_db(cafe_name, menu):
	HakMenu.objects.create(
		cafe_name = cafe_name,
		menu = menu,
		is_new = True
	)

def create_kyo_menu_db(cafe_name, menu):
	KyoMenu.objects.create(
		cafe_name = cafe_name,
		menu = menu,
		is_new = True
	)

def flush_hak_menu_db():
	menu_db = HakMenu.objects.all()
	menu_db.delete()

def flush_kyo_menu_db():
	menu_db = KyoMenu.objects.all()
	menu_db.delete()

