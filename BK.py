import random

RANK,SUIT = 0,1

def win_lose(dealer_hand,player_hand,bet,player_money):
    player_point = get_point(player_hand)
    dealer_point = get_point(dealer_hand)
    if player_point <=21 :
        if(player_point > dealer_point) or (dealer_point > 21):
            if player_point == 21 :
                return('<<Player Win>>',player_money + int(bet * 2.5))
            else :
                return('<<Player Win>>',player_money + 2*bet)
        elif player_point == dealer_point :
            return('<<Push>>',player_money + bet)
        else :
            return('<<Player Lose>>',player_money)
    else:
        return('<<Player Lose>>',player_money)
        
def player_op(deck,player_hand,op):
    doubled,ending = False,False
    
    if op =='1':
        print('[プレイヤー：スタンド]')
        doubled,ending=False,True
            
            #ここにスタンドの処理
    elif op == '2':
        print('[プレイヤー：ヒット]')
        player_hand.append(deck.pop())
        print_player_hand(player_hand)
        doubled,ending = False,False
            
    elif op == '3':
        if len(player_hand) == 2 :
            print('[プレイヤー：ダブル]')
            player_hand.append(deck.pop())
            print_player_hand(player_hand)
            doubled,ending = True,True
        else:
            print('ダブルはできません。')
            
    if get_point(player_hand) > 21: #バースト判定
        print('[プレイヤーはバーストした！]')
        ending = True
        
    elif get_point(player_hand)==21:
        print('21です！')
        ending = True
    
    return doubled,ending        

def dealer_op(deck,player_hand,dealer_hand):
    while get_point(player_hand) <= 21:
        if get_point(dealer_hand) >= 17:
            print('[ディーラー：スタンド]')
            break
        else:
            print('[ディーラー：ヒット]')
            dealer_hand.append(deck.pop())
        print_dealer_hand(dealer_hand,False)
        
def get_point(hand):
    result = 0
    ace_flag = False
    
    for card in hand:
        if card[RANK] == 1:
            ace_flag = True
        if card[RANK] > 10 :
            num = 10
        else:
            num = card[RANK]
        result = result + num
    if ace_flag and result <=11:
        result += 10
    return result

def print_player_hand(player_hand):
    print('プレイヤー(',get_point(player_hand),'):')
    for card in player_hand:
        print('[',card[SUIT],card[RANK],']')
    print()
   
def print_dealer_hand(dealer_hand,uncovered):
    if uncovered :
        print('ディーラー(',get_point(dealer_hand),'):')
    else:
        print('ディーラー(??):    ')
    flag = True
    for card in dealer_hand:
        if flag or uncovered:
            print('[',card[SUIT],card[RANK],']')
            flag = False
        else:
            print('[* *]')
        print()

def make_deck():
    suits = ['S','H','D','C']
    ranks = range(1,14)
    deck = [(x,y) for x in ranks for y in suits]
    random.shuffle(deck)
    return deck

def main():
    turn = 1
    player_money = 100
    deck = make_deck()
    
    while(player_money>0):
        
        #ターンの初めにターン数と所持金の情報を表示
        print('-'*20) #区切り線を作る
        print('ターン：',turn)
        print('所持金：',player_money)
        print('-'*20) #区切り線を作る
        
        player_hand = []
        dealer_hand = []
        
        
        #bet = 10
        try :
            bet = int(input('ベット額 >'))
        except:
            print('整数で入力ください')
            continue
        #入力値が所持金を超えていたらやり直し
        if bet > player_money :
            print('所持金が不足しています')
            continue
        #入力値が０より小さかったらやり直し
        elif bet <= 0:
            print('ベットできる額は１以上です')
            continue
        
        player_money -= bet
        #デッキの残りが１０枚以下ならデッキを再構築＆シャッフル
        if len(deck) <10:
            deck = make_deck()
                    
        for i in range(2):
            player_hand.append(deck.pop())
            dealer_hand.append(deck.pop())
    
        #手札の情報を表示
        print('-'*20) #区切り線を作る
        print_player_hand(player_hand)
        print_dealer_hand(dealer_hand,False) #本来はTrueだが、Falseにしておく
        print('-'*20) #区切り線を作る
           
        #プレイヤーターン
    
        while True :
            op = input('スタンド：1,ヒット：2,ダブル：3>')
            doubled, ending = player_op(deck,player_hand,op)
            if doubled: #ダブルした時の処理
                player_money -= bet
                bet += bet
            if ending : #ターン終了時の処理
                break
        
        #ディーラーターン
        dealer_op(deck,player_hand,dealer_hand)
        
        print('-'*20) #区切り線を作る
        print_player_hand(player_hand)
        print_dealer_hand(dealer_hand,True)
        print('-'*20) #区切り線を作る
        
        message,player_money = win_lose(dealer_hand,player_hand,bet,player_money)
        print(message)
        
        turn += 1
        input('次のターンへ')
    print('ゲームオーバー')
         
if __name__ == '__main__':
    main()
    