import sqlite3

DB_PATH = 'database/gazon.db'


class NotationProduit:
    """Système de notation automatique des produits"""
    
    def __init__(self):
        self.conn = None
        self.cur = None
    
    def connecter_db(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cur = self.conn.cursor()
    
    def fermer_db(self):
        if self.conn:
            self.conn.close()
    
    def calculer_note(self, provenance, qualite, pollution):
        """
        Calcule la note d'un produit sur 10
        
        Critères :
        - Provenance France : +2 points
        - Provenance International : -1 point
        - Qualité (Parfaite/Excellente) : +3 points
        - Qualité (Bonne) : +2 points
        - Qualité (Médiocre/Basse) : +1 point
        - Pollution < 20 : +3 points
        - Pollution 20-50 : +1 point
        - Pollution > 50 : -2 points
        
        Note de base : 5/10
        """
        note = 5.0
        
        if provenance and 'France' in provenance:
            note += 2.0
        elif provenance and provenance != 'France':
            note -= 1.0
        
        if qualite:
            qualite_lower = qualite.lower()
            if 'parfaite' in qualite_lower or 'excellente' in qualite_lower:
                note += 3.0
            elif 'bonne' in qualite_lower:
                note += 2.0
            elif 'médiocre' in qualite_lower or 'basse' in qualite_lower:
                note += 1.0
        
        if pollution is not None:
            if pollution < 20:
                note += 3.0
            elif pollution <= 50:
                note += 1.0
            else:
                note -= 2.0
        
        if note > 10:
            note = 10.0
        elif note < 0:
            note = 0.0
        
        return round(note, 2)
    
    def mettre_a_jour_note_produit(self, id_produit):
        """Met à jour la note d'un produit spécifique"""
        try:
            self.connecter_db()
            
            self.cur.execute("""
                SELECT Provenance, Qualiter, Nv_Polution
                FROM produit
                WHERE id_P = ?
            """, (id_produit,))
            
            result = self.cur.fetchone()
            
            if not result:
                return False
            
            provenance, qualite, pollution = result
            note = self.calculer_note(provenance, qualite, pollution)
            
            self.cur.execute("""
                UPDATE produit
                SET Note = ?
                WHERE id_P = ?
            """, (note, id_produit))
            
            self.conn.commit()
            return True
            
        except sqlite3.Error as e:
            if self.conn:
                self.conn.rollback()
            return False
            
        finally:
            self.fermer_db()
    
    def mettre_a_jour_toutes_notes(self):
        """Met à jour les notes de tous les produits"""
        try:
            self.connecter_db()
            
            self.cur.execute("""
                SELECT id_P, Nom, Provenance, Qualiter, Nv_Polution
                FROM produit
            """)
            
            produits = self.cur.fetchall()
            nb_mis_a_jour = 0
            
            for produit in produits:
                id_p, nom, provenance, qualite, pollution = produit
                note = self.calculer_note(provenance, qualite, pollution)
                
                self.cur.execute("""
                    UPDATE produit
                    SET Note = ?
                    WHERE id_P = ?
                """, (note, id_p))
                
                nb_mis_a_jour += 1
            
            self.conn.commit()
            return nb_mis_a_jour
            
        except sqlite3.Error as e:
            if self.conn:
                self.conn.rollback()
            return 0
            
        finally:
            self.fermer_db()
    
    def obtenir_note_produit(self, id_produit):
        """Récupère la note d'un produit par son ID"""
        try:
            self.connecter_db()
            
            self.cur.execute("""
                SELECT Note
                FROM produit
                WHERE id_P = ?
            """, (id_produit,))
            
            result = self.cur.fetchone()
            
            if result and result[0] is not None:
                return result[0]
            return None
            
        except sqlite3.Error as e:
            return None
            
        finally:
            self.fermer_db()
    
    def afficher_notes_produits(self):
        """Affiche tous les produits avec leurs notes"""
        try:
            self.connecter_db()
            
            self.cur.execute("""
                SELECT Nom, Provenance, Qualiter, Nv_Polution, Note
                FROM produit
                ORDER BY Note DESC
            """)
            
            produits = self.cur.fetchall()
            
            print("\nNOTATION DES PRODUITS")
            print("-" * 80)
            
            for produit in produits:
                nom, provenance, qualite, pollution, note = produit
                pollution_str = f"{pollution}%" if pollution is not None else "N/A"
                note_str = f"{note}/10" if note is not None else "Non notée"
                
                print(f"{nom:<35} | Note: {note_str:<6} | Pollution: {pollution_str:<5} | {qualite}")
            
            print("-" * 80)
            
        except sqlite3.Error as e:
            print(f"Erreur : {e}")
            
        finally:
            self.fermer_db()


if __name__ == '__main__':
    
    notation = NotationProduit()
    
    print("=== CALCUL DES NOTES ===")
    nb = notation.mettre_a_jour_toutes_notes()
    print(f"{nb} produits mis a jour")
    
    print("\n=== AFFICHAGE DES NOTES ===")
    notation.afficher_notes_produits()
    
    print("\n=== TEST CALCUL MANUEL ===")
    note1 = notation.calculer_note("France", "Excellente", 5)
    print(f"France + Excellente + 5% pollution = {note1}/10")
    
    note2 = notation.calculer_note("International", "Basse", 85)
    print(f"International + Basse + 85% pollution = {note2}/10")