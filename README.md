# Ravintolasovellus / Restaurants
Sovelluksessa näkyy tietyn alueen ravintolat, joista voi etsiä tietoa ja lukea arvioita. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee ravintolat kartalla ja voi painaa ravintolasta, jolloin siitä näytetään lisää tietoa (kuten kuvaus ja aukioloajat).
- Käyttäjä voi antaa arvion (tähdet ja kommentti) ravintolasta ja lukea muiden antamia arvioita.
- Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot.
- Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa on annettu sana.
- Käyttäjä näkee myös listan, jossa ravintolat on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti.
- Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.
- Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voi luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään.

Sovelluksen toiminta olisi siis pitkälti esimerkkikuvauksen mukainen.

## Testaaminen

Kloonaa repositorio koneellesi, määritä projektihakemiston juureen 
tiedosto nimeltä `.env`ja määritä sille ympäristömuuttujat `SECRET_KEY=<salainen avain tähän>`
sekä `DATABASE_URL=<paikallisen tietokannan osoite>`.

Seuraavaksi aktivoi ympäristö ja asenna riippuvuudet, sekä alusta tietokanta
seuraavilla komennoilla. Viimeisellä komennolla sovellus käynnistyy.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
psql < schema.sql
flask run
```

Sovelluksen käynnistyttyä on mahdollista testata sovellusta, aloita
luomalla itsellesi käyttäjätunnus. Tämän jälkeen voit siirtyä kirjautumiseen,
jonka onnistuttua pääset takaisin aloitusnäkymään. 

Aluksi tässä näkymässä
ei voi tehdä mitään, sillä peruskäyttäjällä ei ole käyttöoikeuksia ravintolan
lisäämiseen. Voit lisätä itsellesi pääkäyttäjän oikeudet tietokannasta seuraavalla
komennolla:

```sql
UPDATE users SET role = 'admin' WHERE username = <käyttäjänimi tähän>;
```

Tämän jälkeen kun olet uudelleenkirjautunut, pystyt lisäämään ravintoloita
palveluun. Pääkäyttäjä pystyy luomaan ravintolan, määrittelemään sille 
kuvauksen, aukioloajat ja poistamaan ravintolan. Peruskäyttäjä pystyy taas
kirjoittamaan näihin ravintoloihin arvioita, kommentein ja tähtiarviolla.
Ravintolat esitetään päävalikossa keskimääräisen arvosanan perusteella.

Kartta- ja hakutoiminnallisuus, sekä ryhmäluokittelu ovat vielä toistaiseksi työn alla.
