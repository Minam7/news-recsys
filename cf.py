import numpy

import lda
import mf


def user_news_creator():
    file = open('user_news_matrix.txt', 'r')
    user_news_file = file.read().split('\n')
    news = int(user_news_file[0])

    user_news = list()
    user_id = dict()
    for i in range(1, len(user_news_file)):
        data = user_news_file[i].split(' ')
        for i in range(1, len(data)):
            data[i] = float(data[i])
        user_id[data[0]] = i - 1
        user_news.append(data[1:news + 1])

    return user_news, user_id


# read from written file
def news_topic_creator():
    file = open('news_topic_matrix.txt', 'r')
    news_topic_file = file.read().split('\n')
    news_topic = list()
    for i in range(len(news_topic_file)):
        num = news_topic_file[i].split(' ')
        if len(num) != 0:
            for i in range(len(num)):
                num[i] = float(num[i])
            news_topic.append(num)

    # list is string not float convert if needed

    return news_topic


def add_new_doc_to_news_topic(doc_name):
    # update all news_topic
    file = open('news_topic_matrix.txt', 'a+')
    news_topic = lda.news_topic_creator('news2')
    log = ''
    for item_x in news_topic:
        log += str(item_x) + ' '
    file.write(log)
    file.close()


'''
def user_topic_reader():
    file = open('user_topic_matrix.txt', 'r')
    user_topic_file = file.read().split('\n')
    news = int(user_topic_file[0])
    # TODO map id to cookie
    user_news = dict()
    for i in range(1, len(user_news_file)):
        data = user_news_file[i].split(' ')
        user_news[data[0]] = data[1:news]

    return user_news
'''

if __name__ == '__main__':
    # TODO make file
    user_news_matrix, user_id = user_news_creator()
    user_news_matrix = numpy.array(user_news_matrix, dtype=float)
    # print("user news matrix", user_news_matrix)

    news_topic_matrix = news_topic_creator()

    news_topic_matrix = numpy.array(news_topic_matrix, dtype=float)

    user_topic_matrix = numpy.dot(user_news_matrix, news_topic_matrix)

    N = len(user_topic_matrix)
    M = len(user_topic_matrix[0])
    K = 2  # hyper parameter

    P = numpy.random.rand(N, K)
    Q = numpy.random.rand(M, K)

    nP, nQ = mf.matrix_factorization(user_topic_matrix, P, Q, K)

    nR = numpy.dot(nP, nQ.T)

    for item in nR:
        print(item)
