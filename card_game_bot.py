from itertools import combinations
from collections import Counter
ANS = []
open_turn = True
num = {"A": 1, "0": 10, "J": 11, "Q": 12, "K": 13}
count = 0
fresh = False
sec = False
nk = False
joker = 0

def card_sort(hand):
    num = {"A": '1', "0": '10', "J": '11', "Q": '12', "K": '13'}
    alph = {'1': "A", '10': "0", '11': "J", '12': "Q", '13': "K"}
    sort_hand = []
    for card in hand:
        if card[0] in num:
            sort_hand.append(num[card[0]] + card[1])
        else:
            sort_hand.append(card)
    sort_hand.sort(key=lambda x: (len(x), x))
    for i in range(len(sort_hand)):
        if len(sort_hand[i]) == 3:
            sort_hand[i] = alph[sort_hand[i][:2]] + sort_hand[i][2]
        elif sort_hand[i][0] == '1':
            sort_hand[i] = alph[sort_hand[i][0]] + sort_hand[i][1]
    return sort_hand

def score(cards):
    score = 0
    points = {"A": 1, "0": 10, "J": 11, "Q": 12, "K": 13}
    if(cards):
        for card in cards:
            if card[0] in points:
                score += points[card[0]]
            else:
                score += int(card[0])
        return score
    return score

def check_n_kind(group):
    for i in range(1, len(group)):
        if group[0][0] != group[i][0]:
            return False
    if len(group) < 3:
        return False
    if len(group) <= 4:
        if len(set(group)) != len(group):
            return False
    else:
        if len(set(group)) != 4:
            return False
        return True
    return True   

def check_run(group):
    new_group = sortx(group)
    color = {'C': 'b', 'S': 'b', 'H': 'r', 'D': 'r'}
    if len(group) < 3:
        return False
    for i in range(len(new_group) - 1):
        if new_group[i][0] + 1 != new_group[i + 1][0]:
            return False
        elif color[new_group[i][1]] == color[new_group[i + 1][1]]:
            return False
    return True 
        
def n_kind(hand, table):
    global ANS
    global open_turn
    global nk
    global joker
    cards = []
    table_copy = table.copy()
    for i in range(len(hand) - 1):
        rep = 0
        while (hand[i][0] == hand[i + 1][0]):
            rep += 1
            i += 1
            if i == (len(hand) - 1):
                break
        if rep == 1:
            cards = hand[i - rep:i + 1]
            if len(cards) == len(set(cards)):
                if joker != 0:
                    ANS += [('XX', len(table))]
                    ANS += [(cards[0], len(table))]
                    ANS += [(cards[1], len(table))]
                    nk = True
                    joker -= 1
                    return True
                for i in range(len(table)):
                    if 'XX' in table[i]:
                        table_copy[i].remove('XX')
                        if check_run(table_copy[i]) is False and check_n_kind(table_copy[i]) is False:
                            table_copy[i].append('XX')
                            continue
                    if check_n_kind(table_copy[i]) is True:
                        table_copy[i] = list((Counter(table_copy[i]) - Counter(list(set(table_copy[i])))).elements())
                    if len(table_copy[i]) <= 3:
                        if check_n_kind(table[i]) is True:
                            if len(table_copy[i]) == 0:
                                continue
                        else:
                            continue
                    table_copy[i] = card_sort(table_copy[i])
                    if cards[0][0] == table_copy[i][0][0] and cards[0][1] != table_copy[i][0][1]:
                        if cards[1][1] != table_copy[i][0][1]:
                            ANS += [(table_copy[i][0], i, len(table))]
                            ANS += [(cards[0], len(table))]
                            ANS += [(cards[1], len(table))]
                            nk = True
                            return True
                    elif cards[0][0] == table_copy[i][-1][0] and cards[0][1] != table_copy[i][-1][1]:
                        if cards[1][1] != table_copy[i][-1][1]:
                            ANS += [(table_copy[i][-1], i, len(table))]
                            ANS += [(cards[0], len(table))]
                            ANS += [(cards[1], len(table))]
                            nk = True
                            return True
        if rep >= 2:
            cards = hand[i - rep:i + 1]
            if check_n_kind(cards) is True:
                ANS = cards
                break
            else:
                if len(set(cards)) >= 3:
                    ANS = list(set(cards))
                    break
    if ANS == []:
        return False
    else:
        return True

