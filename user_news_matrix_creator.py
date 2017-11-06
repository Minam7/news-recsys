import random
import uuid


# TODO space and last enter
def user_news_maker(user, news):
    file = open('user_news_matrix.txt', 'w', encoding='utf-8')
    log = ''
    log += str(news) + '\n'
    for i in range(0, user):
        news_rank = [0] * news
        count = random.randint(0, news)
        for j in range(0, count):
            news_index = random.randint(0, news - 1)
            news_rank[news_index] = round(random.uniform(0, 100), 2)

        log += str(uuid.uuid4()) + ' '
        for k in range(len(news_rank)):
            log += str(news_rank[k])
            if k < len(news_rank) - 1:
                log += ' '
        if i < user - 1:
            log += '\n'
    file.write(log)
    file.close()


if __name__ == "__main__":
    user_news_maker(5, 5)
