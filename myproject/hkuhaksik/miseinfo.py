from bs4 import BeautifulSoup
import requests, sys
sys.path.append('/home/ubuntu/Djangojh/myproject/hkuhaksik/key')
import keys

def get_mise():
	mise_url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst?serviceKey='
	mise_url += keys.data + '&numOfRows=1&pageSize=10&pageNo=1&startPage=1&itemCode=PM10&dataGubun=HOUR&searchCondition=MONTH'
	mise_res = requests.get(mise_url)
	mise_soup = BeautifulSoup(mise_res.text, 'html.parser')
	
	mise_List = list()
	mise_x= ['좋음','보통','나쁨','매우나쁨']
	mise_z= list()
	for mise_i in mise_data:
		if(mise_i!='\n'):
			mise_List.append(mise_i)
	del mise_List[0:3]

	mise_List2 = (str(mise_List).replace("[<seoul>","").replace("</seoul>","").replace("<busan>","").replace("</busan>","")
	.replace("<daegu>","").replace("</daegu>","").replace("<incheon>","").replace("</incheon>","")
	.replace("<gwangju>","").replace("</gwangju>","").replace("<daejeon>","").replace("</daejeon>","")
	.replace("<ulsan>","").replace("</ulsan>","").replace("<gyeonggi>","").replace("</gyeonggi>","")
	.replace("<gangwon>","").replace("</gangwon>","").replace("<chungbuk>","").replace("</chungbuk>","")
	.replace("<chungnam>","").replace("</chungnam>","").replace("<jeonbuk>","").replace("</jeonbuk>","")
	.replace("<jeonnam>","").replace("</jeonnam>","").replace("<gyeongbuk>","").replace("</gyeongbuk>","")
	.replace("<gyeongnam>","").replace("</gyeongnam>","").replace("<jeju>","").replace("</jeju>","")
	.replace("<sejong>","").replace("</sejong>]",""))
	mise_List2 = mise_List2.split(",") 
	mise_List2 = [int(i)for i in mise_List2]

	mise_List3 = (str(mise_List).replace("[<seoul>"," 서울 ").replace("</seoul>","").replace("<busan>","부산 ").replace("</busan>","")
	.replace("<daegu>","대구 ").replace("</daegu>","").replace("<incheon>","인천 ").replace("</incheon>","")
	.replace("<gwangju>","광주 ").replace("</gwangju>","").replace("<daejeon>","대전 ").replace("</daejeon>","")
	.replace("<ulsan>","울산 ").replace("</ulsan>","").replace("<gyeonggi>","경기 ").replace("</gyeonggi>","")
	.replace("<gangwon>","강원 ").replace("</gangwon>","").replace("<chungbuk>","충북 ").replace("</chungbuk>","")
	.replace("<chungnam>","충남 ").replace("</chungnam>","").replace("<jeonbuk>","전북 ").replace("</jeonbuk>","")
	.replace("<jeonnam>","전남 ").replace("</jeonnam>","").replace("<gyeongbuk>","경북 ").replace("</gyeongbuk>","")
	.replace("<gyeongnam>","경남 ").replace("</gyeongnam>","").replace("<jeju>","제주 ").replace("</jeju>","")
	.replace("<sejong>","세종 ").replace("</sejong>]",""))
	mise_List3 = mise_List3.split(",") 


	ret = mise_date+'\n' +"미세먼지 정보입니다."'\n\n'+ "-------------------------"+'\n' + "관측지점 현재    예보"+ '\n'
	for i in range(0,17):
		if(mise_List2[i]<=30):
			mise_z.append(mise_x[0])
		elif(30<mise_List2[i]<=80):
			mise_z.append(mise_x[1])
		elif(80<mise_List2[i]<=150):
			mise_z.append(mise_x[2])
		elif(150<=mise_List2[i]):
			mise_z.append(mise_x[3])

	for mise_per,mise_stat in zip(mise_List3,mise_z):
		ret += "-------------------------\n◆{0:<3}\n{1:<5}\n".format(mise_per,mise_stat)

	return ret