from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.database import Client, Commande, get_note
from database.panier import Panier, HistoriqueCommandes
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_super_longue_et_aleatoire_123456'

# Chemin vers la base de données
DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'gazon.db')


def get_db_connection():
    """Crée une connexion à la base de données"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    """Page d'accueil"""
    conn = get_db_connection()
    # Récupérer 4 produits en vedette (les mieux notés)
    produits = conn.execute('SELECT * FROM produit ORDER BY Note DESC LIMIT 4').fetchall()
    conn.close()
    return render_template('index.html', produits=produits)


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
        flash('Erreur : email invalide, déjà utilisé ou mot de passe trop court (min 6 caractères)', 'error')
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
        session['panier'] = []  # Initialiser le panier en session
        
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
    
    # Récupérer l'historique des commandes
    conn = get_db_connection()
    commandes = conn.execute('''
        SELECT cc.id_CC, cc.Date, SUM(p.Prix * fcc.Quantité) as total
        FROM commande_client cc
        JOIN fiche_CC fcc ON cc.id_CC = fcc.id_CC
        JOIN produit p ON fcc.id_P = p.id_P
        WHERE cc.id_C = ?
        GROUP BY cc.id_CC, cc.Date
        ORDER BY cc.Date DESC
    ''', (session['id_client'],)).fetchall()
    conn.close()
    
    return render_template('profil.html', client=session, commandes=commandes)


@app.route('/produits')
def produits():
    """Liste des produits"""
    conn = get_db_connection()
    produits = conn.execute('SELECT * FROM produit ORDER BY Note DESC').fetchall()
    conn.close()
    
    return render_template('produits.html', produits=produits)


@app.route('/produit/<int:id>')
def detail_produit(id):
    """Détail d'un produit"""
    conn = get_db_connection()
    produit = conn.execute('SELECT * FROM produit WHERE id_P = ?', (id,)).fetchone()
    conn.close()
    
    if not produit:
        flash('Produit introuvable', 'error')
        return redirect(url_for('produits'))
    
    return render_template('detail_produit.html', produit=produit)


@app.route('/apropos')
def apropos():
    """Page à propos"""
    return render_template('apropos.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Page de contact"""
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form.get('name')
        email = request.form.get('email')
        sujet = request.form.get('subject')
        message = request.form.get('message')
        
        # Ici, vous pourriez envoyer un email ou sauvegarder dans la BDD
        flash(f'Merci {nom} ! Votre message a été envoyé avec succès.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')


@app.route('/information')
def information():
    """Page CGV et informations légales"""
    return render_template('information.html')


@app.route('/panier')
def panier():
    """Page du panier"""
    if 'id_client' not in session:
        flash('Vous devez être connecté pour accéder au panier', 'error')
        return redirect(url_for('connexion'))
    
    # Récupérer les produits du panier depuis la session
    panier = session.get('panier', [])
    
    # Récupérer les détails des produits
    conn = get_db_connection()
    produits_panier = []
    total = 0
    
    for item in panier:
        produit = conn.execute('SELECT * FROM produit WHERE id_P = ?', (item['id_produit'],)).fetchone()
        if produit:
            prix_ligne = produit['Prix'] * item['quantite']
            produits_panier.append({
                'produit': produit,
                'quantite': item['quantite'],
                'prix_ligne': prix_ligne
            })
            total += prix_ligne
    
    conn.close()
    
    return render_template('panier.html', produits=produits_panier, total=total)


@app.route('/ajouter-panier/<int:id_produit>', methods=['POST'])
def ajouter_panier(id_produit):
    """Ajouter un produit au panier"""
    if 'id_client' not in session:
        flash('Vous devez être connecté pour ajouter au panier', 'error')
        return redirect(url_for('connexion'))
    
    quantite = int(request.form.get('quantite', 1))
    
    # Vérifier que le produit existe et qu'il y a assez de stock
    conn = get_db_connection()
    produit = conn.execute('SELECT * FROM produit WHERE id_P = ?', (id_produit,)).fetchone()
    conn.close()
    
    if not produit:
        flash('Produit introuvable', 'error')
        return redirect(url_for('produits'))
    
    if produit['Stock'] < quantite:
        flash(f'Stock insuffisant. Seulement {produit["Stock"]} disponibles.', 'error')
        return redirect(url_for('detail_produit', id=id_produit))
    
    # Ajouter au panier en session
    if 'panier' not in session:
        session['panier'] = []
    
    # Vérifier si le produit est déjà dans le panier
    panier = session['panier']
    produit_existe = False
    
    for item in panier:
        if item['id_produit'] == id_produit:
            item['quantite'] += quantite
            produit_existe = True
            break
    
    if not produit_existe:
        panier.append({'id_produit': id_produit, 'quantite': quantite})
    
    session['panier'] = panier
    session.modified = True
    
    flash(f'{produit["Nom"]} ajouté au panier !', 'success')
    return redirect(url_for('panier'))


@app.route('/retirer-panier/<int:id_produit>')
def retirer_panier(id_produit):
    """Retirer un produit du panier"""
    if 'id_client' not in session:
        flash('Vous devez être connecté', 'error')
        return redirect(url_for('connexion'))
    
    panier = session.get('panier', [])
    session['panier'] = [item for item in panier if item['id_produit'] != id_produit]
    session.modified = True
    
    flash('Produit retiré du panier', 'success')
    return redirect(url_for('panier'))


@app.route('/vider-panier')
def vider_panier():
    """Vider le panier"""
    if 'id_client' not in session:
        flash('Vous devez être connecté', 'error')
        return redirect(url_for('connexion'))
    
    session['panier'] = []
    session.modified = True
    
    flash('Panier vidé', 'success')
    return redirect(url_for('panier'))


@app.route('/commander', methods=['POST'])
def commander():
    """Passer une commande"""
    if 'id_client' not in session:
        flash('Vous devez être connecté pour commander', 'error')
        return redirect(url_for('connexion'))
    
    panier = session.get('panier', [])
    
    if not panier:
        flash('Votre panier est vide', 'error')
        return redirect(url_for('panier'))
    
    # Créer la commande en utilisant la classe Commande
    nom_client = session['nom']
    commande = Commande(nom_client)
    
    # Préparer la liste des produits
    liste_produits = [(item['id_produit'], item['quantite']) for item in panier]
    
    # Passer la commande
    resultat = commande.passer_commande(liste_produits)
    
    if resultat:
        # Vider le panier
        session['panier'] = []
        session.modified = True
        
        flash(f'Commande n°{resultat["id_commande"]} passée avec succès ! Total : {resultat["total"]:.2f} €', 'success')
        return redirect(url_for('profil'))
    else:
        flash('Erreur lors de la commande', 'error')
        return redirect(url_for('panier'))


@app.route('/compte')
def compte():
    """Page compte (alias de profil)"""
    return redirect(url_for('profil'))


# Gestionnaire d'erreur 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # Vérifier que la base de données existe
    if not os.path.exists(DB_PATH):
        print("⚠️  ERREUR: La base de données n'existe pas.")
        print("👉 Exécutez d'abord: python database/Init_BDD.py")
    else:
        print("✅ Base de données trouvée")
        print("🚀 Démarrage du serveur Flask...")
        app.run(debug=True, host='0.0.0.0', port=5000)
