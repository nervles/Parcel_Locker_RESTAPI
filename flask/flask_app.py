
from flask import Flask, request, jsonify, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from forms import AddUserForm, SendPackageForm, OpenForm
import random
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'development key'

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="Paczkomat",
    password="alamakota", # database passowrd hidden
    hostname="Paczkomat.mysql.pythonanywhere-services.com",
    databasename="Paczkomat$baza_v4",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299 # connection timeouts
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # no warning disruptions

db = SQLAlchemy(app)
ma = Marshmallow(app)


def generate_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(10))
    return password


def send_email(sender_email, sender_password, recipient_email, subject, message):
    # Utwórz obiekt wiadomości typu MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Dodaj treść wiadomości
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Utwórz połączenie z serwerem SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Zaloguj się do konta nadawcy
        server.login(sender_email, sender_password)
        # Wyślij wiadomość
        server.send_message(msg)
        # Zamknij połączenie
        server.quit()
        print("E-mail został wysłany!")
    except Exception as e:
        print("Wystąpił błąd podczas wysyłania e-maila:", str(e))



class Uzytkownik(db.Model):

    __tablename__ = "uzytkownik"
    id = db.Column(db.Integer, primary_key=True)
    imie_i_nazwisko = db.Column(db.String(4096))
    email = db.Column(db.String(4096))
    adres_uzytkownika = db.Column(db.String(4096))


    def __init__(self, imie_i_nazwisko, email, adres_uzytkownika):
        self.imie_i_nazwisko = imie_i_nazwisko
        self.email = email
        self.adres_uzytkownika = adres_uzytkownika

class UzytkownikSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id' ,'imie_i_nazwisko', 'email', 'adres_uzytkownika')
        #fields = ('id', 'full_name')


uzytkownik_schema = UzytkownikSchema()
uzytkownicy_schema = UzytkownikSchema(many=True)


class Paczkomat(db.Model):

    __tablename__ = "paczkomat"
    id = db.Column(db.Integer, primary_key=True)
    adres_paczkomatu = db.Column(db.String(4096))
    czy_jest_paczka = db.Column(db.Boolean)
    paczka_id = db.Column(db.Integer)
    otworz = db.Column(db.Boolean)


    def __init__(self, adres_paczkomatu, czy_jest_paczka, paczka_id, otworz):
        self.adres_paczkomatu = adres_paczkomatu
        self.czy_jest_paczka = czy_jest_paczka
        self.paczka_id = paczka_id
        self.otworz = otworz

class PaczkomatSchema(ma.Schema):
    class Meta:
        fields = ('id', 'adres_paczkomatu', 'czy_jest_paczka', 'paczka_id', 'otworz')

paczkomat_schema = PaczkomatSchema()
paczkomaty_schema = PaczkomatSchema(many=True)


class Paczka(db.Model):

    __tablename__ = "paczka"
    id = db.Column(db.Integer, primary_key=True)
    odbiorca_id = db.Column(db.Integer)
    nadawca_id = db.Column(db.Integer)
    paczkomat_id = db.Column(db.Integer)
    rozmiar = db.Column(db.String(4096))
    waga = db.Column(db.String(4096))
    haslo = db.Column(db.String(11))
    czy_paczka_odebrana = db.Column(db.Boolean)


    def __init__(self, odbiorca_id, nadawca_id, paczkomat_id, rozmiar, waga, haslo, czy_paczka_odebrana):
        self.odbiorca_id = odbiorca_id
        self.nadawca_id = nadawca_id
        self.paczkomat_id = paczkomat_id
        self.rozmiar = rozmiar
        self.waga = waga
        self.haslo = haslo
        self.czy_paczka_odebrana = czy_paczka_odebrana

class PaczkaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'odbiorca_id', 'nadawca_id', 'paczkomat_id', 'rozmiar', 'waga', 'haslo', 'czy_paczka_odebrana')

paczka_schema = PaczkaSchema()
paczki_schema = PaczkaSchema(many=True)



@app.route("/user/<id>", methods=["GET"])
def get_user_by_one(id):
    uzytkownik = Uzytkownik.query.get(id)
    result = uzytkownik_schema.dump(uzytkownik)
    return jsonify(result)

