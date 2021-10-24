"""Константы, необходимые для работы приложения."""

QUESTION_TYPE_TEXT = 'text'
QUESTION_TYPE_SINGLE = 'single'
QUESTION_TYPE_MULTIPLE = 'multiple'
QUESTION_TYPE = (
    (QUESTION_TYPE_TEXT, 'Ответ текстом'),
    (QUESTION_TYPE_SINGLE, 'Ответ с выбором одного варианта'),
    (QUESTION_TYPE_MULTIPLE, 'Ответ с выбором нескольких вариантов'),
)
