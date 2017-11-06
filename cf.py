from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import numpy
import lda
import mf


def user_news_creator():
    file = open('files/user_news_matrix.txt', 'r')
    user_news_file = file.read().split('\n')
    news = int(user_news_file[0])

    user_news = list()
    user_id = dict()
    for i in range(1, len(user_news_file)):
        data = user_news_file[i].split(' ')
        for j in range(1, len(data)):
            data[j] = float(data[j])
        user_id[data[0]] = i - 1
        user_news.append(data[1:news + 1])

    return user_news, user_id


# read from written file
def user_topic_creator():
    file = open('files/user_topic_matrix.txt', 'r')
    user_topic_file = file.read().split('\n')
    user_topic = list()
    for i in range(len(user_topic_file)):
        num = user_topic_file[i].split(' ')
        if len(num) != 0:
            for j in range(len(num)):
                num[j] = float(num[j])
            user_topic.append(num)

    return user_topic


# read from written file
def news_topic_creator():
    file = open('files/news_topic_matrix.txt', 'r')
    news_topic_file = file.read().split('\n')
    news_topic = list()
    for i in range(len(news_topic_file)):
        num = news_topic_file[i].split(' ')
        if len(num) != 0:
            for j in range(len(num)):
                num[j] = float(num[j])
            news_topic.append(num)

    return news_topic


def add_new_doc_to_news_topic(doc_name):
    # update all news_topic
    file = open('files/news_topic_matrix.txt', 'a+')
    news_topic = lda.news_topic_creator('news2')
    log = ''
    for item_x in news_topic:
        log += str(item_x) + ' '
    file.write(log)
    file.close()


'''
def user_topic_reader():
    file = open('files/user_topic_matrix.txt', 'r')
    user_topic_file = file.read().split('\n')
    news = int(user_topic_file[0])
    # TODO map id to cookie
    user_news = dict()
    for i in range(1, len(user_news_file)):
        data = user_news_file[i].split(' ')
        user_news[data[0]] = data[1:news]

    return user_news
'''


def user_topic_matrix(user_news_matris):
    user_news_matris = numpy.array(user_news_matris, dtype=float)
    # print("user news matrix", user_news_matrix)

    news_topic_matrix = news_topic_creator()

    news_topic_matrix = numpy.array(news_topic_matrix, dtype=float)

    user_topic_matris = numpy.dot(user_news_matris, news_topic_matrix)

    N = len(user_topic_matris)
    M = len(user_topic_matris[0])
    K = 2  # hyper parameter

    P = numpy.random.rand(N, K)
    Q = numpy.random.rand(M, K)

    nP, nQ = mf.matrix_factorization(user_topic_matris, P, Q, K)

    nR = numpy.dot(nP, nQ.T)

    file = open('files/user_topic_matrix.txt', 'w')
    log = ''
    for j in range(len(nR)):
        item = nR[j]
        for i in range(len(item)):
            log += str(item[i])
            if i < len(item) - 1:
                log += ' '
        if j < len(nR) - 1:
            log += '\n'
    file.write(log)
    file.close()

    return nR, user_topic_matris


def user_recommendation(user_cookie):
    user_news_matrix, user_id = user_news_creator()
    user = user_id[user_cookie]
    nR, utm = user_topic_matrix(user_news_matrix)
    # nR is a mf matrix and utm is raw matrix

    # you can use utm or nR!
    utm = sparse.csr_matrix(utm)

    similarities = cosine_similarity(utm)
    print('pairwise dense output:\n {}\n'.format(similarities))

    similarities_sparse = cosine_similarity(utm, dense_output=False)
    print('pairwise sparse output:\n {}\n'.format(similarities_sparse))
    pass


if __name__ == '__main__':
    user_news_matrix, user_id = user_news_creator()
    nR, utm = user_topic_matrix(user_news_matrix)
    # nR is a mf matrix and utm is raw matrix

    # you can use utm or nR!
    utm = sparse.csr_matrix(utm)

    similarities = cosine_similarity(utm)

    similarities_sparse = cosine_similarity(utm, dense_output=False)
    print('pairwise sparse output:\n {}\n'.format(similarities_sparse))
