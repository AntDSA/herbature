from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.database import Client, get_note
from database.panier import Panier
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_super_longue_et_aleatoire_123456'

# Chemin vers la base de données
DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'gazon.db')


@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    """Page d'inscription"""
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
        flash('Compte créé avec succès !', 'success')
        return redirect(url_for('connexion'))
    else:
        flash('Erreur : email invalide, déjà utilisé ou mot de passe trop court', 'error')
        return render_template('inscription.html')


@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    """Page de connexion"""
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
    """Déconnexion"""
    session.clear()
    flash('Déconnexion réussie', 'success')
    return redirect(url_for('index'))


@app.route('/profil')
def profil():
    """Page de profil utilisateur"""
    if 'id_client' not in session:
        flash('Vous devez être connecté', 'error')
        return redirect(url_for('connexion'))
    
    return render_template('profil.html', client=session)


@app.route('/produits')
def produits():
    """Liste des produits"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM produit ORDER BY Note DESC")
    produits = cur.fetchall()
    
    conn.close()
    
    return render_template('produits.html', produits=produits)


@app.route('/produit/<int:id>')
def detail_produit(id):
    """Détail d'un produit"""
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


@app.route('/apropos')
def apropos():
    """Page à propos"""
    return render_template('apropos.html')


@app.route('/contact')
def contact():
    """Page de contact"""
    return render_template('contact.html')


@app.route('/panier')
def panier():
    """Page du panier"""
    if 'id_client' not in session:
        flash('Vous devez être connecté pour accéder au panier', 'error')
        return redirect(url_for('connexion'))
    
    # TODO: Implémenter l'affichage du panier
    return render_template('panier.html')


@app.route('/ajouter-panier/<int:id_produit>', methods=['POST'])
def ajouter_panier(id_produit):
    """Ajouter un produit au panier"""
    if 'id_client' not in session:
        flash('Vous devez être connecté pour ajouter au panier', 'error')
        return redirect(url_for('connexion'))
    
    quantite = int(request.form.get('quantite', 1))
    
    # TODO: Implémenter l'ajout au panier en session
    flash('Produit ajouté au panier !', 'success')
    return redirect(url_for('produits'))


if __name__ == '__main__':
    # Vérifier que la base de données existe
    if not os.path.exists(DB_PATH):
        print("ERREUR: La base de données n'existe pas.")
        print("Exécutez d'abord: python database/Init_BDD.py")
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)