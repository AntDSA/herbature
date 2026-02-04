CREATE TABLE clients (
    id_C INTEGER PRIMARY KEY AUTOINCREMENT,
    Email VARCHAR(255) UNIQUE NOT NULL,
    MDP VARCHAR(255) NOT NULL,
    Nom VARCHAR(100) NOT NULL,
    Prenom VARCHAR(100) NOT NULL,
    Adresse TEXT,
    Ville VARCHAR(100),
    Code_Postal VARCHAR(10)
);

CREATE TABLE fournisseurs (
    id_F INTEGER PRIMARY KEY AUTOINCREMENT,
    Nom VARCHAR(150) NOT NULL,
    Adresse TEXT,
    Délai_livr INTEGER
);

CREATE TABLE produit (
    id_P INTEGER PRIMARY KEY AUTOINCREMENT,
    Nom VARCHAR(150) NOT NULL,
    Description TEXT,
    Prix DECIMAL(10, 2) NOT NULL,
    Promo DECIMAL(5, 2) DEFAULT 0,
    Stock INTEGER DEFAULT 0,
    Provenance TEXT,
    Qualiter TEXT,
    Nv_Polution INTEGER,
    Production TEXT,
    Type TEXT,
    Note DECIMAL(3, 2),
    Note_Client TEXT,
    P_HT DECIMAL(10, 2),
    id_F INTEGER,
    FOREIGN KEY (id_F) REFERENCES fournisseurs(id_F)
);

CREATE TABLE commande_client (
    id_CC INTEGER PRIMARY KEY AUTOINCREMENT,
    Date DATE NOT NULL,
    id_C INTEGER NOT NULL,
    FOREIGN KEY (id_C) REFERENCES clients(id_C)
);

CREATE TABLE fiche_CC (
    id_F_CC INTEGER PRIMARY KEY AUTOINCREMENT,
    id_CC INTEGER NOT NULL,
    id_P INTEGER NOT NULL,
    Quantité INTEGER NOT NULL,
    FOREIGN KEY (id_CC) REFERENCES commande_client(id_CC),
    FOREIGN KEY (id_P) REFERENCES produit(id_P)
);

CREATE TABLE commande_fournisseur (
    id_CF INTEGER PRIMARY KEY AUTOINCREMENT,
    Date DATE NOT NULL,
    id_F INTEGER NOT NULL,
    FOREIGN KEY (id_F) REFERENCES fournisseurs(id_F)
);

CREATE TABLE fiche_CF (
    id_F_CF INTEGER PRIMARY KEY AUTOINCREMENT,
    id_CF INTEGER NOT NULL,
    id_P INTEGER NOT NULL,
    Quantité INTEGER NOT NULL,
    FOREIGN KEY (id_CF) REFERENCES commande_fournisseur(id_CF),
    FOREIGN KEY (id_P) REFERENCES produit(id_P)
);

-- Index pour optimisation
CREATE INDEX idx_clients_email ON clients(Email);
CREATE INDEX idx_produit_type ON produit(Type);
CREATE INDEX idx_commande_client_date ON commande_client(Date);
CREATE INDEX idx_commande_fournisseur_date ON commande_fournisseur(Date);

-- Données de test 
INSERT INTO fournisseurs (Nom, Adresse, Délai_livr) VALUES
('GazonPro France', '10 rue de l''Industrie, 59000 Lille', 7),
('Verdura International', '25 avenue des Champs, 33000 Bordeaux', 14),
('HerbaNature Bio', '3 chemin des Prés Verts, 46000 Cahors', 5),
('UrbanGrass', '18 boulevard Haussmann, 75009 Paris', 3),
('Oceanica Flora', 'Port de la Mer, 13008 Marseille', 10),
('Exotic Green World', 'Zone Export, 97100 Pointe-à-Pitre', 21),
('LuxGrass Prestige', '1 avenue du Luxe, 98000 Monaco', 30);


INSERT INTO produit (Nom, Description, Prix, Stock, Provenance, Qualiter, Nv_Polution, Type, id_F) VALUES
-- PRIX BAS
('Herbe morte', 'Herbe avec peu d''odeur pour les plus petits budgets.', 40.00, 95, 'France', 'Basse', 70, 'Bronze 3', 1),
('Herbe polluée', 'Herbe issue des grandes villes, soigneusement nettoyée.', 60.00, 70, 'France', 'Basse', 85, 'Or 2', 4),
('Herbe sèche', 'Herbe subtile pour nez fins, à consommer avec modération.', 45.00, 85, 'France', 'Médiocre', 60, 'Or 1', 2),

-- PRIX MOYEN
('Herbe d''élevage', 'Herbe élevée avec soin par des agriculteurs passionnés.', 90.00, 60, 'France', 'Bonne', 20, 'Platine 3', 3),
('Herbe avec fleurs', 'Herbe fleurie rappelant la campagne et l''enfance.', 100.00, 45, 'France', 'Bonne', 10, 'Diamant 2', 3),
('Herbe peu polluée', 'Herbe récoltée près des villes avec pollution réduite.', 80.00, 65, 'France', 'Médiocre-Bonne', 40, 'Platine 1', 2),
('Herbe marine', 'Herbe marine au goût salé, respectueuse des coraux.', 95.00, 35, 'France', 'Bonne', 15, 'Diamant 1', 5),

-- PRIX FORT
('Herbe fraîchement tondue', 'Odeur fraîche et sensation naturelle sous les pieds.', 135.00, 40, 'France', 'Excellente', 5, 'Champion 2', 1),
('Herbe sauvage', 'Herbe récoltée dans des zones dangereuses.', 120.00, 30, 'France', 'Bonne', 25, 'Champion 1', 6),
('Herbe cultivée sous serre', 'Herbe bio cultivée en serre à air pur.', 145.00, 55, 'France', 'Excellente', 0, 'Champion 3', 3),
('Herbe de chaque continent', 'Herbe provenant de plusieurs pays pour un voyage sensoriel.', 160.00, 25, 'International', 'Bonne', 50, 'Champion 1', 6),

-- Exception
('Herbe spéciale', 'Herbe magique bio, relaxante et apaisante.', 1000.00, 30, 'France', 'Excellente', 0, 'SSL', 3),
('Herbe en or', 'Herbe en or pur, extrêmement rare et prestigieuse.', 1000000.00, 20, 'France', 'Parfaite', 0, 'SSL', 7);
