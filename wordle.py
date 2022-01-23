from traceback import print_tb
import pandas as pd
import numpy as np
import random
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    # warnings.warn("deprecated", DeprecationWarning)

class Wordle:
    def __init__(self):
        self.word = None
        self.player_words = []
        self.data = pd.read_csv('words_def.csv')
        self.ronda = 0
        self.total_words = len(self.data)
        self.win = False
        self.results = []
    

    def play(self):
        index = random.randint(0, self.total_words)
        self.word = self.data.iloc[index]['words']
        print(self.word)
        
        while self.ronda < 5 and self.win==False:
            self.player_round()
            self.check()
            self.ronda += 1

        if self.win == True:
            print("Has guanyaaaat!")
        else:
            print("Has perdut, eres un puto loser")
        self.play_again()
    
    def player_round(self):
        check = True
        while check:
            pal = input('Paraula {}: '.format(self.ronda+1))
            if len(pal) != 5 or pal not in self.data.values:
                print("Inserta una paraula vàlida!")
            else:
                check = False
        self.player_words.append(pal)

    def check(self):
        result = {}
        # print(self.player_words)
        if self.player_words[self.ronda] == self.word:
            self.win = True   
        else:
            i = 0
            for let in self.player_words[self.ronda]:
                pos = self.word.find(let)
                if pos == i:
                    result[let] = 2
                elif pos>=0 and pos!=i:
                    result[let] = 1
                else:
                    result[let] = 0
                i += 1
            print(result)
        self.results.append(result)


    def play_again(self):
        resp = input('Vols tornar a jugar (s/n): ')
        if resp.lower() == 's':
            self.win = False
            self.player_words = []
            self.ronda = 0
            self.play()
        else:
            print('Follen pringao')

class Wordle_Solver:
    def __init__(self):
        self.wordle = Wordle()
        self.data = pd.read_csv('words_def.csv')
        self.data_aux = self.data.copy()
        self.let_in = ''
        self.let_not_in = ''
        self.position = {}
        self.word_try = []

    def solve(self):
        index = random.randint(0, len(self.data))
        # self.wordle.word = self.wordle.data.iloc[index]['words']
        self.wordle.word = 'parel'
        print(self.wordle.word)
        while self.wordle.win == False and self.wordle.ronda < 6:
            self.chose_word()
            self.wordle.player_words = self.word_try
            self.wordle.check()
            print("Ronda {}: {}".format(self.wordle.ronda, self.word_try[self.wordle.ronda]))
            acc = self.wordle.results[self.wordle.ronda]
            print('Resultat: {}'.format(acc))
            i = 0
            for let in acc.keys():
                if acc[let] == 0:
                    self.let_not_in += let
                elif acc[let] == 1 or acc[let] == 2:
                    self.let_in += let
                if acc[let] == 2:
                    self.position[let] = i
                i += 1
            self.let_not_in = ''.join(set(self.let_not_in))
            self.let_in = ''.join(set(self.let_in))
            print(self.position)
            print(self.let_in)
            print(self.let_not_in)

            self.wordle.ronda += 1

        if self.wordle.win == True:
            print("Has guanyaaaat!")
        else:
            print("Has perdut, eres un puto loser")

    def chose_word(self):
        if self.wordle.ronda != 0:
            self.refresh_data()
            print(self.word_try)
            print(self.data_aux.iloc[0]['words'])
            # if self.data_aux.iloc[0]['words'] == self.word_try[self.wordle.ronda-1]:
            #     self.data_aux = self.data_aux.iloc[1: , :]

        print('Paraules restants: {}'.format(self.data_aux.shape[0]))
        self.word_try.append(self.data_aux.iloc[0]['words'])

    
    def refresh_data(self):
        if len(self.let_in) != 0:
            self.data_aux['cond'] = self.data_aux['words'].apply(lambda x: 0 not in [c in x for c in self.let_in])
            self.data_aux.drop(self.data_aux[self.data_aux['cond'] == False].index, inplace=True)
            print('='*10, '  let_in: ', self.wordle.ronda)
            print(self.wordle.word in self.data_aux['words'].values)

        if len(self.let_not_in) != 0:
            self.data_aux['cond'] = self.data_aux['words'].apply(lambda x: 1 not in [c in x for c in self.let_not_in])
            self.data_aux.drop(self.data_aux[self.data_aux['cond'] == False].index, inplace=True)
            print('='*10, '  let_not_in: ', self.wordle.ronda)
            print(self.wordle.word in self.data_aux['words'].values)

        if len(self.position.keys()) != 0:
            for let in list(self.position.keys()):
                pos = self.position
                for i in range(len(self.data_aux)):
                    # print(self.data_aux.loc[i]['words'])
                    self.data_aux.iloc[i]['cond'] = self.check_positions(self.data_aux.iloc[i]['words'], self.position, let)
                self.data_aux.drop(self.data_aux[self.data_aux['cond'] == False].index, inplace=True)
                print('='*10, '  dict: ', self.wordle.ronda)
                print(self.wordle.word in self.data_aux['words'].values)
                print(self.position)
        print(self.data_aux.head()) # [self.data_aux['words']==self.wordle.word]
        print(self.wordle.word in self.data_aux['words'].values)

    def check_positions(self, name, pos, let):
        pos_aux = pos
        a = True
        while a:
            if name.find(let) == pos_aux[let]:
                a = False
                return True
            else:
                pos_aux[let] -= name.find(let)+1
                name = name[name.find(let)+1:]
                if name.find(let) < 0:
                    a = False
                    return False


if __name__ == '__main__':
    wordle = Wordle_Solver()
    wordle.solve()
        