<div align="center">
  <h1><img src="pin-map-fill.svg" height="25"> Ravintolat</h1>  
</div>


Sovelluksessa näkyy tietyn alueen ravintolat, joista voi etsiä tietoa ja lukea arvioita.

Tiivistetysti ominaisuuksista: pääkäyttäjä pystyy luomaan ravintolan, määrittelemään sille 
kuvauksen, aukioloajat, kategoriat, sijainnin kartalta ja poistamaan ravintolan, sekä arvioita. Peruskäyttäjä pystyy taas
kirjoittamaan näihin ravintoloihin arvioita, kommentein ja tähtiarviolla, sekä lukemaan muiden kirjoittamia arvioita. Sovelluksessa ravintolat
esitetään kartalla, jossa linkin ravintolaan löytää painamalla ravintolan kuvaketta kartalla. Ravintolat ovat myös listattuna arvioiden mukaiseen
järjestykseen, sekä niitä voi hakea kategorioiden ja hakutoiminnon avulla.


## Testaaminen

Sovellus on tällä hetkellä saatavilla osoitteessa: https://restaurants-or6x.onrender.com

#

### Paikallisesti

>[!NOTE]
> Sovelluksen testaaminen vaatii toimiakseen, että asennettuna on PostgreSQL ja Python. Ohjeet Linux/MacOS–järjestelmälle.

Kloonaa repositorio koneellesi, määritä projektihakemiston juureen 
tiedosto nimeltä `.env`ja määritä sille ympäristömuuttujat `SECRET_KEY=<salainen avain tähän>`
sekä `DATABASE_URL=<paikallisen tietokannan osoite>`.

Seuraavaksi aktivoi ympäristö ja asenna riippuvuudet, sekä alusta tietokanta
seuraavia komentoja käyttäen, viimeisellä komennolla sovellus käynnistyy. Vaihtoehtoisesti voit tehdä saman ajamalla
projektin juuressa komennon `./restaurants.sh`.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
psql < schema.sql
flask run
```

Sovelluksen käynnistyttyä on mahdollista testata sovellusta, pääkäyttäjätoiminnallisuuksien testaaminen
ei vaadi uuden käyttäjän luomista, vaan kyseisen käyttäjän toiminnallisuuksiin pääsee käsiksi tunnuksilla:
`käyttäjätunnus: admin, salasana: password`. Peruskäyttäjän ominaisuuksia on mahdollista testata myös heti aluksi
luomalla itselleen käyttäjätunnuksen, mutta on suositeltavaa luoda ensin ravintoloita ja lisätä tietoja
pääkäyttäjän oikeuksilla, jonka jälkeen pystyy tarkastelemaan näitä peruskäyttäjän näkökulmasta.



## Kuvat
<img alt="sovelluskuva1" src="https://github.com/mpajuka/restaurants/assets/56785774/d1210177-ddd6-456f-b023-305308504e4e">

<img alt="sovelluskuva2" src="https://github.com/mpajuka/restaurants/assets/56785774/e8250e54-5e4e-4e29-8413-eea548cac69f">
