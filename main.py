import deeppavlov

BOT = 1
OPERATOR = 2
VIOLATION = 3
CONST = 0.5


def greeting():
    print('Привет, разговоры прослушиваются, чем я могу помочь?')
    print('Вы можете выбрать разговор со мной, с оператором или хочешь оставить заявку о нарушении?')
    answer = input()

    return int(answer)


def record():
    # Запись о нарушении
    pass


def faq(question):
    """
    Функция является по факту детектором намерений пользователя:
    Обрабатывается входящий вопрос от пользователя и выбирается некоторое действие
    на основе определнных шаблонов
    Ссылка на реализацию:
    https://https://medium.com/deeppavlov/simple-intent-recognition-and-question-answering-with-deeppavlov-c54ccf5339a9
    """
    return question


def odqa_document():
    """
    Функция хранит модель, которая позволяет ответить
    на вопрос пользователя (ответ находится в документе)
    ссылка на реализацию:
    https://https://medium.com/deeppavlov/open-domain-question-answering-with-deeppavlov-c665d2ee4d65
    """
    pass


def ner(question):
    """
    Функция извлекает улицу, номер дома и т.д.
    и отбрасывает ее, оставляя суть вопроса для
    дальнейшей классификации намерений (faq)
    Реализация: кому как удобно - deeppavlov, natasha ...
    """
    return question


def sql_query_to_base():
    """
    Функция, вызывается при активации соответсвующего шаблона
    в нее передаются сущности предметной области для выполнения запроса к БД
    (пример: какие дворы участвуют в программе?)
    """
    pass


if __name__ == '__main__':

    answer = greeting()
    if answer == VIOLATION:
        record()
    elif answer == OPERATOR:
        dialog = False
    else:
        dialog = True

    # Будем создавать словарь с параметрами для хранения контекста
    context = {}
    while dialog:
        question = input()

        '''
        Допустим, мы определили, что сущетсвует N типов вопросов:
        -1.. {общая информация, на которые есть готовые ответы}: 1.1. как проходит отбор, 1.2. информация о программе (тут может быть несколько состояний)
        -2.. {предопределнные вопросы, на которые существуют готовые SQL-запросы}: 2.1. какие дворы участвуют в программе (тут может быть несколько состояний)
        -3 участвет ли двор N в программе
        -4 когда закончится обустройство во дворе N
        -5 сколько лавочек во дворе N         
        '''

        raw_question, entity = ner(question)
        answer_state, threshold = faq(raw_question)
        if threshold > CONST:  # Проверяем уверенность нейронной сети
            state = answer_state  # Проверяем ответ и переходим в соответсвующее состояние
            # Выполняем соответсвующее действие

            if state == '1.1' or state == '1.2':
                print('answer')
            elif state == '2.1':
                if not context and entity or context and entity:  # Если передали новую локацию - меняем контекст
                    context['loc'] = entity
                print(sql_query_to_base(context['loc']))  # Выполняем предопределнный запрос
            #    ... и так далее с остальными
        else:
            # Иначе пытаемся найти вопрос в документах
            odqa_document(question)




