class User():
    def __init__(self, DATA) -> None:
        self.user_id, self.first_name, self.last_name, \
            self.status, self.rating, self.student_group = DATA

class Test():
    def __init__(self) -> None:
        self.name = None
        self.questions = []
    
    def add_question(self, question):
        self.questions.append(question)

class Question():
    def __init__(self) -> None:
        self.content = None
        self.type = None
        self.price = None
        self.answers = []
    
    def add_answer(self, answer):
        self.answers.append(answer)

class Answer():
    def __init__(self) -> None:
        self.content = None
        self.correctness = None

class Article():
    def __init__(self) -> None:
        self.name = None
        self.link = None