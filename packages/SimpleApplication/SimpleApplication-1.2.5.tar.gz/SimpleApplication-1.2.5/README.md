
# 2023_assignment1_carrigerva

  

## Introduzione

  

## Contesto della realizzazione

  

Questo documento fa riferimento alla realizzazione della pipeline per un'applicazione Python denominata **SimpleApplication**. L'applicazione è formata da una semplice architettura Back-End - Front-End, nel quale il modulo BE (ripetiamo, scritto mediante il linguaggio di programmazione Python) permette di trasferire una stringa che verrà successivamente mostrata in una pagina HTML (corrispondente al nostro FE). Il focus di questo assignment riguarderà esclusivamente la pipeline, dunque ci interesseremo principalmente sulla descrizione e orchestrazione dei vari stages che la compongo. La pipeline in esame è disponibile presso il suddetto [link](https://gitlab.com/carrivalegervasi/2023_assignment1_carrigerva.git).

# Componenti del gruppo

Coloro che hanno lavorato su questa pipeline sono:

  

- Gabriele Carrivale 872488

  

- Alessandro Gervasi 866140

  

# Applicazione realizzata: SimpleApplication

  

Questa applicazione `Python` invia una stringa a una pagina `HTML` che la visualizza e la stampa a video quando gli utenti accedono all'applicazione web. Una volta eseguita l'applicazione `app.py`, possiamo visualizzare la pagina web presso l'indirizzo `http://127.0.0.1:5000/`.

  

## Front-End

  

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

## Back-End

  

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

  

In questa prima versione, verranno descritte esclusivamente le prime 5 fasi (da [**Build**](#build) a [**Package**](#package)). Iniziamo, dunque, dettagliando le fasi appena menzionate, a partire dalla la creazione e configurazione della cache e del virtual environment.

## Configurazione cache


``` {style="yaml"}
cache:
    paths:
    - .cache/pip
    - venv/
```
  
Una cache è un meccanismo utilizzato per memorizzare temporaneamente i risultati o i file intermedi in modo da poterli riutilizzare più tardi senza doverli ricreare o ricalcolare. Nel contesto della pipeline `CI/CD`, la cache può essere utilizzata per memorizzare le dipendenze, i risultati dei test o altri file temporanei che possono essere riutilizzati tra gli stage della pipeline.

La directory `.cache/pip` rappresenta la cache di `pip`, il gestore di pacchetti Python. pip può memorizzare temporaneamente le dipendenze scaricate in questa directory in modo che possano essere riutilizzate in futuro, facendoci risparmiare tempo.

Invece, la directory `venv/` rappresenta l'ambiente virtuale Python (`venv`). L'ambiente virtuale contiene le dipendenze del progetto e può essere riutilizzato in altri stage per garantire un'installazione coerente delle dipendenze.

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

Il comando `pip install -r requirements.txt` viene eseguito, permette di leggere il file `requirements.txt` e installare tutte le dipendenze elencate con le rispettive versioni specificate nel file. Le dipendenze vengono scaricate e installate all'interno dell'ambiente virtuale.

  

## Verify

  

``` {style="yaml"}
verify:
  stage: verify
  script:
    - source venv/bin/activate
    - pip install prospector
    - prospector
    - pip install bandit
    - bandit -r src/app.py
```


Questo stage è dedicato alla verifica del codice sorgente. Il comando `pip install prospector` installa `Prospector`, uno strumento di analisi statica del codice per Python. Prospector è in grado di rilevare una serie di problemi comuni nel codice sorgente, come stile di codifica, errori sintattici, complessità del codice, uso delle variabili non dichiarate e altro ancora. Dopo aver effettuato l'installazione, viene eseguito il comando `prospector` per far partire il programma. Questo comando analizza il codice sorgente del progetto alla ricerca di problemi e restituisce un rapporto dettagliato che elenca gli errori e le aree di miglioramento rilevate.

Il secondo comando `pip install bandit`, invece, permette di installare `Bandit`, uno strumento di sicurezza del codice Python. `Bandit` è progettato per rilevare potenziali vulnerabilità nel codice, come possibili falle di sicurezza, uso errato delle funzioni di crittografia, ecc.

Dopo aver installato Bandit, viene eseguito il comando `bandit -r src/app.py`. L'opzione `-r` per scansionare il codice sorgente del progetto, in particolare il file `app.py`, alla ricerca di potenziali vulnerabilità o problemi di sicurezza.

## Unit-Test

  

``` {style="yaml"}
unit-test:
  stage: unit-test
  script:
    - source venv/bin/activate
    - pytest src/tests/unit_test.py
```

Questo stage rappresenta la fase dedicata ai test unitari all'interno della pipeline `CI/CD`. I test unitari sono progettati per verificare il funzionamento di unità specifiche del codice, come funzioni o classi, in modo isolato e indipendente. Il comando `pytest src/tests/unit_test.py` esegue i test unitari definiti nel file `unit_test.py` all'interno della directory `src/tests`.

Il framework di testing `pytest` è utilizzato per l'esecuzione dei test unitari, inoltre, pytest riconosce automaticamente i test e produce rapporti dettagliati sui risultati.

## Integration-Test

  

``` {style="yaml"}
integration-test:
  stage: integration-test
  script:
    - source venv/bin/activate
    - pytest src/tests/integration_test.py
```

Questo stage rappresenta la fase dedicata ai test di integrazione all'interno della pipeline `CI/CD`. I test di integrazione sono progettati per verificare il funzionamento dell'applicazione nel suo complesso, inclusi i componenti che collaborano tra loro. 

Questo comando esegue i test di integrazione definiti nel file `integration_test.py` all'interno della directory `src/tests`. Come abbiamo definito precedentemente, il framework di testing pytest è utilizzato per l'esecuzione dei test di integrazione.
  

## Package

  

``` {style="yaml"}
package:
  stage: package
  script:
    - source venv/bin/activate
    - pip install setuptools
    - pip install wheel
    - python setup.py sdist bdist_wheel
```

Lo stage `package` rappresenta la fase di confezionamento e distribuzione del progetto all'interno della pipeline `CI/CD`. In questo stage, il progetto viene preparato per essere confezionato in un formato distribuibile.

  
Il comando `pip install setuptools` installa `setuptools`, un pacchetto Python essenziale per la creazione di pacchetti Python e la gestione delle dipendenze. Successivamente eseguiamo il comando per installare il pacchetto `wheel`: `pip install wheel`. Questo è un pacchetto Python utilizzato per creare pacchetti binari Python compatibili con il formato \"wheel\". I pacchetti \"wheel\" sono una forma di distribuzione ottimizzata che semplifica l'installazione delle librerie Python. Invece, il comando `python setup.py sdist bdist_wheel` utilizza il file `setup.py` per creare i pacchetti di distribuzione. 

In particolare, genera un pacchetto di distribuzione sorgente (`SDIST`) e un pacchetto di distribuzione binario (`BDIST_WHEEL`). Questi pacchetti sono pronti per essere confezionati e distribuiti attraverso il sistema di gestione delle librerie Python, come pip.

## Release

  

## Docs