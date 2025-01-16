FROM python:3.9-slim

WORKDIR /app

# Copier tous les fichiers de l'application dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port utilisé par Streamlit
EXPOSE 8501

# Définir la commande pour exécuter l'application
CMD ["streamlit", "run", "main.py", "--server.port", "$PORT"]