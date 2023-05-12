# Générer des fichiers tcx à partir de l'export runtastic

L'export runtastic se structure comme ceci :
- Challenges
- Photos
- Privacity-settings
- Purchases
- Social-connections
- Sport-sessions
	+ Cadence-data
		fichiers json
	+ GPS-data
		fichiers gpx et json
	+ Heart-rate-data
	  	fichiers json
	+ Speed-data
	  	fichiers json
	fichiers json
- Training-plans
- User
- User-Connections
- User-Events

Certains dossiers peuvent ne pas apparaitre s'il n'y a pas de données
Il faut mettre tous ces dossiers dans le dossier `runtastic_export_data`


Pour chaque activité (fichier json à la racine de `Sport-sessions`, il existe peut-être un fichier du même nom dans un des autres dossiers avec les données correspondantes)