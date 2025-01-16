# dashboard-analyse-vente

## Note méthodologique : preuve de concept

### 1. Dataset retenu

Pour cette étude, nous avons utilisé le dataset intitulé "Store Item Demand Forecasting Challenge" disponible sur la plateforme Kaggle. Ce dataset contient des données de ventes quotidiennes pour différents produits dans plusieurs magasins, couvrant une période de début 2013 à fin 2017.

**Description du dataset**

Le dataset initial comprend les colonnes suivantes : la date de la vente, l'identifiant du magasin, l’identifiant du produit, le nombre de ventes du produit.

Pour simplifier l'analyse et se concentrer sur une série univariée, nous avons filtré les données pour ne retenir que les ventes de l’item 1 (appelé "produit") dans le store 1 (appelé "magasin"). Après ce filtrage, les colonnes store et item n'ont plus d'intérêt et ont été supprimées.

**Objectif de la modélisation**

L'objectif de cette modélisation est de prévoir les ventes quotidiennes futures du produit. Le magasin nécessite des prévisions sur un horizon de deux mois maximums pour une gestion optimale des stocks. Bien que des prévisions hebdomadaires puissent être utiles, l'accent est mis sur des prédictions couvrant jusqu'à deux mois, voire une année, pour une planification à plus long terme.

De plus, cette étude vise à comparer les performances du modèle N-Beats avec celles du modèle SARIMAX afin de comparer les démarches de modélisations et les résultats.

### 2. Les concepts de l’algorithme récent : N-Beats

Le modèle N-Beats est un modèle de prévision de séries temporelles basé sur des réseaux de neurones. Il a été introduit par Boris Oreshkin et al. dans un article publié en 2020, intitulé "N-BEATS: Neural Basis Expansion Analysis for Time Series Forecasting". Ce modèle a démontré des performances supérieures sur plusieurs benchmarks de prévision de séries temporelles.

**Fonctionnement Général du Modèle N-Beats**

L’architecture du Modèle N-Beats utilise une architecture composée de blocs empilés, chacun étant responsable de capturer des patterns spécifiques dans les données. Les blocs peuvent être configurés pour se concentrer sur des tendances ou des saisonnalités, permettant ainsi une décomposition efficace des séries temporelles.

**Le principe de Fonctionnement**

Le modèle N-Beats apprend à partir des données historiques pour prédire les valeurs futures. Il est composé de plusieurs blocs, chacun étant conçu pour capturer différents aspects des données, tels que les tendances et les saisonnalités. Chaque bloc contribue à la prévision finale en analysant et en modélisant des patterns spécifiques dans les données, ce qui permet d'améliorer la précision globale des prévisions.

**Les hyperparamètres du Modèle N-Beats**

**Liste des Hyperparamètres**

- Nombre de blocs : Détermine le nombre de blocs dans le modèle.
- Taille des blocs : Spécifie la taille de chaque bloc.
- Nombre de couches : Indique le nombre de couches dans chaque bloc.
- Taille des couches : Définit la taille de chaque couche.
- Fenêtre de prévision : Détermine la longueur de la fenêtre de prévision.

**Fonction de Chaque Hyperparamètre**

- Nombre de blocs : Plus le nombre de blocs est élevé, plus le modèle peut capturer des patterns complexes.
- Taille des blocs : Une taille de bloc plus grande permet de capturer des patterns plus longs.
- Nombre de couches : Un nombre plus élevé de couches permet une modélisation plus profonde des données.
- Taille des couches : Une taille de couche plus grande permet de capturer plus de détails dans les données.
- Fenêtre de prévision : Une fenêtre de prévision plus longue permet de faire des prédictions sur une période plus étendue.

**Utilisation de la bibliothèque Darts**

Darts est une bibliothèque Python dédiée à la prévision de séries temporelles. Elle offre une interface simple et intuitive pour utiliser divers modèles de prévision, y compris N-Beats. Darts facilite l'intégration et l'évaluation de différents modèles, ce qui en fait un outil précieux pour les analystes de données.

**Extrait : International Journal of Forecasting (Journal international de prévision)**

Volume 39, numéro 2, Avril-juin 2023, Pages 884-900