def run(hand):
    global ANS
    i = 0
    cards = []
    while i < (len(hand) - 3):
        flag = True
        cards = []
        get_out = False
        while flag:
            while hand[i][0] == hand[i + 1][0]:
                cards.append(hand[i])
                i += 1
                if (i >= len(hand) - 2):
                    cards.append(hand[i])
                    break
            if i == len(hand) - 1:
                if len(cards)>=3:
                    for l in [3, 4, 5, 6]:
                        for s in combinations(cards, l):
                            if check_run(list(s)) is True:
                                if score(ANS) <= score(s):
                                    ANS = list(s)
                                    cards = list(s)
                                    break
                break
            if hand[i][0] in num and hand[i + 1][0] in num:
                if num[hand[i][0]] + 1 == num[hand[i + 1][0]]:
                    flag = True
                else:
                    flag = False
            elif hand[i][0] in num and hand[i + 1][0] not in num:
                if num[hand[i][0]] + 1 == int(hand[i + 1][0]):
                    flag = True
                else:
                    flag = False
            elif hand[i][0] not in num and hand[i + 1][0] in num:
                if int(hand[i][0]) + 1 == num[hand[i + 1][0]]:
                    flag = True
                else:
                    flag = False
            else:
                if int(hand[i][0]) + 1 == int(hand[i + 1][0]):
                    flag = True
                else:
                    flag = False
            cards.append(hand[i])
            i += 1
            if (i == len(hand) - 1):
                if flag is True:
                    cards.append(hand[i])    
                if len(cards) >= 3:
                    for l in [3, 4, 5, 6]:
                        for s in combinations(cards, l):
                            if check_run(list(s)) is True:
                                if score(ANS) <= score(s):
                                    ANS = list(s).copy()
                                    cards = list(s)
                                    get_out = True
                                    break
                break    
            if len(cards) >= 3:
                for l in [3, 4, 5, 6]: 
                    for s in combinations(cards, l):
                        if check_run(list(s)) is True:
                            if score(ANS) <= score(s):
                                ANS = list(s).copy()
                                cards = list(s)
                        else:
                            get_out = True
            if flag == False and len(cards)>=3:
                get_out = True
        if get_out is True:
            if ANS == cards:
                break
    if cards != []:
        if ANS == cards:
            return True
        else:
            return False
    else:
        return False

def sortx(hand):
    new_hand = []
    sorted_hand = card_sort(hand)
    for card in sorted_hand:
        if card[0] in num:
            new_hand.append([num[card[0]], card[1]])
        else:
            new_hand.append([int(card[0]), card[1]])
    return new_hand


def bac(card):
    alph = {1: "A", 10: "0", 11: "J", 12: "Q", 13: "K"}
    if card[0] in alph:
        return alph[card[0]] + card[1]
    else:
        return str(card[0]) + card[1] 

    
def check(hand, table):
    global ANS
    table_copy = table.copy()
    n_hand = sortx(hand)
    comp = {"S": "HD", "C": "HD", "H": "SC", "D": "SC"}
    for card in n_hand:
        for i in range(len(table_copy)):
            if 'XX' in table_copy[i]:
                table_copy[i].remove('XX')
                if check_run(table_copy[i]) is True:
                    if len(table_copy[i]) == 12:
                        continue
                if check_run(table_copy[i]) is False and check_n_kind(table_copy[i]) is False:
                    table_copy[i].append('XX')
                    continue
            c = sortx(table_copy[i])
            if check_n_kind(table_copy[i]) is False:
                if card[0] + 1 == c[0][0] and card[1] in comp[c[0][1]]:
                    ANS.append((bac(card), i))
                    return True
                elif card[0] - 1 == c[-1][0] and card[1] in comp[c[-1][1]]:
                    ANS.append((bac(card), i))
                    return True
    return False
   

def check_in_table(hand, table):
    global ANS
    copy_table = table.copy()
    copy_hand = hand.copy()
    for card in copy_hand:
        for j in range(len(copy_table)):
            if 'XX' in copy_table[j]:
                copy_table[j].remove('XX')
                if check_run(copy_table[j]) is True:
                    if len(copy_table[j]) == 12:
                        continue
                if check_n_kind(copy_table[j]) is True:
                    if len(copy_table[j]) == 7:
                        continue
                if check_run(copy_table[j]) is False and check_n_kind(copy_table[j]) is False:
                    copy_table[j].append('XX')
                    continue
            if copy_table[j][-1][0] == card[0]:
                check = copy_table[j].copy()
                check.append(card)
                if check_n_kind(check) is True:
                    ANS.append((card, j))
                    return True
    
