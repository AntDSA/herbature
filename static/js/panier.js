// Base de données produits (identique à script.js)
const productsDB = {
    1: { 
        icon: '🌱', 
        title: 'Herbe morte', 
        price: 40,
        unit: '/m²'
    },
    2: { 
        icon: '🌱', 
        title: 'Herbe polluée', 
        price: 60,
        unit: '/m²'
    },
    3: { 
        icon: '🌱', 
        title: 'Herbe sèche', 
        price: 45,
        unit: '/m²'
    },
    4: { 
        icon: '🌱', 
        title: 'Herbe d\'élevage', 
        price: 90,
        unit: '/m²'
    },
    5: { 
        icon: '🌱', 
        title: 'Herbe à fleurs', 
        price: 100,
        unit: '/m²'
    },
    6: { 
        icon: '🌿', 
        title: 'Herbe peu polluée', 
        price: 80,
        unit: '/m²'
    },
    7: { 
        icon: '🌊', 
        title: 'Herbe marine', 
        price: 95,
        unit: '/m²'
    },
    8: { 
        icon: '✂️', 
        title: 'Herbe fraichement tondue', 
        price: 135,
        unit: '/m²'
    },
    9: { 
        icon: '🦁', 
        title: 'Herbe sauvage', 
        price: 120,
        unit: '/m²'
    },
    10: { 
        icon: '🏠', 
        title: 'Herbe cultivée sous serre', 
        price: 145,
        unit: '/m²'
    },
    11: { 
        icon: '🌍', 
        title: 'Herbe de chaque continants', 
        price: 160,
        unit: '/m²'
    },
    12: { 
        icon: '⭐', 
        title: 'Herbe excellent qualité', 
        price: 175,
        unit: '/m²'
    },
    13: { 
        icon: '👑', 
        title: 'Herbe en or', 
        price: 1000000,
        unit: ''
    }
};

// Charger le panier depuis localStorage
function loadCart() {
    const cart = localStorage.getItem('herbature_cart');
    return cart ? JSON.parse(cart) : [];
}

// Sauvegarder le panier dans localStorage
function saveCart(cart) {
    localStorage.setItem('herbature_cart', JSON.stringify(cart));
}

// Afficher le panier
function displayCart() {
    const cart = loadCart();
    const cartItemsList = document.getElementById('cart-items-list');
    const emptyCart = document.getElementById('empty-cart');
    const cartContent = document.getElementById('cart-content');

    // Si le panier est vide
    if (cart.length === 0) {
        emptyCart.style.display = 'block';
        cartContent.style.display = 'none';
        updateCartCount();
        return;
    }

    // Afficher le contenu du panier
    emptyCart.style.display = 'none';
    cartContent.style.display = 'grid';

    // Générer le HTML des articles
    cartItemsList.innerHTML = '';
    cart.forEach((item, index) => {
        const product = productsDB[item.productId];
        if (!product) return;

        const itemTotal = product.price * item.quantity;

        const cartItemHTML = `
            <div class="cart-item">
                <div class="cart-item-image">${product.icon}</div>
                
                <div class="cart-item-details">
                    <div class="cart-item-title">${product.title}</div>
                    <div class="cart-item-price">${product.price.toLocaleString('fr-FR')}€${product.unit}</div>
                    
                    <div class="cart-item-actions">
                        <div class="quantity-controls">
                            <button onclick="decreaseQuantity(${index})">-</button>
                            <span>${item.quantity}</span>
                            <button onclick="increaseQuantity(${index})">+</button>
                        </div>
                        <button class="remove-item" onclick="removeItem(${index})">
                            🗑️ Supprimer
                        </button>
                    </div>
                </div>

                <div class="cart-item-total">
                    <div class="item-total-price">${itemTotal.toLocaleString('fr-FR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}€</div>
                </div>
            </div>
        `;
        
        cartItemsList.innerHTML += cartItemHTML;
    });

    // Mettre à jour les totaux
    updateTotals();
    updateCartCount();
}

// Augmenter la quantité
function increaseQuantity(index) {
    const cart = loadCart();
    cart[index].quantity++;
    saveCart(cart);
    displayCart();
}

// Diminuer la quantité
function decreaseQuantity(index) {
    const cart = loadCart();
    if (cart[index].quantity > 1) {
        cart[index].quantity--;
        saveCart(cart);
        displayCart();
    }
}

