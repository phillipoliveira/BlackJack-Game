from random import choice

class Cards(object):
    def __init__(self,num_of_decks=0,deck_list=[],deck_dict={'2':2,'3':3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"Jack":10,"Queen":10,"King":10,"Ace":1}):
        self.num_of_decks = num_of_decks
        self.deck_list = deck_list
        self.deck_dict = deck_dict
        self.game_functions = Game_functions()
        
    def set_num_of_decks(self,new_num_of_decks):
        self.num_of_decks = new_num_of_decks
    

    def draw_card(self):
        card = str(choice(self.deck_list))
        self.deck_list.remove(card)
        return card

    def print_card(self,card):
        print " _______"
        print "|       |"
        print "|       |"
        print "|%s|" %(card.center(7))
        print "|       |"
        print "|_______|"
        return

    def reset_deck(self,num_of_decks):
        print "Shuffling the deck..."
#        print self.num_of_decks
        self.deck_list = ['2','3',"4","5","6","7","8","9","10","Jack","Queen","King","Ace"]*4*self.num_of_decks
        
    def how_many_decks(self,game=True):
        while game == True:
            try: 
                new_num_of_decks = int(raw_input("How many decks do you want to play with?: (Enter an number greater than one, but less than 10.)"))
                if new_num_of_decks not in range(1,10):
                    raise ValueError
            except: 
                continue
            else:
                self.set_num_of_decks(new_num_of_decks)
                print "deck num = %s" %(self.num_of_decks)
                self.reset_deck(self.num_of_decks)
                self.game_functions.new_round()
        return 

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
    
class Round_stats(object):
    def __init__(self,comp_hand=0,comp_hand_soft=0,player_hand=0,player_hand_soft=0,hand_num=0,player_hand_list=[],player_hand_last=[],comp_hand_eval=0,first_comp_card=0,num_of_decks=0,deck_list=[]):
        self.comp_hand = comp_hand
        self.comp_hand_soft = comp_hand_soft
        self.comp_hand_eval = comp_hand_eval
        self.hand_num = hand_num
        self.player_hand = player_hand
        self.player_hand_soft = player_hand_soft
        self.player_hand_list = player_hand_list
        self.player_hand_last = player_hand_last
        self.first_comp_card = first_comp_card

    def reset_game(self):
        self.comp_hand = 0
        self.comp_hand_soft = 0
        self.comp_hand_eval = 0
        self.hand_num = 0
        self.player_hand = 0
        self.player_hand_soft = 0
        self.player_hand_list = []
        self.player_hand_last = []
        self.first_comp_card = 0

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
        self.player_hand_last.append(last_card)
        
    def set_hand_num(self,new_hand_num):
        self.hand_num += new_hand_num

class Game_functions(object):
    def __init__(self,game = True):
        self.game = True

    def play(self):
        self.game = True
        bjroundstats.reset_game()
        print "Welcome to Blackjack!"
        print "Rules:"
        print "• Type 'Hit' or 'Stand' at the beginning of each round"
        print "• You'll be given the option to double in your first two turns."
        print "• All face cards are equal 10, with the exception of the Ace which is equal to 1 or 11"
        print "• You'll start with a bankroll of 100"
        bjcards.how_many_decks(game=True)
        return

    def play_again_q(self):
        answer = ""
        while answer == "":
            try: 
                responce = str(raw_input("Do you want to play again? "))
                if responce.lower() == "yes":
                    answer = "yes"
                    self.play()
                elif responce.lower() == "no":
                    answer = "no"
                    self.game = False
            except: 
                continue
        return

    def new_round(self):
        if bjplayer.bankroll <= 4:
            print "Your bankroll has dropped below $5. You lose!"
            self.play_again_q()
        else:
            bjroundstats.first_comp_card = 0
            bjroundstats.comp_hand = 0
            bjroundstats.comp_hand_soft = 0
            self.reset_round_stats()
            self.comp_play()
            
    def reset_round_stats(self):
        bjroundstats.hand_num = 0
        bjroundstats.player_hand = 0
        bjroundstats.player_hand_soft = 0
        bjroundstats.player_hand_list = []
        return

    def place_bet(self):
        print "The dealer card:"
        bjcards.print_card(str(bjroundstats.first_comp_card))
        bjplayer.bet = "" 
        while bjplayer.bet == "":
            try: 
                bet = int(raw_input("Place your bet! Enter a number less than your current bankroll (%s). Minimum bet = $5 " %(bjplayer.bankroll)))
                bjplayer.bet = bet
                if bet > bjplayer.bankroll:
                    raise ValueError
                elif bet < 5:
                    raise ValueError
            except: 
                continue
            else:
                self.hit_stand_double_split()
            return
        
    def player_hit(self,double=True):
        player_card = bjcards.draw_card()
        bjroundstats.set_player_hand_list(player_card)
