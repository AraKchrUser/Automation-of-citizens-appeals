import numpy as np

import deeppavlov
from deeppavlov import configs
from deeppavlov.core.common.file import read_json
from deeppavlov.core.commands.infer import build_model
from deeppavlov import configs, train_model

tkn_split = '>>>>>>>>>>>>'
text = ''' 
В 2022 года начата реализация программы “1000 дворов” в Амурской области. В течении года 
будет реализовано порядка 100 современных дворовых территорий. Все работы по созданию дворовых территорий будут 
завершены не позднее 30.11.2022 г. 
>>>>>>>>>>>>
Города которые участвуют в программе: Благовещенск, Белогорск, Тында, Циолковский, 
Шимановск, Райчихинск, Зея, Свободный.
>>>>>>>>>>>>
В Зее будет реализовано 5 дворовых территорий, это - мкр. Светлый, 6; мкр. Светлый, 61; мкр. Солнечный, 13,15; 
мкр. Светлый, 72, 73; пер. Школьный, 110-112.
>>>>>>>>>>>>
В Светлый, 6 будет установлено 10 лавочек, 5 качелей, 1 детский игровой комплекс, 3 карусели, 123 квадратных 
метра плитки, 44 метра леерного ограждения. На пер. Школьный, 110-112 будет установлено 8 лавочек, 6 качелей, 2 детских игровых комплексов, 
1 карусель, 144 квадратных метра плитки, 67 метра леерного ограждения.
>>>>>>>>>>>>
В Благовещенске будет реализовано 55 дворовых территорий.
В Циолковском будет реализовано 2 дворовые территории.
В Тынде 7 дворовых территорий.
В Райчихинске будет реализовано 4 дворовые территории.
В Белогорске будет реализовано 6 дворовые территории.
В Свободном будет реализовано 21 дворовая территория.
В Шимановске будет реализовано 4 дворовые территории.
>>>>>>>>>>>>
ул.Театральная, д.35/1
ул.Трудовая, д.27, ул.Амурская, д.114
л.Загородная, д. 48, ул.Красноармейская, д.194
ул.Чайковского,д.211
 ул.Чайковского, д.110
ул.Чайковского, 47
ул.Амурская, д.208
ул.Калинина,д.76 , ул.Калинина, 76/2
ул.Ленина, д.12/2, ул.Ленина, д.14/2
ул.Строителей,д.79/3
 п.Моховая падь, ДОС-18
ул.50 лет Октября, д.203, ул.50 лет Октября, д,203/1, ул. Кольцевая,42А, ул. Островского, 236
ул.Ленина, д.171, ул.Б.Хмельницкого,д.6
п.Моховая падь, Литер- 25
 ул.Амурская,д.112
ул. Пионерская, 147, ул. 50 лет Октября 140, 142, 144
ул.Шевченко, 109
ул. Муравьева Амурского, 24, ул.Трудовая, 268
ул.Театральная,31, ул.Зейская,88
ул. Ленина,42
ул. Студенческая, 34/9
ул.Чайковского, 33
ул. Студенческая, 28
ул.Пионерская, 112/2
ул. Игнатьевское шоссе, 14, 14/1, 14/2, 14/4
ул.Горького,д. 97/1
ул. Игнатьевское шоссе, 3, 3/1
ул.Пушкина, д.3/ Краснофлотская д.53
ул. Ленина 235
ул. Политехническая 88
ул. Пограничная 124, 124/3
пер. Св.Иннокентия 19
ул. Дьяченко 2А,2В,2Г
ул. Игнатьевское шоссе 12/6
ул. Забурхановская 93, 93/1
ул. Шевченко 44
ул. Институтская 17, 17/1
п. Мясокомбинат, Литер 1
ул. Красноармейская, 198
ул.Зейская,256
ул. 50 лет Октября, 197; ул. 50 лет Октября, 199;
ул. Институтская, 11
ул. Горького, 150
ул. Пушкина, 199/1
ул. Институтская 14
ул. Театральная, 94
ул. Чайковского, 64 
ул.Политехническая,48
ул.Горького,64
ул. Партизанская, 22/2
'''

model_ru = build_model(configs.squad.squad_ru_rubert, download=True)
ner_model = build_model(configs.ner.ner_ontonotes_bert_mult, download=True)
model_config = read_json(configs.faq.tfidf_logreg_autofaq)
model_config['dataset_reader']['data_path'] = 'faq.csv'
model_config['dataset_reader']['data_url'] = None
faq = train_model(model_config)


def process(question, token_first='B-FAC', token_last='I-FAC', replace='улица N'):
    answer = ner_model([question])

    first = 0
    l = 0
    entity = list()

    for i, v in zip(range(1, len(answer[1][0]) + 1), answer[1][0]):

        if v == token_first:
            if l != 0:
                entity.append(answer[0][0][first - 1: first + l])
                question = question.replace(' '.join(answer[0][0][first - 1: first + l]), replace)
            first = i
            l = 0
        elif v == token_last:
            l += 1

        if i == len(answer[1][0]) and first:
            entity.append(answer[0][0][first - 1: first + l])
            question = question.replace(' '.join(answer[0][0][first - 1: first + l]), replace)

    return entity, question


def greeting():
    print('/start')
    print('Привет, чем я могу помочь?')


# def faq_func(question):
#     state, score = faq(question)
#     return state[0], not all(np.array(score[0]) < 0.5)


def odqa_document(question):
    return model_ru([text], [question])[0][0]


def ner_func(question):
    ent1, qu = process(question, token_first='B-FAC', token_last='I-FAC', replace='улица N')
    ent2, qu = process(qu, 'B-GPE', 'I-GPE', ' ')
    if ent1:
        ent1[0][0] = 'улица'
    if ent2:
        ent2[0].insert(0, 'город')
    return qu, ent1 + ent2


def sql_query_to_base():
    pass


def main():
    greeting()

    dialog = True

    # Будем создавать словарь с параметрами для хранения контекста
    context = {}
    while dialog:
        question = input()

        if question == '/stop':
            return

        raw_question, entity = ner_func(question)
        if entity:
            for i in entity:
                context[i[0]] = ' '.join(i)

        print(raw_question)

        # state, threshold = faq_func(raw_question)
        state, threshold = faq([question])

        state = state[0]
        threshold = not all(np.array(threshold[0]) < 0.5)

        print(state, threshold)

        if threshold:

            if state == 'state1':
                # odqa_document(raw_question.replace('N', context['город']))
                if ''.join(context['улица'].split()[1:]) in ''.join(
                        process(text, token_first='B-FAC', token_last='I-FAC', replace='улица N')[0][0]):
                    print('Участвует')
                else:
                    print('Не участвует')
            elif state == 'state2':
                print(odqa_document(question))  # Выполняем предопределнный запрос
            elif state == 'state3':
                print(odqa_document(question))
            elif state == 'state4':
                print(odqa_document(question))
        else:
            # Иначе пытаемся найти вопрос в документах
            print(odqa_document(question))


main()
