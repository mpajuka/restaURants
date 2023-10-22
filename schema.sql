/* Tietokannan alustaminen */

DROP TABLE IF EXISTS restaurants CASCADE;
CREATE TABLE restaurants(
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    lat FLOAT,
    lon FLOAT
);

CREATE TYPE usertype AS ENUM('basic', 'admin');

DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    role usertype
);

DROP TABLE IF EXISTS opening_hours CASCADE;
CREATE TABLE opening_hours(
    restaurantId INT,
    openDay INT,
    openHourStart TEXT,
    openHourEnd TEXT,
    CONSTRAINT fk_restaurantId
        FOREIGN KEY(restaurantId)
            REFERENCES restaurants(id)
);

DROP TABLE IF EXISTS reviews CASCADE;
CREATE TABLE reviews(
    reviewId SERIAL PRIMARY KEY,
    restaurantId INT,
    userId INT,
    starReview INT,
    textReview TEXT,
    CONSTRAINT fk_restaurantId
        FOREIGN KEY(restaurantId)
            REFERENCES restaurants(id),

    CONSTRAINT fk_userId
        FOREIGN KEY(userId)
            REFERENCES users(id)

);

DROP TABLE IF EXISTS restaurant_group CASCADE;
CREATE TABLE restaurant_group(
    id SERIAL PRIMARY KEY,
    restaurantId INT,
    type TEXT,
    CONSTRAINT fk_restaurantId
        FOREIGN KEY(restaurantId)
            REFERENCES restaurants(id)
);

INSERT INTO users(username, password, role)
VALUES('admin',
       'pbkdf2:sha256:600000$tV8LHbfQh08SNKsQ$049525b6b90551189f8c6914d6ff43015727ff1c16af1eaa62261403d613a0be',
       'admin');

/*
aseta pääkäyttäjän oikeudet
UPDATE users SET role = 'admin' WHERE username = <käyttäjänimi tähän>;
 */
