# parser.py
# need to install selenium, bs4, parse package
from selenium import webdriver
from bs4 import BeautifulSoup
from parse import compile
import json, os, time

# Selenium projects

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pattern = compile('[<script type="text/javascript">\nvar jsonResultData={}\nvar f9DataList={}')

option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_argument('window-size=1920x1080')
option.add_argument("disable-gpu")
driver = webdriver.Chrome(os.path.join(BASE_DIR,'driver/chromedriver.exe'), options=option)
'''
# chrome driver와 chrome browser 모두 84버전을 사용했는지 확인
driver = webdriver.Chrome(os.path.join(BASE_DIR,'driver/chromedriver.exe'))
'''
driver.implicitly_wait(3)
# frameset회피를 위해 직접 링크 이용
driver.get('http://portal.kleague.com/user/loginById.do?portalGuest=rstNE9zxjdkUC9kbUA08XQ==')
# 데이터 포털로 이동
driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/div[2]/ul/li/a').click()

#초크보드 사전 선택을 위해서 먼저 시작 값 선택
driver.find_element_by_xpath("//select[@name='meetYear']/option[text()='2019']").click()
driver.find_element_by_xpath("//select[@name='meetSeq']/option[@value='1']").click()
driver.find_element_by_xpath("//select[@name='roundId']/option[text()='1']").click()
driver.find_element_by_xpath("//select[@name='gameId']/option[@value=1]").click()
time.sleep(5)
driver.find_element_by_xpath('//*[@id="contentsLayer"]/div/div/ul/li[7]/a').click()
team = 0
for round in range(1,39):
    driver.find_element_by_xpath("//select[@name='roundId']/option[@value={}]".format(round)).click()
    for i in range(1,7):
        #드롭다운박스 설정
        team += 1
        driver.find_element_by_xpath("//select[@name='gameId']/option[@value={}]".format(team)).click()
        #체크박스 설정
        #driver.find_element_by_xpath('//*[@id="checkContent_ST"]').click()

        #파싱 파트
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        j = soup.select(
            '#contentsLayerBody > script:nth-child(2)'
        )
        result = pattern.parse(str(j))
        # JSON저장
        json_data = json.loads(result[0])
        # list-comprehension으로 필터링
        json_data = [play for play in json_data if "TYPE_CD" in play and play["TYPE_CD"] == "ST"]
        # 파일 저장
        textround = '0' + str(round) if round < 10 else str(round)
        with open(os.path.join(BASE_DIR, 'shoot_info_91{}{}.json'.format(textround,team%6)), 'w+') as json_file:
            json.dump(json_data, json_file)
driver.quit()