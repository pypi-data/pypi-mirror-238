# Introduzione

## Contesto della realizzazione

Questo documento fa riferimento alla realizzazione della pipeline per un'applicazione Python denominata **SimpleApplication**. L'applicazione è formata da una semplice architettura Back-End - Front-End, nel quale il modulo BE (ripetiamo, scritto mediante il linguaggio di programmazione Python) permette di trasferire una stringa che verrà successivamente mostrata in una pagina HTML (corrispondente al nostro FE). Il focus di questo assignment riguarderà esclusivamente la pipeline, dunque ci interesseremo principalmente sulla descrizione e orchestrazione dei vari stages che la compongo. La pipeline in esame è disponibile presso il suddetto [link](https://gitlab.com/carrivalegervasi/2023_assignment1_carrigerva.git).

# Componenti del gruppo

Coloro che hanno lavorato su questa pipeline sono:

-   Gabriele Carrivale 872488

-   Alessandro Gervasi 866140

# Applicazione realizzata: SimpleApplication

Questa applicazione `Python` invia una stringa a una pagina `HTML` che la visualizza e la stampa a video quando gli utenti accedono all'applicazione web. Una volta eseguita l'applicazione `app.py`, possiamo visualizzare la pagina web presso l'indirizzo `http://127.0.0.1:5000/`.

## Layout dell'applicazione

``` {style="yaml"}
SimpleApplication/
    template/
        index.html
    tests/
        __init__.py
        integration_test.py
        unit_test.py
    __init__.py
    app.py
.gitlab-ci.yml
README.md
requirements.txt
setup.py
```

## Back-End

``` {style="yaml"}
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    message = "Troppo Pacchio!"
    return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run()
```

## Front-End

``` {style="yaml"}
<!DOCTYPE html>
<html>
<head>
    <title>Simple Python App</title>
</head>
<body>
    <h1>Welcome to the Simple Python App</h1>
    <p>Message from the back-end: {{message}}</p>
</html>
```

# Stages della pipeline

La pipeline contiene i seguenti stages:

- [**Build**](#build)

  

-  [**Verify**](#verify)

  

-  [**Unit-Test**](#unit-test)

  

-  [**Integration-Test**](#integration-test)

  

-  [**Package**](#package)

  

-  [**Release**](#release)
  

-  [**Docs**](#docs)

Iniziamo, dunque, dettagliando le fasi appena menzionate, a partire dalla la creazione e configurazione della cache e del virtual environment.

## Configurazione cache

``` {style="yaml"}
cache:
    paths:
      - .cache/pip
      - venv/
```

Una cache è un meccanismo utilizzato per memorizzare temporaneamente i risultati o i file intermedi in modo da poterli riutilizzare successivamente senza doverli ricreare o ricalcolare. Nel contesto della pipeline `CI/CD`, la cache può essere utilizzata per memorizzare le dipendenze, i risultati dei test o altri file temporanei che possono essere riutilizzati tra gli stage della pipeline.

La directory `.cache/pip` rappresenta la cache di `pip`, il gestore di pacchetti Python. pip può memorizzare temporaneamente le dipendenze scaricate in questa directory in modo che possano essere riutilizzate in futuro, facendoci risparmiare tempo. Invece, la directory `venv/` rappresenta l'ambiente virtuale Python (`venv`). L'ambiente virtuale contiene le dipendenze del progetto e può essere riutilizzato in altri stage per garantire un'installazione coerente delle dipendenze.

## Build

``` {style="yaml"}
build:
  stage: build
  script:
    - python -m venv venv
    - source venv/bin/activate
    - pip install -r requirements.txt
```

Viene inizializzato un ambiente virtuale Python, denominato `venv`, usando `python -m venv venv`. Questo ambiente virtuale è una directory isolata in cui verranno installate le dipendenze del progetto.

L'ambiente virtuale viene quindi attivato utilizzando `source venv/bin/activate`. Questo assicura che tutte le operazioni successive vengano eseguite all'interno dell'ambiente virtuale.

Questo stage è responsabile dell'installazione delle dipendenze del progetto elencate nel file `requirements.txt`. Le dipendenze sono scaricate e installate all'interno dell'ambiente virtuale Python.

Il comando `pip install -r requirements.txt` viene eseguito, permettendo di leggere il file `requirements.txt` e installare tutte le dipendenze elencate con le rispettive versioni specificate nel file. Le dipendenze vengono scaricate e installate all'interno dell'ambiente virtuale.

## Verify

Per la realizzazione di questo stage, abbiamo deciso di sfruttare i `multi-jobs`, al fine di eseguire i due moduli necessari per il
completamento di questo task. L'utilizzo dei multi-jobs ci ha consentito di gestire questa fase in modo più efficiente e organizzato, in quanto possono essere eseguiti contemporaneamente più operazioni, consentendoci di risparmiare tempo nell'esecuzione di attività lunghe o dispendiose.

### Prospector

``` {style="yaml"}
verify_prospector:
  stage: verify
  script:
    - source venv/bin/activate
    - prospector
```

### Bandit

``` {style="yaml"}
verify_bandit:
  stage: verify
  script:
    - source venv/bin/activate
    - bandit -r SimpleApplication/app.py
```

Questo stage è dedicato alla verifica del codice sorgente. Uno dei moduli utilizzati è `Prospector`, uno strumento di analisi statica del codice per Python. Prospector è in grado di rilevare una serie di problemi comuni nel codice sorgente, come stile di codifica, errori sintattici, complessità del codice, uso delle variabili non dichiarate e altro ancora. Dopo aver effettuato l'installazione, viene eseguito il comando `prospector` per far partire il programma.

Il secondo comando `pip install bandit`, invece, permette di installare `Bandit`, uno strumento di sicurezza del codice Python. `Bandit` è progettato per rilevare potenziali vulnerabilità nel codice, come possibili falle di sicurezza, uso errato delle funzioni di crittografia, ecc. Dopo aver installato Bandit, viene eseguito il comando:

`bandit -r SimpleApplication/app.py`


L'opzione `-r` permette di scansionare il codice sorgente del progetto, in particolare il file `app.py`.

## Unit-Test

``` {style="yaml"}
unit-test:
  stage: unit-test
  script:
    - source venv/bin/activate
    - pytest SimpleApplication/tests/unit_test.py
```

Questo stage rappresenta la fase dedicata ai test unitari all'interno della pipeline `CI/CD`. I test unitari sono progettati per verificare il funzionamento di unità specifiche del codice, come funzioni o classi, in modo isolato e indipendente.

Il comando `pytest SimpleApplication/tests/unit_test.py` esegue i test unitari definiti nel file `unit_test.py` all'interno della directory `SimpleApplication/tests`. Il framework di testing `pytest` è utilizzato per l'esecuzione dei test unitari, inoltre, pytest riconosce automaticamente i test e produce rapporti dettagliati sui risultati.

## Integration-Test
``` {style="yaml"}
integration-test:
  stage: integration-test
  script:
    - source venv/bin/activate
    - pytest SimpleApplication/tests/integration_test.py
```

Questo stage rappresenta la fase dedicata ai test di integrazione all'interno della pipeline `CI/CD`. I test di integrazione sono progettati per verificare il funzionamento dell'applicazione nel suo complesso, inclusi i componenti che collaborano tra loro.

Questo comando esegue i test di integrazione definiti nel file `integration_test.py` all'interno della directory `SimpleApplication/tests`. Come abbiamo definito precedentemente, il framework di testing pytest è utilizzato per l'esecuzione dei test di integrazione.

## Package

``` {style="yaml"}
package:
  stage: package
  script:
    - source venv/bin/activate
    - python setup.py sdist bdist_wheel
  artifacts:
    paths:
      - dist/
```

Lo stage `package` rappresenta la fase di confezionamento e distribuzione del progetto all'interno della pipeline `CI/CD`. In questo stage, il progetto viene preparato per essere confezionato in un formato distribuibile. I comandi che verranno utilizzati in questo stage saranno: `setuptools` e `wheel`

-   `Setuptools` è un modulo Python che fornisce strumenti per definire, confezionare e distribuire pacchetti. È comunemente utilizzato per creare pacchetti Python che possono essere facilmente installati tramite pip, il gestore dei pacchetti. Questo li rende accessibili e utilizzabili da altri sviluppatori.

-   `Wheel` è un formato di distribuzione binaria dei pacchetti Python. Si tratta di un formato specifico per la distribuzione di librerie precompilate e può semplificare notevolmente il processo di installazione di pacchetti Python su un sistema.

Invece, il comando `python setup.py sdist bdist_wheel` utilizza il file `setup.py` per creare i pacchetti di distribuzione. In particolare, genera un pacchetto di distribuzione sorgente (`SDIST`) e un pacchetto di distribuzione binario (`BDIST_WHEEL`). Questi pacchetti sono pronti per essere confezionati e distribuiti attraverso il sistema di gestione delle librerie Python, come pip.

Infine, la sezione `artifacts` permette di memorizzare i risultati che devono essere conservati o pubblicati. In altre parole, il risultato della generazione della directory `dist` verrà conservato e potrà essere utilizzato successivamente o pubblicato.

## Release

``` {style="yaml"}
variables:
  PYPI_USERNAME: $PYPI_USERNAME_ENV_VARIABLE
  PYPI_PASSWORD: $PYPI_PASSWORD_ENV_VARIABLE
```

``` {style="yaml"}
release:
  stage: release
  script:
    - source venv/bin/activate
    - twine upload --username $PYPI_USERNAME --password $PYPI_PASSWORD dist/*
```

Questo stage si riferisce al processo di caricamento (pubblicazione) del pacchetto Python appena costruito su PyPI utilizzando uno strumento chiamato `twine`. Twine è uno strumento che semplifica il processo di upload di pacchetti Python su PyPI in modo sicuro e efficiente. Dopo aver attivato, come abbiamo visto nelle fasi precedenti, il virtual environment attraverso il comando `source venv/bin/activate`, è possibile eseguire il comando:

`twine upload –username $PYPI_USERNAME –password $PYPI_PASSWORD dist/*`

Questo comando utilizza Twine per caricare i pacchetti nella directory `dist/` su PyPI. Le variabili d'ambiente `$PYPI_USERNAME` e `$PYPI_PASSWORD` sono definite e fornite in modo sicuro (tramite le variabili protette nel sistema di `CI/CD`) per autenticare l'utente durante l'upload. Alla fine dell'operazione, il risultato ricavato sarà questo:

## Docs

``` {style="yaml"}
pages:
  stage: docs
  script:
    - source venv/bin/activate
    - pdoc SimpleApplication/ -o public
  artifacts:
    paths:
      - public
```

Questo job è responsabile della generazione e della pubblicazione della documentazione. Possiamo inoltre notare che il nome del job `pages` non coincide con il nome dello stage `docs` (a differenza degli esempi precedenti). Questo perché GitLab qualora vedesse che il nome del job sia pages, permette di generare ed avviare un nuovo job "fittizio" denominato deploy:release nel quale viene effettuato l'upload della cartella public su `GitLab Pages`.

Il comando `pdoc src/ -o public` utilizza lo strumento `pdoc` per generare la documentazione dalla directory `SimpleApplication/` e la salva nella directory `public`. pdoc è uno strumento comune per la generazione della documentazione Python. La sezione `artifacts`, come abbiamo visto precedentemente, permette di memorizzare la cartella public appena generata.

# Problemi riscontrati

## GitLab

### Cache

Una delle principali problematiche riscontrate durante la realizzazione del progetto è stata la configurazione della cache e del virtual environment per salvare temporaneamente i dati/file utili ai vari stage definiti. Abbiamo provato diverse metodologie per realizzare il task appena descritto, fino a raggiungere la struttura corrente.

### Docs

Un ulteriore problematica riguarda la generazione del sito statico per la pubblicazione della documentazione. In un primo momento abbiamo deciso di utilizzare la libreria `MkDocs` (consigliato anche dalla traccia dell'assignment), però questo non permetteva di portare a buon fine la visualizzazione del sito stesso una volta eseguito l'upload su GitLab Pages. Per sopperire a questa problematica, dunque, abbiamo deciso di utilizzare la libreria `pdoc`, la quale ci ha permesso inoltre di generare automaticamente la documentazione dell'applicazione completa di tutti i suoi moduli.