def n_kind_open(hand, table):
    global ANS
    global open_turn
    hand.reverse()
    n = len(table)
    i = 0
    while i < len(hand) - 1:
        rep = 0
        cards = []
        while (hand[i][0] == hand[i + 1][0]):
            rep += 1
            i += 1
            if i == (len(hand) - 1):
                break
        if rep >= 2:
            cards = hand[i - rep:i + 1]
            if check_n_kind(cards) is True:
                if len(cards)>=3 and len(ANS)==3:
                    cards = list(set(cards))[:3]
                    for card in cards:
                        ANS += [(card, n + 1)]
                else:
                    for card in cards:
                        ANS += [(card, n)]
            else:
                if len(set(cards))>=3:
                    if len(cards)>=3 and len(ANS)==3:
                        cards = list(set(cards))[:3]
                        for card in cards:
                            ANS += [(card, n + 1)]
                    else:
                        cards = list(set(cards))
                        for card in cards:
                            ANS += [(card, n)]
        if len(ANS)>3:
            break
        i += 1
    if ANS == []:
        return False
    else:
        return True
    
def check_open(hand, table):
    global ANS
    table_copy = table.copy()
    n_hand = sortx(hand)
    n_hand.reverse()
    comp = {"S": "HD", "C": "HD", "H": "SC", "D": "SC"}
    for card in n_hand:
        for i in range(len(table_copy)):
            if 'XX' in table_copy[i]:
                table_copy[i].remove('XX')
                if check_run(table_copy[i]) is False and check_n_kind(table_copy[i]) is False:
                    table_copy[i].append('XX')
                    continue
            c = sortx(table_copy[i])
            if check_n_kind(table_copy[i]) is False:
                if card[0] + 1 == c[0][0] and card[1] in comp[c[0][1]]:
                    ANS.append((bac(card), i))
                    table_copy[i] = table_copy[i] + [bac(card)]
                    break
                elif card[0] - 1 == c[-1][0] and card[1] in comp[c[-1][1]]:
                    ANS.append((bac(card), i))
                    table_copy[i] = table_copy[i] + [bac(card)]
                    break
            else:
                if card[0] == c[0][0]:
                    if len(table_copy[i]) == 3:
                        if len(set(table_copy[i] + [bac(card)])) == 4:
                            ANS.append((bac(card), i))
                            table_copy[i] = table_copy[i] + [bac(card)]
                            break
                    else:
                        ANS.append((bac(card), i))
                        table_copy[i] = table_copy[i] + [bac(card)]
                        break
        if len(ANS) == 6:
            break
            
            
