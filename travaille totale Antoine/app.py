from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.database import Client, get_note
import sqlite3

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_super_longue_et_aleatoire_123456'

DB_PATH = 'database/gazon.db'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/templates', methods=['GET', 'POST'])
def inscription():
    if request.method == 'GET':
        return render_template('inscription.html')
    
    email = request.form.get('email')
    mdp = request.form.get('password')
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    adresse = request.form.get('adresse', '')
    ville = request.form.get('ville', '')
    code_postal = request.form.get('code_postal', '')
    
    client = Client(email, mdp)
    resultat = client.inscrire(nom, prenom, adresse, ville, code_postal)
    
    if resultat:
        flash('Compte cree avec succes !', 'success')
        return redirect(url_for('connexion'))
    else:
        flash('Erreur : email invalide, deja utilise ou mot de passe trop court', 'error')
        return render_template('inscription.html')


@app.route('/templates', methods=['GET', 'POST'])
def connexion():
    if request.method == 'GET':
        return render_template('connexion.html')
    
    email = request.form.get('email')
    mdp = request.form.get('password')
    
    client = Client(email, mdp)
    infos = client.connexion()
    
    if infos:
        session['id_client'] = infos['id_client']
        session['nom'] = infos['nom']
        session['prenom'] = infos['prenom']
        session['email'] = infos['email']
        
        flash(f'Bienvenue {infos["prenom"]} !', 'success')
        return redirect(url_for('index'))
    else:
        flash('Email ou mot de passe incorrect', 'error')
        return render_template('connexion.html')


@app.route('/deconnexion')
def deconnexion():
    session.clear()
    flash('Deconnexion reussie', 'success')
    return redirect(url_for('index'))


@app.route('/profil')
def profil():
    if 'id_client' not in session:
        flash('Vous devez etre connecte', 'error')
        return redirect(url_for('connexion'))
    
    return render_template('profil.html', client=session)


@app.route('/produits')
def produits():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM produit ORDER BY Note DESC")
    produits = cur.fetchall()
    
    conn.close()
    
    return render_template('produits.html', produits=produits)


@app.route('/produit/<int:id>')
def detail_produit(id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM produit WHERE id_P = ?", (id,))
    produit = cur.fetchone()
    
    conn.close()
    
    if not produit:
        flash('Produit introuvable', 'error')
        return redirect(url_for('produits'))
    
    note = get_note(id)
    
    return render_template('detail_produit.html', produit=produit, note=note)


if __name__ == '__main__':
    app.run(debug=True)