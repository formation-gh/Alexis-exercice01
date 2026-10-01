# Alexis-exercice01

## Test end-to-end

Ce projet contient un scénario Selenium qui vérifie que l’application se charge
sans erreur JavaScript dans la console du navigateur :
<https://aouzgaga.github.io/formation-gh-api/>.

Prérequis : Python 3 et Google Chrome ou Chromium. Selenium Manager récupère
automatiquement le pilote correspondant au navigateur.

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests
```

Les tests s’exécutent automatiquement avec GitHub Actions à chaque push et
pull request.