> - Architecture du bloc : N-BEATS se compose d'une pile de réseaux neuronaux entièrement connectés appelé "blocs". Chaque bloc traite les données des séries temporelles d'entrée et délivre un ensemble de prévisions.
> - Blocs génériques et interprétables : Il existe deux types de blocs dans le N-BEATS: Generic et Interprétable. Les blocs génériques sont conçus pour apprendre les modèles sous-jacents dans les données automatiquement, tandis que les blocs interprétables intègrent des connaissances préalables sur les données et sont structurés pour fournir des informations sur les modèles appris.
> - Ensemble empilé : Les blocs sont empilés en un ensemble, et leurs prévisions sont combinées pour produire la prédiction finale. Cette approche d'ensemble permet à N-BEATS de traiter efficacement un large éventail de problèmes de prévision des séries chronologiques.
> - Partage et évolutivité des paramètres: N-BEATS est conçu avec le partage des paramètres à travers les blocs, ce qui favorise l'évolutivité et l'efficacité dans la formation et l'inférence.
> - Apprentissage rapide : N-BEATS est un apprentissage rapide, et il peut être formé à quelques époques sur un seul GPU. Cela permet d'expérimenter facilement différents hyperparamètres et architectures. Il s'installe généralement rapidement dans un minimum relatif. Comme de nombreux modèles peuvent être formés rapidement, il est facile de construire un ensemble de modèles différents pour améliorer les performances et la généralisation.

L'algorithme N-BEATS est un outil puissant pour la prévision des séries chronologiques, fournissant un mélange d'apprentissage automatique, d'interprétabilité et de performances robustes dans différents domaines.

### 3. La modélisation

#### a. Analyse des données

L'objectif de cette analyse des données est de comprendre les patterns et les tendances dans les ventes afin d'informer la modélisation. Nous allons utiliser plusieurs visualisations pour explorer les données.

**Visualisations des Ventes**

Graphique linéaire montrant l'évolution des ventes quotidiennes sur la période couverte par les données. Il permet d’identifier une tendance à la hausse suivant les années avec une saisonnalité hebdomadaire.

- ANOVA des ventes par rapport au jour de la semaine par année

Analyse de la variance (ANOVA) pour déterminer si les ventes varient significativement en fonction du jour de la semaine afin de comprendre l'impact des jours de la semaine sur les ventes.

**Résultat de l'ANOVA pour l'année 2013:**

- F-statistic: 9.62
- P-value: 0.0000

Les ventes dépendent significativement du jour de la semaine.

#### b. Les métriques 

Trois métriques adaptées aux séries chronologique on été suivis pour l’entrainement :

- **Root Mean Squared Error (RMSE)** : Le RMSE est la racine carrée de la moyenne des carrés des erreurs. Il mesure l'écart-type des résidus (erreurs de prédiction). Il est sensible aux grandes erreurs, ce qui est important pour la prévision des ventes où de grandes erreurs peuvent avoir un impact significatif sur la gestion des stocks.
- **Mean Absolute Error (MAE)** : Le MAE est la moyenne des valeurs absolues des erreurs. Il mesure la magnitude moyenne des erreurs de prédiction. Il est plus intuitif et facile à interpréter car il représente l'erreur moyenne en unités de la variable prédite (ventes). Il est moins sensible aux grandes erreurs si on compare au RMSE.
- **Mean Absolute Percentage Error (MAPE)** : Le MAPE est la moyenne des erreurs absolues en pourcentage des valeurs réelles. Il mesure la précision de la prévision en termes relatifs, ce qui permet de comparer l'erreur de prédiction entre différentes séries temporelles ou différentes périodes. Le MAPE est particulièrement utile pour évaluer les performances de modèles de prévision lorsque les valeurs réelles varient considérablement. Cependant, il peut être biaisé par des valeurs réelles proches de zéro.

#### c. Les données et la recherche des meilleures paramètres

**Préprocessing pour entrainer le modèle SARIMAX**

1. **Transformation des Ventes** : Pour stabiliser la variance des données de ventes et éviter les valeurs négatives, une transformation logarithmique a été appliqué permettant de gérer les grandes variations dans les données de ventes, rendant ainsi le modèle plus performant.
2. **Division des Données** : Les données ont été divisées en deux ensembles distincts : un ensemble d'entraînement de 2013 à 2016 et un ensemble de test qui couvre l’année 2017.
3. **Préparation de la série Temporelle** : Pour préparer les données de manière adéquate pour l'analyse temporelle, un tri des Données par Date a été effectué, un index Temporel a été défini, un ajustement afin de définir une fréquence quotidienne a été réalisé.
4. **Identification des Paramètres** : Utilisation de l'ACF (Autocorrelation Function) et PACF (Partial Autocorrelation Function) pour identifier les paramètres respectifs q et p. Utilisation de tests de stationnarité, comme le test de Dickey-Fuller, pour déterminer le paramètre d. Identification des paramètres saisonniers P, D, Q, et s en analysant les patterns saisonniers dans les données. 

