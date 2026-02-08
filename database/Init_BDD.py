import sqlite3
import hashlib
import os

DB_PATH = 'database/gazon.db'
SCHEMA_PATH = 'database/Table.sql'

def hasher_mot_de_passe(mdp):
    """Hash un mot de passe avec SHA-256"""
    return hashlib.sha256(mdp.encode()).hexdigest()

def calculer_note(provenance, qualite, pollution):
    """Calcule la note d'un produit sur 10"""
    note = 0.0
    
    # QUALITE (critère principal - sur 5 points)
    if qualite:
        qualite_lower = qualite.lower()
        if 'parfaite' in qualite_lower:
            note += 5.0
        elif 'excellente' in qualite_lower:
            note += 4.5
        elif 'bonne' in qualite_lower:
            note += 3.5
        elif 'médiocre' in qualite_lower:
            note += 2.0
        elif 'basse' in qualite_lower or 'morte' in qualite_lower:
            note += 0.5
    
    # POLLUTION (sur 3 points)
    if pollution is not None:
        if pollution == 0:
            note += 3.0
        elif pollution < 10:
            note += 2.5
        elif pollution < 30:
            note += 2.0
        elif pollution < 50:
            note += 1.0
        elif pollution < 70:
            note += 0.5
        else:
            note += 0.0
    
    # PROVENANCE (sur 2 points)
    if provenance:
        if 'France' in provenance:
            note += 2.0
        elif 'International' in provenance or ',' in provenance:
            note += 0.5
        else:
            note += 1.0
    
    if note > 10:
        note = 10.0
    elif note < 0:
        note = 0.0
    
    return round(note, 2)


def initialiser_database():
    """
    Crée la base de données et insère les données de test
    À exécuter UNE SEULE FOIS au début du projet
    """
    # Créer le dossier database s'il n'existe pas
    os.makedirs('database', exist_ok=True)
    
    # Supprimer l'ancienne base si elle existe (pour réinitialisation)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Ancienne base de données supprimée")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Créer les tables
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())
        
        # Ajouter des clients de test avec mots de passe hashés
        clients_test = [
            ('jean.dupont@email.fr', 'password123', 'Dupont', 'Jean', '12 rue des Fleurs', 'Paris', '75001'),
            ('antoine42@email.fr', 'password456', 'Tkt', 'Antoine', '42 rue de Paris', 'Paris', '75001'),
            ('snowden@email.fr', 'password789', 'Snowden', 'Edward', '13 rue des ambassades', 'Moscou', '00000'),
            ('mac.dem@email.fr', 'password111', 'Dimitrius', 'Marcus', '69 boulevard du Dévergondage', 'Paris', '75001'),
            ('niko.sarko@email.fr', 'password222', 'Sarkozy', 'Nicolas', 'Prison de Fleury-Mérogis', 'Fleury-Mérogis', '91700')
        ]
        
        for email, mdp, nom, prenom, adresse, ville, cp in clients_test:
            mdp_hash = hasher_mot_de_passe(mdp)
            cursor.execute("""
                INSERT INTO clients (Email, MDP, Nom, Prenom, Adresse, Ville, Code_Postal)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (email, mdp_hash, nom, prenom, adresse, ville, cp))
        
        cursor.execute("SELECT id_P, Provenance, Qualiter, Nv_Polution, Nom FROM produit")
        produits = cursor.fetchall()
        
        nb_notes = 0
        for produit in produits:
            id_p, provenance, qualite, pollution, Nom = produit
            note = calculer_note(provenance, qualite, pollution)
            cursor.execute("UPDATE produit SET Note = ? WHERE id_P = ?", (note, id_p))
            nb_notes += 1
            cursor.execute("UPDATE produit SET Note = 100 WHERE Nom = 'Herbe spéciale'",)
            
        
        conn.commit()
        print("Base de données créée avec succès")
        print(f"{len(clients_test)} clients de test ajoutés")
        print(f"{nb_notes} notes de produits calculées")
        print(f"Fichier : {DB_PATH}")

        
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la base : {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("INITIALISATION DE LA BASE DE DONNÉES")
    initialiser_database()
    print("\nVous pouvez maintenant utiliser database.py")