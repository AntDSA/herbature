import sqlite3
import hashlib
from datetime import datetime

DB_PATH = 'database/gazon.db'
STOCK_SECURITE = 10
DELAI_LIVRAISON_STANDARD = 2


class Client:
    def __init__(self, email, mot_de_passe):
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.nom = None
        self.prenom = None
        self.adresse = None
        self.ville = None
        self.code_postal = None
        self.id_client = None
        self.conn = None
        self.cur = None
    
    def connecter_db(self):
        """Ouvre la connexion à la base de données"""
        self.conn = sqlite3.connect(DB_PATH)
        self.cur = self.conn.cursor()
    
    def fermer_db(self):
        """Ferme la connexion à la base de données"""
        if self.conn:
            self.conn.close()
    
    def hasher_mot_de_passe(self):
        """Hash le mot de passe avec SHA-256"""
        return hashlib.sha256(self.mot_de_passe.encode()).hexdigest()
    
    def email_existe(self):
        self.cur.execute("SELECT id_C FROM clients WHERE Email = ?", (self.email,))
        result = self.cur.fetchone()
        return result is not None
    
    def valider_email(self):
        """Validation basique de l'email"""
        if '@' not in self.email or '.' not in self.email:
            return False
        if len(self.email) < 5:
            return False
        return True
    
    def valider_mot_de_passe(self):
        """Validation du mot de passe (minimum 6 caractères)"""
        if len(self.mot_de_passe) < 6:
            return False
        return True
    
    def inscrire(self, nom, prenom, adresse="", ville="", code_postal=""):
        """Inscrit un nouveau client dans la base de données"""
        try:
            self.connecter_db()
            
            if not self.valider_email():
                return None
            
            if not self.valider_mot_de_passe():
                return None
            
            if self.email_existe():
                return None
            
            self.nom = nom
            self.prenom = prenom
            self.adresse = adresse
            self.ville = ville
            self.code_postal = code_postal
            
            mdp_hash = self.hasher_mot_de_passe()
            
            self.cur.execute("""
                INSERT INTO clients (Email, MDP, Nom, Prenom, Adresse, Ville, Code_Postal)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (self.email, mdp_hash, self.nom, self.prenom, 
                  self.adresse, self.ville, self.code_postal))
            
            self.id_client = self.cur.lastrowid
            self.conn.commit()
            
            return {
                'id_client': self.id_client,
                'email': self.email,
                'nom': self.nom,
                'prenom': self.prenom,
                'adresse': self.adresse,
                'ville': self.ville,
                'code_postal': self.code_postal
            }
            
        except sqlite3.Error as e:
            if self.conn:
                self.conn.rollback()
            return None
            
        finally:
            self.fermer_db()
    
    def connexion(self):
        """Vérifie les identifiants du client pour la connexion"""
        try:
            self.connecter_db()
            
            mdp_hash = self.hasher_mot_de_passe()
            
            self.cur.execute("""
                SELECT id_C, Email, Nom, Prenom, Adresse, Ville, Code_Postal
                FROM clients 
                WHERE Email = ? AND MDP = ?
            """, (self.email, mdp_hash))
            
            result = self.cur.fetchone()
            
            if not result:
                return None
            
            return {
                'id_client': result[0],
                'email': result[1],
                'nom': result[2],
                'prenom': result[3],
                'adresse': result[4],
                'ville': result[5],
                'code_postal': result[6]
            }
            
        except sqlite3.Error as e:
            return None
            
        finally:
            self.fermer_db()
    
    def obtenir_par_id(self, id_client):
        try:
            self.connecter_db()
            
            self.cur.execute("""
                SELECT id_C, Email, Nom, Prenom, Adresse, Ville, Code_Postal
                FROM clients 
                WHERE id_C = ?
            """, (id_client,))
            
            result = self.cur.fetchone()
            
            if not result:
                return None
            
            return {
                'id_client': result[0],
                'email': result[1],
                'nom': result[2],
                'prenom': result[3],
                'adresse': result[4],
                'ville': result[5],
                'code_postal': result[6]
            }
            
        except sqlite3.Error as e:
            return None
            
        finally:
            self.fermer_db()
    
    def modifier_profil(self, nouvelles_infos):
        """Modifie les informations du client"""
        if not self.id_client:
            return False
        
        try:
            self.connecter_db()
            
            champs_modifiables = ['Nom', 'Prenom', 'Adresse', 'Ville', 'Code_Postal']
            
            for champ, valeur in nouvelles_infos.items():
                champ_sql = champ.capitalize()
                if champ_sql in champs_modifiables:
                    self.cur.execute(f"""
                        UPDATE clients 
                        SET {champ_sql} = ? 
                        WHERE id_C = ?
                    """, (valeur, self.id_client))
            
            self.conn.commit()
            return True
            
        except sqlite3.Error as e:
            if self.conn:
                self.conn.rollback()
            return False
            
        finally:
            self.fermer_db()


class Commande:
    
    def __init__(self, nom_client):
        self.nom_client = nom_client
        self.id_client = None
        self.id_commande = None
        self.produits = []
        self.total = 0
        self.conn = None
        self.cur = None
    
    def connecter_db(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cur = self.conn.cursor()
    
    def fermer_db(self):
        if self.conn:
            self.conn.close()
    
    def recuperer_id_client(self):
        """Récupère l'ID du client à partir de son nom"""
        self.cur.execute("SELECT id_C FROM clients WHERE Nom = ?", (self.nom_client,))
        result = self.cur.fetchone()
        
        if not result:
            return False
        
        self.id_client = result[0]
        return True
    
    def creer_commande(self):
        """Crée une nouvelle commande dans la base de données"""
        self.cur.execute("""
            INSERT INTO commande_client (Date, id_C) 
            VALUES (DATE('now'), ?)
        """, (self.id_client,))
        self.id_commande = self.cur.lastrowid
    
    def traiter_produit(self, id_produit, quantite):
        """vérifie stock, ajoute à la commande"""
        self.cur.execute("""
            SELECT p.Stock, p.id_F, p.Nom, p.Prix, f.Délai_livr
            FROM produit p
            JOIN fournisseurs f ON p.id_F = f.id_F
            WHERE p.id_P = ?
        """, (id_produit,))
        
        result = self.cur.fetchone()
        
        if not result:
            return
        
        stock_actuel, id_fournisseur, nom_produit, prix, delai_fournisseur = result
        
        prix_ligne = prix * quantite
        self.total += prix_ligne
        
        self.cur.execute("""
            INSERT INTO fiche_CC (id_CC, id_P, Quantité) 
            VALUES (?, ?, ?)
        """, (self.id_commande, id_produit, quantite))
        
        if quantite <= stock_actuel:
            self._gerer_stock_suffisant(id_produit, stock_actuel, quantite, nom_produit)
        else:
            self._gerer_stock_insuffisant(id_produit, id_fournisseur, stock_actuel, quantite, nom_produit, delai_fournisseur)
        
        self.produits.append({
            'nom': nom_produit,
            'quantite': quantite,
            'prix_unitaire': prix,
            'prix_total': prix_ligne
        })
    
    def _gerer_stock_suffisant(self, id_produit, stock_actuel, quantite, nom_produit):
        nouveau_stock = stock_actuel - quantite
        self.cur.execute("""
            UPDATE produit 
            SET Stock = ? 
            WHERE id_P = ?
        """, (nouveau_stock, id_produit))
    
    def _gerer_stock_insuffisant(self, id_produit, id_fournisseur, stock_actuel, quantite, nom_produit, delai_fournisseur):
        quantite_manquante = quantite - stock_actuel
        quantite_a_commander = quantite_manquante + STOCK_SECURITE
        
        self.cur.execute("""
            INSERT INTO commande_fournisseur (Date, id_F)
            VALUES (DATE('now'), ?)
        """, (id_fournisseur,))
        id_cf = self.cur.lastrowid
        
        self.cur.execute("""
            INSERT INTO fiche_CF (id_CF, id_P, Quantité) 
            VALUES (?, ?, ?)
        """, (id_cf, id_produit, quantite_a_commander))
        
        self.cur.execute("""
            UPDATE produit 
            SET Stock = 0 
            WHERE id_P = ?
        """, (id_produit,))
    
    def passer_commande(self, liste_produits):
        """Méthode principale pour passer une commande complète"""
        try:
            self.connecter_db()
            
            if not self.recuperer_id_client():
                return None
            
            self.creer_commande()
            
            for id_produit, quantite in liste_produits:
                self.traiter_produit(id_produit, quantite)
            
            self.conn.commit()
            
            return {
                'id_commande': self.id_commande,
                'nom_client': self.nom_client,
                'total': self.total,
                'produits': self.produits
            }
            
        except sqlite3.Error as e:
            if self.conn:
                self.conn.rollback()
            return None
            
        finally:
            self.fermer_db()

def get_note(id_produit):
    """Récupère la note d'un produit"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("SELECT Note FROM produit WHERE id_P = ?", (id_produit,))
    result = cur.fetchone()
    
    conn.close()
    
    if result and result[0] is not None:
        return result[0]
    return None