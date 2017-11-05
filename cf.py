import lda


if __name__ == '__main__':
    '''
    file = open('user_news.txt', 'r', encoding='utf-8')
    user_news_file = file.read().split('\n')
    news = int(user_news_file[0])

    user_news = dict()
    for i in range(1, len(user_news_file)):
        data = user_news_file[i].split(' ')
        user_news[data[0]] = data[1:news]
    '''
    # TODO make file
    news_topic = lda.news_topic_creator('news2')
    print(news_topic)