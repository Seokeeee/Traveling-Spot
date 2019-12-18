from gensim.models import Word2Vec

model = Word2Vec.load('model/Word2vec_iter5.model')

k1 = '가이드'; k2 = '투어'
print('2: ', model.wv.similarity(k1, k2))

k3 = ['쇼핑']
print('3: ', model.wv.most_similar(positive=k3, topn=20))
