#!/usr/bin/env python
# coding: utf-8
#copyRight by heibanke


import time    
import os

def readFile(file_name):
    time.sleep(0.1)
    print "current process id is ",os.getpid()

    f=open(file_name,'r')
    y=[]
    x=f.readlines()
    for line in x:
        y.extend(line.split())
    
    f.close()
    word_list2 = []
    
    #单词格式化
    for word in y:
        # last character of each word
        word1 = word
       
        # use a list of punctuation marks
        while True:
            lastchar = word1[-1:]
            if lastchar in [",", ".", "!", "?", ";",'"']:
                word2 = word1.rstrip(lastchar)
                word1 = word2
            else:
                word2 = word1
                break
                
        while True:        
            firstchar = word2[0]    
            if firstchar in [",", ".", "!", "?", ";",'"']:
                word3 = word2.lstrip(firstchar)
                word2 = word3
            else:
                word3 = word2
                break
            # build a wordList of lower case modified words
        word_list2.append(word3.lower())
    
    #统计词频
    freq_list = []
    word_saved = []
    for word2 in word_list2:
        if not word2 in word_saved:
            word_saved.append(word2)
            freq_list.append((word2,word_list2.count(word2)))
    
    #排序
    sorted_list = sorted(freq_list,key=lambda x:x[1],reverse=True)  
    return sorted_list




def wordnumStatic(list1,list2):
    
    word1,num1=zip(*list1)
   
    merge_list = []
    
    #将list2中的word加入到merge_list
    for word,num in list2:
        if not word in word1:
            merge_list.append((word,num))
        else:
            index = word1.index(word)
            merge_list.append((word,num+num1[index]))
    
    #将list1中没有统计到merge_list的word加入
    word2,num2=zip(*list2)        
    for word,num in list1:
        if not word in word2:
            merge_list.append((word,num))
    
    #排序
    sorted_list = sorted(merge_list,key=lambda x:x[1],reverse=True)    
    return sorted_list
    
    
if __name__=="__main__":
    # 15*6 = 90 articles
    file_list = ['article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt',
    'article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt',
    'article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt',
    'article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt',
    'article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt',
    'article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt',
    'article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt',
    'article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt',
    'article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt',
    'article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt',
    'article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt',
    'article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt',
    'article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt',
    'article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt',
    'article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt'] 

    import multiprocessing as multi
    #创建进程池
    pool_num = 16
    pool = multi.Pool(pool_num) 

    start = time.time()

    #cc = map(readFile, file_list)
    cc = pool.map(readFile, file_list)

    end = time.time()
    print "Total cost time is ",end-start,"s"
    
    #关闭进程池
    pool.close() 
    pool.join()

    word_list = reduce(wordnumStatic,cc)

    print u"最常用的单词排行榜:"
    for word in word_list[0:10]:
        print "%-10s %d" % (word[0], word[1])    