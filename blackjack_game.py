from random import choice
global player
global current_round
global deck_list
global deck_dict

def reset_game():
    deck_list = ['1','2','3',"4","5","6","7","8","9","10","Jack","Queen","King","Ace"]*8
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
    def __init__(self,round_num=0,comp_hand=0,player_hand=0,player_hand_soft=0,hand_num=0):
        self.round_num = round_num
        self.comp_hand = comp_hand
        self.hand_num_soft = hand_num
        self.player_hand = player_hand
        self.player_hand_soft = player_hand_soft
        
    def set_round_num(self,new_round_num):
        self.round_num += new_round_num
    
    def set_comp_hand(self,new_comp_hand):
        self.comp_hand = new_comp_hand
        
    def set_player_hand(self,new_player_hand):
        self.player_hand += new_player_hand
        
    def set_player_hand_soft(self,new_player_hand_soft):
        self.player_hand_soft += new_player_hand_soft
        
    def set_hand_num(self,new_hand_num):
        self.hand_num += new_hand_num

def draw_card():
    card = str(choice(deck_list))
    deck_list.remove(card)
    print_card(card)
    return card

def print_card(card):
    print " _______"
    print "|       |"
    print "|       |"
    print "|%s|" %(card.center(7))
    print "|       |"
    print "|_______|"


def play():
    reset_game()
    print "Welcome to Blackjack!"
    print "Rules:"
    print "• Type 'Hit' or 'Stand' at the beginning of each round"
    print "• You'll be given the option to double in your first two turns."
    print "• All face cards are equal 10, with the exception of the Ace which is equal to 1 or 11"
    print "• You'll start with a bankroll of 100"
    new_round()

def new_round():
    global current_round
#    comp_play()
    current_round.set_round_num(1)
    set_hand_num(0)
    place_bet()    

def place_bet():
    global player
    global current_hand
    while True:
        try: 
            bet = int(raw_input("Please enter a number, less than your current bankroll (%s): " %(player.bankroll)))
            player.set_bet(bet)
            if bet > player.bankroll:
                raise ValueError
        except: 
            continue
        else:
            hit_stand_double()

def player_hit():
    global new_round
    player_card = draw_card()
    val = deck_dict[player_card]
# set the cards value
    if player_card == 'Ace':
        current_round.set_player_hand_soft(11)
        current_round.set_player_hand(1)
    else:
        current_round.set_player_hand_soft(val)
        current_round.set_player_hand(val)
# calculate the player hand and determine if they won.
    if current_round.player_hand > 21:
        print "Bust!"
        player.adjust_bankroll((player.bet),add=False)
        print "Your bankroll: %s" %player.bankroll
        new_round = True
    else:
        new_round = False
        current_round.set_hand_num(1)
        hit_stand_double()

def player_stand():
    print "The dealer's hand: %s" %(current_round.comp_hand)
    if current_round.player_hand_soft > 21:
        eval_hand = current_round.player_hand
    elif current_round.player_hand_soft <= 21:
        eval_hand = current_round.player_hand_soft    
    if eval_hand > current_round.comp_hand:
        print "You win the round!. Your winnings: %s" %(player.bet*2)
        player.adjust_bankroll((player.bet*2),add=True)
    elif eval_hand == current_round.comp_hand:
        print "Stand off!. Your winnings: %s" %(player.bet)
        player.adjust_bankroll((player.bet),add=True)                                                                                            
    elif eval_hand < current_round.comp_hand:
        print "You lose the round!"
        player.adjust_bankroll((player.bet),add=False)
    print "Your bankroll: %s" %player.bankroll
    print "Starting the next round..."
    new_round = True    

def player_double():
    player.set_bet((player.bet*2))
    player_stand()


def hit_stand_double():
    if current_round.hand_num == 0:
        player_hit()
        return
    while True:
        try: 
            if current_round.hand_num <= 1 and player.bet <= player.bankroll:
                answer = str(raw_input("Do you want to hit, stand or double?: "))
                if answer.lower() == "hit":
                    player_hit()
                if answer.lower() == "stand":
                    player_stand()
                if answer.lower() == 'double':
                    player_double()
            else:
                answer = str(raw_input("Do you want to Hit or stand?"))
                if answer.lower() == "hit":
                    player_hit(bet)
                if answer.lower() == "stand":
                    player_stand()            
        except: 
            continue

    