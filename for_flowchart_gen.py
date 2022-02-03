answer = greeting()
if answer == VIOLATION:
    record()
    dialog = False
elif answer == OPERATOR:
    dialog = False
else:
    dialog = True

context = {}
while dialog:
    question = input()
    raw_question, entity = ner(question)
    answer_state, threshold = faq(raw_question)

    if threshold > CONST:
        state = answer_state

        if state == '1.1' or state == '1.2':
            print('answer')
        elif state == '2.1':
            if not context and entity or context and entity:
                context['loc'] = entity
            print(sql_query_to_base(context['loc']))
        #    ... и так далее с остальными
    else:
        odqa_document(question)
