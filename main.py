from pynput. keyboard import Key, Controller
from python_imagesearch.imagesearch import imagesearch
import pyautogui, threading, time, keyboard


__click_thread__ = 4
__click_hyper_thread__ = 5

class Bot:
    def __init__(self):
        self.hyper_thread = False
        self.clicking = False
        self.coin_thread = False
        self.upgrade_thread = False

        self.keyboard = Controller()

        threading.Thread(target= self.check_for_upgrade).start()
        threading.Thread(target= self.coin_get).start()
        for _ in range(__click_thread__):
            threading.Thread(target= self.click_thread).start()

    def click_thread(self, temp: bool= False):
        while True:
            if not temp:
                while self.clicking:
                    pyautogui.click()
                time.sleep(1)
            else:
                while self.hyper_thread:
                    pyautogui.click()
    
    def coin_get(self):
        found = 0
        no_coin = 0

        while True:
            while self.coin_thread:
                pos = imagesearch("img/coin.png")
            
                if pos[0] != -1:
                    found += 1
                    print(f'[CoinGet] Found coin #{found} at {pos[0]},{pos[1]}')
                    pyautogui.moveTo(pos[0], pos[1])
                    
                    if no_coin >= 5:
                        print(f'[CoinGet] Coin found, hyper-threading mode: OFF')
                        self.hyper_thread = False
                    
                    no_coin = 0
                else:
                    no_coin += 1

                    if no_coin == 5:
                        print(f'[CoinGet] 5s without coin, hyper-threading mode: ON (force: {__click_hyper_thread__})')
                        self.hyper_thread = True

                        for _ in range(__click_hyper_thread__):
                            threading.Thread(target= self.click_thread, args=[True]).start()
                    
                    time.sleep(1)
            time.sleep(1)

    def check_for_upgrade(self):
        while True:
            while self.upgrade_thread:
                time.sleep(30)
                print(f'[Upgrader] Looking for heroes upgrade')

                self.hyper_thread = False
                self.coin_thread  = False
                self.clicking = False

                upgraded = 0

                while upgraded != 10:
                    pos = imagesearch("img/max_ok.png")
                    
                    if pos[0] != -1:
                        upgraded += 1

                        print(f'[Upgrader] Found upgrade #{upgraded}/10 at {pos[0]},{pos[1]}')
                        
                        for i in range(3):
                            print(f'[Upgrader] Try to upgrade #{i}/3 --> #{upgraded}/10')
                            pyautogui.click(pos[0], pos[1])
                    else:
                        print('[Upgrader] 0 Upgrades found')
                        break

                print(f'[Upgrader] try switching new map')
                pyautogui.click(1731, 302)

                pos = imagesearch("img/bonus1.png")
                    
                if pos[0] != -1:
                    print(f'[Upgrader] Try the Bonus 1')
                    pyautogui.click(pos[0], pos[1])

                self.coin_thread = True
                self.clicking = True 
            time.sleep(1)

    def start(self):
        while True:
            time.sleep(0.5)
            if keyboard.is_pressed('a'):
                if self.clicking == False and self.coin_thread == False and self.upgrade_thread == False:
                    self.clicking = True
                    self.coin_thread = True
                    self.upgrade_thread = True
                else:
                    self.clicking = False
                    self.coin_thread = False
                    self.hyper_thread = False
                    self.upgrade_thread = False
                
                print(f'[Clicker: {self.clicking}] [CoinGet: {self.coin_thread}] [HyperThread: {self.hyper_thread}] [Upgrade: {self.upgrade_thread}]')

Bot().start()