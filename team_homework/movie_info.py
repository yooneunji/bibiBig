# %%
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import pandas as pd
import flask
import pymysql

def get_movie_info(mcode):
  """영화코드를 받아서 영화 정보를 받아오는 함수 정의
  완전자동화를 하기위해서는 더 수정이 필요함
  각 영화 마다 정보의 항목 마다 뒷부분 수정 필요"""

  url = "https://movie.naver.com/movie/bi/mi/basic.nhn?code=" + str(mcode)
  
  response = urllib.request.urlopen(url).read()
  soup = BeautifulSoup(response, 'html.parser')
  
  title = soup.find('a', {'href' : './basic.nhn?code=' + str(mcode)}).get_text()
  genre = soup.find('a', {'href' : '/movie/sdb/browsing/bmovie.nhn?genre=1'}).get_text()
  nation = soup.find('a', {'href' : '/movie/sdb/browsing/bmovie.nhn?nation=US'}).get_text()
  director = soup.find('a', {'href' : '/movie/bi/pi/basic.nhn?code=131235'}).get_text()
  
  year = soup.find('a', {'href' : '/movie/sdb/browsing/bmovie.nhn?open=2021'}).get_text()
  date = soup.find('a', {'href' : '/movie/sdb/browsing/bmovie.nhn?open=20210303'}).get_text()
  open_date = year + date
  
  peoplecount = soup.find('p', {'class' : 'count'}).get_text().replace(',', '')
#   print(title)
#   print(genre)
#   print(nation)
#   print(director)
#   print(open_date)
  # print(peoplecount)
  
  conn = pymysql.connect(host='192.168.0.14', port=3306, user='root', passwd='tlwkr5',
                       db='moviereview', charset='utf8', autocommit=True)

  sql = 'insert into movie_info values("{}", "{}", "{}", "{}", "{}", "{}");'.format(title,
                                                                             genre,
                                                                             nation,
                                                                             director,
                                                                             open_date,
                                                                             peoplecount)

  cur = conn.cursor()
  cur.execute(sql)

  cur.close()
  conn.close()
  
  print('데이터가 정상적으로 입력되었습니다.')
  
  
# %%
minari_info = get_movie_info(187310)


# %%
