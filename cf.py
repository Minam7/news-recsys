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
def user_topic_creator(norm):
    if norm:
        file = open('files/user_topic_matrix_normal.txt', 'r')
    else:
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


def user_news_topic_creator():
    user_topic = user_topic_creator(False)
    user_count = len(user_topic)
    news_topic = news_topic_creator()
    news_count = len(news_topic)
    un_topic = list(user_topic)
    un_topic.extend(news_topic)

    return un_topic, news_count, user_count


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

    file = open('files/user_topic_matrix_normal.txt', 'w')
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

    file = open('files/user_topic_matrix.txt', 'w')
    log = ''
    for j in range(len(user_topic_matris)):
        item = user_topic_matris[j]
        for i in range(len(item)):
            log += str(item[i])
            if i < len(item) - 1:
                log += ' '
        if j < len(user_topic_matris) - 1:
            log += '\n'
    file.write(log)
    file.close()

    return nR, user_topic_matris


def user_recommendation(user_cookie):
    user_news_matrix, user_id = user_news_creator()
    user = user_id[user_cookie]
    print("For user with user id : {} and user cookie : {}".format(user, user_cookie))
    nR, utm = user_topic_matrix(user_news_matrix)
    # nR is a mf matrix and utm is raw matrix

    # you can use utm or nR!
    # utm = sparse.csr_matrix(utm)

    unt, n_count, u_count = user_news_topic_creator()

    unt = sparse.csr_matrix(unt)
    similarities_sparse = cosine_similarity(unt, dense_output=False)

    simi_list = list()
    for i in range(0, n_count + u_count):
        if i == user:
            simi_list.append(0)
        else:
            ss = similarities_sparse[user, i]
            simi_list.append(ss)

    u_f = False
    n_f = False
    while not u_f or not n_f:
        rec = max(simi_list)
        indx = simi_list.index(rec)

        if indx >= u_count and not n_f:
            print("Recommended news : ", str(indx - u_count))
            n_f = True
            simi_list[indx] = -1
        if indx < u_count and not u_f:
            print("Recommended user : ", str(indx))
            u_f = True
            simi_list[indx] = -1
        else:
            simi_list[indx] = -1


def news_recommendation(news_id):
    print("For news with news id : {}".format(news_id))
    unt, n_count, u_count = user_news_topic_creator()
    print(n_count, u_count)
    unt = sparse.csr_matrix(unt)
    similarities_sparse = cosine_similarity(unt, dense_output=False)
    print(similarities_sparse)
    simi_list = list()
    for i in range(n_count + u_count):
        if i == news_id + u_count:
            simi_list.append(0)
        else:
            ss = similarities_sparse[news_id + u_count, i]
            simi_list.append(ss)

    print(simi_list)

    u_f = False
    n_f = False
    while not u_f or not n_f:
        rec = max(simi_list)
        indx = simi_list.index(rec)

        if indx < u_count and not u_f:
            print("Recommended user : ", str(indx))
            u_f = True
            simi_list[indx] = -1

        if indx >= u_count and not n_f:
            print("Recommended news : ", str(indx - u_count))
            n_f = True
            simi_list[indx] = -1

        else:
            simi_list[indx] = -1


if __name__ == '__main__':
    user_recommendation('95fba71f-54da-4dae-9125-44e4390b5480')
    news_recommendation(0)
