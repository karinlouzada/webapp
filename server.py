import csv
import random
import copy, re
import os
import hyperBoggleMod as bogFunc
from flask import Flask, render_template, request
app = Flask(__name__)


# define functions
def select_random_word():
    English = []
    French = []
    article = []
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, './static/french_nouns_final.csv')

    words = []
    with open(my_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            dummy = {'eng': row[0], 'fre': row[2], 'art': row[1]}
            words.append(dummy)
            English.append(row[0])
            French.append(row[2])
            article.append(row[1])
    # number of entries in the complete noun list
    n = reader.line_num
    i = random.randrange(1, n)
    # return English[i], French[i], article[i]
    return words[i]


@app.route('/french.html')
def french():
    # data = select_random_word()
    # return render_template('french.html', English = data[0], French = data[1], Article = data[2])
    word = select_random_word()
    return render_template('french.html', English=word['eng'], French=word['fre'], Article=word['art'])


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/resume.html')
def resume():
    return render_template('resume.html')


@app.route('/gallery.html')
def gallery():
    return render_template('gallery.html')


@app.route('/gridder.html')
def gridder():
    return render_template('gridder.html')


@app.route('/boggle.html', methods=['GET','POST'])
def boggle():
    if request.method == "GET":
        letters = bogFunc.die_cast()
        f = open('letters.txt', 'w')
        for lett in letters:
            f.write(lett)
        f.close()
        return render_template("boggle.html", letters=letters)

@app.route('/boggleresults.html', methods=['GET', 'POST'])
def boggleresults():
    if request.method == 'POST': 
        letters=[]
        f = open('letters.txt', 'r')
        x = f.read()
        for lett in x:
            letters.append(lett)
        f.close()

        w=request.form.get("words")
        a=''
        words=[]
        for i in range(len(w)):
            if w[i] != ' ':
                a+=w[i]
            else:
                words.append(a.lower())
                a=''
            if i == len(w)-1:
                words.append(a.lower())
        f.close()
        
        letters_lower = []
        for i in letters:
            letters_lower.append(i.lower())


        # determine illegal letters
        alphabet = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}
        ill = list(alphabet.difference(set(letters_lower)))

        # connectivity matrix = nearest neighbor indices per dice
        nn_ind=[[1,4,5],
            [0,2,4,5,6],
            [1,3,5,6,7],
            [2,6,7],
            [0,1,5,8,9],
            [0,1,2,4,6,8,9,10],
            [1,2,3,5,7,9,10,11],
            [2,3,6,10,11],
            [4,5,9,12,13],
            [4,5,6,8,10,12,13,14],
            [5,6,7,9,11,13,14,15],
            [6,7,10,14,15],
            [8,9,13],
            [8,9,10,12,14],
            [9,10,11,13,15],
            [10,11,14]]

        nn_ind_original=copy.deepcopy(nn_ind)

        # remove duplicates from the list of words
        print('Step 1 - removing duplicates')
        words2 = list(set(words))
        words2 = bogFunc.rem_empt(words2)

        #remove words longer than the number of die
        print('Step 2 - removing words with more letters than die: ',end=' ')
        for i in range(len(words2)):
            if len(words2[i]) > len(letters_lower):
                print(words2[i],end=' ')
                words2[i]=''
        words2 = bogFunc.rem_empt(words2)
        print('')

        # remove words with illegal letters
        print('Step 3 - removing words using uncast letters: ',end=' ')
        for j in range(len(words2)):
            for letter in words2[j]:
                if letter in ill:
                    print(words2[j],end=' ')
                    words2[j]=''
                    break
        words2 = bogFunc.rem_empt(words2)
        print('')

        # remove words not in the dictionary
        print('Step 4 - removing words not in the dictionary: ',end=' ')
        # load the dictionary:
        my_dict = bogFunc.dictio()
        for i in range(len(words2)):
            a=set()
            a.add(words2[i])
            if a != a.intersection(set(my_dict)):
                print(words2[i],end=' ')
                words2[i]=''
        words2 = bogFunc.rem_empt(words2)
        print('')
        print('Words remaining: ',words2)

        # remove words using letters more often than they appear on the board
        print('Step 5 - removing words that use letters more than once: ',end=' ')
        freq_lett=bogFunc.frequency(letters_lower)
        for i in range(len(words2)):
            for lett in words2[i]:
                if words2[i].count(lett) > letters_lower.count(lett):
                    print(words2[i], end=' ')
                    words2[i] = ''
                    break
        words2 = bogFunc.rem_empt(words2)
        print('')
        print('Words remaining: ', words2)


        # removing words whose letters break the adjacency rule
        print('Step 6 - removing words that do not use adjacent letters: ',end=' ')
        for i in range(len(words2)):
            nn_ind = bogFunc.reset_matrix(nn_ind_original)
            result=bogFunc.rec_func(words2[i],nn_ind,letters_lower)        
            if result == False:
                print(words2[i], end=' ')
                words2[i]=''
        words2 = bogFunc.rem_empt(words2)
        print('')
        bogFunc.display_letters(letters)
        print('Words remaining: ',words2)

        # scoring
        print('step final: printing the score')
        score1 = bogFunc.score(words2)

        incorrect = list((set(words)).difference(set(words2)))


    return render_template('boggleresults.html',letters = letters, words = words2, score1 = score1, incorrect = incorrect)