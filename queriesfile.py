class MyQueries():
    def __init__(self):
        pass
    def insert_to_user_list(self,user_account):
        query = f"INSERT INTO user_list (user_account, created_on, is_activated) VALUES ('{user_account}',CURRENT_TIMESTAMP,true)"
        return query
    def insert_to_instagram_account(self,instagram_account):
        query = f"INSERT INTO instagram_account (instagram_account,created_on,is_activated) VALUES ('{instagram_account}',CURRENT_TIMESTAMP, true)"
        return query
    def insert_to_related_pages(self, user_id, instagram_id):
        query = f"INSERT INTO related_page (user_id,instagram_id,created_on,is_activated) VALUES ('{user_id}','{instagram_id}',CURRENT_TIMESTAMP,true)"
        return query
    def select_user_id(self, user_account):
        query = f"SELECT user_id FROM user_list WHERE user_account='{user_account}'"
        return query
    def select_instagram_id(self, instagram_account):
        query = f"SELECT instagram_id FROM instagram_account WHERE instagram_account='{instagram_account}'"
        return query
    def check_related_id_exists(self,user_id,instagram_id):
        query = f"SELECT related_id FROM related_page WHERE user_id = {user_id} AND instagram_id = {instagram_id}"
        return query
    def select_related_list(self,user_id):
        query = f"SELECT instagram_account FROM instagram_account INNER JOIN related_page ON instagram_account.instagram_id = related_page.instagram_id WHERE user_id = {user_id} ORDER BY instagram_account"
        return query
    def delete_related_page(self,related_id):
        query = f"DELETE FROM related_page WHERE related_id={related_id}"
        return query
    def delete_following(self):
        query = "DELETE FROM following"
        return query
    def delete_follower(self):
        query = "DELETE FROM follower"
        return query
    def insert_following(self,instagram_id):
        query = f"INSERT INTO following (instagram_id) VALUES ({instagram_id})"
        return query
    def insert_follower(self,instagram_id):
        query = f"INSERT INTO follower (instagram_id) VALUES ({instagram_id})"
        return query
    def insert_user(self,user_account):
        query = f"INSERT INTO user_list (user_account,created_on,is_activated) VALUES ('{user_account}',CURRENT_TIMESTAMP, true)"
        return query
    def insert_login_track(self,user_id):
        query = f"INSERT INTO login_track (user_id,login_time) VALUES ({user_id},CURRENT_TIMESTAMP)"
        return query
    def photo_id_by_url(self,url):
        query = f"SELECT photo_id FROM photo WHERE photo_url='{url}'"
        return query
    def insert_photo(self,instagram_id,url):
        query = f"INSERT INTO photo (instagram_id,photo_url,photo_date,is_activated) VALUES ({instagram_id},'{url}',CURRENT_TIMESTAMP,true)"
        return query
    def select_related_page_by_user(self,user_account):
        query = f"SELECT instagram_account FROM instagram_account INNER JOIN related_page ON related_page.instagram_id = instagram_account.instagram_id WHERE user_id =(SELECT user_id FROM user_list WHERE user_account='{user_account}')"
        return query
    def check_liketrack_exist(self,photo_id,instagram_id):
        query = f"SELECT like_id FROM like_track WHERE photo_id = {photo_id} AND instagram_id = {instagram_id}"
        return query
    def insert_liketrack(self,photo_id,instagram_id):
        query = f"INSERT INTO like_track (photo_id,instagram_id,created_on,is_activated) VALUES ({photo_id},{instagram_id},CURRENT_TIMESTAMP,true)"
        return query
    def select_like_list(self,id_list):
        where = "WHERE "
        for id in id_list:
            where =  where + "photo.instagram_id=" + str(id) + " or "
        where = where[:-4]
        query = f"""
        select instagram_account, count(distinct photo.instagram_id),count(distinct like_track.photo_id)
        from instagram_account
        inner join like_track
        on instagram_account.instagram_id = like_track.instagram_id
        inner join photo
        on photo.photo_id = like_track.photo_id
        {where}
        group by instagram_account
        order by count(distinct photo.instagram_id) desc , count(distinct like_track.photo_id) desc
        """
        return query