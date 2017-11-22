import random

class Cards(object):

    suits = ('Hearts', 'Spades', 'Diamonds', 'Clubs')
    rankings = ('Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King')
    deck_dict = {'Ace':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10, 'Queen':10, 'King':10}

    def __init__(self,num_of_decks="",deck_list=[],deck=[]):
        self.num_of_decks = num_of_decks
        self.deck_list = deck_list 
        self.deck = deck
        
    def set_deck(self):
        deck = []
        for suit in self.suits:
            for rank in self.rankings:
                deck.append((suit,rank))
        self.deck = deck*self.num_of_decks
        return
                
    def shuffle(self):
        random.shuffle(self.deck)
        return
        
# Use self.deck.pop() to draw cards.
        
    def print_card(self,card):
        print " ________"
        print "|        |"
        print "|%s|" %(card[1].center(8))
        print "|%s|" %("of".center(8))
        print "|%s|" %(card[0].center(8))
        print "|________|"
        return
                
class Player(object):
    
    cards = Cards()
        
    def __init__(self,hand=[],bet=0,bankroll=100,split_hand=[]):
        self.hand = hand
        self.bet = bet
        self.bankroll = bankroll
        self.split_hand = split_hand
        
    def reset_stats(self):
        self.hand = []
        self.bet = 0
        return
        
    def hand_val(self):
        val = 0
        for x, y in self.hand:
            val += self.cards.deck_dict[y]
        for x, y in self.hand:
            if y == 'Ace':
                if val + 10 <= 21:
                    val += 10
        return val
            
    def check_bust(self):
        if self.hand_val() > 21:
            return True
        return
        
    def double(self):
        new_bet = self.bet*2
        self.bet = new_bet
        return
        
        
class Game(object):
    
    comp = Player()
    player = Player()
    cards = Cards()
    
    def __init__(self,game=True,hand_num=0):
        self.game = True
        self.hand_num = hand_num
        
    def play(self):
        self.game = True
        print "Welcome to Blackjack!"
        print "Rules:"
        print "• Type 'Hit' or 'Stand' at the beginning of each round"
        print "• You'll be given the option to double in your first two turns."
        print "• All face cards are equal 10, with the exception of the Ace which is equal to 1 or 11"
        print "• You'll start with a bankroll of 100"
        self.how_many_decks()
        return
    
    def new_round(self):
        if self.player.bankroll <= 4:
            print "Your bankroll has dropped below $5. You lose!"
            self.play_again_q()
        else:
            self.game = True
            self.hand_num = 0
            self.cards.set_deck()
            self.cards.shuffle()
            self.player.reset_stats()
            self.comp.reset_stats()
            self.comp_logic()
            self.comp.hand_val()
        return

    def new_game(self):
        self.player.bankroll = 100
        self.player.split_hand = []
        self.cards.num_of_decks=""
        self.cards.deck_list=[]
        self.cards.deck=[]
        self.game.play()
        return
    
    def how_many_decks(self):
        while self.cards.num_of_decks == "":
            try: 
                num_of_decks = int(raw_input("How many decks do you want to play with?: (Enter an number greater than one, but less than 10.)"))
                self.cards.num_of_decks = num_of_decks
                if self.cards.num_of_decks not in range(1,10):
                    raise ValueError
            except: 
                self.cards.num_of_decks = ""
            else:
                print "starting new round..."
                self.new_round()
        return        
    
    def place_bet(self):
        print "The dealer card:"
        self.cards.print_card(self.comp.hand[0]) 
        while self.player.bet == 0:
            try: 
                bet = int(raw_input("Place your bet! Enter a number less than your current bankroll (%s). Minimum bet = $5 " %(self.player.bankroll)))
                if bet > self.player.bankroll:
                    raise ValueError
                elif bet < 5:
                    raise ValueError
                else:
                    self.player.bet = bet
                    print "-----------------------------------"
                    self.hit_stand_double_split()
            except: 
                continue
            return
        
    def comp_logic(self):
        while self.comp.hand_val() < 17:
            self.comp.hand.append(self.cards.deck.pop())
        else:
            self.place_bet()
        return
    
    def hit_stand_double_split(self):
        while self.game == True:
            self.hand_num += 1
            if len(self.cards.deck) == 0:
                print "You're out of cards!"
                self.cards.set_deck()
            if len(self.player.split_hand) > 0 and self.hand_num == 1:
                print "Starting a new round with your split hand:"
                card = self.player.split_hand.pop(0)
                self.player.hand.append(card)
                self.cards.print_card(card)    
            elif self.hand_num == 1:
                print "Your first card:"
                card = self.cards.deck.pop()
                self.player.hand.append(card)
                self.cards.print_card(card)
            else: 
                option = ['hit','stand']
                if len(self.player.hand) == 1 and self.player.bet <= self.player.bankroll:
                    option.append('double')                
                if (len(self.player.hand) == 2 and 
                    self.player.hand[0][1] == self.player.hand[1][1]):
                    option.append('split')  
                try:
                    answer = str(raw_input("Choose an option: %s " %(option)))        
                    if option.count(answer) != 0:
                        if answer.lower() == "hit":
                            self.hit_func(double=False)
                        elif answer.lower() == "stand":
                            self.stand_func()
                        elif answer.lower() == 'double':
                            self.double_func()
                        elif answer.lower() == 'split':
                            self.split_func()
                    else:
                        raise ValueError
                except: 
                    continue
        return            
        
    def hit_func(self,double=False):
        card = self.cards.deck.pop()
        self.player.hand.append(card)
        self.cards.print_card(card)
        if self.player.check_bust():
            print "Bust!"
            self.player.bankroll -= self.player.bet
            print "Your bankroll: %s" %self.player.bankroll
            print "Starting the next round..."
            self.new_round()
        else:
            if double == False:
                self.hit_stand_double_split()
            else: 
                self.stand_func()
        return
                                
    def stand_func(self):
        print "Your hand: %s" %(self.player.hand_val())
        print "The dealer's hand: %s" %(self.comp.hand_val())
        if self.comp.check_bust():
            print "The dealer busted!. Your winnings: %s" %(self.player.bet*2)
            self.player.bankroll += self.player.bet*2   
        elif self.player.hand_val() > self.comp.hand_val():
            print "You win the round!. Your winnings: %s" %(self.player.bet*2)
            self.player.bankroll += self.player.bet*2                              
        elif self.player.hand_val() <= self.comp.hand_val():
            print "You lose the round!"
            self.player.bankroll -= self.player.bet
        print "Starting the next round..."
        self.new_round()
        return
    
    def double_func(self):
        self.player.double()
        self.hit_func(double=True)
        return
    
    def split_func(self):
        self.player.split_hand = self.player.hand
        self.player.hand = []
        self.hand_num = 0
        
        return
                                 
    def play_again_q(self):
        self.game = False
        answer = ""
        while answer == "":
            try: 
                responce = str(raw_input("Do you want to play again? "))
                if responce.lower() == "yes":
                    answer = "yes"
                    self.new_game()
                elif responce.lower() == "no":
                    answer = "no"
            except:
                continue
        return                                 
        
startgame = Game()
startgame.play()