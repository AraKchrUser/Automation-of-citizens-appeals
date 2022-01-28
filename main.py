import deeppavlov

BOT = 1
OPERATOR = 2
VIOLATION = 3
CONST = 0.5


def greeting():
    print('Привет, чем я могу помочь?')
    print('Вы можете выбрать разговор со мной, с оператором или хочешь оставить заявку о нарушении?')
    answer = input()

    if int(answer) == BOT:
        return BOT
    elif int(answer) == OPERATOR:
        return OPERATOR
    else:
        return VIOLATION


def record():
    # Запись о нарушении
    pass


def faq(question):
    return question


def odqa_document():
    pass


def ner(question):
    return question


def sql_query_to_base():
    pass


if __name__ == '__main__':

    answer = greeting()
    if answer == VIOLATION:
        record()
    elif answer == OPERATOR:
        dialog = False
    else:
        dialog = True

    if dialog:
        question = input()
        answer, threshold = faq(question)
        if threshold > CONST:
            print(answer)
        elif 'I-FAC' in ner(question):
            sql_query_to_base()
        else:
            odqa_document()




