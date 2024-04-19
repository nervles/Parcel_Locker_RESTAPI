from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, DateField, PasswordField, BooleanField
from wtforms import validators, ValidationError


class AddUserForm(Form):
   imie_i_nazwisko = TextField("Imie nazwisko",[validators.Required("Wprowadz dane")],default="dane")
   email=TextField("Email",[validators.Required("Wprowadz swoj email")],default="email")
   adres_uzytkownika = TextField("Adres uzytkownika",[validators.Required("Wprowadz swoj adres")],default="adres")
   submit = SubmitField("Dodaj uzytkownika")
   select = SelectField('Produce',coerce=int,validate_choice=False)



class SendPackageForm(Form):
    odbiorca_id = TextField("ID odbiorcy",[validators.Required("Wprowadz ID odbiorcy")],default="id odbiorcy")
    nadawca_id = TextField("ID nadawcy",[validators.Required("Wprowadz ID nadawcy")],default="id nadawcy")
    paczkomat_id = TextField("ID paczkomatu",[validators.Required("Wprowadz ID paczkomatu")],default="id paczkomatu")
    rozmiar = TextField("Rozmiar paczki",[validators.Required("Wprowadz rozmiar paczki")],default="rozmiar paczki")
    waga = TextField("Waga paczki",[validators.Required("Wprowadz wage paczki")],default="waga paczki")
    submit = SubmitField("Wyslij Paczke")
    select = SelectField('Produce',coerce=int,validate_choice=False)


class OpenForm(Form):
    haslo1 = TextField("Haslo",[validators.Required("Wprowadz dane")],default="dane")
    submit = SubmitField("Otworz")
    select = SelectField('Produce',coerce=int,validate_choice=False)
