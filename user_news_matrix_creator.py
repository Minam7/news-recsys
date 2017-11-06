import random

# TODO space and last enter
def user_news_maker(user, news):
    file = open('user_news_matrix.txt', 'a+', encoding='utf-8')
    log = ''
    log += str(news) + '\n'
    for i in range(0, user):
        news_rank = [0] * news
        count = random.randint(0, news)
        for j in range(0, count):
            news_index = random.randint(0, news - 1)
            news_rank[news_index] = round(random.uniform(0, 100), 2)

        log += str(i) + ' '
        for k in news_rank:
            log += str(k) + ' '
        log += '\n'
    file.write(log)
    file.close()

if __name__ == "__main__":
    user_news_maker(5, 5)
