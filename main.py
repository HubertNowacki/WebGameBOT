import time

from tkinter import *

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class PokeWarsBOT:

    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Handles the browser and UI
    def main_handler(self):
        self.driver.get('chrome://settings/')
        self.driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.67);')
        self.driver.get('game url here')
        
        # Everything for the simplest of simplest UIs below mainly the text boxes to input the location name
        # and how many stamina pots we want to use and the button to run the bot so the user doesn't need to run
        # the code and open a new browser everytime the bot finishes its job.
        self.pwbot = Tk()
        self.pwbot.geometry("200x300")
        self.pwbot.title("PokeWars BOT")

        Button(self.pwbot, text="Odpal BOTA!", font='arial 15 bold', bg='purple', padx=2, command=self.bot_body).place(
            x=20, y=100)
        Button(self.pwbot, text="Zaloguj!", font='arial 15 bold', bg='purple', padx=2, command=self.zaloguj).place(x=20,
                                                                                                                  y=30)
        self.text_enter_lokacja = StringVar(self.pwbot, value="Wpisz nazwe lokacji")
        self.enter_lokacja = Entry(self.pwbot, width=25, textvariable=self.text_enter_lokacja).place(x=32, y=160)

        self.text_enter_drinki = StringVar(self.pwbot, value="Wpisz ilość drinków")
        self.enter_drinki = Entry(self.pwbot, width=25, textvariable=self.text_enter_drinki).place(x=32, y=200)

        self.pwbot.mainloop()

    # Function that logs the player in.
    def zaloguj(self):
        login = self.driver.find_element("xpath", '//*[@name="login"]')
        login.send_keys("Email here")

        password = self.driver.find_element("xpath", '//*[@name="pass"]')
        password.send_keys("Password Here")

        login_btn = self.driver.find_element("xpath", '//*[@name="zaloguj"]')
        login_btn.click()

    # The main body of the bot
    def bot_body(self):
        self.driver.find_element("xpath", '//*[@title="Poluj w ' + str(self.text_enter_lokacja.get()) + '"]').click()
        drink = 0

        while drink < int(self.text_enter_drinki.get()):

            # Checks if the pokemon xpath is present if yes starts a fight if not checks for ability to restore
            # stamina if this is not present too it means that we found nothing, so it keeps skipping until one of
            # the 2 above (the code on site is crappy so we have like 5 different xpaths for the same button)
            while not self.driver.find_elements("xpath", '//*[@name="poke_163301562"]'):
                if self.driver.find_elements("xpath", '//*[@onclick="drinkOak();"]'):
                    self.driver.find_element("xpath", '//*[@onclick="drinkOak();"]').click()
                    time.sleep(0.3)
                    drink += 1
                    self.driver.find_element("xpath", '//*[@name="poluj"]').click()
                elif self.driver.find_elements("xpath", '//*[@value="Dalsza wędrówka"]'):
                    self.driver.find_element("xpath", '//*[@value="Dalsza wędrówka"]').click()
                elif self.driver.find_elements("xpath", '//*[@value="Dalsza wyprawa"]'):
                    self.driver.find_element("xpath", '//*[@value="Dalsza wyprawa"]').click()
                elif self.driver.find_elements("xpath", '//*[@value="Poluj dalej"]'):
                    self.driver.find_element("xpath", '//*[@value="Poluj dalej"]').click()
                elif self.driver.find_elements("xpath", '//*[@value="Szukaj dalej"]'):
                    self.driver.find_element("xpath", '//*[@value="Szukaj dalej"]').click()
                else:
                    self.driver.find_element("xpath", '//*[@name="poluj"]').click()

            self.driver.find_element("xpath", '//*[@name="poke_163301562"]').click()

            # Handles everything after the fight: the ball usage, check for items
            self.driver.find_element("xpath", '//*[@name="pokeball_Netball"]').click()

            if self.driver.find_elements("xpath", '//*[@name="pokeball_Levelball"]'):
                self.driver.find_element("xpath", '//*[@name="pokeball_Levelball"]').click()

            if self.driver.find_elements("xpath", '//*[@name="zdejmij_przedmioty"]'):
                self.driver.find_element("xpath", '//*[@name="zdejmij_przedmioty"]').click()

            # Checks for our reserve if it's full then sells all pokemon and continues looping through the location
            if int(self.driver.find_element("xpath", '//*[@class="rezerwa-count"]').text) == 30:
                self.driver.find_element("xpath", '//*[@id="sell_all_btn"]').click()
                self.driver.find_element("xpath", '//*[@class="vex-dialog-button-primary '
                                                  'vex-dialog-button vex-first"]').click()
                time.sleep(0.5)
                self.driver.find_element("xpath", '//*[@title="Poluj w ' +
                                         str(self.text_enter_lokacja.get()) + '"]').click()
            else:
                self.driver.find_element("xpath", '//*[@name="poluj"]').click()


bot = PokeWarsBOT()
bot.main_handler()
