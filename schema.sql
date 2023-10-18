/* Tietokannan alustaminen */

DROP TABLE IF EXISTS restaurants CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS opening_hours CASCADE;


CREATE TABLE restaurants(
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    lat FLOAT,
    lon FLOAT
);

CREATE TYPE usertype AS ENUM('basic', 'admin');

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    role usertype
);

CREATE TABLE opening_hours(
    restaurantId INT,
    openDay INT,
    openHourStart TEXT,
    openHourEnd TEXT,
    CONSTRAINT fk_restaurantId
        FOREIGN KEY(restaurantId)
            REFERENCES restaurants(id)
);

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

INSERT INTO users(username, password, role)
VALUES('admin',
       'pbkdf2:sha256:600000$LA066yJik2jkpYwo$e4c6afd6706b46cfe89a847202ead61d9d1d5b3137976b395d8a382f623cf061',
       'admin');

/*
aseta pääkäyttäjän oikeudet
UPDATE users SET role = 'admin' WHERE username = <käyttäjänimi tähän>;
 */
