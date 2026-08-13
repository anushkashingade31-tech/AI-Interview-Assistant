QUESTION_BANK = {

    "C": [
        "What is a pointer in C?",
        "What is the difference between malloc() and calloc()?",
        "What are storage classes in C?",
        "Explain structures and unions.",
        "What is a segmentation fault?"
    ],

    "Python": [
        "What are Python decorators?",
        "Explain List and Tuple.",
        "What is OOP in Python?"
    ],

    "Java": [
        "What is JVM?",
        "What is Method Overloading?",
        "What are Interfaces?"
    ],

    "HTML": [
        "What is Semantic HTML?",
        "Difference between id and class?"
    ],

    "CSS": [
        "What is Flexbox?",
        "What is CSS Grid?"
    ],

    "MySQL": [
        "What is Primary Key?",
        "What is Foreign Key?",
        "Explain JOIN."
    ]
}
import random

def generate_questions(skills):

    questions = []

    for skill in skills:

        if skill in QUESTION_BANK:

            questions.extend(
                random.sample(
                    QUESTION_BANK[skill],
                    min(2,len(QUESTION_BANK[skill]))
                )
            )

    return questions