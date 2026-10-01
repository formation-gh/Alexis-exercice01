# Alexis-exercice01

## Test end-to-end

Ce projet contient des tests Selenium couvrant le chargement de l’écran sécurisé,
le refus d’un mot de passe invalide, l’accès à la liste et aux détails d’un
utilisateur, ainsi que la création et la suppression d’un congé. Ils vérifient
aussi qu’une période limitée au week-end ne peut pas être soumise :
<https://aouzgaga.github.io/formation-gh-api/>.

Prérequis : Python 3 et Google Chrome ou Chromium. Selenium Manager récupère
automatiquement le pilote correspondant au navigateur.

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests
```

Les tests s’exécutent automatiquement avec GitHub Actions à chaque push et
pull request. Pour exécuter les scénarios qui nécessitent une connexion,
définissez `APP_PASSWORD` avec le mot de passe de l’application. Configurez le
même nom comme secret GitHub Actions (**Settings** → **Secrets and variables** →
**Actions**) ; sans ce secret, les scénarios authentifiés sont ignorés. Vous
pouvez définir `APPLICATION_URL` pour tester un autre déploiement.
