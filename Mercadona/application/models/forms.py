


from flask_wtf import FlaskForm
from flask_wtf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField,\
    EmailField, DateField, RadioField, HiddenField

from wtforms.validators import DataRequired, Length, Email




class ConnexionAdministrateur(FlaskForm):
    identifiant = StringField('Identifiant', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')
    csrf_token = HiddenField()


class ConnexionClient(FlaskForm):
    identifiant = StringField("Identifiant", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")
    csrf_token = HiddenField()



class SouscriptionForm(FlaskForm):
    nom = StringField("Nom", validators=[DataRequired()])
    prenom = StringField("Prenom", validators=[DataRequired()])
    identifiant = StringField("Identifiant", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    date_naissance = DateField("Date de naissance", validators=[DataRequired()])
    genre = RadioField("Genre", choices=[("masculin", "Masculin"), ("feminin", "Féminin")], validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Souscrire aux conditions de Mercadona")
    csrf_token = HiddenField()

    def __repr__(self):
        return f"SouscriptionForm(nom='{self.nom.data}', prenom='{self.prenom.data}', email='{self.email.data}', genre='{self.genre.data}')"


class NouvelleCategorieForm(FlaskForm):
    nom = StringField("Nom de la catégorie", validators=[DataRequired()])
    csrf_token = HiddenField()



class ConnexionClientPromo(ConnexionClient):
    pass