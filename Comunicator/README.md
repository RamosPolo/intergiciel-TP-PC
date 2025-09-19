# Communicator

**Communicator** est un package Python destiné à gérer l'échange de
messages entre différents composants d'un système distribué.\
Il fournit plusieurs classes (par exemple `Com`, `Message`,
`MessageDedies`, `MessageSync`, etc.) permettant de créer, d'envoyer et
de synchroniser des messages tout en maintenant une horloge logique.

## Fonctionnalités principales

-   **Gestion des messages** : création d'objets `Message` et dérivés
    pour encapsuler les données.
-   **Synchronisation** : prise en charge d'un état de synchronisation
    (`SEND` / `CONFIRM`) via la classe `MessageSync`.
-   **Horloge logique** : chaque message transporte une estampille
    (horloge) pour faciliter la cohérence dans un contexte distribué.
-   **Extensibilité** : architecture modulaire facilitant l'ajout de
    nouveaux types de messages ou de protocoles.

## Installation

1. Clonez le dépôt ou téléchargez les sources.
2. Depuis le dossier racine, installez les dépendances

## Utilisation rapide

Exemple d'utilisation de la classe principale `Com` après installation :

``` python
from Communicator import Com

c = Com()
c.sendTo("Hello 2 from c !", 2)
```

## Documentation

Une documentation détaillée est disponible.

-   Elle est disponible en local dans le dossier **`/docs/index.html`**.
-   Pour la consulter, ouvrez simplement ce fichier dans votre
    navigateur web préféré.

Par exemple, double-cliquez sur le fichier ou faites un clic droit →
**Ouvrir avec votre navigateur**.

------------------------------------------------------------------------

© 2025 -- Projet Python Communicator -- @ Paul Coulmeau
