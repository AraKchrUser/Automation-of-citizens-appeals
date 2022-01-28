import deeppavlov

BOT = 1
OPERATOR = 2
VIOLATION = 3
CONST = 0.5


def greeting():
    print('Привет, чем я могу помочь?')
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
    https://
    """
    return question


def odqa_document():
    """
    Функция хранит модель, которая позволяет ответить
    на вопрос пользователя (ответ находится в документе)
    ссылка на реализацию:
    https://
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
        answer, threshold = faq(question)
        if threshold > CONST:  # Проверяем уверенность нейронной сети
            print(answer)  # Проверяем ответ и переходим в соответсвующее состояние
            if 'I-FAC' in ner(question):  # Выполняем соответсвующее дейсвтие
                sql_query_to_base()
            #    ...
        else:
            odqa_document()




