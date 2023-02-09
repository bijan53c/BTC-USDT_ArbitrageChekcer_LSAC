import datetime
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
#--------------------------------------------------------------------------#



#colors 4 texts---------------
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#usage: print(f"{bcolors.WARNING}Warning: No active frommets remain. Continue?{bcolors.ENDC}")


#------------------------------




#user interface welcome
print (f"{bcolors.HEADER}\nWelcom to BRB phase 1\n{bcolors.ENDC}")
print ("-------------------------")
print ("\nBRB starting process pleas wait...")
##----------Browser setting------------------##

# Setting firefox as browser

firefox_options = Options()
firefox_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
browser = webdriver.Firefox(options=firefox_options)

##-------------------------------------------##




################################################
###>> Getting prices<<###

##opening exhanges##
def OpenExchanges():
    # Opening exchange A  website to check USDT price
    browser.get("https://nobitex.ir/app/exchange/btc-usdt/")
    # open new tab
    browser.execute_script("window.open('');")
    #Switch to new tab
    browser.switch_to.window(browser.window_handles[1])
    time.sleep(2)

    # open exchange B for checking USDT price
    browser.get("https://bitpin.ir/trade/BTC_USDT/")
    time.sleep(2)


A_ratio = 0
B_ratio = 0
profit_ratio = 0
##Check prices
def CheckAllPrices():

    global A_ratio , B_ratio , profit_ratio
    #Go back on exchange A tab
    browser.switch_to.window(browser.window_handles[0])
    ## Check price of usdt on A ##
    #There are two types of price , sellers and buyers#
	#They buyers will buy the crypto from you and sellers will sell 2 you, simple
	# So that makes 2 different prices which whole market is about it.
	#Sellers usually sell more expensive and buyers try to buy cheap
    #So we make 2 variables based on all of this story

    #buyers price
    PRICE_Nobi_Buyers = browser.find_element(By.XPATH,"/html/body/div[1]/div/main/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[1]").text
    PRICE_Nobi_Sellers = browser.find_element(By.XPATH,"/html/body/div[1]/div/main/div[2]/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div[1]").text

    #switch to exchange B
    browser.switch_to.window(browser.window_handles[1])
    time.sleep(2)
    #Check price of usdt in B
    PRICE_Bitp_Sellers = browser.find_element(By.XPATH,"/html/body/div[1]/article/div/div/div[1]/div[1]/div/div[1]/div[2]/div[1]/span[4]").text
    PRICE_Bitp_Buyers = browser.find_element(By.XPATH,"/html/body/div[1]/article/div/div/div[1]/div[1]/div/div[2]/div[2]/div[1]/span[4]").text

    #Defining date&time
    TimeNow = datetime.datetime.now()
    #print time , before showing the prices
    print ("\n",TimeNow,"\n")
    #printing prices
    print (f"\n{bcolors.OKGREEN}:$:{bcolors.ENDC} Buyers price {bcolors.OKCYAN}NOBITEX{bcolors.ENDC} = {bcolors.UNDERLINE}%s{bcolors.ENDC}"%PRICE_Nobi_Buyers)
    print (f"\n{bcolors.WARNING}:$:{bcolors.ENDC} Sellers price {bcolors.OKCYAN}NOBITEX{bcolors.ENDC} = {bcolors.UNDERLINE}%s{bcolors.ENDC}"%PRICE_Nobi_Sellers)


    print (f"\n{bcolors.OKGREEN}:$:{bcolors.ENDC} Buyers price {bcolors.OKCYAN}BITPIN{bcolors.ENDC}= {bcolors.UNDERLINE}%s{bcolors.ENDC}"%PRICE_Bitp_Buyers)
    print (f"\n{bcolors.WARNING}:$:{bcolors.ENDC} Sellers price {bcolors.OKCYAN}BITPIN{bcolors.ENDC}= {bcolors.UNDERLINE}%s{bcolors.ENDC}"%PRICE_Bitp_Sellers)

    #Clean prices to use as numbers
    PRICE_Nobi_Buyers = PRICE_Nobi_Buyers.replace(",","")
    PRICE_Nobi_Buyers = float(PRICE_Nobi_Buyers)

    PRICE_Nobi_Sellers = PRICE_Nobi_Sellers.replace(",","")
    PRICE_Nobi_Sellers = float(PRICE_Nobi_Sellers)


    PRICE_Bitp_Sellers = PRICE_Bitp_Sellers.replace(",","")
    PRICE_Bitp_Sellers = float(PRICE_Bitp_Sellers)

    PRICE_Bitp_Buyers = PRICE_Bitp_Buyers.replace(",","")
    PRICE_Bitp_Buyers = float(PRICE_Bitp_Buyers)


    #Ratio counter variables : will show how many buys has happend on each exchange

    #Fees of exchanges(In order A-B-C) in %
    OMPFINEX_FEE_prcnt = 0.35
    NOBITEX_FEE_prcnt = 0.35
    BITPIN_FEE_prcnt = 0.32

    if PRICE_Nobi_Buyers > PRICE_Bitp_Sellers :
        print (f"\n:!: {bcolors.OKGREEN} Arbitrage opportunity detected! {bcolors.ENDC}\n")
        print (f"\n:{bcolors.OKGREEN}${bcolors.ENDC}: Buy on {bcolors.OKCYAN}BITPIN{bcolors.ENDC} , Sell on {bcolors.OKCYAN}NOBITEX{bcolors.ENDC}\nNobiBuys>BitSells")
        B_ratio = A_ratio + 1
        #Calculating difference of prices A to B
        X = PRICE_Nobi_Buyers - PRICE_Bitp_Sellers
        X = X / PRICE_Bitp_Sellers
        DifferencePercent = X * 100

        print (f"\n{bcolors.OKCYAN}:::{bcolors.ENDC}There is {bcolors.OKBLUE}%s percent profit {bcolors.ENDC}in this trade"%str(DifferencePercent))
        #show and calculate if the trade is profitable
        overallFEEprcnt = BITPIN_FEE_prcnt + NOBITEX_FEE_prcnt
        PROFITprcnt = DifferencePercent - overallFEEprcnt
        if PROFITprcnt > 0 :
            print (f"\n {bcolors.OKGREEN}:$: Profitable trade{bcolors.ENDC} \n")
            profit_ratio = profit_ratio + 1
        else :
            print (f"\n {bcolors.FAIL}:$!: This trade won't be profitable.{bcolors.ENDC}")
            print ("Overall fee (prcnt): ",overallFEEprcnt," --- profit(percent): ",PROFITprcnt)



    if PRICE_Bitp_Buyers > PRICE_Nobi_Sellers :
        print (f"\n:!: {bcolors.OKGREEN} Arbitrage opportunity detected! {bcolors.ENDC}\n")
        print (f"\n:{bcolors.OKGREEN}${bcolors.ENDC}: Buy on {bcolors.OKCYAN}NOBITEX{bcolors.ENDC} , Sell on {bcolors.OKCYAN}BITPIN{bcolors.ENDC}\nBitpBuys>NobiSells")
        A_ratio= A_ratio + 1
        #Calculating difference of prices B to A
        X = PRICE_Bitp_Buyers - PRICE_Nobi_Sellers
        X = X / PRICE_Nobi_Sellers
        DifferencePercent = X * 100
        print (f"\n{bcolors.OKCYAN}:::{bcolors.ENDC}There is {bcolors.OKBLUE}%s percent profit{bcolors.ENDC} in this trade"%DifferencePercent)

        #show and calculate if the trade is profitable
        overallFEEprcnt = BITPIN_FEE_prcnt + NOBITEX_FEE_prcnt
        PROFITprcnt = DifferencePercent - overallFEEprcnt
        if PROFITprcnt > 0 :
            print (f"\n{bcolors.OKGREEN}:$: Profitable trade{bcolors.ENDC}\n")
            profit_ratio = profit_ratio + 1
        else :
            print (f"\n{bcolors.FAIL}:$!: This trade won't be profitable.{bcolors.ENDC}")
            print ("Overall fee (prcnt): ",overallFEEprcnt," --- profit(percent): ",PROFITprcnt)
            #




    print ("\nopportunities buy ratio on each exchange in seconds: \nNobitex: ",A_ratio," -- BITPIN: ",B_ratio," -- $Profit-Ratio: ",profit_ratio)


OpenExchanges()
time.sleep(5)

print (":: Testing functions...")

try :
    CheckAllPrice()
    pass
except :
    print (f"{bcolors.FAIL}!: Program might face errors in main functions{bcolors.ENDC}")
    pass



# Checking prices every second
while True :
    CheckAllPrices()
    print ("\n ...\n")
    time.sleep(1)

