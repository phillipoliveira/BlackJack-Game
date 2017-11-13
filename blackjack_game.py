from random import choice

def reset_game(num_of_decks):
    global player
    global current_round
    global deck_list
    global deck_dict
    deck_list = ['1','2','3',"4","5","6","7","8","9","10","Jack","Queen","King","Ace"]*4*num_of_decks
    deck_dict = {'1':1,'2':2,'3':3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"Jack":10,"Queen":10,"King":10,"Ace":1}
    player = Player()
    current_round = Round()

class Player(object):    
    def __init__(self,bankroll=100,bet=0):
        self.bankroll = bankroll
        self.bet = bet
    
    def adjust_bankroll(self,amount,add=True):
        if add==True:
            self.bankroll += amount
        else:
            self.bankroll -= amount
    
    def set_bankroll(self,new_bankroll):
        self.bankroll = new_bankroll
        
    def set_bet(self,new_bet):
        self.bet = new_bet
    
class Round(object):
    def __init__(self,round_num=0,comp_hand=0,comp_hand_soft=0,player_hand=0,player_hand_soft=0,hand_num=0,comp_hand_eval=0,first_comp_card=0):
        self.round_num = round_num
        self.comp_hand = comp_hand
        self.comp_hand_soft = comp_hand_soft
        self.comp_hand_eval = comp_hand_eval
        self.hand_num = hand_num
        self.player_hand = player_hand
        self.player_hand_soft = player_hand_soft
        self.first_comp_card = first_comp_card

        
    def set_round_num(self,new_round_num):
        self.round_num += new_round_num
    
    def set_first_comp_card(self,asign_first_card):
        self.first_comp_card = asign_first_card
    
    def set_comp_hand(self,new_comp_hand):
        self.comp_hand += new_comp_hand

    def set_comp_hand_soft(self,new_comp_hand_soft):
        self.comp_hand_soft += new_comp_hand_soft 
        
    def set_comp_hand_eval(self,new_comp_hand_eval):
        self.comp_hand_eval = new_comp_hand_eval
        
    def set_player_hand(self,new_player_hand):
        self.player_hand += new_player_hand
        
    def set_player_hand_soft(self,new_player_hand_soft):
        self.player_hand_soft += new_player_hand_soft
        
    def set_hand_num(self,new_hand_num):
        self.hand_num += new_hand_num

def draw_card(printcard=True):
    card = str(choice(deck_list))
    deck_list.remove(card)
    if printcard == True:
        print_card(card)
    return card

def print_card(card):
    print " _______"
    print "|       |"
    print "|       |"
    print "|%s|" %(card.center(7))
    print "|       |"
    print "|_______|"
    return


def play():
    print "Welcome to Blackjack!"
    print "Rules:"
    print "• Type 'Hit' or 'Stand' at the beginning of each round"
    print "• You'll be given the option to double in your first two turns."
    print "• All face cards are equal 10, with the exception of the Ace which is equal to 1 or 11"
    print "• You'll start with a bankroll of 100"
    how_many_decks()
    return
    
def how_many_decks():
    while True:
        try: 
            num_of_decks = int(raw_input("How many decks do you want to play with?: (enter an integer)"))
            if num_of_decks == 0:
                raise ValueError
        except: 
            continue
        else:
            reset_game(num_of_decks)
            new_round()
    return
    
def new_round():
    if player.bankroll <= 4:
        print "Your bankroll has dropped below $5. You lose!"
        reset_game()
    else:
        current_round.hand_num = 0
        current_round.set_round_num(1)
        current_round.player_hand = 0
        current_round.player_hand_soft = 0
        current_round.comp_hand = 0
        current_round.comp_hand_soft = 0
        current_round.first_comp_card = 0
        comp_play()
        return
    
def place_bet():
    global player
    global current_hand
    print "The dealer card:"
    print_card(str(current_round.first_comp_card))
    while True:
        try: 
            bet = int(raw_input("Place your bet! Enter a number less than your current bankroll (%s). Minimum bet = $5 " %(player.bankroll)))
            player.set_bet(bet)
            if bet > player.bankroll:
                raise ValueError
            elif bet < 5:
                raise ValueError
        except: 
            continue
        else:
            hit_stand_double()
        return

