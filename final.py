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

    def text(self, s):                  # ũ�Ѹ� ����� file�� ����
       
        target = s.find_all(id='lyrics')
        for a in target:
            with open(self.filename, "w") as f: # ũ�Ѹ� ����� ���Ͽ� ����
                f.write(str(a.get_text()))
                


class WordCounter:              # c �ɼǿ� ���Ǵ� class

    def __init__(self, filename):
        self.filename = filename
    
    def refine(self):                     # text�� ���ǿ� �°� ��ȯ
        with open(self.filename, "r") as f:
            lyric = f.read()
            lyric.lower()   # �ҹ��ڷ� ��ȯ                                    
            lyric = re.sub('[?|.|\'|,|(|)]', '', lyric) # Ư������ ����
            lyric = re.sub('\n',' ', lyric)         # �ٹٲ��� �������� ����
            lst=lyric.split(' ')            # ���� �������� list ����
            
        return lst          # list���·� ��ȯ

    def wcount(self, wordlst):
        count_result = Counter(wordlst) # Counter : �ܾ���� dict���·� ��ȯ
        return count_result
        

class Histogram(WordCounter):   # h �ɼǿ� ���Ǵ� class

    def __init__(self, filename):
        self.filename = filename

    def getlist(self, dictionary): # [�ܾ�,����] list. �������� �������� list�� ��ȯ
        keys = dictionary.keys()    # key(�ܾ�)
        vals = dictionary.values()  # value(�ܾ ����)

        tmp_lst = list()

        for i in range(len(keys)):  # [�ܾ�, ����] list ��ȯ
            tmp_lst.append([keys[i], vals[i]])
    
        tmp_lst.sort(key = lambda x : x[1], reverse=True)   # �������� �������� ����

        return tmp_lst

    def hist(self, tmp_lst):            # [�ܾ�,����(*)] list ��ȯ     
        for j in range(len(tmp_lst)):   # ������ *�� ġȯ�Ͽ� list���� ����
            tmp_lst[j][1] = "*" * tmp_lst[j][1]

        return tmp_lst              # [�ܾ�,����(*)]���·� ��ȯ
    


class MostFiveWords(Histogram):

    def __init__(self, filename):
        self.filename = filename

    def most(self, lst):
        for i in range(5):
                print lst[i][0] + "\t: " + str(lst[i][1])    # �ܾ�    : ���� ���·� ���
                








def main():
    if len(sys.argv) != 3:  # ������ ���� ���� ���
        print len(sys.argv)
        print 'usage: python [�����̸�] {�ɼ�1 | �ɼ�2 | �ɼ� 3} [�������]'
        sys.exit(1)


    option = sys.argv[1]    # option
    filename = sys.argv[2]  # ��� ����
    lst=list()

    queen = Crawler(filename)   # Crawling ����
    r = queen.req()
    s = queen.bsoup(r)
    queen.text(s)               # sample.txt ����
    

    if option == '-c':	    # C �ɼ� : �ܾ� ������ ���� dict�� ��ȯ
        c_option = WordCounter(filename)
        lst = c_option.refine()
        result = c_option.wcount(lst)
        print result


    elif option == '-h':    # H �ɼ� : �ܾ� ������ histogram���� ��ȯ
        h_option = Histogram(filename)
        lst = h_option.refine()
        dict_ = h_option.wcount(lst)
        tmp_lst = h_option.getlist(dict_)
        result = h_option.hist(tmp_lst)

        for i in range(len(result)):
            print result[i][0] + '\t:' + result[i][1]
        

    elif option == '-t':    # T �ɼ�  : �ܾ� ���� ���� 5�� �ܾ� ��ȯ
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
    
