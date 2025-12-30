import time

class WordBuilder:
    def __init__(self):
        self.word = ""
        self.last_letter = ""
        self.last_time = time.time()

    def update(self, letter, fingers):
        now = time.time()

        if letter:
            if letter == self.last_letter:
                if now - self.last_time > 1.5:
                    self.word += letter
                    self.last_time = now
            else:
                self.last_letter = letter
                self.last_time = now

        # fist = space
        if fingers == [0,0,0,0,0]:
            if not self.word.endswith(" "):
                self.word += " "

        return self.word
