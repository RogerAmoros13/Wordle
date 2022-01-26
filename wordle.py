import matplotlib as mpl
import pandas as pd
import numpy as np
import random
import warnings
import matplotlib.animation as animation
import matplotlib.pyplot as plt
# mpl.rcParams['animation.ffmpeg_path'] = r'C:\\Users\\xx\\Desktop\\ffmpeg\\bin\\ffmpeg.exe'
# import seaborn as sns
# %matplotlib qt

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    # warnings.warn("deprecated", DeprecationWarning)

class Wordle:
    def __init__(self):
        self.word = None
        self.player_words = []
        self.data_aux = pd.read_csv('words_def.csv')
        self.data = self.data_aux.copy()
        self.ronda = 0
        self.total_words = len(self.data)
        self.win = False
        self.results = {}
    

    def play(self):
        index = random.randint(0, self.total_words)
        
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
        result = []
        # print(self.player_words)
        if self.player_words[self.ronda] == self.word:
            self.win = True
        else:
            i = 0
            for let in self.player_words[self.ronda]:
                pos = self.word.find(let)
                if pos < 0:
                    result.append([let, 0])
                else:
                    if let == self.word[i]:
                        result.append([let, 2])
                    else:
                        result.append([let, 1])
                i += 1
        self.results[self.ronda] = result

    def play_again_test(self):
        self.win = False
        # self.word = 'None'
        self.player_words = []
        self.ronda = 0
        self.results = {}
        # self.play()

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
        self.position = []

    def solve(self, n):
        self.data_aux = self.data.copy()
        self.word_try = []
        self.position = []
        self.let_in = ''
        self.let_not_in = ''
        # index = random.randint(0, len(self.data))
        self.wordle.word = self.wordle.data.iloc[n]['words']
        while self.wordle.ronda < 6:
            self.chose_word()
            self.wordle.player_words = self.word_try
            self.wordle.check()
            if self.wordle.win == True:
                break
            # print("Ronda {}: {}".format(self.wordle.ronda, self.word_try[self.wordle.ronda]))
            acc = self.wordle.results[self.wordle.ronda]
            # print('Resultat: {}'.format(acc))
            i = 0
            for i in range(5):
                if acc[i][1] == 0:
                    self.let_not_in += acc[i][0]
                elif acc[i][0] == 1 or acc[i][1] == 2:
                    self.let_in += acc[i][0]
                if acc[i][1] == 2:
                    self.position.append([acc[i][0], i])
                i += 1
            self.let_not_in = ''.join(set(self.let_not_in))
            self.let_in = ''.join(set(self.let_in))
            self.wordle.ronda += 1

        # if self.wordle.win == True:
        #     print("Has guanyaaaat!")
        # else:
        #     print("Has perdut, eres un puto loser")

    def chose_word(self):
        if self.wordle.ronda != 0:
            self.refresh_data()
        # print(self.data_aux.shape)
        self.word_try.append(self.data_aux.iloc[0]['words'])

    
    def refresh_data(self):
        if len(self.let_in) != 0:
            self.data_aux['cond'] = self.data_aux['words'].apply(lambda x: 0 not in [c in x for c in self.let_in])
            self.data_aux.drop(self.data_aux[self.data_aux['cond'] == False].index, inplace=True)
            # print(self.wordle.word in self.data_aux['words'].values)
        if len(self.let_not_in) != 0:
            self.data_aux['cond'] = self.data_aux['words'].apply(lambda x: 1 not in [c in x for c in self.let_not_in])
            self.data_aux.drop(self.data_aux[self.data_aux['cond'] == False].index, inplace=True)
            # print(self.wordle.word in self.data_aux['words'].values)

        if len(self.position) != 0:
            for i in range(len(self.position)):
                pos = self.position[i][1]
                let = self.position[i][0]
                self.data_aux['cond'] = self.data_aux['words'].apply(lambda x: self.check_positions(x, pos, let))
                self.data_aux.drop(self.data_aux[self.data_aux['cond'] == False].index, inplace=True)
            # print(self.position)
            # print(self.wordle.word in self.data_aux['words'].values)

    
    def check_positions(self, name, pos, let):
        pos_aux = pos
        a = True
        while a:
            if name.find(let) == pos_aux:
                a = False
                return True
            else:
                pos_aux -= name.find(let)+1
                name = name[name.find(let)+1:]
                if name.find(let) < 0:
                    a = False
                    return False