// Supprimer un article
function removeItem(index) {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet article ?')) {
        const cart = loadCart();
        cart.splice(index, 1);
        saveCart(cart);
        displayCart();
    }
}

// Mettre à jour les totaux
function updateTotals() {
    const cart = loadCart();
    let subtotal = 0;

    cart.forEach(item => {
        const product = productsDB[item.productId];
        if (product) {
            subtotal += product.price * item.quantity;
        }
    });

    // Livraison gratuite si le montant dépasse 200€
    const shippingCost = subtotal >= 200 ? 0 : 15;
    const shippingText = subtotal >= 200 ? 'Gratuite' : '15,00€';

    // Calculer la TVA (20%)
    const tax = subtotal * 0.20;

    // Total
    const total = subtotal + shippingCost + tax;

    // Afficher les totaux
    document.getElementById('subtotal').textContent = subtotal.toLocaleString('fr-FR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '€';
    document.getElementById('shipping').textContent = shippingText;
    document.getElementById('tax').textContent = tax.toLocaleString('fr-FR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '€';
    document.getElementById('total').textContent = total.toLocaleString('fr-FR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '€';
}

// Mettre à jour le compteur du panier dans le header
function updateCartCount() {
    const cart = loadCart();
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    
    const cartCountHeader = document.getElementById('cart-count-header');
    if (cartCountHeader) {
        cartCountHeader.textContent = totalItems;
    }
}

// Appliquer un code promo
function applyPromo() {
    const promoInput = document.getElementById('promo-input');
    const promoCode = promoInput.value.trim().toUpperCase();

    // Codes promo disponibles
    const promoCodes = {
        'HERBE10': 0.10,  // 10% de réduction
        'HERBE20': 0.20,  // 20% de réduction
        'BIENVENUE': 0.15, // 15% de réduction
        'VIP30': 0.30      // 30% de réduction
    };

    if (promoCodes[promoCode]) {
        const discount = promoCodes[promoCode];
        const discountPercent = (discount * 100).toFixed(0);
        alert(`✅ Code promo "${promoCode}" appliqué !\nVous bénéficiez de ${discountPercent}% de réduction !`);
        
        // Ici vous pourriez ajouter la logique pour appliquer réellement la réduction
        // Par exemple, stocker le code promo dans localStorage et recalculer les totaux
        
        promoInput.value = '';
    } else if (promoCode === '') {
        alert('⚠️ Veuillez entrer un code promo');
    } else {
        alert('❌ Code promo invalide');
        promoInput.value = '';
    }
}

// Valider la commande
function checkout() {
    const cart = loadCart();
    
    if (cart.length === 0) {
        alert('⚠️ Votre panier est vide !');
        return;
    }

    // Calculer le total
    let total = 0;
    cart.forEach(item => {
        const product = productsDB[item.productId];
        if (product) {
            total += product.price * item.quantity;
        }
    });

    // Ajouter TVA et livraison
    const shippingCost = total >= 200 ? 0 : 15;
    const tax = total * 0.20;
    const finalTotal = total + shippingCost + tax;

    // Résumé de la commande
    let orderSummary = '📦 Résumé de votre commande :\n\n';
    cart.forEach(item => {
        const product = productsDB[item.productId];
        if (product) {
            orderSummary += `${item.quantity}x ${product.title} - ${(product.price * item.quantity).toFixed(2)}€\n`;
        }
    });
    orderSummary += `\n💰 Total : ${finalTotal.toFixed(2)}€`;
    orderSummary += '\n\n✅ Commande validée ! Vous allez être redirigé vers le paiement...';

    alert(orderSummary);

    // Ici, vous pourriez rediriger vers une vraie page de paiement
    // window.location.href = '../templates/paiement.html';

    // Pour la démo, on vide le panier
    // localStorage.removeItem('herbature_cart');
    // displayCart();
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    console.log('Panier chargé');
    displayCart();
});

// Fonction utilitaire pour ajouter un produit au panier (à appeler depuis la page produits)
function addToCartFromPage(productId, quantity = 1) {
    const cart = loadCart();
    
    // Vérifier si le produit existe déjà dans le panier
    const existingItem = cart.find(item => item.productId === productId);
    
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({ productId, quantity });
    }
    
    saveCart(cart);
    updateCartCount();
    
    return cart;
}

// Exporter les fonctions pour qu'elles soient accessibles globalement
if (typeof window !== 'undefined') {
    window.addToCartFromPage = addToCartFromPage;
    window.loadCart = loadCart;
    window.saveCart = saveCart;
}
