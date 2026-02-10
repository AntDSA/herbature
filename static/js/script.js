// Base de données produits complète avec les 13 produits du site
const productsDB = {
    1: { 
        icon: '🌱', 
        title: 'Herbe morte', 
        price: 40,
        unit: '/m²',
        description: 'Herbe peu odorente pour les plus petits budjets, abordable à tous.'
    },
    2: { 
        icon: '🌱', 
        title: 'Herbe polluée', 
        price: 60,
        unit: '/m²',
        description: 'Herbe qui à vécue dans les grandes villes telles que Paris ou Lyon, bien nettoyée pour vous éviter les cacas de chien.'
    },
    3: { 
        icon: '🌱', 
        title: 'Herbe sèche', 
        price: 45,
        unit: '/m²',
        description: 'Une herbe pour les nez fins avec une subtile odeure pour les renifleurs agueris. Attention aux irritations si vous en abusez.'
    },
    4: { 
        icon: '🌱', 
        title: 'Herbe d\'élevage', 
        price: 90,
        unit: '/m²',
        description: 'Herbe élevée avec les amours de nos petits agriculteurs en herbe qui les ont chouchoutées comme il le faut!'
    },
    5: { 
        icon: '🌱', 
        title: 'Herbe à fleurs', 
        price: 100,
        unit: '/m²',
        description: 'Herbe avec de jolies fleurs remplies de vies et de couleurs pour vous rappeler les belles campagnes de votre enfance.'
    },
    6: { 
        icon: '🌿', 
        title: 'Herbe peu polluée', 
        price: 80,
        unit: '/m²',
        description: 'Herbe récolltée pas loin des grandes villes, permet aux plus sensibles d\'éviter trop de pollution à prix pas trop élevé et de ne pas trop perdre d\'espérence de vie.'
    },
    7: { 
        icon: '🌊', 
        title: 'Herbe marine', 
        price: 95,
        unit: '/m²',
        description: 'Herbe récoltée sans abîmer les coraux pour le bien de la mer, avec un petit goût salé spécial pour les plus gourmands.'
    },
    8: { 
        icon: '✂️', 
        title: 'Herbe fraichement tondue', 
        price: 135,
        unit: '/m²',
        description: 'Herbe faite pour gambader et sentir l\'herbe fraîche et satisfaisante sous nos petits pieds, possède une odeur unique qui fait rêver chacuns.'
    },
    9: { 
        icon: '🦁', 
        title: 'Herbe sauvage', 
        price: 120,
        unit: '/m²',
        description: 'Herbe destinée aux plus fougueux d\'entre vous car récoltée dans les contrées les plus dangereuses pour satisfaire vos esprtis les plus combatifs.'
    },
    10: { 
        icon: '🏠', 
        title: 'Herbe cultivée sous serre', 
        price: 145,
        unit: '/m²',
        description: 'Herbe spéciale pour les plus sensibles et émotifs qui ne connais qu\'un environnement et un air pur de nos serres bio naturelles.'
    },
    11: { 
        icon: '🌍', 
        title: 'Herbe de chaque continants', 
        price: 160,
        unit: '/m²',
        description: 'Herbe récoltée sur chaque continant par nos équipes pour vous offir un choix variés qui ne connais pas de frontiè et parcourir le monde sans bouger de votre jardin. '
    },
    12: { 
        icon: '⭐', 
        title: 'Herbe excellent qualité', 
        price: 175,
        unit: '/m²',
        description: 'Herbe de haute qualité pour les palets les plus raffinés et connaisseurs de gouts subtils et différenciés.'
    },
    13: { 
        icon: '👑', 
        title: 'Herbe en or', 
        price: 1000000,
        unit: '',
        description: 'Herbe 100% en or cultivée dans un endroit spécial et caché de la population ce qui nous permet d\'obtenir cette perfection.'
    }
};

// Variable pour stocker le produit actuellement affiché
let currentProduct = null;

// ==================== GESTION DU PANIER ====================

