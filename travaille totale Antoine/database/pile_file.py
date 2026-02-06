class Pile:
    """
    Utilisée pour gérer les produits du panier
    Le dernier produit ajouté est le premier retiré
    """
    
    def __init__(self):
        self.elements = []
    
    def est_vide(self):
        """Vérifie si la pile est vide"""
        return len(self.elements) == 0
    
    def empiler(self, element):
        """Ajoute un élément au sommet de la pile"""
        self.elements.append(element)
    
    def depiler(self):
        """Retire et retourne l'élément au sommet de la pile"""
        if not self.est_vide():
            return self.elements.pop()
        return None
    
    def sommet(self):
        """Retourne l'élément au sommet sans le retirer"""
        if not self.est_vide():
            return self.elements[-1]
        return None
    
    def taille(self):
        """Retourne le nombre d'éléments dans la pile"""
        return len(self.elements)
    
    def afficher(self):
        """Affiche le contenu de la pile"""
        if self.est_vide():
            print("Pile vide")
        else:
            print("Pile (sommet -> bas) :")
            for i in range(len(self.elements) - 1, -1, -1):
                print(f"  [{i}] {self.elements[i]}")
    
    def vider(self):
        """Vide complètement la pile"""
        self.elements = []


class File:
    """
    Utilisée pour gérer l'historique des commandes
    La première commande ajoutée est la première consultée
    """
    
    def __init__(self):
        self.elements = []
    
    def est_vide(self):
        """Vérifie si la file est vide"""
        return len(self.elements) == 0
    
    def enfiler(self, element):
        """Ajoute un élément à la fin de la file"""
        self.elements.append(element)
    
    def defiler(self):
        """Retire et retourne le premier élément de la file"""
        if not self.est_vide():
            return self.elements.pop(0)
        return None
    
    def premier(self):
        """Retourne le premier élément sans le retirer"""
        if not self.est_vide():
            return self.elements[0]
        return None
    
    def taille(self):
        """Retourne le nombre d'éléments dans la file"""
        return len(self.elements)
    
    def afficher(self):
        """Affiche le contenu de la file"""
        if self.est_vide():
            print("File vide")
        else:
            print("File (premier -> dernier) :")
            for i, element in enumerate(self.elements):
                print(f"  [{i}] {element}")
    
    def vider(self):
        """Vide complètement la file"""
        self.elements = []
