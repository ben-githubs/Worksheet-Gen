import logging
from pathlib import Path
import random
from wsgen import Problem

#arranging_letters = Problem('Arranging Letters', Path('templates/problems/arranging_letters.tex'))

# How many unique arrangements can be made using a set if letters with repeated members?
class ArrangingLetters(Problem):
    def setup(self):
        word_list = 'celebration letter ingenious balloon racecar winnipeg hannah mississippi'.split()
        word = random.choice(word_list)
        wrong_ans = len(word)
        # Count occurances of each letter
        occur = dict()
        for letter in word:
            if letter in occur:
                occur[letter] += 1
            else:
                occur[letter] = 1
        multiples = [occur[x] for x in occur.keys() if occur[x] > 1]
        self.vars = {
            'word': word,
            'wrong_ans': wrong_ans,
            'multiples': multiples
        }
        logging.debug('If this is running, inheritance works!')

# Identifying which terms in a binomial expansion have a particular power of x.
class BinomialExpansionSolveN(Problem):
    def setup(self):
        # Binomial expansion is of form (Ax^B + Cx^D)^n
        A = random.randint(2, 9) * random.choice([-1, 1])
        B = random.randint(2, 5)
        C = random.randint(2, 9) * random.choice([-1, 1])
        D = random.randint(2, 5)
        n = random.randint(3, 16)

        # We are asking student to find an arbitrary term
        term = random.randint(2, n)

        # The power of 'x' in the chosen term is determined here
        term_exponent = B*(n-term+1) + D*(term-1)

        self.vars = {
            'A': A,
            'B': B,
            'C': C,
            'D': D,
            'n': n,
            'term': term,
            'term_exponent': term_exponent
        }