import pybitcointools as pt
import blockchain, copy, state_library
newgame_sig_list=['id', 'type', 'post', 'count', 'amount']
upvote_sig_list=['id', 'post_id', 'type', 'count', 'amount']
downvote_sig_list=['id', 'post_id', 'type', 'count', 'amount']
name_sig_list=['id', 'type', 'count', 'name', 'vote_dic']
burn_sig_list=['id', 'type', 'count', 'name', 'amount']
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
def new_game(tx):
    print('tx: ' +str(tx))
    state=state_library.current_state()
    tx['last_move_time']=state['length']
    tx.pop('signature')
    tx.pop('id')
    tx.pop('count')
    tx.pop('type')
    tx['move_number']=1
    return tx

def nextTurnCheck(i, state):
    if i['game_name'] not in state:
        print('19')
        return False
    board=state[i['game_name']]
    if len(state.keys())==0:
        print('2')
        return False
#    print('state: ' +str(state))
#    print('board: ' +str(board))
    if board['whos_turn']=='white':
        pubkey=board['pubkey_white']
    else:
        pubkey=board['pubkey_black']
    if board['move_number'] != i['move_number']:
        return False
    if not pt.ecdsa_verify(blockchain.message2signObject(i, nextturn_sig_list), i['signature'], pubkey):
        print('i: ' +str(i))
        print('state: ' +str(state))
        print('14')
        return False
    n=next_board(copy.deepcopy(board), i['where'], state['length'])
    if (len(n['black'])+len(n['white']))<=(len(board['black'])+len(board['white'])):#if it kills, then it lives
#        error('here')
        return True
    return valid_board(board, i)
def winGameCheck(tx, state):
    game=state[tx['game_name']]
    print('game: ' +str(game))
    if game['last_move_time']+game['time']>=state['length']:
        return False
    return True
def newGameCheck(i, state):
    if len(i['game_name'])>129:
        print('name too long')
        return False
    if not 'pubkey_white' in i or not 'pubkey_black' in i:
        print('13')
        return False
    if i['whos_turn'] not in ['white', 'black']:
        print('4')
        return False
    for j in i['white']+i['black']:
        #            print('j: ' +str(j))
        if type(j)!=type([1,2]) or len(j)!=2:
            print('5')
            return False
    if 'time' not in i or 'size' not in i or 'white' not in i or 'black' not in i:
        print('12')
        return False
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
        print('bet error')
        return False
    if type(i['amount'])!=type(10):
        print('bet error 2')
        return False
    sign=blockchain.message2signObject(i, newgame_sig_list)
    if not pt.ecdsa_verify(sign, i['signature'], i['pubkey_black']):
        print('i: ' +str(i))
        print('signature error')
        return False
    if i['amount']>0 and not pt.ecdsa_verify(sign, i['signature_white'], pubkey_white):
        print('signature error 2')
        return False
    return True
