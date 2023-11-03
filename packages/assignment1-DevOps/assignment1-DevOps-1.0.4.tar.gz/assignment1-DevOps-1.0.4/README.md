# App-DB

### **Gruppo ELA**

### **Autori**:

- Alessandro Cassani *(n. matricola 920015)*
- Emilio Daverio *(n. matricola 918799)*
- Luca Perfetti *(n. matricola 919835)*


## Repository:
Link GitLab: https://gitlab.com/academicunimib/DevOps

## Obiettivo:

L'obiettivo del progetto consiste nel creare e configurare una **pipeline CI/CD (Continuous Integration/Continuous Deployment)** per automatizzare l'intero processo di sviluppo e distribuzione del software, garantendo che ogni modifica al codice sorgente venga sottoposta a un rigoroso processo di verifica automatica prima del rilascio dell'applicativo in produzione.

## Descrizione target App
Il progetto, sviluppato dal gruppo ELA, rappresenta un'implementazione di un'applicazione **App-DB** sviluppata per verificare le informazioni inserite dall'utente relative alla facoltà frequentata. L'utente inserisce da terminale il proprio username, la propria password e il dipartimento frequentato, l'applicativo si occupa di stabilire una connessione con il database offerto dal servizio cloud di mongoDb nel quale sono presenti le informazioni da verificare, se l'utente ha inserito le informazioni corrette il sw restituirà un messaggio di conferma, altrimenti un messaggio dove indica che le informazioni inserite non sono registrate.
Il sistema contiene due componenti principali; il modulo "mongo_db_connection" che fornisce i metodi per la creazione della connessione al database e dei relativi metodi di disconnessione e di ottenimento del riferimento della collezione nella quale sono contenute le informazioni utilizzate, ed il modulo "main.py" che si occupa dell'ottenimento delle informazioni ricevute dall'utente da terminale ed il relativo utilizzo di queste per interrogare il db grazie ai metodi forniti dal modulo precedente. Questi moduli sono contenuti nella directory "application", mentre i test di unità e di integrazione sono contenuti nella directory "test". Nella root directory del progetto è poi contenuto il file ".gitlab-ci.yml" contenente l'implementazione della pipeline CI/CD, oltre che il file "requirements.txt" contenente le dipendenze necessarie per lo stage di build del progetto e il modulo "setup.py" utile per lo stage "package" della pipeline.
L'applicativo è stato sviluppato utilizzando Python come linguaggio principale e come ambiente di sviluppo  Visual Studio Code (VSCode).


## Pipeline
### Tecnologie Utilizzate

- Python
- Visual Studio Code (VSCode)
- GitLab CI/CD
- MkDocs
- PyPI
- Twine
- Prospector
- Bandit
- pytest
- Virtual Environment

### Configurazione

Per configurare il progetto, è necessario definire alcune variabili d'ambiente e impostazioni:

#### Variabili d'Ambiente

- `PIP_CACHE_DIR`: Directory in cui vengono memorizzate le dipendenze Python. Impostata su `$CI_PROJECT_DIR/.cache/pip`.
- `VENV_DIR`: Directory in cui verrà creato l'ambiente virtuale Python. Impostata su `$CI_PROJECT_DIR/venv`.

#### Cache

La pipeline utilizza la cache per ridurre il tempo di compilazione e rilascio. Le seguenti variabili vengono utilizzate:

- `key`: Impostata su `$CI_COMMIT_REF_NAME`, che memorizza i risultati della build in cache in base al nome del branch.
- `paths`: Memorizza le directory in cache, tra cui `PIP_CACHE_DIR` e `VENV_DIR`.

### Struttura della Pipeline

La pipeline è organizzata nei seguenti stage:

1. `before_script`: Configurazione iniziale dell'ambiente virtuale Python.
2. `build`: Compilazione del progetto e installazione delle dipendenze.
3. `verify`: Analisi statica del codice con Prospector e Bandit.
4. `unit-test`: Esecuzione dei test unitari.
5. `integration-test`: Esecuzione dei test di integrazione.
6. `package`: Creazione di pacchetti Python sorgente e binari.
7. `release`: Upload del pacchetto Python su PyPI.
8. `pages`: Creazione, build e pubblicazione della documentazione in GitLab Pages.

Per ulteriori dettagli su ciascun stage e script, consultare la documentazione.

### Requisiti del Progetto

Prima di avviare la pipeline, è necessario aggiornare la versione del progetto nel file "setup.py". Per dettagli su come eseguire questa operazione, consultare la sezione "Limitazioni della soluzione sviluppata" nella documentazione.

### Esecuzione della Pipeline

La pipeline può essere avviata manualmente:
1. Navigare nella pagina del progetto su GitLab.
2. Selezionare il menu "Build" dal pannello laterale.
3. Sotto la sezione "Pipelines" si trova l'elenco delle pipeline che sono in esecuzione o concluse.
4. Nella parte superiore della pagina, individuare il pulsante blu con l'etichetta "Run pipeline" e cliccare su di esso.
5. Nella finestra che si apre, scegliere il branch denominato "main".
6. Avviare la pipeline premendo il pulsante "Run pipeline".

### Gestione degli Errori
Nel caso ci fossero errori è consigliato provare a pulire la cache. 
Tale operazione può essere eseguita manualmente:
1. Navigare nella pagina del progetto su GitLab.
2. Selezionare il menu "Build" dal pannello laterale.
3. Sotto la sezione "Pipelines" si trova l'elenco delle pipeline che sono in esecuzione o concluse.
4. Nella parte superiore della pagina, individuare il pulsante con l'etichetta "Clear runner caches" e cliccare su di esso.
5. Se l'operazione è andata a buon fine viene mostrato un messaggio 
6. Provare a eseguire nuovamente la pipeline (vedere paragrafo "Esecuzione della Pipeline")

In caso di errori o problemi durante l'esecuzione della pipeline, fare riferimento alla documentazione per la risoluzione dei problemi.