class Wordle_Metrics:
    def __init__(self, mode='total', N=100):
        self.solver = Wordle_Solver()
        self.hist = pd.DataFrame(columns=['1', '2', '3', '4', '5', '6', 'Fail'])
        self.N = N
        self.mode = mode
    
    def chose_model(self):
        if self.mode == 'total':
            self.N = len(self.solver.data)
            n = self.N
        elif self.mode == 'random':
            n = self.N
        for i in range(n):
            # print(i)
            # print(self.hist.tail())
            self.play(i)
        # print(self.hist.head())
        # print(self.hist.sum())
    
    def play(self, i):
        # print(i, 'holae')
        if self.mode == 'total':
            self.solver.solve(i)
        elif self.mode == 'random':
            self.solver.solve(i)
        if self.solver.wordle.win:
            if self.hist.empty:
                col = str(self.solver.wordle.ronda + 1)
                self.hist.loc[0] = 0
                self.hist.loc[0, col] += 1
            else:
                col = str(self.solver.wordle.ronda + 1)
                self.hist.loc[i] = self.hist.loc[i-1]
                self.hist.loc[i, col] = self.hist.loc[i-1, col] + 1
        else:
            if self.hist.empty:
                self.hist.loc[0] = 0
                self.hist.loc[0, 'Fail'] += 1
            else:
                self.hist.loc[i] = self.hist.loc[i-1]
                self.hist.loc[i, 'Fail'] = self.hist.loc[i-1, 'Fail'] + 1
        self.solver.wordle.play_again_test()

    
    def draw_results(self):
        def anim(i):
            # if self.mode == 'total':
            #     self.solver.solve(random.randint(0, self.N))
            # elif self.mode == 'random':
            #     self.solver.solve(i)
            # if self.solver.wordle.win:
            #     col = str(self.solver.wordle.ronda + 1)
            #     self.hist.loc[0, col] += 1
            # else:
            #     self.hist.loc[0, 'Fail'] += 1
            # self.solver.wordle.play_again_test()
            # print(i, 'animacio')
            # print(self.hist.head())
            colors = ['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'red']
            im = plt.bar(self.hist.columns, self.hist.loc[i].values, color = colors)
            return im 
        print(self.hist.tail())
        fig = plt.figure(figsize=(8,6))
        axes = fig.add_subplot(1,1,1)
        axes.set_ylim(0, 1290)
        plt.title("Wordle", color=("black"))
        ani = animation.FuncAnimation(fig=fig, frames=self.N, repeat = False, func=anim, blit = True)
        plt.show()
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=5, metadata=dict(artist='Me'))
        # writergif = animation.FFMpegWriter(fps=60)  
        # ani.save('prova.mp4', writer=writer)


if __name__ == '__main__':
    a = input('Mode: ')
    # a = 'a'
    if a == 'test':
        wordle = Wordle()
        wordle.play()
    elif a == 'go':
        b = input('total/random: ')
        if b == 'total':
            test = Wordle_Metrics()
            test.play()
        elif b == 'random':
            # num = int(input('Mostres: '))
            num = 10
            test = Wordle_Metrics(b, num)
            test.chose_model()
    elif a == 'polla':
        wordle = Wordle_Solver()
        wordle.solve()
    elif a == 'draw':
        wordle = Wordle_Metrics('total')
        wordle.chose_model()
        wordle.draw_results()
    else:
        pass
        