// Charger le panier depuis localStorage
function loadCart() {
    const cart = localStorage.getItem('herbature_cart');
    return cart ? JSON.parse(cart) : [];
}

// Sauvegarder le panier dans localStorage
function saveCart(cart) {
    localStorage.setItem('herbature_cart', JSON.stringify(cart));
}

// Mettre à jour le compteur du panier dans le header
function updateCartCount(additionalItems = 0) {
    const cart = loadCart();
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    
    // Mettre à jour dans le header
    const cartLinks = document.querySelectorAll('a[href*="panier"]');
    cartLinks.forEach(link => {
        const match = link.textContent.match(/(.*?)(\d+)(.*)/);
        if (match) {
            link.innerHTML = match[1] + totalItems + match[3];
        } else {
            link.textContent = '🛒 Panier (' + totalItems + ')';
        }
    });
}

// ==================== NAVIGATION ====================

// Voir les détails d'un produit
function viewProduct(productId) {
    console.log('Affichage du produit:', productId);
    
    // Mettre à jour le produit actuel
    currentProduct = productId;
    
    // 1. Cacher la page produits
    const productsPage = document.getElementById('products');
    const productDetailPage = document.getElementById('produit_detail');
    
    if (productsPage) {
        productsPage.classList.remove('active');
        productsPage.style.display = 'none';
    }
    
    // 2. Afficher la page détail
    if (productDetailPage) {
        productDetailPage.classList.add('active');
        productDetailPage.style.display = 'block';
    }
    
    // 3. Cacher toutes les fiches de détails de produits
    const allDetails = document.querySelectorAll('#produit_detail .container[id]');
    allDetails.forEach(detail => {
        detail.style.display = 'none';
    });
    
    // 4. Afficher le détail du produit cliqué
    const productDetail = document.getElementById(productId.toString());
    if (productDetail) {
        productDetail.style.display = 'block';
    } else {
        console.error('Détail du produit non trouvé:', productId);
    }
    
    // 5. Réinitialiser la quantité
    const qtyInput = document.getElementById('quantity');
    if (qtyInput) {
        qtyInput.value = 1;
    }
    
    // 6. Scroll vers le haut
    window.scrollTo(0, 0);
}

// Naviguer entre les pages
function navigateTo(section) {
    console.log('Navigation vers:', section);
    
    const productsPage = document.getElementById('products');
    const productDetailPage = document.getElementById('produit_detail');
    
    if (section === 'products') {
        // Afficher la page produits
        if (productsPage) {
            productsPage.classList.add('active');
            productsPage.style.display = 'block';
        }
        
        // Cacher la page détail
        if (productDetailPage) {
            productDetailPage.classList.remove('active');
            productDetailPage.style.display = 'none';
        }
        
        // Réinitialiser le produit actuel
        currentProduct = null;
        
        // Scroll vers le haut
        window.scrollTo(0, 0);
    }
}

// ==================== GESTION DES QUANTITÉS ====================

// Diminuer la quantité
function decreaseQty() {
    const qtyInput = document.getElementById('quantity');
    if (qtyInput && parseInt(qtyInput.value) > 1) {
        qtyInput.value = parseInt(qtyInput.value) - 1;
    }
}

// Augmenter la quantité
function increaseQty() {
    const qtyInput = document.getElementById('quantity');
    if (qtyInput) {
        qtyInput.value = parseInt(qtyInput.value) + 1;
    }
}

// ==================== AJOUTER AU PANIER ====================

