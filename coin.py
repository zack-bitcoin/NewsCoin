import pybitcointools as pt
import copy, state_library
spend_list=['id', 'amount', 'count', 'to']
def enough_funds(state, pubkey, enough):
    #if an error comes up, it would crash the miner. We need to catch all errors, and handle them intelligently. That is why I usually take 3 steps when I accept numbers from external source. I make sure the number was actually provided. I made sure the number is the type I expect. I make sure it is in the range that I expect.
    if enough==0:
        return True
    if pubkey not in state:
        print('nonexistant people have no money')
        return False
    if 'amount' not in state[pubkey]:
        print('this person has no money')
        return False
    funds=state[pubkey]['amount']
    return funds>=enough
def verify_count(tx, state):
    #What if I took a valid transaction that you signed, and tried to submit it to the blockchain repeatedly? I could steal all your money. That is why this check exists. Each transaction has a number written on it. This number increments by one every time.
    if 'id' not in tx:
        print('bad input error in verify count')
        error('here')
        return False
    if tx['id'] not in state.keys():
        state[tx['id']]={'count':1}
    if 'count' not in tx:
        print("invalid because we need each tx to have a count")
        return False
    if 'count' not in state[tx['id']]:
        state[tx['id']]['count']=1
    if 'count' in tx and tx['count']!=state[tx['id']]['count']:
        return False
    return True
def attempt_absorb(tx, state):
    state=copy.deepcopy(state)
    state_orig=copy.deepcopy(state)
    if 'nlocktime' in tx and tx['nlocktime']>state['length']:
        return (state, False)
    if 'expirationDate' in tx and tx['nlocktime']<=state['length']:
        return (state, False)
    if not verify_count(tx, state):
       print("invalid because the tx['count'] was wrong")
       return (state, False)
    state[tx['id']]['count']+=1
    types=['spend', 'mint', 'mint_2']
    if tx['type'] not in types: 
        print("invalid because tx['type'] was wrong")
        return (state_orig, False)
    if tx['type']=='mint':
        if not mint_check(tx, state):
            print('MINT ERROR')
            return (state_orig, False)
        #put the mint data into the database
#        if 'amount' not in state[tx['id']].keys():
#            state[tx['id']]['amount']=0
#        state[tx['id']]['amount']+=tx['amount']
    if tx['type']=='mint_2':
        if not mint_2_check(tx, state):
            print('MINT2 ERROR')
            return (state_orig, False)
        if 'amount' not in state[tx['id']].keys():
            state[tx['id']]['amount']=0
        state[tx['id']]['amount']+=tx['amount']
    if tx['type']=='spend':
        if not spend_check(tx, state):
            print('SPEND ERROR')
            return (state_orig, False)
        if tx['to'] not in state:
            print('PUBKEY ERROR')
            state[tx['to']]={'amount':0}
        if 'amount' not in state[tx['to']]:
            state[tx['to']]['amount']=0
        state[tx['id']]['amount']-=tx['amount']
        state[tx['to']]['amount']+=tx['amount']
    return (state, True)
def mint_2_check(tx, state):
    #must occur between 100 and 900 blocks after the block they mined.
    if tx['amount']>10**5:
        return False#you can only mint up to 10**5 coins per block
    return True
def mint_check(tx, state):
    if False:#if mint data is not in the database
        return False
    return True
def spend_check(tx, state):
    if tx['id'] not in state.keys():
        print("you can't spend money from a non-existant account")
        return False
    if 'amount' not in tx:
        print('how much did you want to spend?')
        return False
    if type(tx['amount']) != type(5):
        print('you can only spend integer amounts of money')
        return False
    if tx['amount']<=1000:
        print('the minimum amount to spend is 1000 base units = 0.01 CryptGo coin.')
        return False
    if not enough_funds(state, tx['id'], tx['amount']):
        print('not enough money to spend in this account')
        return False
    if 'signature' not in tx:
        print("spend transactions must be signed")
        return False
    if not pt.ecdsa_verify(message2signObject(tx, spend_list), tx['signature'], tx['id'] ):
        print("bad signature")
        return False
    return True
def message2signObject(tx, keys):
    out=''
    for key in sorted(keys):
        if type(tx[key])==type([1,2]):
            string=str(key)+':'
            for i in tx[key]:
                string+=str(i)+','
        else:
            string=str(key)+':'+str(tx[key])+','
        out+=string
    return out
