from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep


class Ebay_Selenium:
    def __init__(self, proxy_ip=None):
        if proxy_ip != None:
            proxy = Proxy({
                "proxyType": ProxyType.MANUAL,
                "httpProxy": proxy,
                "ftpProxy": proxy,
                "sslProxy": proxy,
                "noProxy": ""
            })
            self.driver = webdriver.Firefox(proxy=proxy)
        else:
            self.driver = webdriver.Firefox()
        return

    def Login(self, username, password):
        self.driver.get("https://www.ebay.com/signin")
        element = self.driver.find_elements_by_xpath(
            u"//div[@class='signin-view-container']/div")
        self.moveToClick(element[0])
        self.keyIn(username)
        self.moveToClick(element[1])
        self.keyIn(password)
        self.moveToClick(
            self.driver.find_element_by_xpath(u"//*[@id='sgnBt']"))
        sleep(5)
        rtnMsg = {}
        try:
            self.driver.find_element_by_xpath(
                u"//span[@class='inline-notice__status']/span")
            rtnMsg["stat"] = "error"
            rtnMsg["msg"] = "Can't login."
        except Exception:
            rtnMsg["stat"] = "ok",
            rtnMsg["msg"] = "Login success."
        return rtnMsg

    def Buy(self, url):
        self.driver.get(url)
        rtnMsg = {}
        try:
            self.moveToClick(self.driver.find_element_by_xpath(
                u"//div[@class='u-flL']"))  # Buy it now
            self.moveToClick(self.driver.find_element_by_xpath(
                "//span[@id='spn_v4-2']"))  # Commit to buy
            self.moveToClick(self.driver.find_element_by_xpath(
                "//span[@id='spn_v4-1']"))  # Pay now
            rtnMsg["stat"] = "ok"
            rtnMsg["msg"] = "Already buy this."
        except Exception:
            try:
                self.driver.get(url)
                self.moveToClick(self.driver.find_element_by_xpath(
                    "//a[@id='msgPanel_pr']"))  # Pay now
                rtnMsg["stat"] = "ok"
                rtnMsg["msg"] = "Already buy this."
            except Exception as e:
                rtnMsg["stat"] = "error",
                rtnMsg["msg"] = "Can't buy, {}.".format(e)
        return rtnMsg

    def Payment(self, method="card", **kwargs):
        rtnMsg = {}
        try:
            targets = self.driver.find_elements_by_xpath(u"//span/input")
        except Exception as e:
            rtnMsg["stat"] = "error"
            rtnMsg["msg"] = e
            return
        if method == "card":
            self.moveToClick(targets[0])  # Credit card / Debit card
            sleep(3)
            try:
                self.moveToClick(self.driver.find_element_by_xpath(
                    u"//input[@id='cardNumber']"))
                self.keyIn(kwargs["card"])
                self.moveToClick(self.driver.find_element_by_xpath(
                    u"//input[@id='cardExpiryDate']"))
                self.keyIn(kwargs["date"])
                self.moveToClick(self.driver.find_element_by_xpath(
                    u"//input[@id='securityCode']"))
                self.keyIn(kwargs["code"])
                self.moveToClick(self.driver.find_element_by_xpath(
                    u"//input[@id='cardHolderFirstName']"))
                self.keyIn(kwargs["first_name"])
                self.moveToClick(self.driver.find_element_by_xpath(
                    u"//input[@id='cardHolderLastName']"))
                self.keyIn(kwargs["last_name"])
                self.moveToClick(self.driver.find_element_by_xpath(
                    u"//input[@id='cardHolderLastName']"))
                self.moveToClick(self.driver.find_element_by_xpath(
                    u"//div/span/div/button"))
            except Exception as e:
                pass
            sleep(5)
            self.moveToClick(self.driver.find_element_by_xpath(
                u"//div[@class='call-to-action']"))
        elif method == "paypal":
            self.moveToClick(targets[1])  # Paypal
            # Not
        else:
            rtnMsg["stat"] = "error",
            rtnMsg["msg"] = "Arg error."
            return rtnMsg

        rtnMsg["stat"] = "ok"
        rtnMsg["msg"] = ""
        return rtnMsg

    def Close(self):
        self.driver.quit()

    def moveToClick(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click()
        actions.perform()

    def keyIn(self, string):
        actions = ActionChains(self.driver)
        for i in range(0, len(string)):
            actions.key_down(string[i])
            actions.key_up(string[i])
        actions.perform()


if __name__ == "__main__":
    URL = "https://www.ebay.com/itm/1986-Philippines-GOLD-2500-Pesos-CORY-REAGAN-Official-US-visit-in-PROOF/192864099482"
    print("Login ebay.")
    username = input("Username: ")
    password = input("Password: ")
    action = Ebay_Selenium()
    print(action.Login(username=username, password=password))
    sleep(3)
    print(action.Buy(url=URL))
    sleep(5)
    print(action.Payment(method="card", card="",
                         date="", code="", first_name="", last_name=""))
    # print(action.Payment(method="paypal", email="", pwd=""))
    # action.Close()
