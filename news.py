import pybitcointools as pt
import copy, coin
#newgame_sig_list=['id', 'type', 'game_name', 'pubkey_white', 'pubkey_black', 'count', 'whos_turn', 'white', 'time', 'black', 'size', 'amount']
#nextturn_sig_list=['id', 'game_name', 'type', 'count', 'where', 'move_number']
'''
4) create named account
* Now people can spend to "ganjaQueen" instead of to nonsense pubkeys like: "1847f892h4f8928294f"
* Give a menu of what goods you are selling.
* Explain the process to purchase from you. Maybe give an XMPP address for OTR chat.
* You can update your info by making a new transaction of this type.
* if a named account runs out of money, then all the reputation associated with that account is deleted.
'''
def createAccount(tx, state):
    pass
'''
5) buy reputation for a named account
* proof of burn
'''
def buyReputation(tx, state):
    pass
'''
6)jury signature
* jury members sign the chain which they think is the valid chain.
* jury members have an incentive to only sign 1 chain.
* this gives the jury member a reward.
* There are about 20 constants built into the currency, examples: transaction fees, difficulty. The jury members vote to slightly adjust each of these constants upward or downward.
'''
def jurySig(tx, state):
    #between 2000 and 2010 blocks after they were elected
    #must have actually been elected to the jury at the time they claim with the address they claim.
    #sha256(n1+n2+...n100+address)<2^256*state['constants']['jurySize']*Balance/(total money supply)
    #juror gets a reward
    pass
'''
7)catch a cheating jury member
* if a jury member signs 2 forks, then anyone else can take those 2 signatures and make this type of transaction.
* the jury member loses their reward
* the person who created this transaction receives a reward
'''
def juryTattle(tx, state):
    #must be within 3000 blocks of the block we are tattling on
    #they supply 2 tx from the same juror, signed for blocks that are at the same blocklength, but which have different hash values.
    #juror should lose his reward. 
    #tattler gets 1/3 the reward.
    pass
'''
8)create post
* When creating a top-level post, you spend X NEWS. The value of the post is X. You own X of the post, which is all of the post.
* If your post is a comment on a different post, then it acts like an upvote and a post at the same time.
'''
def create(tx, state):
    pass
'''
9)upvote post
* spend X NEWS
* a portion of this upvote pays the owners of the post you are upvoting, call this portion P. It includes you as one of the owners of the post, so there is an incentive to do all your investing in 1 go, instead of investing in the same post more than once.
* the post increases in value by X* (1-P)* (1-P3)
* you own the amount of the post that you increased it's value by.
* The parent posts increase in value by X* (1-P)* * 2* P3 according to the same rules.
* you own the portion of the parent post that you increased it's value by.
* The parent post's owners get paid P* X* (1-P)* p3
The goal here is for value to never be created or destroyed. (The total value of all the posts) + (the amount that owners get paid) = (amount that was invested).
* for an upvote to be valid, you need to own non-negative amount of coins at the end.
'''
def upvote(tx, state):
    pass
'''
10)downvote post
* When downvoting, you spend X NEWS. 
* The post you downvoted loses X value.
'''
def downvote(tx, state):
    pass
def attempt_absorb(tx, state, db_ex):
    (State, booll)=coin.attempt_absorb(tx, state)
    if booll:
        return (State, booll)
    state=copy.deepcopy(state)
    state_orig=copy.deepcopy(state)
    state[tx['id']]['count']+=1
    types=['createAccount', 'buyReputation', 'jurySig', 'juryTattle', 'create', 'upvote', 'downvote']
    checks=[createAccount, buyReputation, jurySig, juryTattle, create, upvote, downvote]
    if tx['type'] not in types: 
#        print('tx: ' +str(tx))
        print("invalid because tx['type'] was wrong")
        return (state_orig, False)
    for i in range(len(types)):
        if tx['type']==i:
            check = checks[i](tx, state)
            if not check['bool']:
                print('error: ' + str(types[i]))
                return (state_orig, False)
            state=check['state']
    #for each person who signed tx:
    #   if state[person]['amount']<0:
    #      return (state_orig, False)
    return (state, True)

