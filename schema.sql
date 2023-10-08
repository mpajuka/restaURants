/* Tietokannan alustaminen */

/*
# Toteutus kesken #
CREATE TYPE coord_pair AS (
    lat TEXT,
    lon TEXT
);
 */

CREATE TABLE restaurants(
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT/*,
    coords coord_pair */
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

/*
aseta pääkäyttäjän oikeudet
UPDATE users SET role = 'admin' WHERE username = <käyttäjänimi tähän>;
 */
