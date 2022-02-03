import numpy as np

import deeppavlov
from deeppavlov import configs
from deeppavlov.core.common.file import read_json
from deeppavlov.core.commands.infer import build_model
from deeppavlov import configs, train_model

text = ''' В этом году в Благовещенске участвуют в программе более 100 дворов. 12.24.2021 завершаются ремонтные 
работы на улице Ленина 165. Академический театр драмы обновляется в соответствии с решением губернатора. Также 
13.34.2035 начинаются работы на Богдана-Хмельницкого 156, построят 153 ловочек, 8 тренажеров.'''

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


def faq_func(question):
    state, score = faq(question)
    return state[0], not all(np.array(score[0]) < 0.5)


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
