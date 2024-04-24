import json
import pickle # Библиотека которая сохраняет обученные связи
import asyncio
from sklearn.feature_extraction.text import CountVectorizer # Векторизация слов, т.е. перевод в цифры вроде
from sklearn.neural_network import MLPClassifier # Машинное обучение библиотека

    # Функция для обучения модели
async def training_model():
    with open("./training_data/dataset.json", 'r') as f:
        data = json.load(f)
        x = []
        y = []
        for intent_name in data:
            for example in data[intent_name]['exemples']:
                x.append(example)
                y.append(intent_name)
            for response in data[intent_name]['responses']:
                x.append(response)
                y.append(intent_name)

            # Создание и обучение векторизатора
        vectorizer = CountVectorizer()
        x_vec = vectorizer.fit_transform(x)

            # Создание модели MLPClassifier с увеличенным количеством итераций, # Увеличение значения alpha усиливает L2 регуляризацию
        model = MLPClassifier(max_iter=1000, alpha=0.01) # Создаем модель
        model.fit(x_vec, y) # Обучаем модель

        print(f"Качество натренированной модели:{model.score(x_vec, y)}") # Качество на тренировочной выборке = accuracy / больше = лучше

            # Сохранение обученного векторизатора и модели
        with open("./training_model/vectorizer.pkl", 'wb') as f_vec:
            pickle.dump(vectorizer, f_vec)
        with open("./training_model/model.pkl", 'wb') as f_model:
            pickle.dump(model, f_model)



if __name__ == "__main__":
    asyncio.run(training_model())




















# import torch






# # Функция для создания эмбеддингов с помощью BERT
# def create_bert_embeddings(sentences, tokenizer, model):
#     inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")
#     outputs = model(**inputs)
#     # Используем [CLS] токен для представления всего предложения
#     embeddings = outputs.last_hidden_state[:, 0, :].detach().numpy()
#     return embeddings

# async def training_model():
#     # Загрузка данных
#     with open("./training_data/dataset.json", 'r') as f:
#         data = json.load(f)

#     # Инициализация токенизатора и модели BERT
#     tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
#     model = BertModel.from_pretrained('bert-base-uncased')

#     x = []
#     y = []
#     for intent_name in data:
#         for example in data[intent_name]['exemples']:
#             x.append(example)
#             y.append(intent_name)
#         for response in data[intent_name]['responses']:
#             x.append(response)
#             y.append(intent_name)

#     # Создание эмбеддингов для всех текстов
#     x_embeddings = create_bert_embeddings(x, tokenizer, model)

#     # Создание и обучение классификатора
#     classifier = MLPClassifier()#max_iter=1000, alpha=0.01)
#     classifier.fit(x_embeddings, y)

#     print(f"Качество натренированной модели: {classifier.score(x_embeddings, y)}")

#     # Сохранение обученного классификатора
#     with open("./training_model/classifier.pkl", 'wb') as f_model:
#         pickle.dump(classifier, f_model)

#     # Сохранение токенизатора и модели BERT не требуется, так как они могут быть загружены напрямую из Hugging Face

# if __name__ == "__main__":
#     asyncio.run(training_model())