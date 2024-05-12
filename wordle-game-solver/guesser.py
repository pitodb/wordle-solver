import numpy as np
import pandas as pd
from collections import defaultdict, Counter
from itertools import chain
from random import choice
import yaml
from rich.console import Console
import csv


class Guesser:
    '''
        INSTRUCTIONS: This function should return your next guess. 
        Currently it picks a random word from wordlist and returns that.
        You will need to parse the output from Wordle:
        - If your guess contains that character in a different position, Wordle will return a '-' in that position.
        - If your guess does not contain thta character at all, Wordle will return a '+' in that position.
        - If you guesses the character placement correctly, Wordle will return the character. 

        You CANNOT just get the word from the Wordle class, obviously :)
    '''

    def __init__(self, manual):
        self.word_list_or = list(yaml.load(open('wordlist.yaml'), Loader=yaml.FullLoader))
        
        with open('totword_list.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            self.tot_list = [row[1] for row in csv_reader if row[1].isalpha()]

        self._manual = manual
        self.console = Console()

        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.vowels = 'aeiou'
        self.word_list = list(set(self.word_list_or.copy()))

        self.green_let = defaultdict(list)            # tupla con carattere e indice giusto
        self.yellow_let = defaultdict(list)           # tupla con carattere giusto ma INDICE SBAGLIATO
        self.grey_let = []                           # lista con lettere sbagliate

        self.guess = None
        self.list_guesses = []

        self.count = defaultdict(list)

        self.turno = 0
        self.entropie = {word: self.entropy(word) for word in self.word_list}

    def restart_game(self):
        self.word_list_or = list(yaml.load(open('wordlist.yaml'), Loader=yaml.FullLoader))
    
        self.console = Console()

        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.word_list = list(set(self.word_list_or.copy()))

        self.green_let = defaultdict(list)            # tupla con carattere e indice giusto
        self.yellow_let = defaultdict(list)           # tupla con carattere giusto ma INDICE SBAGLIATO
        self.grey_let = []                           # lista con lettere sbagliate

        self.guess = None
        self.list_guesses = []

        self.count = defaultdict(list)
        self.turno = 0


    def entropy(self,parola):
        # Compute the frequency of each character and the length of the string
        freqs = np.bincount(np.frombuffer(parola.encode(), dtype=np.uint8), minlength=256)
        n = len(parola)

        # Compute the probability of each character
        probs = freqs[freqs > 0] / n

        # Compute the entropy
        return -np.sum(probs * np.log2(probs))


    def update_lists(self, result):
        for ind, car in enumerate(result):
            if car == '-':
                self.yellow_let.setdefault(self.guess[ind], set()).add(ind)
            
            if car!='-' and car!='+':
                self.green_let.setdefault(car, set()).add(ind)

        for ind, car in enumerate(result):
            if car == '+':
                    if self.guess[ind] not in self.yellow_let and self.guess[ind] not in self.green_let:
                        self.grey_let.append(self.guess[ind])
    

    def update_counter(self, results):
        green_let_values = self.green_let.values()
        flat_list = [i for pos in green_let_values for i in pos]
        lung_green = len(flat_list)

        for let, pos in self.green_let.items():
            self.count[let] = [len(pos), 5 - lung_green + len(pos)]

        for ind, char in enumerate(results):
            guess_ind = self.guess[ind]
            
            if char == '-':
                if guess_ind in self.green_let:
                    self.count[guess_ind][0] += 1
                elif guess_ind not in self.count:
                    self.count[guess_ind] = [1, 5-lung_green]
            
            elif char == '+':
                if guess_ind in self.count:
                    self.count[guess_ind][1] = self.count[guess_ind][0]

    def update_words(self):
        words_copy_0 = self.word_list.copy()

        words_copy_0 = [word0 for word0 in self.word_list if all(self.count[let][0] <= Counter(word0)[let] <= self.count[let][1] for let in self.count.keys())]

        words_copy_1 = [word1 for word1 in words_copy_0 if not any(let_grey in word1 for let_grey in self.grey_let)]

        words_copy_2 = [word2 for word2 in words_copy_1 if all(word2[val] == key for key, vals in self.green_let.items() for val in vals)]

        words_copy_3 = [word3 for word3 in words_copy_2 if all((str(key) in word3) and (word3[val] != key) for key, vals in self.yellow_let.items() for val in vals)]

        self.word_list = words_copy_3.copy()

    def get_guess(self,result):
        '''
        This function must return your guess as a string. 
        '''
        if self._manual=='manual':
            return self.console.input('Your guess:\n')
        else: 

            if self.turno == 0:
                guess = 'arise'
                self.guess = guess
                self.turno+=1
                self.console.print(guess)
                self.list_guesses.append(guess)
                return guess

            else:
                
                try:

                    self.update_lists(result)
                    self.update_counter(result)
                    self.update_words()
                    
                    d = {word: entr for word,entr in self.entropie.items() if word in self.word_list}
                    lista_entr_bassa = [par for par,ent in d.items() if ent==max(d.values())]
                    guess = choice(lista_entr_bassa)

                    if guess not in self.list_guesses:
                        self.list_guesses.append(guess)
                        self.guess = guess
                        self.console.print(guess)
                        return guess

                    else:
                        guess = '+++++'

                        set_alpha = set(self.alphabet)
                        set_grey = set(self.grey_let)
                        set_possibili = set_alpha ^ set_grey

                        guess_l = list(guess)

                        for let,poss in self.green_let.items():
                            for pos in poss:
                                guess_l[pos] = let
                    
                        for pos,char in enumerate(guess_l):
                            if char == '+':
                                non_ci_sono = set([let for let in self.yellow_let.keys() if pos in self.yellow_let[let]])
                                potrebbero_esserci = set_possibili ^ non_ci_sono

                                condition = False
                                while not condition:
                                    guess_l[pos] = choice(list(potrebbero_esserci))
                                    guess = ''.join(guess_l)

                                    if guess not in self.list_guesses:
                                        self.list_guesses.append(guess)
                                        self.guess = guess
                                        condition = True
                                        self.console.print(guess)
                                        return guess
                    
                
                except:
                    self.word_list = self.tot_list.copy()
                    self.update_lists(result)
                    self.update_counter(result)
                    self.update_words()
                    self.entropie = {word: self.entropy(word) for word in self.word_list}
                    
                    #print('lunghezza lista:', len(self.word_list))

                    if len(self.word_list) <= 5000 and len(self.word_list)!=0:
                        
                        d = {word: entr for word,entr in self.entropie.items() if word in self.word_list}
                        lista_entr_bassa = [par for par,ent in d.items() if ent==max(d.values())]
                        guess = choice(lista_entr_bassa)

                        if guess not in self.list_guesses:
                            self.list_guesses.append(guess)
                            self.guess = guess
                            self.console.print(guess)
                            return guess

                        else:
                            guess = '+++++'

                            set_alpha = set(self.alphabet)
                            set_grey = set(self.grey_let)
                            set_possibili = set_alpha ^ set_grey

                            guess_l = list(guess)

                            for let,poss in self.green_let.items():
                                for pos in poss:
                                    guess_l[pos] = let
                        
                            for pos,char in enumerate(guess_l):
                                if char == '+':
                                    non_ci_sono = set([let for let in self.yellow_let.keys() if pos in self.yellow_let[let]])
                                    potrebbero_esserci = set_possibili ^ non_ci_sono

                                    condition = False
                                    while not condition:
                                        guess_l[pos] = choice(list(potrebbero_esserci))
                                        guess = ''.join(guess_l)

                                        if guess not in self.list_guesses:
                                            self.list_guesses.append(guess)
                                            self.guess = guess
                                            condition = True
                                            self.console.print(guess)
                                            return guess

                    else:
                        guess = '+++++'

                        set_alpha = set(self.alphabet)
                        set_grey = set(self.grey_let)
                        set_possibili = set_alpha ^ set_grey

                        guess_l = list(guess)

                        for let,poss in self.green_let.items():
                            for pos in poss:
                                guess_l[pos] = let
                    
                        condition = False
                        while not condition:
                            for pos,char in enumerate(guess_l):
                                if char == '+':
                                    non_ci_sono = set([let for let in self.yellow_let.keys() if pos in self.yellow_let[let]])
                                    potrebbero_esserci = set_possibili ^ non_ci_sono
                                    guess_l[pos] = choice(list(potrebbero_esserci))
                            
                            guess = ''.join(guess_l)
                            if guess not in self.list_guesses:
                                self.list_guesses.append(guess)
                                self.guess = guess
                                condition = True
                                self.console.print(guess)
                                return guess
                                            

                
            
    


        
