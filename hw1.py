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
    with open(data_path) as f:
        word_count_pairs = [line.split('\t')[:2]
                            for line in f]

        word_count_pairs = [((word[i], word[i + 1]), int(count))
                            for word, count in word_count_pairs
                            for i in range(len(word) - 1)
                            if len(word) > 1]

        digram_count_map = {}

        for digram, count in word_count_pairs:
            digram_count_map[digram] = digram_count_map.get(digram, 0.0) + count

        total_digram_frequency = sum(digram_count_map.values())

        digram_count_map = {digram: count / total_digram_frequency
                            for digram, count in digram_count_map.items()}

        return digram_count_map


def FittsLaw(W,D):
    #implement the Fitt's Law based on the given arguments and constant
    a = 0.083
    b = 0.127
    ratio = D * 1.0 / W * 1.0 + 1.0
    #print ratio
    return a + b * (m.log(ratio, 2))


def computeAMT(layout, digram_table):
    # Compute the average movement time
    AMT = 0.0

    for char1 in layout:
        x1, y1 = float(layout[char1][0]), float(layout[char1][1])

        for char2 in layout:
            x2, y2 = float(layout[char2][0]), float(layout[char2][1])

            W = 1.0

            X = (x2 - x1) ** 2
            Y = (y2 - y1) ** 2
            D = float(m.sqrt(X + Y))

            MT = FittsLaw(W, D)
            P = digram_table.get((char1, char2), 0.0)

            AMT += (MT * P)

    return AMT


def swap(layout, a, b):
    layout1 = layout.copy()
    layout1[a], layout1[b] = layout1[b], layout1[a]
    return layout1


def SA(num_iter, num_random_start, tbl):
    final_result = ({}, 1.0)
    count = 0
    for _ in range(num_random_start):
        ss = get_random_layout()
        cost = computeAMT(ss, tbl)

        for _ in range(num_iter):
            a = random.choice(ss.keys())
            b = random.choice(ss.keys())
            while b == a:
                b = random.choice(ss.keys())

            new_layout = swap(ss, a, b)
            new_cost = computeAMT(new_layout, tbl)
            if new_cost < cost:
                cost = new_cost
                ss = new_layout

        if final_result[1] > cost:
            count = 0
            final_result = (ss, cost)
        else:
            count += 1
            if final_result[1] < 0.239 and count > 10:
                break

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