@app.route("/users", methods=["GET"])
def get_user_by():
    uzytkownicy = Uzytkownik.query.all()
    result = uzytkownicy_schema.dump(uzytkownicy)
    return jsonify(result)

@app.route("/query/part", methods=["POST"])
def get_user_by_part():
    imie_i_nazwisko= request.json["imie_i_nazwisko"]
    email= request.json["email"]
    adres_uzytkownika = request.json["adres_uzytkownika"]
    nowy_uzytkownik = Uzytkownik(imie_i_nazwisko, email, adres_uzytkownika)
    db.session.add(nowy_uzytkownik)
    db.session.commit()
    uzytkownik = Uzytkownik.query.get(nowy_uzytkownik.id)
    result = uzytkownik_schema.dump(uzytkownik)
    return jsonify(result)

@app.route("/paczkomat/<id>", methods=["GET"])
def get_paczkomat_by_one(id):
    paczkomat = Paczkomat.query.get(id)
    result = paczkomat_schema.dump(paczkomat)
    return jsonify(result)

@app.route("/paczkomaty", methods=["GET"])
def get_paczkomat_by():
    paczkomaty = Paczkomat.query.all()
    result = paczkomaty_schema.dump(paczkomaty)
    return jsonify(result)

@app.route("/query/paczkomat", methods=["POST"])
def get_paczkomat_by_part():
    adres_paczkomatu = request.json["adres_paczkomatu"]
    czy_jest_paczka = request.json["adres_paczkomatu"]
    paczka_id = request.json["paczka_id"]
    otworz = request.json["otworz"]
    nowy_paczkomat = Paczkomat(adres_paczkomatu, czy_jest_paczka, paczka_id, otworz)
    db.session.add(nowy_paczkomat)
    db.session.commit()
    paczkomat = Paczkomat.query.get(nowy_paczkomat.id)
    result = paczkomat_schema.dump(paczkomat)
    return jsonify(result)


@app.route("/paczka/<id>", methods=["GET"])
def get_paczka_by_one(id):
    paczka = Paczka.query.get(id)
    result = paczka_schema.dump(paczka)
    return jsonify(result)

@app.route("/paczki", methods=["GET"])
def get_paczka_by():
    paczki = Paczka.query.all()
    result = paczki_schema.dump(paczki)
    return jsonify(result)

@app.route("/query/paczka", methods=["POST"])
def get_Paczka_by_part():
    odbiorca_id = request.json["odbiorca_id"]
    nadawca_id = request.json["nadawca_id"]
    paczkomat_id = request.json["paczkomat_id"]
    rozmiar = request.json["rozmiar"]
    waga = request.json["waga"]
    haslo = request.json["haslo"]
    czy_paczka_odebrana = request.json["czy_paczka_odebrana"]
    nowa_paczka = Paczka(odbiorca_id, nadawca_id, paczkomat_id, rozmiar, waga, haslo, czy_paczka_odebrana)
    db.session.add(nowa_paczka)
    db.session.commit()
    paczka = Paczka.query.get(nowa_paczka.id)
    result = paczka_schema.dump(paczka)
    return jsonify(result)



@app.route("/web/users", methods=["GET"])
def get_users_nasz():
    all_users = Uzytkownik.query.order_by(Uzytkownik.imie_i_nazwisko).all()
    result = uzytkownicy_schema.dump(all_users)
    return render_template('paczkomatipz.hmtl', title = 'Strona bazy danych paczkomatu IPZ', uzytkownik=result)


@app.route("/webpostuser", methods=["GET", "POST"])
def getUserNaszDodaj():
    form = AddUserForm()
    if request.method == 'POST':
        imie_i_nazwisko = str(request.form['imie_i_nazwisko'])
        email = str(request.form['email'])
        adres_uzytkownika = str(request.form['adres_uzytkownika'])
        new_user = Uzytkownik(imie_i_nazwisko, email, adres_uzytkownika)

        if Uzytkownik.query.filter_by(email=email).first() is not None:
            return'Użytkownik o podanym adresie email już istnieje!'

        db.session.add(new_user)
        db.session.commit()

    user = Uzytkownik.query.all()
    result = uzytkownik_schema.dump(user)
    flash('Dodano uzytkownika!')
    redirect('/webpostuser')
    return render_template('wpiszdaneuser.html', title='Baza danych paczkomatu', uzytkownik= result, form=form)