// Ajouter au panier
function addToCart(productId) {
    // Déterminer quel produit ajouter
    let idToAdd = productId || currentProduct;
    let quantity = 1;
    
    // Si on est sur la page de détail, récupérer la quantité
    if (!productId && currentProduct) {
        const qtyInput = document.getElementById('quantity');
        quantity = qtyInput ? parseInt(qtyInput.value) : 1;
    }
    
    if (!idToAdd) {
        alert('⚠️ Erreur : Aucun produit sélectionné');
        return;
    }
    
    // Vérifier que le produit existe
    const product = productsDB[idToAdd];
    if (!product) {
        alert('⚠️ Erreur : Produit introuvable');
        return;
    }
    
    // Charger le panier actuel
    const cart = loadCart();
    
    // Vérifier si le produit existe déjà dans le panier
    const existingItem = cart.find(item => item.productId === idToAdd);
    
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({ 
            productId: idToAdd, 
            quantity: quantity 
        });
    }
    
    // Sauvegarder le panier
    saveCart(cart);
    
    // Mettre à jour le compteur
    updateCartCount();
    
    // Message de confirmation
    if (quantity === 1) {
        alert('✅ ' + product.title + ' a été ajouté au panier !');
    } else {
        alert('✅ ' + quantity + ' x ' + product.title + ' ajoutés au panier !');
    }
}

// ==================== ACHETER MAINTENANT ====================

// Acheter maintenant
function buyNow() {
    if (!currentProduct) {
        alert('⚠️ Veuillez sélectionner un produit');
        return;
    }
    
    const product = productsDB[currentProduct];
    const qtyInput = document.getElementById('quantity');
    const qty = qtyInput ? parseInt(qtyInput.value) : 1;
    
    if (product) {
        // Ajouter au panier
        addToCart(currentProduct);
        
        // Rediriger vers le panier
        setTimeout(() => {
            window.location.href = '../templates/panier.html';
        }, 500);
    } else {
        alert('⚠️ Produit introuvable');
    }
}

// ==================== RECHERCHE ====================

// Fonction de recherche
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    
    if (searchButton) {
        searchButton.addEventListener('click', function() {
            const query = searchInput ? searchInput.value.toLowerCase() : '';
            if (query) {
                alert('Recherche pour : ' + query);
                // Ici vous pouvez implémenter la vraie logique de recherche
            }
        });
    }
    
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const query = searchInput.value.toLowerCase();
                if (query) {
                    alert('Recherche pour : ' + query);
                    // Ici vous pouvez implémenter la vraie logique de recherche
                }
            }
        });
    }
}

// ==================== FORMULAIRE DE CONTACT ====================

// Gestion du formulaire de contact (si présent dans la page)
function setupContactForm() {
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const subject = document.getElementById('subject').value;
            const message = document.getElementById('message').value;
            
            // Simulation d'envoi
            alert('Merci ' + name + ' !\n\nVotre message a été envoyé avec succès.\nNous vous répondrons dans les plus brefs délais à l\'adresse : ' + email);
            
            // Réinitialiser le formulaire
            this.reset();
        });
    }
}

// ==================== FAQ ====================

// Toggle FAQ
function toggleFaq(element) {
    if (element) {
        element.classList.toggle('active');
    }
}

// ==================== IMAGES DE PRODUITS ====================

// Ajouter les emojis dans les images de produits (optionnel)
function updateProductImages() {
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach((card, index) => {
        const productId = index + 1;
        const product = productsDB[productId];
        if (product) {
            const imageDiv = card.querySelector('.product-image');
            if (imageDiv && imageDiv.textContent === '...') {
                imageDiv.textContent = product.icon;
            }
        }
    });
}

// ==================== INITIALISATION ====================

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    console.log('Script chargé avec succès !');
    console.log('Produits disponibles:', Object.keys(productsDB).length);
    
    // Configurer la recherche
    setupSearch();
    
    // Configurer le formulaire de contact
    setupContactForm();
    
    // Mettre à jour le compteur du panier
    updateCartCount();
    
    // S'assurer que la page produits est affichée par défaut
    const productsPage = document.getElementById('products');
    const productDetailPage = document.getElementById('produit_detail');
    
    if (productsPage) {
        productsPage.classList.add('active');
        productsPage.style.display = 'block';
    }
    
    if (productDetailPage) {
        productDetailPage.classList.remove('active');
        productDetailPage.style.display = 'none';
    }
});
