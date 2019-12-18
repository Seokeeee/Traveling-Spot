#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import multiprocessing

def crawlingLastPageNum(url, page):
    html = requests.get(url)
    plain_text = html.text
    bs = BeautifulSoup(plain_text, 'lxml')

    class_name = ''; spotName = ''
    if page == 'SPOT':
        class_name = 'pageNum taLnk'
    else:
        class_name = 'pageNum'
        spotName = bs.find('h1', class_="ui_header h1").text

    try:
        result = list(bs.find_all('a', class_=class_name))
        # lastPage = result[-1].attrs['data-page-number']
        lastPage = result[-1].text
    except:
        lastPage = 1

    return int(lastPage), spotName

def crawlingLinks(url):
    fileName = r"C:\Users\wlsdu\Desktop\ai_project\data/spotLinks.txt"
    f = open(fileName, 'w', -1, "utf-8")

    html = requests.get(url)
    plain_text = html.text
    bs = BeautifulSoup(plain_text, 'lxml')

    spot_urls = []
    spot_list = bs.find_all('div', class_="listing_title")
    for link in spot_list:
        spot_url = link.find("a").attrs['href']
        f.write(spot_url + "\n")
        spot_urls.append(spot_url)

    return spot_urls

def crawlingReviews(url, start, index):
    try:
        lastPageNum, spotName = crawlingLastPageNum(url, 'REVIEW')
        fileName = r"C:\Users\wlsdu\Desktop\ai_project\data/" + spotName + ".txt"
        print("process id:", start, "index", index, "spotName:", spotName, "Last PageNum", lastPageNum)
        f = open(fileName, 'w', -1, "utf-8")
        f.write(spotName+"\n")

        offset = 10
        for i in range(0, lastPageNum*offset, offset):
            # print(i/10+1)
            offset_url = url[:url.find('Reviews') + 7] + "-or" + str(i) + url[url.find('Reviews') + 7:]

            html = requests.get(offset_url)
            plain_text = html.text
            bs = BeautifulSoup(plain_text, 'lxml')

            result = list(bs.find_all('q', class_='location-review-review-list-parts-ExpandableReview__reviewText--gOmRC'))
            for i in range(0, len(result)):
                t = result[i].text + "\n"
                # print(t)
                f.write(t)

        f.close()
    except:
        pass

def multiCrawling(start):
    try:
        spotLinks = open(r"C:\Users\wlsdu\Desktop\TextLink\data/spotLinks.txt").read().split('\n')
        t = spotLinks.pop()
        for i in range(start, start+10):
            reviewUrl = "https://www.tripadvisor.co.kr" + spotLinks[i]
            crawlingReviews(reviewUrl, start, i)
    except:
        print("error id is", start)

    pass

if __name__ == '__main__':

    # 모든 여행지 링크 크롤링
    # spotUrl = "https://www.tripadvisor.co.kr/Attractions-g294197-Activities-Seoul.html#FILTERED_LIST"
    # lastPageNum, _ = crawlingLastPageNum(spotUrl, 'SPOT')
    #
    # spotLinks = []; offset = 30
    # for i in range(0, lastPageNum*30, offset):
    #     linkUrl = "https://www.tripadvisor.co.kr/Attractions-g294197-Activities-oa" + str(i) + "-Seoul.html#FILTERED_LIST"
    #     spotLinks += crawlingLinks(linkUrl)
    # print(len(spotLinks))
    #
    # fileName = r"C:\Users\wlsdu\Desktop\ai_project\data/spotLinks.txt"
    # file_spot = open(fileName, 'w', -1, "utf-8")
    # for link in spotLinks:
    #     file_spot.write(link+"\n")

    # 여행지 별 리뷰 데이터 크롤링
    spotLinks = open(r"C:\Users\wlsdu\Desktop\ai_project\data/spotLinks.txt").read().split('\n')
    t = spotLinks.pop()
    # for i in range(7, len(spotLinks)):
    #     print("index", i)
    #     reviewUrl = "https://www.tripadvisor.co.kr" + spotLinks[i]
    #     crawlingReviews(reviewUrl)

    # 여행지 별 리뷰 멀티프로세싱으로 크롤링
    start = [0, 10, 20, 30, 40]
    pool = multiprocessing.Pool(processes=5)
    pool.map(multiCrawling, start)
    pool.close()
    pool.join()

    # print(crawlingReviews("https://www.tripadvisor.co.kr/Attraction_Review-g294197-d15693012-Reviews-K_Style_Hub-Seoul.html", 1, 2))
    # print(spotLinks[543])

    pass