@app.route("/web/sendpackage", methods=["GET", "POST"])
def getPackageDodaj():
    form = SendPackageForm()
    if request.method == 'POST':

        odbiorca_email = str(request.form['odbiorca_email'])
        nadawca_email = str(request.form['nadawca_email'])
        temp_user = Uzytkownik.query.filter_by(email = odbiorca_email).first()
        odbiorca_id = temp_user.id
        temp_user = Uzytkownik.query.filter_by(email = nadawca_email).first()
        nadawca_id = temp_user.id


        paczkomat_id = str(request.form['paczkomat_id'])
        rozmiar = str(request.form['rozmiar'])
        waga = str(request.form['waga'])
        haslo = generate_password()
        otworz = 0
        new_package = Paczka(odbiorca_id, nadawca_id, paczkomat_id, rozmiar, waga, haslo, otworz)
        paczkomat = Paczkomat.query.get(new_package.paczkomat_id)
        if paczkomat.czy_jest_paczka == 1:
            return "Paczkomat jest pełen"

        db.session.add(new_package)
        db.session.commit()
        paczkomat.czy_jest_paczka = 1
        paczkomat.paczka_id = new_package.id
        db.session.commit()


        paczkomat.otworz = 1
        db.session.commit()


        uzytkownik = Uzytkownik.query.get(odbiorca_id)
        recipient_email = uzytkownik.email
        sender_email = "pwr.paczka@gmail.com"
        sender_password = "qqqdhoilqeloqjjf"
        subject = "Przyszla paczka"
        message = "Aby otworzyc paczkomat i odebrac paczke wpisz ponizsze haslo na stronie Paczkomat.pythonanywhere.com/otworz \n"+ haslo
        send_email(sender_email, sender_password, recipient_email, subject, message)





    flash('Wyslano paczke!')
    redirect('/web/sendpackage')
    return render_template('wpiszdanepaczka.html', title='Wyslij paczke', form=form)


@app.route("/web/packages", methods=["GET"])
def get_packages():
    all_packages = Paczka.query.order_by(Paczka.id).all()
    result = paczki_schema.dump(all_packages)
    return render_template('paczki.html', title = 'Strona paczek zarejestrowanych w paczkomacie IPZ', paczka=result)

#Proba otwierania paczkomatu z linka przychodzacaego na mail
"""
@app.route("/<haslo1>" , methods=["POST"])
def otworz(haslo1):
    paczka = Paczka.query.filter_by(haslo = haslo1).first()
    paczkomat = Paczkomat.query.get(paczka.paczkomat_id)
    if paczka.czy_paczka_odebrana == 0:
        paczkomat.otworz = 1
        db.session.commit()

        paczkomat.otworz = 0
        paczkomat.czy_jest_paczka = 0
        paczka.czy_paczka_odebrana = 1
        db.session.commit()
    return "Otwarto"
"""

@app.route("/otworz" , methods=["GET", "POST"])
def otworz():
    form = OpenForm()
    if request.method == 'POST':
        haslo1 = str(request.form["haslo1"])
        paczka = Paczka.query.filter_by(haslo = haslo1).first()

        if paczka is None:
            return "Brak paczki o podanym haśle."

        paczkomat = Paczkomat.query.get(paczka.paczkomat_id)

        if paczkomat is None:
            return "Brak paczkomatu dla podanej paczki."


        if paczka.czy_paczka_odebrana == 1:
            return "Paczka już została odebrana"
        paczkomat.otworz = 1
        db.session.commit()


        paczkomat.czy_jest_paczka = 0
        paczka.czy_paczka_odebrana = 1
        db.session.commit()

    flash('Otworzono!')
    #redirect('/zamknij')
    return render_template('open.html', title='otworz', form=form)


@app.route("/zamknij" , methods=["GET", "POST"])
def zamknij():

    paczkomat = Paczkomat.query.filter_by(id=1).first()

    paczkomat.otworz = 0
    db.session.commit()

    result=paczkomat.otworz


    return jsonify(result)




@app.route('/z')
def hello_world():
    return 'Pozdrawiamy!!!'