#        print bjroundstats.player_hand_list
        bjcards.print_card(player_card)
        val = bjcards.deck_dict[player_card]
    # set the cards value
        if player_card == 'Ace':
            bjroundstats.set_player_hand_soft(11)
            bjroundstats.set_player_hand(1)
        else:
            bjroundstats.set_player_hand_soft(val)
            bjroundstats.set_player_hand(val)
    # calculate the player hand and determine if they won.
#        print "Your hand: %s" %(bjroundstats.player_hand)
        if bjroundstats.player_hand > 21:
            print "Bust!"
            bjplayer.adjust_bankroll((bjplayer.bet),add=False)
            print "Your bankroll: %s" %bjplayer.bankroll
            print "Starting the next round..."
            self.new_round()
        else:
            bjroundstats.set_hand_num(1)
            if double == True:
                self.player_stand()
            elif double == False:
#                print "Starting the next hand.."
                self.hit_stand_double_split()
        return

    def player_stand(self):
        print "The dealer's hand: %s" %(bjroundstats.comp_hand_eval)
        if bjroundstats.player_hand_soft > 21:
            eval_hand = bjroundstats.player_hand
        elif bjroundstats.player_hand_soft <= 21:
            eval_hand = bjroundstats.player_hand_soft
        print "Your hand: %s" %(eval_hand)
        if  bjroundstats.comp_hand_eval > 21:
            print "The dealer busted!. Your winnings: %s" %(bjplayer.bet*2)
            bjplayer.adjust_bankroll((bjplayer.bet*2),add=True) 
        elif eval_hand > bjroundstats.comp_hand_eval:
            print "You win the round!. Your winnings: %s" %(bjplayer.bet*2)
            bjplayer.adjust_bankroll((bjplayer.bet*2),add=True)
        elif eval_hand == bjroundstats.comp_hand_eval:
            print "Stand off!. Your winnings: %s" %(bjplayer.bet)
            bjplayer.adjust_bankroll((bjplayer.bet),add=True)                                                                                            
        elif eval_hand < bjroundstats.comp_hand_eval:
            print "You lose the round!"
            bjplayer.adjust_bankroll((bjplayer.bet),add=False)
        print "Your bankroll: %s" %bjplayer.bankroll
        print "Starting the next round..."
        self.new_round()
        return

    def player_double(self):
        bjplayer.bet = (bjplayer.bet*2)
        self.player_hit(double=True)
        return

    def player_split_set(self):
#        print 'assigning the next first cards...'
        bjroundstats.player_hand_last.append(bjroundstats.player_hand_list[0])
        bjcards.deck_list.append(bjroundstats.player_hand_list[0])
        bjroundstats.player_hand_last.append(bjroundstats.player_hand_list[1])
        bjcards.deck_list.append(bjroundstats.player_hand_list[1])
