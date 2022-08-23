import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException

class InstaBot():
    def __init__(self,path):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(executable_path=path,options=options)

    def login(self,myusername,mypassword):
        self.driver.get("https://www.instagram.com/")
        time.sleep(5)

        username = self.driver.find_element(By.NAME,"username")
        password = self.driver.find_element(By.NAME,"password")
        username.send_keys(myusername)
        password.send_keys(mypassword)
        time.sleep(2)
        password.send_keys(Keys.ENTER)
        time.sleep(2)

    def get_followers(self,useraccount):
        '''get followers list'''
        followers_list = self.get_profile_info('followers',useraccount)
        return followers_list

    def get_following(self, useraccount):
        '''get following list'''
        following_list = self.get_profile_info('following',useraccount)
        return following_list

    def get_likes(self):
        pass

    def auto_follow(self):
        pass

    def unfollow(self):
        pass

    def get_profile_info(self,info,useraccount):
        '''get followers or folliwing list'''
        time.sleep(5)
        self.driver.get(f"https://www.instagram.com/{useraccount}/{info}/")
        time.sleep(2)
        modal = self.driver.find_element(by=By.CLASS_NAME, value="_aano")
        last_height = self.driver.execute_script(
            "return arguments[0].scrollTop = arguments[0].scrollHeight",modal)
        while True:
            time.sleep(2)
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)
            new_height = self.driver.execute_script(
                "return arguments[0].scrollTop = arguments[0].scrollHeight",modal)
            if new_height == last_height:
                break
            last_height = new_height
        unfiltered_list = self.driver.find_elements(
            by=By.CSS_SELECTOR,value="._ab8y._ab94._ab97._ab9f._ab9k._ab9p._abcm")
        filtered_list = filter_verified(unfiltered_list)
        return filtered_list 
    def check_login(self):
        time.sleep(2)
        login_url = self.driver.current_url
        if login_url == 'https://www.instagram.com/accounts/onetap/?next=%2F':
            check_login = True
        else:
            check_login = False
        time.sleep(1)
        return check_login

def filter_verified(userlist):
    '''filter data from the followers and following list'''
    mylist = []
    for user in range(len(userlist)):
        if user != 'Verified':
            mylist.append(userlist[user].text)
    for user in range(len(mylist)):
        pos = mylist[user].find('\nVerified')
        if pos > -1:
            mylist[user] = mylist[user][:pos]
    return mylist
