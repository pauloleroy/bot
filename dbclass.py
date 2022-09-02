import psycopg2 as pg2

class DBConnection():
    def __init__(self, queries):
        self.conn = pg2.connect(database='bottest', user='postgres',password='3720')
        self.queries = queries
            
    def select_instagram_id_by_account(self, instagram_account):
        '''get instagram id by account name'''
        cur = self.conn.cursor()
        query = self.queries.select_instagram_id(instagram_account)
        cur.execute(query)
        my_instagram_id = cur.fetchall()
        return my_instagram_id

    def select_user_id_by_account(self, user_account):
        '''get user id by user account'''
        cur = self.conn.cursor()
        query = self.queries.select_user_id(user_account)
        cur.execute(query)
        my_user_id = cur.fetchall()
        return my_user_id
    
    def check_return_if_new_account(self, instagram_account):
        '''return instagram id and if new account also insterts into DB'''
        cur = self.conn.cursor()
        my_instagram_id = self.select_instagram_id_by_account(instagram_account)
        if len(my_instagram_id) == 0:
            query = self.queries.insert_to_instagram_account(instagram_account)
            cur.execute(query)
            self.conn.commit()
            query = self.queries.select_instagram_id(instagram_account)
            cur.execute(query)
            my_instagram_id = self.select_instagram_id_by_account(instagram_account)[0][0]
        else:
            my_instagram_id = my_instagram_id[0][0]
        return my_instagram_id

    def insert_user(self, user_account):
        '''insert user to DB if doesnt exists'''
        cur = self.conn.cursor()
        user_id = self.select_user_id_by_account(user_account)
        if len(user_id) == 0:
            query = self.queries.insert_user(user_account)
            cur.execute(query)
            self.conn.commit()

    def insert_login_track(self,user_id):
        '''insert to login track DB'''
        cur = self.conn.cursor()
        query = self.queries.insert_login_track(user_id)
        cur.execute(query)
        self.conn.commit()
        query = self.queries.select_login_id()
        cur.execute(query)
        login_id = cur.fetchone()[0]
        return login_id

    def insert_following(self, instagram_account):
        '''insert 1 following need to call for loop'''
        cur = self.conn.cursor()
        my_instagram_id = self.check_return_if_new_account(instagram_account)
        query = self.queries.insert_following(my_instagram_id)
        cur.execute(query)
        self.conn.commit()

    def delete_following(self):
        '''delete all following'''
        cur = self.conn.cursor()
        query = self.queries.delete_following()
        cur.execute(query)
        self.conn.commit()

    def insert_follower(self, instagram_account):
        '''insert 1 follower need to call for loop'''
        cur = self.conn.cursor()
        my_instagram_id = self.check_return_if_new_account(instagram_account)
        query = self.queries.insert_follower(my_instagram_id)
        cur.execute(query)
        self.conn.commit()

    def delete_follower(self):
        '''delete all follower'''
        cur = self.conn.cursor()
        query = self.queries.delete_follower()
        cur.execute(query)
        self.conn.commit()

    def check_related_id_exists(self,user_account,instagram_account):
        '''check if account is on the related list for that user'''
        cur = self.conn.cursor()
        my_user_id = self.select_user_id_by_account(user_account)
        my_instagram_id = self.select_instagram_id_by_account(instagram_account)
        if len(my_user_id) >0 and len(my_instagram_id) > 0:
            query = self.queries.check_related_id_exists(my_user_id[0][0],my_instagram_id[0][0])
            cur.execute(query)
            related_id = cur.fetchall()
            if len(related_id)==0:
                to_insert = True
            else:
                to_insert = False
        else:
            to_insert = True
        return to_insert
    
    def select_related_page(self, user_account):
        '''get all user related pages'''
        cur = self.conn.cursor()
        my_user_id = self.select_user_id_by_account(user_account)[0][0]
        query = self.queries.select_related_list(my_user_id)
        cur.execute(query)
        related_pages = cur.fetchall()
        return related_pages

    def insert_related_page(self, user_account, instagram_account):
        '''insert related page to DB'''
        cur = self.conn.cursor()
        my_user_id = self.select_user_id_by_account(user_account)[0][0]
        my_instagram_id = self.check_return_if_new_account(instagram_account)
        query = self.queries.insert_to_related_pages(my_user_id,my_instagram_id)
        cur.execute(query)
        self.conn.commit()

    def delete_related_page(self, user_account,instagram_account):
        '''delete relted page from DB'''
        cur = self.conn.cursor()
        my_user_id = self.select_user_id_by_account(user_account)
        my_instagram_id = self.select_instagram_id_by_account(instagram_account)
        query = self.queries.check_related_id_exists(my_user_id[0][0],my_instagram_id[0][0])
        cur.execute(query)
        related_id = cur.fetchall()[0][0]
        query = self.queries.delete_related_page(related_id)
        cur.execute(query)
        self.conn.commit()

    def insert_photo(self,instagram_id,url):
        cur = self.conn.cursor()
        photo_id = self.photo_id_by_url(url)
        if len(photo_id) == 0:
            query = self.queries.insert_photo(instagram_id,url)
            cur.execute(query)
            self.conn.commit()
            photo_id = self.photo_id_by_url(url)[0][0]
        else:
            photo_id = photo_id[0][0]
        return photo_id

    def photo_id_by_url(self,url):
        cur = self.conn.cursor()
        query = self.queries.photo_id_by_url(url)
        cur.execute(query)
        photo_id = cur.fetchall()
        return photo_id
    
    def insert_like_track(self,photo_id,instagram_account):
        cur = self.conn.cursor()
        instagram_id = self.check_return_if_new_account(instagram_account)
        query = self.queries.check_liketrack_exist(photo_id,instagram_id)
        cur.execute(query)
        like_track = cur.fetchall()
        if len(like_track)==0:
            query = self.queries.insert_liketrack(photo_id,instagram_id)
            cur.execute(query)
            self.conn.commit()
            query = self.queries.check_liketrack_exist(photo_id,instagram_id)
            cur.execute(query)
            like_track = cur.fetchall()[0][0]
        else:
            like_track = like_track[0][0]
        return like_track

    def select_related_page_by_user(self,user_account):
        cur = self.conn.cursor()
        query = self.queries.select_related_page_by_user(user_account)
        cur.execute(query)
        related_pages = cur.fetchall()
        return related_pages

    def select_like_list(self,id_list):
        cur = self.conn.cursor()
        query = self.queries.select_like_list(id_list)
        cur.execute(query)
        like_list = cur.fetchall()
        return like_list

    def insert_bot_follow(self,login_id,instagram_id):
        cur = self.conn.cursor()
        query = self.queries.insert_bot_follow(login_id,instagram_id)
        cur.execute(query)
        self.conn.commit()