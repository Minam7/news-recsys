from __future__ import unicode_literals

import gensim
from hazm import *


def matrix_builder(doc_name):
    name = 'docs/' + doc_name
    file = open(name, 'r', encoding='utf-8')
    content = file.read()
    normalizer = Normalizer()
    content = normalizer.normalize(content)
    sentences = sent_tokenize(content)

    tagger = POSTagger(model='resources/postagger.model')
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


def lda_learner(doc_num):
    docs_words = []

    for i in range(1, doc_num):
        docs_words.append(matrix_builder('news' + str(i)))

    dictionary = gensim.corpora.Dictionary(docs_words)
    dictionary.save('files/lda_dictionary.dict')

    corpus = [dictionary.doc2bow(text) for text in docs_words]

    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=100, id2word=dictionary, passes=50)
    ldamodel.save('files/lda.model')


def news_topic_creator(doc_name):
    ldamodel = gensim.models.LdaModel.load('files/lda.model')
    dictionary = gensim.corpora.Dictionary.load('files/lda_dictionary.dict')
    corpus = dictionary.doc2bow(matrix_builder(doc_name))

    topics = [0 for x in range(100)]
    lda_topics = ldamodel.get_document_topics(corpus)
    for item in lda_topics:
        topics[item[0]] = item[1]

    return topics


if __name__ == '__main__':
    lda_learner(21)
