import lda


def make_string(listed):
    log = ''
    for i in range(len(listed)):
        log += str(listed[i])
        if i < len(listed) - 1:
            log += ' '
    return log


# write news_topic to news_topic_matrix
def news_topic_file_writer(start_index, end_index):
    file = open('files/news_topic_matrix.txt', 'w')
    log = ''
    for i in range(start_index + 1, end_index + 1):
        name = 'news' + str(i)
        news_topic = lda.news_topic_creator(name)
        log += make_string(news_topic)
        if i < end_index:
            log += '\n'

    file.write(log)
    file.close()


if __name__ == '__main__':
    news_topic_file_writer(0, 21)
