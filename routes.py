import secrets
from os import abort

from flask import render_template, redirect, session, request, flash, url_for
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from app import app


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/loginresult", methods=["POST"])
def loginresult():
    error = None
    username = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT id, password, role FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        # TODO: invalid username
        error = 'Käyttäjää ei ole olemassa'
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            # TODO: correct username and password
            if user.role == "admin":
                session["role"] = "admin"
            else:
                session["role"] = "basic"
            session["username"] = username
            session["id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            # TODO: invalid password
            error = 'Väärä salasana'
    return render_template("login.html", error=error)


@app.route("/newaccount")
def newaccount():
    return render_template("newaccount.html")


@app.route("/newaccountresult", methods=["POST"])
def newaccountresult():
    newUsername = request.form["username"]
    newPassword = request.form["password"]
    hash_value = generate_password_hash(newPassword)
    sqlUser = text("SELECT id, password, role FROM users WHERE username=:username")
    sqlUserResult = db.session.execute(sqlUser, {"username": newUsername})
    userExists = sqlUserResult.fetchone()
    if userExists:
        error = "Syöttämäsi käyttäjätunnus on jo viety"
        return render_template("newaccount.html", error=error)
    else:
        sql = text("INSERT INTO users (username, password, role) VALUES (:username, :password, 'basic')")
        db.session.execute(sql, {"username":newUsername, "password":hash_value})
        db.session.commit()
        error = 'Käyttäjä luotu onnistuneesti!'
        return render_template("login.html", error=error)


@app.route("/addrestaurant", methods=["POST"])
def addrestaurant():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    newRestaurantName = request.form["restaurantName"]
    sqlCheck = text("SELECT * FROM restaurants WHERE name = :restaurantName")
    sqlRestaurants = db.session.execute(sqlCheck, {"restaurantName": newRestaurantName})
    if sqlRestaurants.fetchone() or newRestaurantName == '':
        return redirect("/")
    sql = text("INSERT INTO restaurants (name) VALUES (:restaurantName)")
    db.session.execute(sql, {"restaurantName": newRestaurantName})
    db.session.commit()
    return redirect("/")


@app.route("/addreview/<restaurantName>", methods=["POST"])
def addreview(restaurantName):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    starReview = request.form["rating"]
    textReview = request.form["textReview"]
    idQuery = text("SELECT id FROM restaurants WHERE name = :restaurantName")
    restaurant = db.session.execute(idQuery, {"restaurantName": restaurantName})
    result = restaurant.fetchone()

    if result:
        restaurantId = result[0]
        userId = session.get("id")
        sql = text("INSERT INTO reviews (restaurantId, userId, starReview, textReview) "
                   "VALUES (:restaurantId, :userId, :starReview, :textReview)")

        db.session.execute(sql, {"restaurantId": restaurantId,
                                 "userId": userId,
                                 "starReview": starReview,
                                 "textReview": textReview})
        db.session.commit()
        return redirect(f'/restaurants/{restaurantName}')
    else:
        return redirect(f'/restaurants/{restaurantName}')


@app.route("/adddescription/<restaurantName>", methods=["POST"])
def adddescription(restaurantName):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    description = request.form["description"]
    sql = text("UPDATE restaurants "
               "SET description = :description "
                "WHERE name = :restaurantName; ")
    db.session.execute(sql, {"description": description,
                             "restaurantName": restaurantName})
    db.session.commit()
    return redirect(f'/restaurants/{restaurantName}')


@app.route("/addhours/<restaurantName>", methods=["POST"])
def addhours(restaurantName):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    mondayStart = request.form["timeStart1"]
    tuesdayStart = request.form["timeStart2"]
    wednesdayStart = request.form["timeStart3"]
    thursdayStart = request.form["timeStart4"]
    fridayStart = request.form["timeStart5"]
    saturdayStart = request.form["timeStart6"]
    sundayStart = request.form["timeStart7"]
    mondayEnd = request.form["timeEnd1"]
    tuesdayEnd = request.form["timeEnd2"]
    wednesdayEnd = request.form["timeEnd3"]
    thursdayEnd = request.form["timeEnd4"]
    fridayEnd = request.form["timeEnd5"]
    saturdayEnd = request.form["timeEnd6"]
    sundayEnd = request.form["timeEnd7"]
    print(type(mondayEnd), type(mondayStart))
    idQuery = text("SELECT id FROM restaurants WHERE name = :restaurantName")
    restaurant = db.session.execute(idQuery,
                                    {"restaurantName": restaurantName})
    result = restaurant.fetchone()

    if result:
        restaurantId = result[0]

        sql = text("INSERT INTO opening_hours(restaurantId, openDay, openHourStart, openHourEnd)"
                " VALUES (:restaurantId, 1, :timeStart1, :timeEnd1) ")

        sql2 = text("INSERT INTO opening_hours(restaurantId, openDay, openHourStart, openHourEnd)"
                " VALUES (:restaurantId, 2, :timeStart2, :timeEnd2) ")

        sql3 = text("INSERT INTO opening_hours(restaurantId, openDay, openHourStart, openHourEnd)"
                " VALUES (:restaurantId, 3, :timeStart3, :timeEnd3) ")

        sql4 = text("INSERT INTO opening_hours(restaurantId, openDay, openHourStart, openHourEnd)"
                " VALUES (:restaurantId, 4, :timeStart4, :timeEnd4) ")

        sql5 = text("INSERT INTO opening_hours(restaurantId, openDay, openHourStart, openHourEnd)"
                " VALUES (:restaurantId, 5, :timeStart5, :timeEnd5) ")

        sql6 = text("INSERT INTO opening_hours(restaurantId, openDay, openHourStart, openHourEnd)"
                " VALUES (:restaurantId, 6, :timeStart6, :timeEnd6) ")

        sql7 = text("INSERT INTO opening_hours(restaurantId, openDay, openHourStart, openHourEnd)"
                " VALUES (:restaurantId, 7, :timeStart7, :timeEnd7) ")

        db.session.execute(sql, {
            "restaurantId": restaurantId, "timeStart1": mondayStart, "timeEnd1": mondayEnd
        })
        db.session.execute(sql2, {
            "restaurantId": restaurantId, "timeStart2": tuesdayStart,
            "timeEnd2": tuesdayEnd
        })
        db.session.execute(sql3, {
            "restaurantId": restaurantId, "timeStart3": wednesdayStart,
            "timeEnd3": wednesdayEnd
        })
        db.session.execute(sql4, {
            "restaurantId": restaurantId, "timeStart4": thursdayStart,
            "timeEnd4": thursdayEnd
        })
        db.session.execute(sql5, {
            "restaurantId": restaurantId, "timeStart5": fridayStart,
            "timeEnd5": fridayEnd

        })
        db.session.execute(sql6, {
            "restaurantId": restaurantId, "timeStart6": saturdayStart,
            "timeEnd6": saturdayEnd
        })
        db.session.execute(sql7, {
            "restaurantId": restaurantId, "timeStart7": sundayStart,
            "timeEnd7": sundayEnd
        })

        db.session.commit()
        return redirect(f"/restaurants/{restaurantName}")
    else:
        return redirect(f"/restaurants/{restaurantName}")


@app.route("/addcoords/<restaurantName>", methods=["POST"])
def addcoords(restaurantName):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    idQuery = text("SELECT id FROM restaurants WHERE name = :restaurantName")
    restaurant = db.session.execute(idQuery,
                                    {"restaurantName": restaurantName})
    result = restaurant.fetchone()

    lat = request.form["latitude"]
    lon = request.form["longitude"]
    if result:
        if lon == '' or lat == '':
            return redirect(f"/restaurants/{restaurantName}")

        restaurantId = result[0]
        sql = text("UPDATE restaurants "
                   "SET (lat, lon) = (:lat, :lon) "
                   "WHERE id = :restaurantId")
        db.session.execute(sql, {"lat": lat, "lon": lon, "restaurantId": restaurantId})
        db.session.commit()
        return redirect(f"/restaurants/{restaurantName}")
    else:
        return redirect(f"/restaurants/{restaurantName}")


@app.route("/addcategory/<restaurantName>", methods=["POST"])
def addcategory(restaurantName):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    idQuery = text("SELECT id FROM restaurants WHERE name = :restaurantName")
    restaurant = db.session.execute(idQuery,
                                        {"restaurantName": restaurantName})
    result = restaurant.fetchone()
    category = request.form["category"]


    if result:
        if category == '':
            return redirect(f"/restaurants/{restaurantName}")

        restaurantId = result[0]

        categoryExistsQuery = text("SELECT type "
                                   "FROM restaurant_group "
                                   "WHERE type = :category AND restaurantId = :restaurantId")
        categoryExistsResult = db.session.execute(categoryExistsQuery,
                                                  {"category": category,
                                                   "restaurantId": restaurantId})
        if categoryExistsResult.fetchone():
            return redirect(f"/restaurants/{restaurantName}")

        sql = text("INSERT INTO restaurant_group(restaurantId, type)"
                   "VALUES (:restaurantId, :category) ")
        db.session.execute(sql, {"restaurantId": restaurantId,
                                 "category": category})
        db.session.commit()
        return redirect(f"/restaurants/{restaurantName}")
    else:
        return redirect(f"/restaurants/{restaurantName}")


@app.route("/removerestaurant/<restaurantName>", methods=["POST"])
def removerestaurant(restaurantName):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    idQuery = text("SELECT id FROM restaurants WHERE name = :restaurantName")
    restaurantQuery = db.session.execute(idQuery,
                                    {"restaurantName": restaurantName})
    restaurantExists = restaurantQuery.fetchone()

    if restaurantExists:
        restaurantId = restaurantExists[0]
        reviewsQuery = text("SELECT * FROM reviews WHERE restaurantid = :restaurantId")
        reviews = db.session.execute(reviewsQuery, {"restaurantId": restaurantId})
        reviewsExist = reviews.fetchone()

        sqlHours = text(
            "DELETE FROM opening_hours WHERE restaurantid = :restaurantId")
        sqlReviews = text(
            "DELETE FROM reviews WHERE restaurantid = :restaurantId")
        sqlRestaurants = text(
            "DELETE FROM restaurants WHERE id = :restaurantId")
        sqlGroups = text(
            "DELETE FROM restaurant_group WHERE restaurantId = :restaurantId"
        )

        if reviewsExist:
            db.session.execute(sqlHours, {"restaurantId": restaurantId})
            db.session.execute(sqlReviews, {"restaurantId": restaurantId})
            db.session.execute(sqlGroups, {"restaurantId": restaurantId})
            db.session.execute(sqlRestaurants, {"restaurantId": restaurantId})
        else:
            db.session.execute(sqlHours, {"restaurantId": restaurantId})
            db.session.execute(sqlGroups, {"restaurantId": restaurantId})
            db.session.execute(sqlRestaurants, {"restaurantId": restaurantId})

        db.session.commit()
        return redirect("/")
    else:
        return redirect(f"/restaurants/{restaurantName}")


@app.route("/removereview/<restaurantName>/<reviewid>", methods=["POST"])
def removereview(restaurantName, reviewid):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    sql = text("DELETE FROM reviews WHERE reviewid = :reviewid")
    db.session.execute(sql, {"reviewid": reviewid})
    db.session.commit()
    return redirect(f"/restaurants/{restaurantName}")


@app.route("/removedescription/<restaurantName>", methods=["POST"])
def removedescription(restaurantName):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    sql = text("UPDATE restaurants "
               "SET description = ''"
                "WHERE name = :restaurantName; ")
    db.session.execute(sql, {"restaurantName": restaurantName})
    db.session.commit()
    return redirect(f"/restaurants/{restaurantName}")


@app.route("/removehours/<restaurantName>", methods=["POST"])
def removehours(restaurantName):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    idQuery = text("SELECT id FROM restaurants WHERE name = :restaurantName")
    restaurant = db.session.execute(idQuery,
                                    {"restaurantName": restaurantName})
    result = restaurant.fetchone()

    if result:
        restaurantId = result[0]
        sql = text("DELETE FROM opening_hours WHERE restaurantid = :restaurantId")
        db.session.execute(sql, {"restaurantId": restaurantId})
        db.session.commit()
        return redirect(f"/restaurants/{restaurantName}")
    else:
        return redirect(f"/restaurants/{restaurantName}")


@app.route("/removecoords/<restaurantName>", methods=["POST"])
def removecoords(restaurantName):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    coordQuery = text("SELECT lat, lon FROM restaurants WHERE name = :restaurantName")
    restaurant = db.session.execute(coordQuery,
                                    {"restaurantName": restaurantName})
    result = restaurant.fetchone()

    if result:
        deleteCoordSql = text(" UPDATE restaurants"
                              " SET lat = NULL, lon = NULL"
                              " WHERE name = :restaurantName")
        db.session.execute(deleteCoordSql, {"restaurantName": restaurantName})
        db.session.commit()
        return redirect(f"/restaurants/{restaurantName}")
    else:
        return redirect(f"/restaurants/{restaurantName}")

@app.route("/removecategory/<restaurantName>/<category>", methods=["POST"])
def removecategory(restaurantName, category):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    idQuery = text("SELECT id FROM restaurants WHERE name = :restaurantName")
    restaurant = db.session.execute(idQuery,
                                    {"restaurantName": restaurantName})
    result = restaurant.fetchone()

    if result:
        restaurantId = result[0]
        sql = text(
            "DELETE FROM restaurant_group "
            "WHERE restaurantid = :restaurantId AND type = :category ")
        db.session.execute(sql, {"restaurantId": restaurantId,
                                 "category": category})
        db.session.commit()
        return redirect(f"/restaurants/{restaurantName}")
    else:
        return redirect(f"/restaurants/{restaurantName}")


@app.route("/restaurants/<restaurantName>", methods=["GET"])
def restaurant(restaurantName):
    sql = text("SELECT reviews.starReview, reviews.textReview, restaurants.name,"
               " restaurants.description, reviews.userid, reviews.reviewid,"
               " restaurants.lat, restaurants.lon "
               "FROM reviews "
               "RIGHT JOIN restaurants ON reviews.restaurantId = restaurants.id "
               "WHERE restaurants.name = :restaurantName;")
    reviews = db.session.execute(sql, {"restaurantName": restaurantName})
    data = reviews.fetchall()

    session["reviewed"] = "false"
    userId = session.get("id")
    reviewsSql = text("SELECT reviews.userId, restaurants.name "
                      "FROM reviews "
                      "RIGHT JOIN restaurants ON reviews.restaurantId = restaurants.id "
                      "WHERE userId = :userId AND restaurants.name = :restaurantName")
    userIdInReviews = db.session.execute(reviewsSql, {"userId": userId,
                                                      "restaurantName": restaurantName})
    alreadyReviewed = userIdInReviews.fetchall()
    if alreadyReviewed:
        session["reviewed"] = "true"

    if data:
        opening_hours_sql = text("SELECT openDay, openHourStart, openHourEnd "
                                 "FROM opening_hours "
                                 "INNER JOIN restaurants ON opening_hours.restaurantId = restaurants.id "
                                 "WHERE restaurants.name = :restaurantName;")
        hoursResult = db.session.execute(opening_hours_sql, {"restaurantName": restaurantName})
        hoursData = hoursResult.fetchall()
        category_data_sql = text("SELECT type "
                                 "FROM restaurant_group "
                                 "INNER JOIN restaurants ON restaurant_group.restaurantId = restaurants.id "
                                 "WHERE restaurants.name = :restaurantName ")
        categoryDataResult = db.session.execute(category_data_sql, {"restaurantName": restaurantName})
        categoryData = categoryDataResult.fetchall()
        starreview_sum = 0
        count = 0
        for i in data:
            if i.starreview is not None:
                starreview_sum += int(i.starreview)
                count += 1
        if starreview_sum != 0:
            meanScore = starreview_sum / count
            return render_template("restaurant.html",
                               restaurantName=restaurantName,
                               reviews=data,
                               meanScore="{:.1f}".format(meanScore),
                                openingHours=hoursData,
                                   categoryData=categoryData)
        else:
            return render_template("restaurant.html",
                                   restaurantName=restaurantName,
                                   openingHours=hoursData,
                                   reviews=data,
                                   categoryData=categoryData)
    else:
        return redirect("/")


@app.route("/searchrestaurant", methods=["POST"])
def searchrestaurant():
    searchWord = request.form["word"]
    searchWordFormatted = f'%{searchWord}%'
    sql = text("SELECT * FROM restaurants WHERE description ILIKE :searchWordFormatted ")
    restaurants = db.session.execute(sql, {"searchWordFormatted": searchWordFormatted})
    result = restaurants.fetchall()
    if result:
        return render_template("restaurantlist.html", restaurants=result,
                               searchWord=searchWord)
    else:
        return redirect("/")


@app.route("/categories")
def categories():
    category_data_sql = text("SELECT type "
                             "FROM restaurant_group "
                             "INNER JOIN restaurants ON restaurant_group.restaurantId = restaurants.id "
                             "GROUP BY type ")
    categoryDataResult = db.session.execute(category_data_sql)
    categoryData = categoryDataResult.fetchall()

    return render_template("categories.html", categoryData=categoryData)


@app.route("/searchrestaurant/<category>")
def searchbycategory(category):
    sql = text("SELECT restaurants.name "
               "FROM restaurant_group "
               "INNER JOIN restaurants ON restaurant_group.restaurantId = restaurants.id "
               "WHERE type = :category;")
    restaurantDataResult = db.session.execute(sql, {"category": category})
    restaurantData = restaurantDataResult.fetchall()
    if restaurantData:
        return render_template("restaurantlist.html", restaurants=restaurantData,
                               category=category)

@app.route("/logout")
def logout():
    del session["username"]
    try:
        del session["role"]
    except:
        pass
    return redirect("/")


@app.route("/")
def index():
    sqlReviews = text("SELECT * FROM reviews;")
    checkReviews = db.session.execute(sqlReviews)
    if checkReviews.fetchone():
        sql = text(
            "SELECT restaurants.name, ROUND(AVG(starreview), 1) as average_rating, lat, lon "
            "FROM reviews "
            "RIGHT JOIN restaurants ON reviews.restaurantid = restaurants.id "
            "GROUP BY restaurants.name, lat, lon "
            "ORDER BY average_rating DESC, restaurants.name ASC")
        sortedRestaurants = db.session.execute(sql)
        restaurantsData = sortedRestaurants.fetchall()
        return render_template("restaurants.html",
                               restaurants=restaurantsData)
    else:
        sqlNoReviews = text("SELECT name, lat, lon FROM restaurants ORDER BY name ASC")
        restaurantsNoReviews = db.session.execute(sqlNoReviews)
        data = restaurantsNoReviews.fetchall()
        return render_template("restaurants.html",
                               restaurants=data)
