
        // Base de données produits
        const productsDB = {
            1: { 
                icon: '📱', 
                title: 'Herbe morte', 
                price: '40€',
                quantité: 'au m²',
                provenance: 'France',
                qualité: 'Basse'
            },
            
            2: { 
                icon: '📱', 
                title: 'Herbe polluée', 
                price: '60€',
                quantité: 'au m²',
                provenance: 'France',
                qualité: '85% de pollution'
            },

            3: { 
                icon: '📱', 
                title: 'Herbe sèche', 
                price: '45€',
                quantité: 'au m²',
                provenance: 'France',
                qualité: 'Médiocre'
            },
             
            4: { 
                icon: '📱', 
                title: 'Herbe délevage', 
                price: '90€',
                quantité: 'au m²',
                provenance: 'France',
                qualité: 'Bonne'
            },

            5: { 
                icon: '📱', 
                title: 'Herbe à fleurs', 
                price: '100€',
                quantité: 'au m²',
                provenance: 'France',
                qualité: 'Bonne'
            },
            
            6: { 
                icon: '📱', 
                title: 'Herbe morte', 
                price: '40€',
                quantité: 'au m²',
                provenance: 'France',
                qualité: 'Basse'
            },

            7: { 
                icon: '📱', 
                title: 'Herbe morte', 
                price: '40€',
                quantité: 'au m²',
                provenance: 'France',
                qualité: 'Basse'
            },

            8: { 
                icon: '📱', 
                title: 'Herbe morte', 
                price: '40€',
                quantité: 'au m²',
                provenance: 'France',
                qualité: 'Basse'
            },

            9: { 
                icon: '📱', 
                title: 'Herbe morte', 
                price: '40€',
                quantité: 'au m²',
                provenance: 'France',
                qualité: 'Basse'
            },

            10: { 
                icon: '📱', 
                title: 'Herbe morte', 
                price: '40€',
                quantité: 'au m²',
                provenance: 'France',
                qualité: 'Basse'
            },
            
            11: { 
                icon: '📱', 
                title: 'Herbe morte', 
                price: '40€',
                quantité: 'au m²',
                provenance: 'France',
                qualité: 'Basse'
            },

            12: { 
                icon: '📱', 
                title: 'Herbe morte', 
                price: '40€',
                quantité: 'au m²',
                provenance: 'France',
                qualité: 'Basse'
            },

            13: { 
                icon: '📱', 
                title: 'Herbe morte', 
                price: '40€',
                quantité: 'au m²',
                provenance: 'France',
                qualité: 'Basse'
            },
        };

        // Variable pour stocker le produit actuellement affiché
        let currentProduct = null;

        // Navigation entre les pages
        function navigateTo(pageName) {
            // Masquer toutes les pages
            const pages = document.querySelectorAll('.page');
            pages.forEach(page => page.classList.remove('active'));

            // Afficher la page demandée
            document.getElementById(pageName).classList.add('active');

            // Mettre à jour la navigation active
            const navLinks = document.querySelectorAll('.nav-link');
            navLinks.forEach(link => link.classList.remove('active'));

            // Scroll en haut
            window.scrollTo(0, 0);
        }


        // Voir les détails d'un produit
        function viewProduct(productId) {
            // 1. Retirer 'active' de products et l'ajouter à produit_detail
            document.getElementById('products').classList.remove('active');
            document.getElementById('produit_detail').classList.add('active');
            
            // 2. Cacher toutes les div container (détails produits)
            document.querySelectorAll('#produit_detail .container').forEach(div => {
                div.style.display = 'none';
            });
            
            // 3. Afficher le produit cliqué
            const productDetail = document.getElementById(productId);
            if (!productDetail) return;
            productDetail.style.display = 'block';
            
            // 4. Mettre à jour les informations du produit
            const product = productsDB[productId];
            if (product){
                document.getElementById('detailProductImage').textContent = product.icon;
                document.getElementById('detailProductTitle').textContent = product.title;
                document.getElementById('detailProductPrice').textContent = product.price;
                document.getElementById('specBrand').textContent = product.brand;
                document.getElementById('specModel').textContent = product.model;
                document.getElementById('specRef').textContent = product.ref;
                document.getElementById('quantity').value = 1;
            }
        }

        // Naviguer entre les pages
        function navigateTo(section) {
            if (section === 'products') {
                // Retirer 'active' de produit_detail et l'ajouter à products
                document.getElementById('produit_detail').classList.remove('active');
                document.getElementById('products').classList.add('active');
                
                // IMPORTANT : Réinitialiser le style inline de produit_detail
                document.getElementById('produit_detail').style.display = '';
            }
            
            if (section === 'product-detail') {
                // Retirer 'active' de products et l'ajouter à produit_detail
                document.getElementById('products').classList.remove('active');
                document.getElementById('produit_detail').classList.add('active');
            }
        }

        // Ajouter au panier
        function addToCart(productId) {
            if (productId) {
                const product = productsDB[productId];
                alert('✓ ' + product.title + ' a été ajouté au panier !');
            } else if (currentProduct) {
                const product = productsDB[currentProduct];
                const qty = document.getElementById('quantity').value;
                alert('✓ ' + qty + ' x ' + product.title + ' ajouté(s) au panier !');
            }
        }

        // Acheter maintenant
        function buyNow() {
            const product = productsDB[currentProduct];
            const qty = document.getElementById('quantity').value;
            alert('🛒 Commande de ' + qty + ' x ' + product.title + '\nTotal: ' + product.price + '\n\nRedirection vers le paiement...');
        }
        // Gestion du formulaire de contact
        document.getElementById('contactForm').addEventListener('submit', function(e) {
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

        // Toggle FAQ
        function toggleFaq(element) {
            element.classList.toggle('active');
        }

        function navigateTo(section) {
            if (section === 'products') {
                // Masquer les détails du produit
                document.getElementById('produit_detail').style.display = 'none';
                
                // Réafficher la grille des produits
                document.querySelector('.products-grid').style.display = 'grid';
            }
        }