import random, copy, re

# cast the die to generate random letters on a grid
def die_cast():    
    die=[['R','I','F','O','B','X'], 
         ['I','F','E','H','E','Y'],
         ['D','E','N','O','W','S'], 
         ['U','T','O','K','N','D'],
        ['H','M','S','R','A','O'],
        ['L','U','P','E','T','S'],
        ['A','C','I','T','O','A'],
        ['Y','L','G','K','U','E'],
        ['Q','B','M','J','O','A'],
        ['E','H','I','S','P','N'],
        ['V','E','T','I','G','N'],
        ['B','A','L','I','Y','T'],
        ['E','Z','A','V','N','D'],
        ['R','A','L','E','S','C'],
        ['U','W','I','L','R','G'],
        ['P','A','C','E','M','D']]
    letters=[]
    for i in range(len(die)):
        letters.append(die[i][random.randrange(6)])
    if 'Q' in letters:
        ind = random.choice([4,5,9,12,13])
        letters[ind]='U'
    return letters


# determine frequency of the thrown letters
def frequency(word):
    freq = {'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}
    for i in range(len(word)):
        freq[word[i]] = word.count(word[i])
    return freq


# remove empties
def rem_empt(words):
    ''' removes empty entries in the list of words '''
    words=list(set(words))
    if '' in words:
        words.remove('')
    return words
    

# determine all indices of occurences of value in list
# returns a list
def find_index(my_list,value):
    '''returns a list'''

    count= my_list.count(value)
    if count==0:
        return False
    else:
        a=0
        b=len(my_list)
        ii=[]
        for i in range(count):
            index = my_list.index(value,a,b)
            a = index + 1
            ii.append(index)
        return ii


def set_ind_to_empty(matrix_ind,value):
    for i in range(len(matrix_ind)):
        for j in range(len(matrix_ind[i])):
            if matrix_ind[i][j] == value:
                matrix_ind[i][j] = ''
    return matrix_ind


# reset the matrix
def reset_matrix(matrix):
    matrixnew=copy.deepcopy(matrix)
    return matrixnew


# displaying the letters on the screen
def display_letters(letters):
    print(letters[0],letters[1],letters[2],letters[3])
    print(letters[4],letters[5],letters[6],letters[7])
    print(letters[8],letters[9],letters[10],letters[11])
    print(letters[12],letters[13],letters[14],letters[15])


def rec_func(word,nn_ind,letters):
    """This is a recursive function
    to find if the nearest neighbor includes the following letter and 
    prevents reuse of the same letter"""
    test=0
    for i in range(len(word)-1):
        ind_curr = find_index(letters,word[i])
        for ind in ind_curr:
            nn_ind = set_ind_to_empty(nn_ind,ind)
            ind_next=find_index(letters,word[i+1])
            for ind2 in ind_next:
                if ind2 in nn_ind[ind]:
                    test += 1
                    nn_ind = set_ind_to_empty(nn_ind,ind2)
                    return (rec_func(word[i+1:],nn_ind,letters))
        if test == 0 and ind2 == max(ind_next):
            reset_matrix(nn_ind)
            break
        return (rec_func(word[i+1:],nn_ind,letters))
    if test >= len(word)-1:
        return True
    else:
        return False
    

def score(words):
    s=0
    for i in range (len(words)): 
        if len(words[i]) <=4: # word with 4 or fewer letters = 1 point
            s=s+1
        elif len(words[i]) == 5: # word with 5 letters = 2 points
            s=s+2
        elif len(words[i]) == 6: # word with 6 letters = 3 points
            s=s+3 
        elif len(words[i]) == 7: # word with 7 letters = 5 points
            s=s+5
        elif len(words[i]) > 7: # word with more than 7 letters = 11 points
            s=s+11
    print('Congats, your score is: '+str(s)+'!')
    return s


# open and read dictionary:
def dictio():
    f = open('en_US_KLL.dic', 'r')
    x = f.readlines()
    f.close()
    for i in range(len(x)):
        x[i]=x[i].strip()
    return x