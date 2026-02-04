import sqlite3
from database.pile_file import Pile, File

DB_PATH = 'database/gazon.db'


class Panier:
    """
    Gestion du panier d'un client
    Utilise une Pile pour stocker les produits (LIFO)
    """
    
    def __init__(self, id_client):
        self.id_client = id_client
        self.produits = Pile()
        self.conn = None
        self.cur = None
    
    def connecter_db(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cur = self.conn.cursor()
    
    def fermer_db(self):
        if self.conn:
            self.conn.close()
    
    def ajouter_produit(self, id_produit, quantite):
        """Ajoute un produit au panier (empile)"""
        try:
            self.connecter_db()
            
            self.cur.execute("""
                SELECT id_P, Nom, Prix, Stock
                FROM produit
                WHERE id_P = ?
            """, (id_produit,))
            
            result = self.cur.fetchone()
            
            if not result:
                return False
            
            id_p, nom, prix, stock = result
            
            if quantite > stock:
                return False
            
            produit = {
                'id_produit': id_p,
                'nom': nom,
                'prix': prix,
                'quantite': quantite,
                'total': prix * quantite
            }
            
            self.produits.empiler(produit)
            return True
            
        except sqlite3.Error as e:
            return False
            
        finally:
            self.fermer_db()
    
    def retirer_dernier_produit(self):
        """Retire le dernier produit ajouté (dépile)"""
        return self.produits.depiler()
    
    def voir_dernier_produit(self):
        """Consulte le dernier produit sans le retirer"""
        return self.produits.sommet()
    
    def est_vide(self):
        """Vérifie si le panier est vide"""
        return self.produits.est_vide()
    
    def nombre_produits(self):
        """Retourne le nombre de produits dans le panier"""
        return self.produits.taille()
    
    def calculer_total(self):
        """Calcule le total du panier"""
        total = 0
        for produit in self.produits.elements:
            total += produit['total']
        return total
        
    def obtenir_liste_produits(self):
        """Retourne la liste des produits pour passer commande"""
        liste = []
        for produit in self.produits.elements:
            liste.append((produit['id_produit'], produit['quantite']))
        return liste
    
    def vider_panier(self):
        """Vide complètement le panier"""
        self.produits.vider()


    def afficher_panier(self):
        """Affiche le contenu du panier"""
        if self.est_vide():
            print("Panier vide")
            return
        
        print(f"\nPanier du client {self.id_client} :")
        print("-" * 60)
        for i in range(len(self.produits.elements) - 1, -1, -1):
            p = self.produits.elements[i]
            print(f"  {p['nom']:<30} x{p['quantite']:<3} {p['total']:>8.2f} euros")
        print("-" * 60)
        print(f"{'TOTAL':>46} {self.calculer_total():>8.2f} euros")


class HistoriqueCommandes:
    """
    Gestion de l'historique des commandes d'un client
    Utilise une File pour stocker les commandes (FIFO)
    """
    
    def __init__(self, id_client):
        self.id_client = id_client
        self.commandes = File()
    
    def ajouter_commande(self, commande):
        """Ajoute une commande à l'historique (enfile)"""
        self.commandes.enfiler(commande)
    
    def obtenir_premiere_commande(self):
        """Consulte la première commande sans la retirer"""
        return self.commandes.premier()
    
    def retirer_premiere_commande(self):
        """Retire la première commande (défile)"""
        return self.commandes.defiler()
    
    def est_vide(self):
        """Vérifie si l'historique est vide"""
        return self.commandes.est_vide()
    
    def nombre_commandes(self):
        """Retourne le nombre de commandes"""
        return self.commandes.taille()
    
    def charger_historique(self):
        """Charge l'historique depuis la base de données"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            
            cur.execute("""
                SELECT cc.id_CC, cc.Date, 
                       SUM(p.Prix * fcc.Quantité) as total
                FROM commande_client cc
                JOIN fiche_CC fcc ON cc.id_CC = fcc.id_CC
                JOIN produit p ON fcc.id_P = p.id_P
                WHERE cc.id_C = ?
                GROUP BY cc.id_CC, cc.Date
                ORDER BY cc.Date ASC
            """, (self.id_client,))
            
            commandes = cur.fetchall()
            
            for commande in commandes:
                self.commandes.enfiler({
                    'id_commande': commande[0],
                    'date': commande[1],
                    'total': commande[2]
                })
            
            conn.close()
            return True
            
        except sqlite3.Error as e:
            return False
    
    def afficher_historique(self):
        """Affiche l'historique des commandes"""
        if self.est_vide():
            print("Aucune commande dans l'historique")
            return
        
        print(f"\nHistorique des commandes du client {self.id_client} :")
        print("-" * 60)
        for i, cmd in enumerate(self.commandes.elements):
            print(f"  [{i+1}] Commande n°{cmd['id_commande']} - {cmd['date']} - {cmd['total']:.2f} euros")
        print("-" * 60)