#        print "your hand is clear"
        print "Your hand has been split. The round is restarting with your new starter cards."
        self.reset_round_stats()
        self.hit_stand_double_split()
        
        
    def player_split(self):
        player_card = bjroundstats.player_hand_last[0]
        bjroundstats.player_hand_last.pop()
        bjroundstats.set_player_hand_list(player_card)
        bjcards.print_card(player_card)
        val = bjcards.deck_dict[player_card]
    # set the cards value
        if player_card == 'Ace':
            bjroundstats.set_player_hand_soft(11)
            bjroundstats.set_player_hand(1)
        else:
            bjroundstats.set_player_hand_soft(val)
            bjroundstats.set_player_hand(val)
        bjroundstats.set_hand_num(1)
        self.hit_stand_double_split()

        
    def hit_stand_double_split(self):
        if len(bjcards.deck_list) == 0:
            print "You're out of cards!"
            bjcards.reset_deck(bjcards.num_of_decks)
        if bjroundstats.hand_num == 0 and len(bjroundstats.player_hand_last) > 0:
            print "Starting the round with your split card:"
            self.player_split()          
        elif bjroundstats.hand_num == 0:
            print "Your first card:"
            self.player_hit(double=False)
            return
        else:
#            print "asking you for your next move..."
            while self.game == True:
                try: 
                    if (len(bjroundstats.player_hand_list) == 2 and 
                        bjroundstats.player_hand_list[0] == bjroundstats.player_hand_list[1] and
                        bjroundstats.hand_num <= 2 and 
                        bjplayer.bet <= bjplayer.bankroll):
                        answer = str(raw_input("Do you want to hit, stand, double, or split? "))
                        if answer.lower() == "hit":
                            self.player_hit(double=False)
                        elif answer.lower() == "stand":
                            self.player_stand()
                        elif answer.lower() == 'double':
                            self.player_double()
                        elif answer.lower() == 'split':
#                            print 'splitting..'
                            self.player_split_set()
                    
                    elif bjroundstats.hand_num <= 1 and bjplayer.bet <= bjplayer.bankroll:
                        answer = str(raw_input("Do you want to hit, stand or double? "))
                        if answer.lower() == "hit":
                            self.player_hit(double=False)
                        elif answer.lower() == "stand":
                            self.player_stand()
                        elif answer.lower() == 'double':
                            self.player_double()
                    else:
                        answer = str(raw_input("Do you want to Hit or stand?" ))
                        if answer.lower() == "hit":
                            self.player_hit(double=False)
                        elif answer.lower() == "stand":
                            self.player_stand()            
                except: 
                    continue
        return

    def comp_play(self):
        while bjroundstats.comp_hand < 17:
            if len(bjcards.deck_list) == 0:
#                print "You're out of cards!"
                bjcards.reset_deck(bjcards.num_of_decks) 
            comp_card = bjcards.draw_card()
            val = bjcards.deck_dict[comp_card]
#            print "comp card drawn"
#            print "val type: %s" %(type(val))
            if bjroundstats.comp_hand_soft == 0:
#                print "setting first comp card"
                bjroundstats.set_first_comp_card(comp_card)
                if comp_card == 'Ace':
                    bjroundstats.set_comp_hand_soft(11)
                    bjroundstats.set_comp_hand(1)
                else:
                    bjroundstats.set_comp_hand_soft(val)
                    bjroundstats.set_comp_hand(val)
            else:
#                print "dealer's hitting"
                if comp_card == 'Ace':
                    bjroundstats.set_comp_hand_soft(11)
                    bjroundstats.set_comp_hand(1)
                else:
                    bjroundstats.set_comp_hand_soft(val)
                    bjroundstats.set_comp_hand(val)
        if bjroundstats.comp_hand_soft > 21:
#            print "dealer's card hard is the eval card"
            bjroundstats.set_comp_hand_eval(bjroundstats.comp_hand)
        elif bjroundstats.comp_hand <= bjroundstats.comp_hand_soft:
#            print "dealer's card soft is the eval card"
            bjroundstats.set_comp_hand_eval(bjroundstats.comp_hand_soft)
#        print "comp hand eval: %s" %(bjroundstats.comp_hand_eval)
#        print "comp hand: %s" %(bjroundstats.comp_hand)
        self.place_bet()

bjroundstats = Round_stats()
bjplayer = Player()  
bjcards = Cards()
startgame = Game_functions()
startgame.play()