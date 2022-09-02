import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class InstaBot():
    def __init__(self,path):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(executable_path=path,options=options)

    def login(self,myusername,mypassword):
        '''login to instagram'''
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
        '''check if login was sucessful'''
        time.sleep(4)
        login_url = self.driver.current_url
        if login_url == 'https://www.instagram.com/accounts/onetap/?next=%2F':
            check_login = True
        else:
            check_login = False
        time.sleep(1)
        return check_login

    def check_likes(self,instagram_account, num_pic):
        time.sleep(2)
        self.driver.get(f'https://www.instagram.com/{instagram_account}/')
        time.sleep(3)
        # pic_table = self.driver.find_elements(By.CSS_SELECTOR, '.qi72231t.nu7423ey.n3hqoq4p.r86q59rh.b3qcqh3k.fq87ekyn.bdao358l.fsf7x5fv.rse6dlih.s5oniofx.m8h3af8h.l7ghb35v.kjdc1dyq.kmwttqpk.srn514ro.oxkhqvkx.rl78xhln.nch0832m.cr00lzj9.rn8ck1ys.s3jn8y49.icdlwmnq._a6hd')
        pic_table= self.driver.find_elements(By.TAG_NAME,'a')
        urls = [element.get_attribute('href') for element in pic_table]
        pic_urls = list(filter(lambda url: ('/p/' in url), urls))
        pic_urls = pic_urls[:num_pic]
        likes = []
        urls_likes = {}
        for pic in pic_urls:
            time.sleep(5)
            self.driver.get(pic + 'liked_by/')
            time.sleep(3)
            last_height = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            while True:
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                if new_height == last_height:
                    break
                last_height = new_height
            like_driver = self.driver.find_elements(
                by=By.CSS_SELECTOR,value="._ab8w._ab94._ab97._ab9f._ab9k._ab9p._abcm")
            pic_likes = []
            for like in range(len(like_driver)):
                pic_likes.append(like_driver[like].text)
            pic_likes = list(filter(lambda user: ('\n' not in user),pic_likes))
            pic_likes = list(filter(lambda user: (user != ''),pic_likes))
            likes.append(pic_likes)
            urls_likes.update({pic:pic_likes})
        return urls_likes

    def auto_follow(self, account):
        time.sleep(2)
        self.driver.get(f"https://www.instagram.com/{account}/")
        try:
            time.sleep(3)
            follow_button = self.driver.find_element(by=By.CSS_SELECTOR, value="._acan._acap._acas")
            time.sleep(1)
            follow_button.click()
            it_followed = True
        except NoSuchElementException:
            it_followed = False
        return it_followed



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