def comp10001huxxy_bonus_play(play_history, active_player, hand, table):
    global open_turn
    global count
    global fresh
    global ANS
    global joker
    global sec
    global nk
    joker = hand.count('XX')
    while 'XX' in hand:
        hand.remove('XX')
    hand = card_sort(hand)
    if open_turn is True:
        if play_history != []:
            if play_history[-1][0] != active_player:
                if run_open(hand, table) is True:
                    if len(ANS) != 6:
                        sub = [card[0] for card in ANS]
                        hand = list((Counter(hand) - Counter(sub)).elements())
                        check_open(hand, table)
                        s = [card[0] for card in ANS]
                        if score(s)>=24:
                            return (active_player, 1, ANS.pop(0))
                        else:
                            ANS = []
                    else:
                        a = [card[0] for card in ANS]
                        if score(a)>=24:
                            sub = [card[0] for card in ANS]
                            hand = list((Counter(hand) - Counter(sub)).elements())
                            return (active_player, 1, ANS.pop(0))
                        else:
                            ANS = []
                if n_kind_open(hand, table) is True:
                    if len(ANS) != 6:
                        sub = [card[0] for card in ANS]
                        hand = list((Counter(hand) - Counter(sub)).elements())  
                        check_open(hand, table)
                        s = [card[0] for card in ANS]
                        if score(s)>=24:
                            return (active_player, 1, ANS.pop(0))
                        else:
                            ANS = []
                            return (active_player, 0, None)
                    else:
                        c = [card[0] for card in ANS]
                        if score(c)>24:
                            return (active_player, 1, ANS.pop(0))
                        else:
                            ANS = []
                            return (active_player, 0, None)
                else:
                    ANS = []
                    return (active_player, 0, None)
            else:
                if ANS != []:
                    return (active_player, 1, ANS.pop(0))
                else:
                    open_turn = False
                    ANS = []
                    return (active_player, 3, None)
        else:
            if run_open(hand, table) is True:
                s = [card[0] for card in ANS]
                if score(s)>=24:
                    sub = [card[0] for card in ANS]
                    hand = list((Counter(hand) - Counter(sub)).elements())
                    return (active_player, 1, ANS.pop(0))
                else:
                    if len(ANS) == 3:
                        sub = [card[0] for card in ANS]
                        hand = list((Counter(hand) - Counter(sub)).elements())
                    else:
                        ANS = []
            if n_kind_open(hand, table) is True:
                sub = [card[0] for card in ANS]
                hand = list((Counter(hand) - Counter(sub)).elements())
                s = [card[0] for card in ANS]
                if score(s)>=24:
                    return (active_player, 1, ANS.pop(0))
                else:
                    ANS = []
                    return (active_player, 0, None)
            else:
                ANS = []
                return (active_player, 0, None)
    else:
        if (play_history[-1][0] == active_player) and (fresh is True):
            if sec is True:
                if ANS != []:
                    count += 1 
                    return (active_player, 2, ANS.pop())
                else:
                    sec = False
                    ANS = []
            if nk is True:
                if ANS != []:
                    count += 1
                    if len(ANS) == 1:
                        nk = False
                    if len(ANS[0]) == 2:
                        return (active_player, 1, ANS.pop(0))
                    else:
                        return (active_player, 2, ANS.pop(0))
            if ANS == [] or count == 6:
                count = 0
                ANS = []
                return (active_player, 3, None)
            else:
                count += 1
                if len(ANS) == 1 and count != 6:
                    fresh = False
                return (active_player, 1, (ANS.pop(0), play_history[-1][2][1]))
        else:
            if count <= 3:
                if run(hand) is True:
                    fresh = True
                    count += 1
                    return (active_player, 1, (ANS.pop(0), len(table)))
                elif n_kind(hand, table) is True:
                    fresh = True
                    count += 1
                    if nk is True:
                        return (active_player, 1, ANS.pop())
                    else:
                        return (active_player, 1, (ANS.pop(0), len(table)))
                elif check(hand, table) is True:
                    fresh = False
                    count += 1
                    return (active_player, 1, ANS.pop(0))
                elif check_in_table(hand, table) is True:
                    fresh = False
                    count += 1
                    return (active_player, 1, ANS.pop(0))
                elif bonus(hand, table) is True:
                    fresh = False
                    count += 1
                    return (active_player, 1, ANS.pop(0))
                elif second(hand, table) is True:
                    fresh = True
                    sec = True
                    count += 1
                    return (active_player, 1, ANS.pop())
                elif second_n_run(hand, table) is True:
                    fresh = True
                    nk =  True
                    count += 1 
                    return (active_player, 1, ANS.pop(0))
                elif second_run(hand, table) is True:
                    fresh = True
                    sec = True
                    count += 1
                    return (active_player, 1, ANS.pop())
                elif second2(hand, table) is True:
                    fresh = True
                    sec = True
                    count += 1
                    return (active_player, 1, ANS.pop(0))
                elif run2(hand, table) is True:
                    fresh = True
                    sec = True
                    count += 1
                    return (active_player, 1, ANS.pop(0))
                else:
                    if play_history[-1][0] == active_player:
                        count = 0
                        ANS = []
                        return (active_player, 3, None)
                    else:
                        count = 0
                        return (active_player, 0, None)
            else:
                if check(hand, table) is True and count < 6:
                    fresh = False
                    count += 1
                    return (active_player, 1, ANS.pop(0))
                elif check_in_table(hand, table) is True and count < 6:
                    fresh = False
                    count += 1
                    return (active_player, 1, ANS.pop(0))
                elif bonus(hand, table) is True and count < 6:
                    fresh = False
                    count += 1
                    return (active_player, 1, ANS.pop(0))
                else:
                    if play_history[-1][0] == active_player:
                        count = 0
                        ANS = []
                        return (active_player, 3, None)
                    else:
                        count = 0
                        return (active_player, 0, None)