def player_hit(double=True):
    player_card = draw_card(printcard=True)
    val = deck_dict[player_card]
# set the cards value
    if player_card == 'Ace':
        current_round.set_player_hand_soft(11)
        current_round.set_player_hand(1)
    else:
        current_round.set_player_hand_soft(val)
        current_round.set_player_hand(val)
# calculate the player hand and determine if they won.
#    print "Your hand: %s" %(current_round.player_hand)
    if current_round.player_hand > 21:
        print "Bust!"
        player.adjust_bankroll((player.bet),add=False)
        print "Your bankroll: %s" %player.bankroll
        print "Starting the next round..."
        new_round()
    else:
        current_round.set_hand_num(1)
        if double == True:
            player_stand()
        elif double == False:
            hit_stand_double()
    return

def player_stand():
    print "The dealer's hand: %s" %(current_round.comp_hand_eval)
    if current_round.player_hand_soft > 21:
        eval_hand = current_round.player_hand
    elif current_round.player_hand_soft <= 21:
        eval_hand = current_round.player_hand_soft
    if  current_round.comp_hand_eval > 21:
        print "The dealer busted!. Your winnings: %s" %(player.bet*2)
        player.adjust_bankroll((player.bet*2),add=True) 
    elif eval_hand > current_round.comp_hand_eval:
        print "You win the round!. Your winnings: %s" %(player.bet*2)
        player.adjust_bankroll((player.bet*2),add=True)
    elif eval_hand == current_round.comp_hand_eval:
        print "Stand off!. Your winnings: %s" %(player.bet)
        player.adjust_bankroll((player.bet),add=True)                                                                                            
    elif eval_hand < current_round.comp_hand_eval:
        print "You lose the round!"
        player.adjust_bankroll((player.bet),add=False)
    print "Your bankroll: %s" %player.bankroll
    print "Starting the next round..."
    new_round()
    return

def player_double():
    player.set_bet((player.bet*2))
    player_hit(double=True)
    return


def hit_stand_double():
    if current_round.hand_num == 0:
        print "Your first card:"
        player_hit(double=False)
        return
    else:
        while True:
            try: 
                if current_round.hand_num <= 2 and player.bet <= player.bankroll:
                    answer = str(raw_input("Do you want to hit, stand or double? "))
                    if answer.lower() == "hit":
                        player_hit(double=False)
                    if answer.lower() == "stand":
                        player_stand()
                    if answer.lower() == 'double':
                        player_double()
                else:
                    answer = str(raw_input("Do you want to Hit or stand?" ))
                    if answer.lower() == "hit":
                        player_hit(double=False)
                    if answer.lower() == "stand":
                        player_stand()            
            except: 
                continue
    return

def comp_play():
    while current_round.comp_hand_soft < 17:    
        comp_card = draw_card(printcard=False)
        val = deck_dict[comp_card]
#        print "comp card drawn"
#        print "val type: %s" %(type(val))
        if current_round.comp_hand_soft == 0:
#            print "setting first comp card"
            current_round.set_first_comp_card(comp_card)
            if comp_card == 'Ace':
                current_round.set_comp_hand_soft(11)
                current_round.set_comp_hand(1)
            else:
                current_round.set_comp_hand_soft(val)
                current_round.set_comp_hand(val)
        else:
            if comp_card == 'Ace':
                current_round.set_comp_hand_soft(11)
                current_round.set_comp_hand(1)
            else:
                current_round.set_comp_hand_soft(val)
                current_round.set_comp_hand(val)
    if current_round.comp_hand > 21:
        current_round.set_comp_hand_eval(current_round.comp_hand_soft)
    elif current_round.comp_hand_soft <= current_round.comp_hand:
        current_round.set_comp_hand_eval(current_round.comp_hand)
#    print "comp hand eval: %s" %(current_round.comp_hand_eval)
#    print "comp hand: %s" %(current_round.comp_hand)
    place_bet()