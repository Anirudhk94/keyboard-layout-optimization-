import os,sys
import math as m
import random
import string

#Key Width equal to 1 key
keyWidth = 1.0
#Key coordinate for a 6 rows by 5 column keyboard
cord = [[(x + keyWidth/2.0,y + keyWidth/2.0) for x in range(5)] for y in range(6)]


def get_random_layout():
    # Call this function to a a randomized layout.
    # A layout is dictionary of key symbols(a to z) to it's (row, column) index
    cord_shuffle = [(x ,y) for x in range(6) for y in range(5)]
    random.shuffle(cord_shuffle)

    layout={}
    i=0
    for lt in string.ascii_lowercase:
        layout[lt]=cord_shuffle[i]
        i+=1
    # Since there are 30 slots for a 6*5 keyboard, 
    # we use dummy keys to stuff remaining keys
    layout['1']=cord_shuffle[-1]
    layout['2']=cord_shuffle[-2]
    layout['3']=cord_shuffle[-3]
    layout['4']=cord_shuffle[-4]

    return layout


def makeDigramTable(data_path):
    # Make a Digram Table , which is a dictionary with key format (letter_i,letter_j) to it's Pij
    # You could safely ignore words that have only 1 character when constructing this dictionary
    
    fp = open(data_path)
    content=fp.readlines()
    fp.close()

    pairs = {}

    for line in content :
        word = line.split('\t')[0]
        freq = int(line.split('\t')[1])
        if len(word) == 1 :
            continue 
        for i in range(len(word) - 1) :
            tup = (word[i], word[i+1])
            if tup in pairs :
                pairs[tup] = pairs[tup] + freq
            else :
                pairs[tup] = freq
        
    totalTuples = sum(pairs.values())
    for tup in pairs.keys() :
        occurances = pairs[tup]
        pairs[tup] = occurances * 1.0 / totalTuples * 1.0
    
    # print "digram table :"
    # print pairs    
    return pairs

def FittsLaw(W,D):
    #implement the Fitt's Law based on the given arguments and constant
    a = 0.083
    b = 0.127
    ratio = D * 1.0 / W * 1.0 + 1.0
    #print ratio
    return a + b * (m.log(ratio, 2))


def computeAMT(layout, digram_table):
    # Compute the average movement time
    MT=0.0
    for i in layout.keys() :
        x1 = float(layout[i][0]) 
        y1 = float(layout[i][1])
        # print x1
        for j in layout.keys() :
            x2 = float(layout[j][0])
            y2 = float(layout[j][1])
            W = 1.0
            D = float(m.sqrt((x2 - x1)**2 + (y2 - y1)**2))
            tup = (i, j)
            if(tup in digram_table) :
                MT = MT + (FittsLaw(W, D) * digram_table[tup])
    # print MT        
    return MT

def SA(num_iter, num_random_start, tbl):
    # Do the SA with num_iter iterations, you can random start by num_random_start times
    # the tbl arguments were the digram table
    globalCost = sys.float_info.max
    bestLayout = {}
    r = 0
    while r < num_random_start :
        starting_state = get_random_layout()
        k=0
        cost = computeAMT(starting_state,tbl)

        while k < num_iter :
            key1 = random.choice(starting_state.keys())
            key2 = random.choice(starting_state.keys())

            temp_state = starting_state

            temp = temp_state[key1]
            temp_state[key1] = temp_state[key2]
            temp_state[key2] = temp

            localCost = computeAMT(temp_state, tbl)

            if localCost < cost :
                cost = localCost
                starting_state = temp_state

            k += 1    

        if globalCost > cost :
            bestLayout = starting_state
            globalCost = cost
        r += 1

    final_result = (bestLayout, globalCost)    

    # # # #--------you should return a tuple of (optimal_layout,optimal_MT)----
    return final_result

def printLayout(layout):
    # use this function to print the layout
    keyboard= [[[] for x in range(5)] for y in range(6)]
    for k in layout:
        r=layout[k][0]
        c=layout[k][1]
        keyboard[r][c].append(k)
    for r in range(6):
        row=''
        for c in range(5):
            row+=keyboard[r][c][0] + '  '
        print row

if __name__ == '__main__':

    if len(sys.argv)!=4:
        print "usage: hw1.py [num_SA_iteration] [num_SA_random_start] [dataset_path]"
        exit(0)
    
    k=int(sys.argv[1])
    rs=int(sys.argv[2])
    data_path=sys.argv[3]

    # Test Fitt's Law
    print FittsLaw(10,10)
    print FittsLaw(20,5)
    print FittsLaw(10.5,1)

    #Construct Digram Table
    tbl = makeDigramTable(data_path)

    #Run SA
    result, cost = SA(k,rs,tbl)
    print "Optimal MT:", cost
    printLayout(result)

    