def second(hand, table):
    global ANS
    new = sortx(hand)
    for card in new:
        count = 0
        for i in range(len(table)):
            if 'XX' in table[i]:
                table[i].remove('XX')
                if check_run(table[i]) is False and check_n_kind(table[i]) is False:
                    table[i].append('XX')
                    continue
            c = sortx(table[i])
            if len(c) > 3:
                ncheck = check_n_kind(table[i])
                if ncheck is True:
                    if len(table[i]) > 4:
                        c = sortx(list((Counter(table[i]) - Counter(list(set(table[i])))).elements()))
                if card[0] == c[0][0] and card[1] != c[0][1]:
                    if ANS != []:
                        if ANS[0][0] != bac(c[0]):
                            count += 1
                            ANS += [(bac(c[0]), i, len(table))]
                    else:
                        count += 1
                        ANS += [(bac(c[0]), i, len(table))]
                elif card[0] == c[-1][0] and card[1] != c[-1][1]:
                    if ANS != []:
                        if ANS[0][0] != bac(c[-1]):
                            count += 1
                            ANS += [(bac(c[-1]), i, len(table))]
                    else:
                        count += 1
                        ANS += [(bac(c[-1]), i, len(table))]
            if count == 2:
                break
        if count == 2:
            ANS += [(bac(card), len(table))]
            return True
        else:
            ANS = []
            

def second_run(hand, table):
    global ANS
    color = {'D': 'r', 'S': 'b', 'H': 'r', 'C': 'b'}
    new = sortx(hand)
    for card in new:
        up = False
        down = False
        for i in range(len(table)):
            if 'XX' in table[i]:
                table[i].remove('XX')
                if check_run(table[i]) is False and check_n_kind(table[i]) is False:
                    table[i].append('XX')
                    continue
            c = sortx(table[i])
            if len(c) > 3:
                ncheck = check_n_kind(table[i])
                if ncheck is True:
                    if len(table[i]) > 4:
                        c = sortx(list((Counter(table[i]) - Counter(list(set(table[i])))).elements()))
                if card[0] + 1 == c[0][0] and color[card[1]] != color[c[0][1]]:
                    if up is False:
                        up = True
                        ANS += [(bac(c[0]), i, len(table))]
                elif card[0] - 1 == c[0][0] and color[card[1]] != color[c[0][1]]:
                    if down is False:
                        down = True
                        ANS += [(bac(c[0]), i, len(table))]
                elif card[0] - 1 == c[-1][0] and color[card[1]] != color[c[-1][1]]:
                    if down is False:
                        down = True
                        ANS += [(bac(c[-1]), i, len(table))]
                elif card[0] + 1 == c[-1][0] and color[card[1]] != color[c[-1][1]]:
                    if up is False:
                        up = True
                        ANS += [(bac(c[-1]), i, len(table))]
                elif ncheck is True:
                    if len(c) > 1:
                        if card[0] + 1 == c[1][0] and color[card[1]] != color[c[1][1]]:
                            if up is False:
                                up = True
                                ANS += [(bac(c[1]), i, len(table))]
                        elif card[0] - 1 == c[1][0] and color[card[1]] != color[c[1][1]]:
                            if down is False:
                                down = True
                                ANS += [(bac(c[1]), i, len(table))]
            if up is True and down is True:
                break
        if len(ANS) == 2:
            ANS += [(bac(card), len(table))]
            return True
        else:
            ANS = []
        