'''
def valid_board(board, move):
    #tells whether this is a valid move to make on this board.
    color=board['whos_turn']
    if color=='white':
        other_color='black'
    else:
        other_color='white'
#    print('move: ' +str(move))
    where=move['where']
    return alive(where, copy.deepcopy(board[color]+[where]), copy.deepcopy(board[other_color]), board['size'])
def alive(loc, mine, yours, size):#is my piece at loc still alive?
    if loc[0]<0 or loc[1]<0 or loc[0]>=size or loc[1]>=size:#off the edge
        return False
    if loc in yours:
        return False
    if loc not in mine+yours:
        return True#Found a liberty!!
    if loc in mine:
        yours.append(loc)
        return alive([loc[0]+1, loc[1]], mine, yours, size) or alive([loc[0]-1, loc[1]], mine, yours, size) or alive([loc[0], loc[1]+1], mine, yours, size) or alive([loc[0], loc[1]-1], mine, yours, size)
def next_board(board, move, count):
#how does dictionary "board" change between moves?
    if board['whos_turn']=='black':
        color='black'
        other_color='white'
    else:
        color='white'
        other_color='black'
    board['move_number']+=1
    board[color]+=[move]
    board['whos_turn']=other_color
    board=remove_dead_stones(board, move)
    board['last_move_time']=count
    return board
def new_game(tx, db_ex):
    print('tx: ' +str(tx))
    state=state_library.current_state(db_ex)
    tx['last_move_time']=state['length']
    tx.pop('signature')
    tx.pop('id')
    tx.pop('count')
    tx.pop('type')
    if 'amount' not in tx:
        tx['amount']=0
    if 'time' not in tx:
        tx['time']=5
    if 'size' not in tx:
        tx['size']=19
    if 'white' not in tx:
        tx['white']=[]
    if 'black' not in tx:
        tx['black']=[]
    tx['move_number']=1
    return tx
def remove_dead_stones(board, move):
#    print('board: ' +str(board))
    color=board['whos_turn']
    if color=='white':
        other_color='black'
    else:
        other_color='white'
    def group(pt, color, board):
        if color=='black':
            other_color='white'
        else:
            other_color='black'
        if pt[0]<0 or pt[1]<0 or pt[0]>=board['size'] or pt[1]>=board['size']:
            return []
        if pt in board[other_color]:
            return []
        if pt not in board[other_color]+board[color]:
            return []
        if pt in board[color]:
            board[color].remove(pt)
            board[other_color].append(pt)
            return [pt]+group([pt[0]+1,pt[1]], color, board)+group([pt[0]-1,pt[1]], color, board)+group([pt[0],pt[1]+1], color, board)+group([pt[0],pt[1]-1], color, board)
    def set_minus(l1, l2):#l1-l2
        out=[]
        for i in l1:
            if i not in l2:
                out.append(i)
        return out
    around=[[move[0]+1, move[1]],[move[0]-1, move[1]],[move[0], move[1]+1],[move[0], move[1]-1]]
    around
    for pt in around:
        if not alive(pt, copy.deepcopy(board[color]), copy.deepcopy(board[other_color]), copy.deepcopy(board['size'])):
            board[color]=set_minus(board[color], group(pt, color, copy.deepcopy(board)))
    return board

def nextTurnCheck(i, state):
    if i['game_name'] not in state:
        print('19')
        return False
    board=state[i['game_name']]
    if len(state.keys())==0:
        print('2')
        return False
    if board['whos_turn']=='white':
        pubkey=board['pubkey_white']
    else:
        pubkey=board['pubkey_black']
    if board['move_number'] != i['move_number']:
        return False
    try:#so that invalid pubkeys don't break anything.
        if not pt.ecdsa_verify(coin.message2signObject(i, nextturn_sig_list), i['signature'], pubkey):
            print('i: ' +str(i))
            print('state: ' +str(state))
            print('14')
            return False
    except:
        print('invalid pubkey error')
        return False
    if type(i['where']) != type([1,2]) or len(i['where'])!=2:
        print('move type eerror')
        return False
    if i['where'] in board['white']+board['black']:
        print('spot taken error')
        return False
    if i['where'][0]<0 or i['where'][1]<0:
        print('off board error')
        return False
    if i['where'][0]>=board['size'] or i['where'][1]>=board['size']:
        print('off board error')
        return False
    n=next_board(copy.deepcopy(board), i['where'], state['length'])
    if (len(n['black'])+len(n['white']))<=(len(board['black'])+len(board['white'])):#if it kills, then it lives
        return True
    return valid_board(board, i)
def winGameCheck(tx, state):
    game=state[tx['game_name']]
    print('game: ' +str(game))
    if game['last_move_time']+game['time']>=state['length']:
        return False
    return True
def newGameCheck(i, state):
    if 'pubkey_black' not in i.keys():
        i['pubkey_black']=i['id']
    if 'pubkey_white' not in i.keys() or type(i['pubkey_white']) not in [type('string'), type(u'unicode')] or len(i['pubkey_white'])!=130:
        print('type: ' +str(type(i['pubkey_white'])))
        print('badly formated newgame white pubkey')
        return False
    if not coin.enough_funds(state, i['pubkey_black'], 25000):
        print('you need at least 1/4 of a CryptGo coin in order to play.')
        return False
    if 'game_name' not in i.keys():
        print('the game needs a name')
        return False
    if len(i['game_name'])>129:
        print('name too long')
        return False
    if not 'pubkey_white' in i or not 'pubkey_black' in i:
        print('13')
        return False
    if 'whose_turn' not in i:
        i['whos_turn']='black'
    if i['whos_turn'] not in ['white', 'black']:
        print('4')
        return False
    if type(i['white']) != type([1,2]):
        return False
    if type(i['black']) != type([1,2]):
        return False
    for j in i['white']+i['black']:
        #            print('j: ' +str(j))
        if type(j)!=type([1,2]) or len(j)!=2:
            print('5')
            return False
    if 'time' not in i:
        i['time']=5
    if 'size' not in i:
        i['size']=13
    if 'white' not in i:
        i['white']=[]
    if 'black' not in i:
        i['black']=[]
    if (type(i['time']) != type(3)):
        print('7')
        return False
    if type(i['size']) != type(3) or i['size']<3 or i['size']>30:
        print('8')
        return False
    if type(i['white']) != type([1,2]) or type(['black']) != type([1,2]):
        print('6')
        return False
    if 'amount' not in i:
        i['amount']=0
    if type(i['amount'])!=type(10):
        print('bet error')
        return False
    sign=coin.message2signObject(i, newgame_sig_list)
    if not pt.ecdsa_verify(sign, i['signature'], i['pubkey_black']):
        print('i: ' +str(i))
        print('signature error')
        return False
    if i['amount']>0 and 'signature_white' not in i:
        print('both people need to consent, if you want to bet')
        return False
    if i['amount']>0 and not pt.ecdsa_verify(sign, i['signature_white'], pubkey_white):
        print('signature error 2')
        return False
    return True
'''
