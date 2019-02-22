# -*- encoding: cp949 -*-

import sys
import re
import requests
from bs4 import BeautifulSoup
from collections import Counter

class Crawler:

    url = 'https://www.songtexte.com/songtext/freddie-mercury/bohemian-rhapsody-23982857.html'

    def __init__(self, filename):
        self.filename = filename
        
    def req(self):
        r = requests.get(self.url)
        return r.content

    def bsoup(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        return soup

    def text(self, s):                  # 크롤링 결과를 file로 저장
       
        target = s.find_all(id='lyrics')
        for a in target:
            with open(self.filename, "w") as f: # 크롤링 결과를 파일에 저장
                f.write(str(a.get_text()))
                


class WordCounter:              # c 옵션에 사용되는 class

    def __init__(self, filename):
        self.filename = filename
    
    def refine(self):                     # text를 조건에 맞게 변환
        with open(self.filename, "r") as f:
            lyric = f.read()
            lyric.lower()   # 소문자로 변환                                    
            lyric = re.sub('[?|.|\'|,|(|)]', '', lyric) # 특수문자 제거
            lyric = re.sub('\n',' ', lyric)         # 줄바꿈은 공백으로 변경
            lst=lyric.split(' ')            # 공백 기준으로 list 생성
            
        return lst          # list형태로 반환

    def wcount(self, wordlst):
        count_result = Counter(wordlst) # Counter : 단어수를 dict형태로 반환
        return count_result
        

class Histogram(WordCounter):   # h 옵션에 사용되는 class

    def __init__(self, filename):
        self.filename = filename

    def getlist(self, dictionary): # [단어,개수] list. 개수기준 내림차순 list를 반환
        keys = dictionary.keys()    # key(단어)
        vals = dictionary.values()  # value(단어별 개수)

        tmp_lst = list()

        for i in range(len(keys)):  # [단어, 개수] list 반환
            tmp_lst.append([keys[i], vals[i]])
    
        tmp_lst.sort(key = lambda x : x[1], reverse=True)   # 개수기준 내림차순 정렬

        return tmp_lst

    def hist(self, tmp_lst):            # [단어,개수(*)] list 반환     
        for j in range(len(tmp_lst)):   # 개수를 *로 치환하여 list내용 수정
            tmp_lst[j][1] = "*" * tmp_lst[j][1]

        return tmp_lst              # [단어,개수(*)]형태로 반환
    


class MostFiveWords(Histogram):

    def __init__(self, filename):
        self.filename = filename

    def most(self, lst):
        for i in range(5):
                print lst[i][0] + "\t: " + str(lst[i][1])    # 단어    : 숫자 형태로 출력
                








def main():
    if len(sys.argv) != 3:  # 사용법에 맞지 않을 경우
        print len(sys.argv)
        print 'usage: python [파일이름] {옵션1 | 옵션2 | 옵션 3} [대상파일]'
        sys.exit(1)


    option = sys.argv[1]    # option
    filename = sys.argv[2]  # 대상 파일
    lst=list()

    queen = Crawler(filename)   # Crawling 시작
    r = queen.req()
    s = queen.bsoup(r)
    queen.text(s)               # sample.txt 생성
    

    if option == '-c':	    # C 옵션 : 단어 개수를 세어 dict로 반환
        c_option = WordCounter(filename)
        lst = c_option.refine()
        result = c_option.wcount(lst)
        print result


    elif option == '-h':    # H 옵션 : 단어 개수를 histogram으로 반환
        h_option = Histogram(filename)
        lst = h_option.refine()
        dict_ = h_option.wcount(lst)
        tmp_lst = h_option.getlist(dict_)
        result = h_option.hist(tmp_lst)

        for i in range(len(result)):
            print result[i][0] + '\t:' + result[i][1]
        

    elif option == '-t':    # T 옵션  : 단어 개수 상위 5의 단어 반환
        t_option = MostFiveWords(filename)
        lst = t_option.refine()
        dict_ = t_option.wcount(lst)
        tmp_lst = t_option.getlist(dict_)
        result = t_option.most(tmp_lst)


    else:
        print 'Unknown Option: ' + option
        sys.exit(1)



if __name__ == '__main__':
    main()
    