def run_open(hand, table):
    global ANS
    sub_ans = []
    i = 0
    cards = []
    while i < (len(hand) - 3):
        flag = True
        cards = []
        get_out = False
        while flag:
            while hand[i][0] == hand[i + 1][0]:
                cards.append(hand[i])
                i += 1
                if (i >= len(hand) - 2):
                    cards.append(hand[i])
                    break
            if i == len(hand) - 1:
                if len(cards)>=3:
                    for l in [3, 4, 5, 6]:
                        for s in combinations(cards, l):
                            if check_run(list(s)) is True:
                                sub_ans = list(s)
                                cards = list(s)
                                break
                break
            if hand[i][0] in num and hand[i + 1][0] in num:
                if num[hand[i][0]] + 1 == num[hand[i + 1][0]]:
                    flag = True
                else:
                    flag = False
            elif hand[i][0] in num and hand[i + 1][0] not in num:
                if num[hand[i][0]] + 1 == int(hand[i + 1][0]):
                    flag = True
                else:
                    flag = False
            elif hand[i][0] not in num and hand[i + 1][0] in num:
                if int(hand[i][0]) + 1 == num[hand[i + 1][0]]:
                    flag = True
                else:
                    flag = False
            else:
                if int(hand[i][0]) + 1 == int(hand[i + 1][0]):
                    flag = True
                else:
                    flag = False
            cards.append(hand[i])
            i += 1
            if (i == len(hand) - 1):
                if flag is True:
                    cards.append(hand[i])    
                if len(cards) >= 3:
                    for l in [3, 4, 5, 6]:
                        for s in combinations(cards, l):
                            if check_run(list(s)) is True:
                                sub_ans = list(s).copy()
                                cards = list(s)
                break    
            if len(cards) >= 3:
                for l in [6, 5, 4, 3]: 
                    for s in combinations(cards, l):
                        if check_run(list(s)) is True:
                            sub_ans = list(s).copy()
                            cards = list(s)
                        else:
                            get_out = True
            if flag == False and len(cards)>=3:
                get_out = True
        if get_out is True:
            if sub_ans == cards:
                break
    if cards != []:
        if sub_ans == cards:
            ANS = [(card, len(table)) for card in sub_ans]
            return True
        else:
            return False
    else:
        return False
            
def second_n_run(hand, table):
    global ANS
    global joker
    color = {'D': 'r', 'C': 'b', 'S': 'b', 'H': 'r'}
    new = sortx(hand)
    i = 0
    while i < (len(new) - 1):
        cards = []
        if new[i][0] + 1 == new[i + 1][0] and color[new[i][1]] != color[new[i + 1][1]]:
            cards.append((new[i], len(table)))
            cards.append((new[i + 1], len(table)))
            if joker != 0:
                ANS.append(('XX', len(table)))
                joker -= 1
                for card in cards:
                    ANS.append((bac(card[0]), card[1]))
                return True
            for j in range(len(table)):
                if 'XX' in table[j]:
                    table[j].remove('XX')
                    if check_run(table[j]) is False and check_n_kind(table[j]) is False:
                        table[j].append('XX')
                        continue
                c = sortx(table[j])
                if len(c) > 3:
                    ncheck = check_n_kind(table[j])
                    if ncheck is True:
                        if len(table[j]) > 4:
                            c = sortx(list((Counter(table[j]) - Counter(list(set(table[j])))).elements()))
                    if cards[1][0][0] + 1 == c[0][0]:
                        if color[cards[1][0][1]] != color[c[0][1]]:
                            cards.append((c[0], j, len(table)))
                            break
                    elif cards[1][0][0] + 1 == c[-1][0]:
                        if color[cards[1][0][1]] != color[c[-1][1]]:
                            cards.append((c[-1], j, len(table)))
                            break
                    if cards[0][0][0] - 1 == c[0][0]:
                        if color[cards[0][0][1]] != color[c[0][1]]:
                            cards.append((c[0], j, len(table)))
                            break
                    elif cards[0][0][0] - 1 == c[-1][0]:
                        if color[cards[0][0][1]] != color[c[-1][1]]:
                            cards.append((c[-1], j, len(table)))
                            break   
                    if ncheck is True:
                        if len(c) > 1:
                            if cards[0][0][0] - 1 == c[1][0]:
                                if color[cards[0][0][1]] != color[c[1][1]]:
                                    cards.append((c[1], j, len(table)))
                                    break
                            elif cards[1][0][0] + 1 == c[1][0]:
                                if color[cards[1][0][1]] != color[c[1][1]]:
                                    cards.append((c[1], j, len(table)))
                                    break   
        i += 1
        if len(cards) == 3:
            for card in cards:
                if len(card) == 2:
                    ANS.append((bac(card[0]), card[1]))
                else:
                    ANS.append((bac(card[0]), card[1], card[2]))
            return True

def bonus(hand, table):
    global ANS
    table_copy = table[:]
    for card in hand:
        for i in range(len(table)):
            if 'XX' in table_copy[i]:
                table_copy[i].remove('XX')
                if check_run(table_copy[i]) is False and check_n_kind(table_copy[i]) is False:
                    table_copy[i] += [card]
                    if check_run(table_copy[i]) is True:
                        if len(table_copy[i]) != 13:
                            ANS += [(card, i)]
                            return True
                    elif check_n_kind(table_copy[i]) is True:
                        if len(table_copy[i]) != 8:
                            ANS += [(card, i)]
                            return True
                    table_copy[i].remove(card)
                table_copy[i] += ['XX']        
    
                        
