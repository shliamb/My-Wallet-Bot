import pickle # Библиотека которая сохраняет обученные связи
import asyncio


async def get_category(in_text_category):
        # Загрузка обученного векторизатора
    with open("./training_model/vectorizer.pkl", 'rb') as f_vec:
        vectorizer = pickle.load(f_vec)
        # Загрузка обученной модели
    with open("./training_model/model.pkl", 'rb') as f_model:
        model = pickle.load(f_model)

        # Определение функций get_intent
    def get_intent(text):
        text_vec = vectorizer.transform([text])
        return model.predict(text_vec)[0]

    intent = get_intent(in_text_category.lower()) # Все введенное в боте будет маленькими буквами
    return intent


if __name__ == "__main__":
    asyncio.run(get_category())



























# import torch



# # Загрузка предобученной модели и токенизатора BERT
# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# model = BertModel.from_pretrained('bert-base-uncased')

# # Функция для создания эмбеддингов с помощью BERT
# def create_bert_embedding(text, tokenizer, model):
#     inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
#     outputs = model(**inputs)
#     # Используем [CLS] токен для представления всего предложения
#     embedding = outputs.last_hidden_state[:, 0, :].detach().numpy()
#     return embedding

# async def get_category(in_text_category):
#     # Загрузка обученной модели
#     with open("./training_model/model.pkl", 'rb') as f_model:
#         classifier = pickle.load(f_model)

#     # Получение эмбеддинга для входного текста
#     text_embedding = create_bert_embedding(in_text_category, tokenizer, model)

#     # Предсказание категории
#     category = classifier.predict(text_embedding)[0]
#     return category

# if __name__ == "__main__":
#     # Пример использования
#     category = asyncio.run(get_category("Пример текста для категоризации"))
#     print(f"Категория: {category}")
