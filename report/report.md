# Twitch to the moon
## MA-VI
#### Made by Florian Feuillade, Massimo De Santis et Cédric Campos Carvalho


### Design global

La couleur représente les mêmes couleurs que le site officiel *Twitch*.

Les *Typography guidelines* ont été respectées:
* Seulement deux polices sur tout le site.
* Les couleurs des textes sont balancées par rapport au thème du site et le background.
* Bon contraste pour les couleurs.
* Police sans serif.

Les graphes suivent les conseils suivants:
* Data-Ink ratio: Les graphes contiennent un fond pour contraster plus et les séparer du background blanc du site web.
* Pour effectuer les graduations, on "enlève" de l'encre au lieu d'en rajouter.
* Lie factor: Les échelles sont toutes respectées sauf sur le *plot radar* qui nécessitait une remise à l'échelle logarithmique, car la plage dynamique entre les valeurs les plus grandes et petites rendaient sa lecture illisible.

Tous les graphes contenant des lignes, offrent les fonctionnalités suivantes:
* Changement de couleurs avec des thèmes spéciales pour les daltoniens.
* Changement des marqueurs pour chaque point de la ligne.
* Zoom/Dézoom sur les graphes *(interraction: select)*.
* Sélection de zonnes grâce à un lassot *(interraction: select)*.
* Outil de capture d'écran sur le graphe.
* Possiblité d'enlever des lignes via la légende *(interraction: select)*.

L'outil de la comparaison entre les jeux suit le principe de l'**interaction**. Pouvoir ajouter/enlever des jeux via une recherche et les ajouter/enlever sur les graphiques et tableaux permet de **filtrer** ou encore **explorer** d'autres données. La navigation entre les deux pages permet de **reconfigurer** et montrer un arrangement différent de données.

**Response Time**: Toutes les interractions sont rapides et permettent une utilisation fluide du site web.

La cible pour l'**usabilité** du site se trouve au départ de la "power-curve" (=Nontechnical end-user).

Le site suit les cpnseils de "*The Rules of Usability*" suivantes:
* *Bliss/Distraction/Flow*: Dépendant de l'utilisateur, le site web ne fait rien de spécial sur ces points.
* *Documentation*: Utilisation simple, pas besoin de documentation.
* *Reversibility*: Toutes les actions possibles sont réversibles.
* *Confirmation*: Aucune confirmation, car aucune modification derrière.
* *Failure*: erreurs signalées (par exemple page non trouvée).
* *Default*: Par défaut, une fois arrivée sur la page d'un jeu on à déjà ses informations.

### Home Page
Le but de cette page est d'impacter l'utilisateur directement avec des gros chiffres. C'est pour cette raison que les boîtes sont grandes et de couleur. Pour essayer de donner encore plus de sens au chiffres, ils sont convertis en différentes périodes de temps.

Graphes :
* Un premier graphe représente le nombre de viewers moyennées tous les mois. Ce graphique sert à donner l'information de la croissance globale de la plateforme Twitch. L'idée de mettre une surface sous la courbe démontre mieux la croissance.
* Le deuxième graphe offre une visualisation pour les 5 plus gros jeux de la plateforme sous forme de lignes.

Une barre de recherche est disponible en haut à droite pour se rendre sur la page d'un jeu en particulier.

### Game page

Cette page a pour but d'afficher des informations plus détaillées sur le jeu et de les comparer avec d'autres. Le thème de cette page suit le thème principal.

Il contient trois graphes:
* Les données temporelles sur le nombre de spectateurs moyennés par mois.
* La domination en pourcentage du au fil du temps.
* Un radar plot avec les statistiques suivantes:
  * Avg viewers: Moyenne du nombre de viewers.
  * Ratio watch: Nombres de viewers/Nombres d'heures diffusés
  * Ratio: Moyenne du nombre de viewers par streamer
  * Streamers: Moyenne du nombre d'heure streamer au fil de l'année.
  * Views: Moyenne du nombre d'heure vue au fil de l'année.

Toutes les échelles sont mises à l'échelle logarithmique pour avoir une meilleure visualisation entre les petits et grands jeux. Le tableau est là pour donner les valeurs réelles. Les chiffres trop grands sont remplacés par l'unité $k$.

La barre de recherche offre la possibilité de taper le nom des jeux (avec filtrage sur la liste complète pendant la recherche) puis de les comparer. Les ajouts sont reversibles et visibles à l'oeil de l'utilisateur sur la barre de recherche. Chaque ajout/supression de jeu va mettre à jour les trois graphes et le tableau.

### Source

Les sources utilisées pour ce site web viennent d'une base de données trouvée sur [Top games on Twitch 2016 - 2021 kaggle.com](https://www.kaggle.com/rankirsh/evolution-of-top-games-on-twitch).

Elle contient les données mensuelles suivantes pour chaque jeu (de 2016 à 2021):
* Rank
* Hours watched
* Hours streamed
* Peak viewers
* Peak channels
* Streamers
* Avg viewers
* Avg channels
* Avg viewer ratio
