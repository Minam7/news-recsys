from __future__ import unicode_literals

import gensim
import time

from hazm import *


def matrix_builder(doc_name):
    name = 'docs/' + doc_name
    file = open(name, 'r', encoding='utf-8')
    content = file.read()
    normalizer = Normalizer()
    content = normalizer.normalize(content)
    sentences = sent_tokenize(content)

    tagger = POSTagger(model='resources/postagger.model')
    chars = open('chars', 'r', encoding='utf-8').read().split('\n')
    stop_words = open('stopwords-fa.txt', 'r', encoding='utf-8').read().split('\n')

    words = []
    for s in sentences:
        '''
        for word in s.split(' '):
            tmp_word = word
            for i in range(len(word)):
                if word[i] in chars:
                    tmp_word = tmp_word.replace(word[i], '')
            s = s.replace(word, tmp_word)
        '''
        tagged = list(tagger.tag(word_tokenize(s)))
        new_tag = list(tagged)

        for token in tagged:
            if token[0] in stop_words:
                new_tag.remove(token)
        lemmatizer = Lemmatizer()
        for token in new_tag:
            stemmed = lemmatizer.lemmatize(token[0], pos=token[1])
            stemmer = Stemmer()
            stemmed = stemmer.stem(stemmed)
            if len(stemmed) > 0 and ('#' not in stemmed):
                words.append(stemmed)

    return words


if __name__ == '__main__':
    docs_words = []
    start_time = time.time()

    for i in range(1, 6):
        docs_words.append(matrix_builder('news' + str(i)))

    # print('run time: %s s' % (time.time() - start_time))
    dictionary = gensim.corpora.Dictionary(docs_words)

    corpus = [dictionary.doc2bow(text) for text in docs_words]
    # print('run time: %s s' % (time.time() - start_time))

    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=50)

    # print('run time: %s s' % (time.time() - start_time))

    print(ldamodel.print_topics(num_topics=4, num_words=4))
    print('run time: %s s' % (time.time() - start_time))
