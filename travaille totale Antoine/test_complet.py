from database.database import Client, Commande, get_note
from database.panier import Panier, HistoriqueCommandes


# print("=== INSCRIPTION ===")
# client = Client("test.nsi@email.fr", "password123")
# resultat = client.inscrire("TestNom", "TestPrenom", "1 rue Test", "Lyon", "69000")

# if resultat:
#     print(f"Client cree : {resultat['prenom']} {resultat['nom']}")
#     id_client = resultat['id_client']
# else:
#     print("Erreur inscription")
#     exit()


# print("\n=== CONNEXION ===")
# client_co = Client("antoine42@email.fr", "password456")
# infos = client_co.connexion()


# if infos:
#     print(f"Connecte : {infos['prenom']} {infos['nom']}")
#     id_client = infos['id_client']
#     nom_client = infos['nom']
# else:
#     print("Erreur connexion")
#     exit()
    


# print("\n=== PANIER ===")
# panier = Panier(id_client)

# panier.ajouter_produit(1, 5)
# panier.ajouter_produit(2, 3)
# panier.ajouter_produit(4, 10)

# panier.afficher_panier()

# # pas de print pcq déja une fonction d'afichage dans le code 

# print("\n=== COMMANDE 1 ===")
# liste_produits = panier.obtenir_liste_produits()
# commande1 = Commande(nom_client)
# resultat1 = commande1.passer_commande(liste_produits)

# if resultat1:
#     print(f"Commande n°{resultat1['id_commande']}")
#     for p in resultat1['produits']:
#         print(f"  {p['nom']} x{p['quantite']}")
#     print(f"Total : {resultat1['total']:.2f} euros")
    
# panier.vider_panier()


# print("\n=== COMMANDE 2 ===")
# panier.ajouter_produit(1, 2)
# panier.ajouter_produit(3, 27)
# panier.ajouter_produit(2, 4)
# panier.ajouter_produit(4, 100)

# liste_produits = panier.obtenir_liste_produits()
# commande2 = Commande(nom_client)
# resultat2 = commande2.passer_commande(liste_produits)

# if resultat2:
#     print(f"Commande n°{resultat2['id_commande']}")
#     for p in resultat2['produits']:
#         print(f"  {p['nom']} x{p['quantite']}")
#     print(f"Total : {resultat2['total']:.2f} euros")

# panier.vider_panier()


# print("\n=== HISTORIQUE ===")
# historique = HistoriqueCommandes(id_client)
# historique.charger_historique()
# historique.afficher_historique()

note = get_note(2)
print(note)