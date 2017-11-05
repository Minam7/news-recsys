import lda


def user_news_creator():
    file = open('user_news_matrix.txt', 'r')
    user_news_file = file.read().split('\n')
    news = int(user_news_file[0])

    user_news = dict()
    for i in range(1, len(user_news_file)):
        data = user_news_file[i].split(' ')
        user_news[data[0]] = data[1:news]

    return user_news


# read from written file
def news_topic_creator():
    file = open('news_topic_matrix.txt', 'r')
    news_topic_file = file.read().split('\n')
    news_topic = dict()
    for i in range(len(news_topic_file)):
        news_topic[i] = news_topic_file[i].split(' ')

    return news_topic


def add_new_doc_to_news_topic(doc_name):
    # update all news_topic
    file = open('news_topic_matrix.txt', 'a+')
    news_topic = lda.news_topic_creator('news2')
    log = ''
    for item in news_topic:
        log += str(item) + ' '
    file.write(log)
    file.close()


if __name__ == '__main__':
    # TODO make file
    # user_news_matrix = user_news_creator()
    news_topic_matrix = news_topic_creator()
    print(news_topic_matrix)
