def readFile(file_name):
    f = open(file_name, 'r')
    y = []
    x = f.readlines()
    for line in x:
        y.extend(line.split())

    f.close()
    word_list2 = []

    for word in y:
        word1 = word

        while True:
            lastchar = word1[-1:]
            if lastchar in [',', '.', '!', '?', ';', '"']:
                word2 = word1.rstrip(lastchar)
                word1 = word2
            else:
                word2 = word1
                break

        while True:
            firstchar = word2[0]
            if firstchar in [',', '.', '!', '?', ';', '"']:
                word3 = word2.lstrip(firstchar)
                word2 = word3
            else:
                word3 = word2
                break

        word_list2.append(word3.lower())
    
    freq_list = []
    word_saved = []
    for word2 in word_list2:
        if not word2 in word_saved:
            word_saved.append(word2)
            freq_list.append((word2, word_list2.count(word2)))

            sorted_list = sorted(freq_list, key=lambda x:x[1],reverse=True)
            return sorted_list


import re
def readFile1(filename):
    f = open(filename, 'r')
    y = []
    x = f.readlines()
    for line in x:
        words = re.findall('[a-zA-Z\']+', line)
        for word in words:
            y.append(word.lower())

    f.close()

    freq_list = []
    word_saved = []
    for word2 in y:
        if not word2 in word_saved:
            word_saved.append(word2)
            freq_list.append((word2, y.count(word2)))

    sorted_list = sorted(freq_list, key=lambda x:x[1], reverse=True)
    return sorted_list

def mergeStatic(list1, list2):
    word1, num1 = zip(*list1)
    merge_list = []

    for word, num in list2:
        if not word in word1:
            merge_list.append((word, num))
        else:
            index = word1.index(word)
            merge_list.append((word, num+num1[index]))

    word2, num2 = zip(*list2)
    for word, num in list1:
        if not word in word2:
            merge_list.append((word, num))

    sorted_list = sorted(merge_list, key=lambda x:x[1],reverse=True)
    return sorted_list

if __name__ == '__main__':
    file_list = ['article_000.txt','article_001.txt','article_002.txt','article_003.txt','article_004.txt','article_005.txt']
    cc = map(readFile, file_list)
    word_list = reduce(mergeStatic, cc)

    print 'Word List:'
    for word in word_list[0:10]:
        print '%-10s %d' % (word[0], word[1])
