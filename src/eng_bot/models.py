class User():
    def __init__(self, DATA) -> None:
        self.user_id, self.first_name, self.last_name, \
            self.status, self.rating, self.student_group = DATA.values()

class Test():
    def __init__(self, name=None) -> None:
        self.name = name
        self.questions : list(Question) = []
    
    def add_question(self, question):
        self.questions.append(question)

class Question():
    def __init__(self, content=None, type=None, price=None) -> None:
        self.content = content
        self.type = type
        self.price = price
        self.answers : list(Answer) = []
    
    def add_answer(self, answer):
        self.answers.append(answer)

class Answer():
    def __init__(self, content=None, correctness=None) -> None:
        self.content = content
        self.correctness = correctness

class Article():
    def __init__(self) -> None:
        self.name = None
        self.link = None