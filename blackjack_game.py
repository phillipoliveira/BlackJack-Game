from random import choice

def reset_game():
#    print "reseting game.."
    global player
    global current_round
    global deck_dict
    deck_dict = {'2':2,'3':3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"Jack":10,"Queen":10,"King":10,"Ace":1}
    player = Player()
    current_round = round_stats()

def reset_deck():
    print "Shuffling the deck..."
    current_round.deck_list = ['2','3',"4","5","6","7","8","9","10","Jack","Queen","King","Ace"]*4*current_round.num_of_decks

    
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
    
class round_stats(object):
    def __init__(self,round_num=0,comp_hand=0,comp_hand_soft=0,player_hand=0,player_hand_soft=0,hand_num=0,player_hand_list=[],player_hand_last=[],comp_hand_eval=0,first_comp_card=0,num_of_decks=0,deck_list=[]):
        self.round_num = round_num
        self.comp_hand = comp_hand
        self.comp_hand_soft = comp_hand_soft
        self.comp_hand_eval = comp_hand_eval
        self.hand_num = hand_num
        self.player_hand = player_hand
        self.player_hand_soft = player_hand_soft
        self.player_hand_list = player_hand_list
        self.player_hand_last = player_hand_last
        self.first_comp_card = first_comp_card
        self.num_of_decks = num_of_decks
        self.deck_list = deck_list

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
        
    def set_player_hand_list(self,added_card):
        self.player_hand_list.append(added_card)
    
    def set_player_hand_last(self,last_card):
        self.player_hand_last = last_card
        
    def set_hand_num(self,new_hand_num):
        self.hand_num += new_hand_num

def draw_card():
    card = str(choice(current_round.deck_list))
    current_round.deck_list.remove(card)
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
    global game
    game = True
    reset_game()
    print "Welcome to Blackjack!"
    print "Rules:"
    print "• Type 'Hit' or 'Stand' at the beginning of each round"
    print "• You'll be given the option to double in your first two turns."
    print "• All face cards are equal 10, with the exception of the Ace which is equal to 1 or 11"
    print "• You'll start with a bankroll of 100"
    how_many_decks()
    return
    
def how_many_decks():
    global game
    while game == True:
        try: 
            current_round.num_of_decks = int(raw_input("How many decks do you want to play with?: (Enter an number greater than one, but less than 10.)"))
            if current_round.num_of_decks not in range(1,10):
                raise ValueError
        except: 
            continue
        else:
            reset_deck()
            new_round()
    return

def play_again_q():
    global game
    answer = ""
    while answer == "":
        try: 
            responce = str(raw_input("Do you want to play again? "))
            if responce.lower() == "yes":
                answer = "yes"
                play()
            elif responce.lower() == "no":
                answer = "no"
                game = False
        except: 
            continue
    return

def new_round():
    if player.bankroll <= 4:
        print "Your bankroll has dropped below $5. You lose!"
        play_again_q()
    else:
        current_round.first_comp_card = 0
        current_round.comp_hand = 0
        current_round.comp_hand_soft = 0
        reset_round_stats()
        comp_play()
        print "new_round else code run"
        
def reset_round_stats():
    print 'round stats reset..'
    current_round.hand_num = 0
    current_round.set_round_num(1)
    current_round.player_hand = 0
    current_round.player_hand_soft = 0
    current_round.player_hand_list = []
    return
    
def place_bet():
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
            hit_stand_double_split()
        return
        
def player_hit(double=True):
    player_card = draw_card()
    current_round.set_player_hand_list(player_card)
#    print current_round.player_hand_list
    print_card(player_card)
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
#            print "Starting the next hand.."
            hit_stand_double_split()
    return

def player_stand():
    print "The dealer's hand: %s" %(current_round.comp_hand_eval)
    if current_round.player_hand_soft > 21:
        eval_hand = current_round.player_hand
    elif current_round.player_hand_soft <= 21:
        eval_hand = current_round.player_hand_soft
    print "Your hand: %s" %(eval_hand)
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

def player_split_set():
    print 'assigning the next first cards...'
    current_round.player_hand_last.append(current_round.player_hand_list[0])
    current_round.deck_list.append(current_round.player_hand_list[0])
    current_round.player_hand_last.append(current_round.player_hand_list[1])
    current_round.deck_list.append(current_round.player_hand_list[1])
    print "Your hand has been split. The round is restarting with your new starter cards."
    reset_round_stats()
    hit_stand_double_split()
    
    
def player_split():
    player_card = current_round.player_hand_last[0]
    current_round.set_player_hand_list(player_card)
    print_card(player_card)
    val = deck_dict[player_card]
# set the cards value
    if player_card == 'Ace':
        current_round.set_player_hand_soft(11)
        current_round.set_player_hand(1)
    else:
        current_round.set_player_hand_soft(val)
        current_round.set_player_hand(val)
    current_round.set_hand_num(1)
    hit_stand_double_split()

    
def hit_stand_double_split():
    global game
    if len(current_round.deck_list) == 0:
        print "You're out of cards!"
        reset_deck()
    if current_round.hand_num == 0 and len(current_round.player_hand_last) > 0:
        print "Starting the round with your split card:"
        player_split()          
    elif current_round.hand_num == 0:
        print "Your first card:"
        player_hit(double=False)
        return
    else:
#        print "asking you for your next move..."
        while game == True:
            try: 
                if (len(current_round.player_hand_list) == 2 and 
                    current_round.player_hand_list[0] == current_round.player_hand_list[1] and
                    current_round.hand_num <= 2 and 
                    player.bet <= player.bankroll):
                    answer = str(raw_input("Do you want to hit, stand, double, or split? "))
                    if answer.lower() == "hit":
                        player_hit(double=False)
                    elif answer.lower() == "stand":
                        player_stand()
                    elif answer.lower() == 'double':
                        player_double()
                    elif answer.lower() == 'split':
                        print 'splitting..'
                        player_split_set()
                
                elif current_round.hand_num <= 1 and player.bet <= player.bankroll:
                    answer = str(raw_input("Do you want to hit, stand or double? "))
                    if answer.lower() == "hit":
                        player_hit(double=False)
                    elif answer.lower() == "stand":
                        player_stand()
                    elif answer.lower() == 'double':
                        player_double()
                else:
                    answer = str(raw_input("Do you want to Hit or stand?" ))
                    if answer.lower() == "hit":
                        player_hit(double=False)
                    elif answer.lower() == "stand":
                        player_stand()            
            except: 
                continue
    return

def comp_play():
    while current_round.comp_hand_soft < 17:    
        comp_card = draw_card()
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
#            print "dealer's hitting"
            if comp_card == 'Ace':
                current_round.set_comp_hand_soft(11)
                current_round.set_comp_hand(1)
            else:
                current_round.set_comp_hand_soft(val)
                current_round.set_comp_hand(val)
    if current_round.comp_hand > 21:
#        print "dealer's card soft is the eval card"
        current_round.set_comp_hand_eval(current_round.comp_hand_soft)
    elif current_round.comp_hand_soft <= current_round.comp_hand:
#        print "dealer's card hard is the eval card"
        current_round.set_comp_hand_eval(current_round.comp_hand)
#    print "comp hand eval: %s" %(current_round.comp_hand_eval)
#    print "comp hand: %s" %(current_round.comp_hand)
    place_bet()

play()