cf (annexe (1) et annexe (2)) les résidus ne suivent pas une distribution normale et montrent hétéroscédasticité. Ils ne peuvent donc pas être considérés comme un bruit blanc, ce qui peut entraîner des prédictions non optimales.

**Préprocessing pour entraîner le modèle N-Beats**

Deux approches distinctes ont été utilisées pour préparer et entraîner le modèle N-Beats mais ont abouti à la même optimisation du modèle.

1. **Première Approche : Division en Trois Ensembles**

Les données normalisées ont été divisées en trois ensembles :
- Ensemble d'Entraînement : Comprend les données jusqu'au 31 décembre 2015.
- Ensemble de Validation : Comprend les données du 1er janvier 2016 au 31 décembre 2016.
- Ensemble de Test : Comprend les données à partir du 1er janvier 2017.

Les paramètres du modèle ont été optimisés en utilisant les résultats de l'ensemble de validation. Une fois les paramètres optimaux déterminés, le modèle a été réentraîné en combinant les ensembles d'entraînement et de validation.

2. **Deuxième Approche : Validation Croisée Temporelle**

La deuxième méthode a consisté à diviser les données en deux ensembles et à utiliser une validation croisée temporelle pour optimiser les paramètres.

#### d. Synthèse de la modélisation

Pour les deux modèles, peu de transformations des données ont été nécessaires. Aucune variable exogène n'a été utilisée dans un premier temps, afin de tester l'efficacité des modèles sur des données "brutes".

**Comparaison des modèles sur la recherche de paramètres et sur l’entrainement**

- **SARIMAX** : La recherche des paramètres pour le modèle SARIMAX demande du temps et une connaissance spécifique des séries temporelles. Cette étape est également gourmande en ressources mémoire. Malgré ces efforts, la recherche n'a pas permis d'aboutir à des résidus correspondant à un bruit blanc, ce qui montre les limites de ce modèle pour cette série temporelle.
- **N-Beats** : La bibliothèque Darts propose une implémentation rapide du modèle N-Beats. L'utilisation d'un GPU permet d'optimiser rapidement les hyperparamètres par validation croisée, rendant le processus d'entraînement plus efficace.

### 4. Les résultats

Les performances des deux modèles ont été évaluées en termes de RMSE (Root Mean Squared Error), MAE (Mean Absolute Error) et MAPE (Mean Absolute Percentage Error) pour des prédictions d’un an sur l’ensemble du jeu de test. Les métriques ont été calculées sur l'ensemble de l'année prédite ainsi que spécifiquement sur les deux premiers mois de cette période. Il est important de noter que, selon le produit, une prédiction à un an n’est pas forcément nécessaire. L’étendue des prédictions devrait en effet être discutée d’un point de vue métier.

Les résultats montrent que le modèle N-Beats dépasse le modèle SARIMAX en termes de précision des prévisions, que ce soit pour les résultats sur un an ou sur deux mois mais très largement sur la période d’un an.

### Conclusion

Le modèle SARIMAX représente une solution classique et bien établie pour la prévision des séries temporelles, il présente cependant des limitations en termes de complexité de paramétrage et de performance sur cette série de données. En revanche, le modèle N-Beats, grâce à son implémentation efficace dans la bibliothèque Darts et à l'utilisation de GPU, offre des prévisions plus rapides qui se révèlent en outre plus précises avec moins de transformations des données. Ces résultats suggèrent que N-Beats est mieux adapté pour cette tâche de prévision des ventes.

### 5. L’analyse de la feature importance globale et locale du nouveau modèle

Il est clair que le modèle N-Beats n'a pas réussi à capturer l’évolution saisonnière durant l’année, et il ne prédit pas toujours les pics de ventes certains jours de la semaine. Il semble donc important d’intégrer des covariables dans le modèle, notamment le jour de la semaine, le mois, et également des informations de position temporelle.

Pour améliorer les performances du modèle N-Beats, les covariables suivantes ont été intégrées :

- Covariables cycliques pour les mois futurs : Ces covariables permettent de capturer les variations saisonnières en représentant les mois de manière cyclique.
- Attributs de jour de la semaine futurs : Ces covariables aident le modèle à comprendre les variations hebdomadaires des ventes en incluant des informations sur le jour de la semaine.
- Covariables de position relative pour les périodes passées et futures : Ces covariables fournissent des informations sur la position temporelle relative des données, ce qui peut aider le modèle à mieux comprendre les tendances temporelles.
- Scaler pour normaliser les covariables : Un scaler est utilisé pour normaliser les covariables, ce qui permet d'améliorer la convergence du modèle et la stabilité de l'apprentissage.

