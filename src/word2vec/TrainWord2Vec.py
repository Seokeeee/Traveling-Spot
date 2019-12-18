from gensim.models import word2vec
import logging

f = open('data/sentences_korquad_spot.txt', 'r', encoding='UTF-8')
sentences = []
lines = f.readlines()
for i in range(len(lines)):
  lines[i] = lines[i].split()
  sentences.append(lines[i])

# 하이퍼 파라미터
num_features = 300    # 워드 백터 특정값 수
min_word_count = 2    # 단어에 대한 최소 빈도 수
num_workers = 4       # 프로세스 개수
context = 10          # 컨텍스트 윈도우 크기
downsampling = 1e-3   # 다운 샘플링 비율
iteration = 5         # 에폭
skip_gram = 1         # skip_gram 사용 여부

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

print("Training model...")

model = word2vec.Word2Vec(sentences,
                          workers=num_workers,
                          size=num_features,
                          min_count=min_word_count,
                          window=context,
                          sample=downsampling,
                          iter=iteration,
                          sg=skip_gram
                          )
model.init_sims(replace=True)

print("Training finish")

model.save('model/Word2vec_iter5.model')

