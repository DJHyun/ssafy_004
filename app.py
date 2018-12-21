import requests
import time
import json
from bs4 import BeautifulSoup as bs
from flask import Flask,render_template , request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/toon')    
def toon():
    cat = request.args.get('type')
    today = time.strftime("%a").lower()
    
    if(cat == 'naver'):
        '''
        1. 네이버 웹툰을 가져올 수 있는 주소(url)를 파악하고 url 변수에 저장한다.
        
        2. 해당 주소로 요청을 보내 정보를 가져온다.
        
        3. 받은 정보를 bs를 이용해 검색하기 좋게 만든다.
        
        4. 네이버 웹툰 페이지로 가서, 내가 원하는 정보가 어디에 있는지 파악한다.
        오늘자 업데이트 된 웹툰들의 각각 리스트 페이지, 웹툰의 제목 + 해당 웹툰의 썸네일
        
        5. 3번에서 저장한 문서를 이용해 4번에서 파악한 위치를 뽑아내는 코드를 작성한다.
        
        6. 출력한다.
        '''
        
        naver_url = 'https://comic.naver.com/webtoon/weekdayList.nhn?week='+today
        response = requests.get(naver_url).text
        soup = bs(response,'html.parser')
        toons = []
        li = soup.select('.img_list li')
        
        for item in li:
          toon = {"title":item.select_one('dt a').text,
                  "url": "https://comic.naver.com"+item.select('dt a')[0]["href"],
                  "img_url":item.select('.thumb img')[0]['src']
                 }
          toons.append(toon)
    else:
        #1. 내가 원하는 정보를 얻을 수 있는 주소를 url이라고 하는 변수에 담는다.
        url = "http://webtoon.daum.net/data/pc/webtoon/list_serialized/"+today
        #2. 해당 url에 요청을 보내 응답을 받아 저장한다.
        response = requests.get(url).text
        #3. 구글신에게 python으로 어떻게 json을 파싱(딕셔너리 형으로 변환)하는지 물어본다.
        #4. 파싱한다.(변환한다)
        document = json.loads(response)
        #5. 내가 원하는 데이터를 꺼내서 조합한다.
        data = document["data"]
        toons = []
        for toon in data:
            toon = {"title":toon["title"], 
                    "img_url":toon["pcThumbnailImage"]["url"], 
                    "url":"http://webtoon.daum.net/webtoon/view/{}".format(toon["nickname"]) 
                    }
            toons.append(toon)
            
    return render_template('toon.html', cat = cat, t = toons, today = today)
    
    
@app.route('/lotto')
def lotto():
    return render_template('lotto.html')
    
@app.route('/apart')
def apart():
#1. 내가 원하는 정보를 얻을 수 있는 url을 url 변수에 저장한다.
#1-1. header에 추가할 정보를 dictionary 형태로 저장한다.
#2. requests의 get 기능을 이용하여 해당 url에 header와 함께 요청을 보낸다.
#3. 응답으로 온 코드의 형태를 살펴본다.(json/xml/html)
    url = "http://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do?menuGubun=A&p_apt_code=20333305&p_house_cd=1&p_acc_year=2018&areaCode=&priceCode="
    headers = {
                'Host': 'rt.molit.go.kr',
                'Referer': 'http://rt.molit.go.kr/new/gis/srh.do?menuGubun=A&gubunCode=LAND'
                }
    response = requests.get(url, headers = headers).text
    document = json.loads(response)
    
    print(response)
    for d in document["result"]:
        print(d["BLDG_NM"])
    return render_template('apart.html')
    
@app.route('/exchange')
def exchange():
    #어느 사이트든 좋습니다.
    #크롤링을 통해 가장 많은 환율 정보를 끌어 오시는 분께 커피 삽니다.
    url = 'http://finance.daum.net/api/exchanges/summaries'
    headers = {
                'Host': 'finance.daum.net',
                'Referer': 'http://finance.daum.net/exchanges',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
                }
    response = requests.get(url, headers = headers).text
    document = json.loads(response)
    
    data = document["data"]
    ex = []
    
    for x in data:
        x = {"country":x["country"], 
             "basePrice":x["basePrice"] 
            }
        ex.append(x)
            
    return render_template('exchange.html', ex = ex)

@app.route('/food')
def food():
    #어느 사이트든 좋습니다.
    #크롤링을 통해 가장 많은 환율 정보를 끌어 오시는 분께 커피 삽니다.
    url = 'https://map.naver.com/search2/local.nhn?menu=location&type=SITE_1&queryRank=0&tab=1&isFirstSearch=true&__fromRestorer=true&query=%EA%B0%95%EB%82%A8%EC%97%AD+%EB%A7%9B%EC%A7%91&searchCoord=&sm=clk&mpx=37.4954844%2C127.0333571%3AZ11%3A0.0153438%2C0.0151543'
    headers = {
                'Referer': 'https://map.naver.com/?query=%EA%B0%95%EB%82%A8%EC%97%AD+%EB%A7%9B%EC%A7%91&type=SITE_1&queryRank=0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'Host': 'map.naver.com'
    }   
   
    response = requests.get(url, headers = headers).text
    document = json.loads(response)
    
    data = document['result']
    print(data)
            
    return render_template('food.html' )