L'intégration de ces covariables vise à fournir au modèle des informations contextuelles supplémentaires, permettant ainsi une meilleure capture des tendances et des variations saisonnières, et améliorant ainsi la précision des prévisions.

**Résultats**

Le MAPE est passé de 23.08 à 21.18 ce qui représente une baisse de 8,2% du pourcentage d’erreur moyen.

Si de plus on regroupe les prédictions par semaine ce qui peut correspondre à une période de livraison pour un magasin nous obtenons les résultats suivants :

- MAPE : 7.8

On obtient ainsi une erreur moyenne de moins de 8% par semaine.

Une étude statistique et graphique des données a montré que la saisonnalité hebdomadaire et l'importance des jours de la semaine jouent un rôle significatif dans les variations des ventes. Cette tendance saisonnière annuelle a été capturée par les covariables cycliques pour les mois futurs, permettant au modèle de mieux prédire les variations saisonnières. Les covariables de positions relatives pour les périodes passées et futures ont également contribué à améliorer la compréhension des tendances temporelles par le modèle. Les notions mises en jeu pour l’interprétabilité du modèle dépassent le cadre de cette mais le modèle N-Beats est conçu pour être interprétable en décomposant les séries temporelles en différentes composantes telles que les tendances et les saisonnalités.

**Feature Importance Globale**

- Le modèle N-Beats décompose les séries temporelles en plusieurs composantes. Chaque composante capture un aspect spécifique des données, comme les tendances à long terme ou les variations saisonnières. En analysant les contributions des différents blocs du modèle, il est possible de quantifier l'importance relative de chaque composante sur l'ensemble des données. Par exemple, les tendances peuvent représenter une part significative des prédictions, tandis que les saisonnalités peuvent exercer une influence moindre.

**Feature Importance Locale**

- L'importance locale des composantes peut être évaluée en analysant les contributions des différents blocs pour des périodes spécifiques. Par exemple, pendant les mois d'été, les composantes saisonnières peuvent exercer une influence plus importante sur les prédictions en raison de l'augmentation des ventes. En visualisant les contributions des composantes pour des périodes spécifiques, il est possible de comprendre comment les tendances et les saisonnalités varient au fil du temps et influencent les prédictions.

### 6. Les limites et les améliorations possibles

N-Beats offre des possibilités d'analyse avancées grâce à sa capacité à décomposer les séries temporelles en différentes composantes. Cependant, les concepts et les techniques nécessaires pour exploiter pleinement ces capacités dépassent le niveau de ce travail. Une exploration plus approfondie de ces fonctionnalités pourrait être envisagée dans des études futures pour tirer parti de l'interprétabilité et des insights offerts par le modèle N-Beats.

Une des principales limites observées dans ce travail est que le modèle N-Beats n'a pas réussi à prédire de manière précise la baisse significative des ventes durant le début octobre et le début novembre. Cette incapacité à capturer ces variations peut s'expliquer par l'absence de certains facteurs exogènes dans le modèle. Il est probable que des événements spécifiques, des vacances, des changements de comportement des consommateurs ou d'autres facteurs externes aient influencé ces baisses de ventes. Pour améliorer le modèle, il serait essentiel d'identifier et d'intégrer ces facteurs exogènes. Une analyse approfondie des données historiques et des événements contextuels pourrait aider à comprendre les raisons de ces baisses de ventes. En intégrant ces informations supplémentaires comme covariables dans le modèle, il serait possible d'améliorer la précision des prévisions et de mieux capturer les variations saisonnières et les tendances spécifiques.

De plus, une autre limite importante est que le modèle N-Beats a été utilisé pour la prévision sur une série univariée, alors que le magasin avait à l'origine 50 produits en vente. Il n'est peut-être pas raisonnable de répéter ce travail pour chaque produit individuellement. Une solution plus efficace pourrait consister à utiliser des modèles capables de traiter plusieurs séries temporelles simultanément, tels que les modèles multivariés. Une piste prometteuse serait d'envisager l'utilisation de N-Beats X, une extension de N-Beats conçue pour les séries temporelles multivariées. N-Beats X peut capturer les interactions entre les différents produits et fournir des prévisions plus cohérentes et précises. Il serait intéressant de vérifier notamment si les prédictions sont meilleures en entrainant un modèle sur tous les produits du magasin ou non.