def second2(hand, table):
    global ANS
    color = {'D': 'r', 'S': 'b', 'H': 'r', 'C': 'b'}
    new = sortx(hand)
    table_copy = table.copy()
    cards = []
    for card in new:
        cards = [card]
        up = False
        down = False
        for i in range(len(table)):
            if 'XX' in table[i]:
                table[i].remove('XX')
                if check_run(table[i]) is False and check_n_kind(table[i]) is False:
                    table[i].append('XX')
                    continue
            c = sortx(table_copy[i])
            if len(c) <= 3:
                continue
            ncheck = check_n_kind(table[i])
            if ncheck is True:
                if len(table[i]) > 4:
                    # stores the cards that can be transfered from the group
                    c = sortx(list((Counter(table[i]) - Counter(list(set(table[i])))).elements()))
            if len(cards) == 1:
                if card[0] + 1 == c[0][0] and color[card[1]] != color[c[0][1]]:
                    if up is False:
                        up = True
                        cards += [(c[0], i, len(table))]
                elif card[0] + 1 == c[-1][0] and color[card[1]] != color[c[-1][1]]:
                    if up is False:
                        up = True
                        cards += [(c[-1], i, len(table))]
                elif card[0] - 1 == c[0][0] and color[card[1]] != color[c[0][1]]:
                    if down is False:
                        down = True
                        cards += [(c[0], i, len(table))]
                elif card[0] - 1 == c[-1][0] and color[card[1]] != color[c[-1][1]]:
                    if down is False:
                        down = True
                        cards += [(c[-1], i, len(table))]
                elif ncheck is True:
                    if len(c) > 1:
                        if card[0] + 1 == c[1][0] and color[card[1]] != color[c[1][1]]:
                            if up is False:
                                up = True
                                cards += [(c[1], i, len(table))]
                        elif card[0] - 1 == c[1][0] and color[card[1]] != color[c[1][1]]:
                            if down is False:
                                down = True
                                cards += [(c[1], i, len(table))]
            elif len(cards) == 2:
                if ncheck is True:
                    if len(c) == 0:
                        continue
                else:
                    if len(c) <= 3:
                        continue
                if up is True:
                    if cards[-1][0][0] + 1 == c[0][0] and color[cards[-1][0][1]] != color[c[0][1]]:
                        cards.append((c[0], i, len(table)))
                        break
                    elif cards[-1][0][0] + 1 == c[-1][0] and color[cards[-1][0][1]] != color[c[-1][1]]:
                        cards.append((c[-1], i, len(table)))
                        break
                elif down is True:
                    if cards[-1][0][0] - 1 == c[-1][0] and color[cards[-1][0][1]] != color[c[-1][1]]:
                        cards.append((c[-1], i, len(table)))
                        break
                    elif cards[-1][0][0] - 1 == c[0][0] and color[cards[-1][0][1]] != color[c[0][1]]:
                        cards.append((c[0], i, len(table)))
                        break
        if len(cards) == 3:
            break
    if len(cards) == 3:
        ANS += [(bac(cards[0]), len(table))]
        ANS += [(bac(cards[1][0]), cards[1][1], cards[1][2])]
        ANS += [(bac(cards[2][0]), cards[2][1], cards[2][2])]
        return True
            
def run2(hand, table):
    global ANS
    color = {'D': 'r', 'S': 'b', 'H': 'r', 'C': 'b'}
    new = sortx(hand)
    for card in new:
        for i in range(len(table)):
            if 'XX' in table[i]:
                table[i].remove('XX')
                if check_run(table[i]) is False and check_n_kind(table[i]) is False:
                    table[i].append('XX')
                    continue
            c = sortx(table[i])
            if len(c) >= 5 and check_n_kind(table[i]) is False:
                if card[0] + 2 == c[-1][0] and color[c[-1][1]] == color[card[1]]:
                    ANS += [(bac(card), len(table))]
                    ANS += [(bac(c[-1]), i, len(table))]
                    ANS += [(bac(c[-2]), i, len(table))]
                    return True
                elif card[0] - 2 == c[0][0] and color[c[0][1]] == color[card[1]]:
                    ANS += [(bac(card), len(table))]
                    ANS += [(bac(c[0]), i, len(table))]
                    ANS += [(bac(c[1]), i, len(table))]
                    return True
