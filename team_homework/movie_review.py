# %%
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import pandas as pd


def get_movie_reviews(mcode, page_num=10):

  movie_review_df = pd.DataFrame(columns=("Title", "Score", "Review"))

  url = "https://movie.naver.com/movie/point/af/list.nhn?st=mcode&sword=" + str(mcode) + "&target=after"

  idx = 0

  for _ in range(0, page_num):
    movie_page = urllib.request.urlopen(url).read()
    movie_page_soup = BeautifulSoup(movie_page, 'html.parser')

    review_list = movie_page_soup.find_all('td', {'class' : 'title'})

    for review in review_list:
      title = review.find('a', {'class' : 'movie color_b'}).get_text()
      score = review.find('em').get_text()
      review_text = review.find('a', {'class' : 'report'}).get('onclick').split(',')[2]
      movie_review_df.loc[idx] = [title, score, review_text]
      idx += 1
      print("#", end="")

    try:
      url = "https://movie.naver.com" +movie_page_soup.find('a', {'class' : 'pg_next'}).get('href')
    except:
      break

  return movie_review_df


# %%
movie_review_df = get_movie_reviews(187310, 1)
movie_review_df

# %%
import pymysql

con = pymysql.connect(host = "192.168.0.13", port=3306, user='root', passwd='passwd',
                     db='moviereview', charset='utf8', autocommit=True)

cur = con.cursor()

for i in range(len(movie_review_df)):
    sql = 'insert into movie_review values("{}","{}","{}")'.format(movie_review_df['Title'][i],movie_review_df['Score'][i],movie_review_df['Review'][i])
    cur.execute(sql)
    i += 1
print('데이터가 정상적으로 입력되었습니다.')

cur.close()
con.close()

