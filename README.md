**Présentation projet.**

Voici le code de mon projet de site de vente en ligne dans le cadre de mon évaluation de compétences du bloc 3 développement d'une solution digitale.

L'objectif était de réaliser un front ainsi qu'un back afin de pouvoir rentrer des produits pour l'enseigne de vente de produits "Mercadona".

La programmation est en langage Python et le framework utilisé est Flask. La base de données utilisée est PostgreSQL.


**Back-end.**

Nous pouvons nous connecter à l'interface administrateur avec login et mot de passe qui sont stockés dans la base de données sous forme cryptée avec le module "bcrypt". La session administrateur autorise la connexion au back et il est alors possible d'intégrer de nouveaux produit en renseignant : 

le libelle, la description, le prix, une image ainsi que la catégorie.

Nous pouvons ajouter de nouvelles catégories.

Nous pouvons ajouter sur un produit particulier une promotion directement visible en rouge sur le front lors de la présentation du produit.

Nous pouvons accéder à la page des clients qui ont effectués une demande d'inscription via un formulaire sécurisé par le module "FLaskForm", ajout des protections contre les attaques XSS (CSRFProtect) et les injections de code. L'administrateur peut accepter un nouveau client et celui-ci est autorisé à profiter des promotions, il est prévenu par réception d'un mail automatique dès lors où l'administrateur l'accepte en tant que "superclient".


**Front-end.**

La première page est un accueil présentant les magasins "Mercadona", horaires d'ouverture, type de produits vendus avec images et descriptions.

Plusieurs lien ont été ajoutés dans le header : 
- Le site de Mercadona.
- Le wiki de Mercadona.
- La souscription utilisateur.
- La connexion administrateur.
- La connexion en tant que "superclient" pour profiter des promotions.
- La redirection vers le catalogue.

Le produits sont présentés via une interface de trente produits par page. Nous pouvons sélectionner les produits par catégorie. Les informations comme le libelle, la description, le prix ainsi que le prix réduit s'il y a, sont visibles.

Les fonctionnalités comme le forum, le remboursement, le panier et l'API de paiement n'ont pas été ajoutées car elles n'étaient pas demandées. 


**Footer.**

Il possède des liens vers : 
- Les informations de contact de l'entreprise mère.
- Les services proposés par Mercadona.
- Le service client des magasins Mercadona.
- Les mentions légales.
- La politique de confidentialité.
- Les liens vers facebook, X et instagram.
- Les droits d'auteurs factices me concernant.


  
