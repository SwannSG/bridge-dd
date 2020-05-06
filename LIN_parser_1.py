import re
import pprint
import bbr


END_OF_LINE_CHAR = '\n'

# B1
file = '/home/steve/development/doubleDummy/data/3399426367.lin'
# B4
file = '/home/steve/development/doubleDummy/data/3399426420.lin'
file = '/home/steve/development/doubleDummy/data/3399426641.lin'
#file = '/home/steve/development/doubleDummy/data/3399426655.lin'

labels = {
    'ah':   'Board Name',
    'an':   'Alert',
    'pc':   'Played Card',
    'pg':   "Don't know",
    'pn':   'Players Names',    # value S, W, N, E
    'mb':   'Bid',
    'md':   'Hands',
    'rh':   "Don't know",
    'st':   "Don't know",
    'sv':   'Vulnerability',
}


fp = open(file, 'r')
for lin in fp:
    pass
# 'lin' contains the entire LIN string representation
l = lin.split('|')
if l[-1]==END_OF_LINE_CHAR:
    # remove it
    l = l[:len(l)-1]
# create (label,value) tuples in an ordered seqence (list)
i = 0
seq = []
while i < len(l):
    seq.append( (l[i], l[i+1]))
    i = i + 2


# create Board object from BBO LIN
board = bbr.Board()
bid_rec = bbr.BidRecorder()
#play_rec = bbr.PlayRecorder()
pg = bbr.PgState()

for (label, value) in seq:
    if label=='pn':
        board.set_players_from_LIN(value)
    if label=='ah':
        board.board_name = value
    if label=='sv':
        board.vulnerablity = value
    if label=='md':
        board.dealer = value[0]
        board.hands_from_LIN(value)
    if label=='mb':
        bid_rec.add_bid(value)
    if label=='an':
        bid_rec.add_alert(value)
    if label=='pg':
        pg.update()
        if pg.pg_first_ever:
            # get contract
            # update master with bidding
            #board.bidding = bbr.Bidding(bid_rec.bid_round_chunks())
            board.methodA(bbr.Bidding(bid_rec.bid_round_chunks()))
    
    if label=='pc':
        # card played
        pass