En conclusion, bien que le modèle N-Beats présente des capacités prometteuses, une meilleure compréhension et intégration des facteurs exogènes, ainsi que l'exploration de modèles capables de traiter plusieurs séries temporelles simultanément, comme N-Beats X, pourraient être envisager pour essayer d’améliorer ses performances. Des études futures pourraient se concentrer sur l'exploration de ces aspects pour tirer pleinement parti du potentiel du modèle.

## Annexes

### (1) Synthèse de l’optimisation du modèle Sarimax

- **Convergence de l'optimisation**
  - L'optimisation a atteint la limite du nombre d'itérations avec un RMSE final de 0.07588.
  - Bien que l'optimisation ait échoué à converger complètement, les résultats obtenus sont significatifs.

- **Paramètres du modèle**
  - **Paramètres non saisonniers**
    - AR(1) : 0.0502 (p-value = 0.081)
    - MA(1) : -0.9102 (p-value < 0.001)
  - **Paramètres saisonniers (période de 7 jours)**
    - AR(7) : -0.8457 (p-value < 0.001)
    - AR(14) : -0.7255 (p-value < 0.001)
    - AR(21) : -0.6216 (p-value < 0.001)
    - AR(28) : -0.4570 (p-value < 0.001)
    - AR(35) : -0.3543 (p-value < 0.001)
    - AR(42) : -0.2424 (p-value < 0.001)
    - AR(49) : -0.1107 (p-value < 0.001)
    - MA(7) : -0.9993 (p-value < 0.001)
  - **Variance des résidus (sigma2)** : 0.0650 (p-value < 0.001)

- **Interprétation des résultats**
  - **Paramètres AR et MA**
    - Les coefficients AR et MA sont significatifs, indiquant que les valeurs passées et les erreurs passées influencent fortement les prévisions.
    - Les coefficients saisonniers montrent une forte dépendance des ventes aux valeurs passées avec une périodicité de 7 jours.
  - **Variance des résidus**
    - La faible valeur de sigma2 indique que les résidus du modèle sont relativement faibles, ce qui suggère une bonne adéquation du modèle aux données.

- **Tests de diagnostic**
  - **Ljung-Box Test**
    - Probabilité (Q) = 0.99, indiquant que les résidus ne sont pas autocorrélés.
  - **Jarque-Bera Test**
    - Probabilité (JB) < 0.001, indiquant que les résidus ne suivent pas une distribution normale.
  - **Heteroskedasticity Test**
    - Probabilité (H) = 0.02, indiquant une hétéroscédasticité dans les résidus.

- **Conclusion**
  - Le modèle SARIMAX avec les paramètres choisis offre une bonne performance pour la prévision des ventes quotidiennes, malgré l'échec de la convergence complète de l'optimisation.
  - Les tests de diagnostic montrent que les résidus ne sont pas autocorrélés, mais présentent une hétéroscédasticité et ne suivent pas une distribution normale.

### (2) les modèles AR, AM, ARIMA et SARIMA

- **Modèles AR, MA, et ARIMA**
  - **Modèle AR (AutoRegressive)** : Le modèle AR utilise les valeurs passées de la série pour prédire les valeurs futures. Il est défini par le paramètre p, qui représente l'ordre de l'auto-régression, c'est-à-dire le nombre de valeurs passées utilisées pour la prédiction.
  - **Modèle MA (Moving Average)** : Le modèle MA utilise les erreurs passées (résidus) pour prédire les valeurs futures. Il est défini par le paramètre q, qui représente l'ordre de la moyenne mobile, c'est-à-dire le nombre de résidus passés utilisés pour la prédiction.
  - **Modèle ARIMA (AutoRegressive Integrated Moving Average)** : Le modèle ARIMA combine les modèles AR et MA avec la différentiation pour rendre la série stationnaire. Il est défini par les paramètres p (ordre de l'auto-régression), d (ordre de la différentiation), et q (ordre de la moyenne mobile).
  - **Le modèle SARIMAX (Seasonal AutoRegressive Integrated Moving Average with eXogenous regressors)** : Le modèle SARIMAX est un modèle de prévision de séries temporelles qui prend en compte les composantes saisonnières et les variables exogènes. Il est particulièrement utile pour les séries temporelles présentant des patterns saisonniers et des influences externes.

- **Différentiation** : La différentiation est une technique utilisée pour rendre une série temporelle stationnaire en supprimant les tendances. Une série est dite stationnaire si ses propriétés statistiques, telles que la moyenne et la variance, sont constantes dans le temps. La différentiation consiste à soustraire la valeur précédente de la valeur actuelle de la série.





