CREATE TABLE IF NOT EXISTS user_list(
    user_id SERIAL PRIMARY KEY,
    user_account VARCHAR(100) UNIQUE NOT NULL,
    created_on TIMESTAMP NOT NULL,
    is_activated BOOLEAN NOT NULL
)
CREATE TABLE IF NOT EXISTS instagram_account (
    instagram_id SERIAL PRIMARY KEY,
    instagram_account VARCHAR(100) UNIQUE NOT NULL,
    created_on TIMESTAMP NOT NULL,
    is_activated BOOLEAN NOT NULL
)
CREATE TABLE IF NOT EXISTS follower (
    follower_id SERIAL PRIMARY KEY,
    instagram_id INTEGER REFERENCES instagram_account(instagram_id) NOT NULL
)
CREATE TABLE IF NOT EXISTS following (
    following_id SERIAL PRIMARY KEY,
    instagram_id INTEGER REFERENCES instagram_account(instagram_id) NOT NULL
)
CREATE TABLE IF NOT EXISTS login_track (
    login_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user_list(user_id) NOT NULL,
    login_time TIMESTAMP NOT NULL
)
CREATE TABLE IF NOT EXISTS bot_follow_track(
    follow_id SERIAL PRIMARY KEY,
    instagram_id INTEGER REFERENCES instagram_account(instagram_id )NOT NULL,
    user_id INTEGER REFERENCES user_list(user_id) NOT NULL,
    created_on TIMESTAMP NOT NULL,
    is_activated BOOLEAN NOT NULL
)
CREATE TABLE IF NOT EXISTS related_page(
    related_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user_list(user_id) NOT NULL,
    instagram_id INTEGER REFERENCES instagram_account(instagram_id) NOT NULL,
    created_on TIMESTAMP NOT NULL,
    is_activated BOOLEAN NOT NULL
)
CREATE TABLE IF NOT EXISTS photo(
    photo_id SERIAL PRIMARY KEY,
    instagram_id INTEGER REFERENCES instagram_account(instagram_id) NOT NULL,
    photo_url VARCHAR(400) UNIQUE NOT NULL,
    photo_date DATE NOT NULL,
    is_activated BOOLEAN NOT NULL
)
CREATE TABLE IF NOT EXISTS like_track(
    like_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user_list(user_id) NOT NULL,
    instagram_id_related INTEGER REFERENCES instagram_account(instagram_id) NOT NULL,
    instagram_id_client INTEGER REFERENCES instagram_account(instagram_id) NOT NULL,
    photo_id INTEGER REFERENCES photo(photo_id)NOT NULL,
    is_activated BOOLEAN NOT NULL
)
