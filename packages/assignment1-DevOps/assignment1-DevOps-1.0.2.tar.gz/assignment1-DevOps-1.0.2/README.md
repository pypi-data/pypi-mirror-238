**Gruppo ELA** 

**Autori**:
- Alessandro Cassani _(n. matricola 920015)_
- Emilio Daverio _(n. matricola 918799)_
- Luca Perfetti _(n. matricola 919835)_

**Link GitLab**: https://gitlab.com/2023_assignment1/DevOps



**Introduzione**:

Il progetto, sviluppato dal gruppo ELA, rappresenta un'implementazione di un'applicazione **App-DB** sviluppata per raccogliere informazioni sulla facoltà frequentata dall'utente. Questa applicazione è stata concepita per stabilire una connessione con il servizio cloud offerto da MongoDB, sfruttando Python come linguaggio principale e utilizzando come ambiente di sviluppo  Visual Studio Code (VSCode). Al fine di agevolare una collaborazione efficiente tra i membri del team di sviluppo e garantire il controllo accurato delle versioni del codice, è stato fatto ampio uso di GitLab. Il progetto non si è focalizzato principalmente sull'applicazione stessa, piuttosto sull'implementazione di una pipeline dedicata (quindi anche dei relativi moduli per la creazione di test, documentazione package e release). L'obiettivo principale è stato creare una pipeline di sviluppo che agevolasse e automatizzasse le fasi di: build, testing, package, release e documentazione, consentendo al team di effettuare verifiche più approfondite e regolari del codice. In questo contesto, l'applicazione App-DB è stata sviluppata come un caso d'uso concreto per testare l'efficacia e l'efficienza della pipeline, in modo da garantire che il processo di sviluppo e rilascio fosse il più fluido e affidabile possibile.



**Obiettivo:**

L'obiettivo del progetto era creare e configurare una **pipeline CI/CD (Continuous Integration/Continuous Deployment)** per automatizzare l'intero processo di sviluppo e distribuzione dell'applicazione utilizzando l'infrastruttura CI/CD fornita da GitLab. 
Questa pipeline CI/CD automatizza il flusso di sviluppo, test e distribuzione del software, garantendo che ogni modifica al codice sorgente venga sottoposta a un rigoroso processo di verifica prima di essere rilasciata in produzione. Ciò contribuisce a ridurre errori, migliorare la qualità del software e semplificare il processo di distribuzione. Inoltre, l'uso dell'infrastruttura GitLab per questa pipeline assicura una gestione centralizzata e affidabile del processo di sviluppo e distribuzione.

 

**Tecnologie utilizzate**:

1)**Python**: E' stato utilizzato il linguaggio di programmazione Python per sviluppare l'applicativo. 

 
2)**MongoDB**: Come database principale, si è scelto di utilizzare il servizio cloud di MongoDB, ovvero MongoDB Atlas.


3)**Visual Studio Code (VSCode)**: VSCode è stato l'ambiente di sviluppo principale per scrivere il codice dell'applicazione.

 
4)**GitLab**: Per garantire un controllo di versione efficace e la collaborazione tra i membri del team, è stato utilizzato GitLab. Questa piattaforma permette di gestire il codice in modo efficiente e di mantenere una traccia chiara delle modifiche apportate al progetto. Inoltre, è utile per creare la Pipeline in maniera molto semplice ed intuitiva.

 

**Stato di avanzamento del progetto**:

Prima di creare la pipeline, il team ha suddiviso i compiti tra i membri. Inizialmente, si è concentrato sulla creazione della struttura dell'applicazione, comprensiva della classe necessaria per la connessione al database e l'inserimento dei dati da terminale utili all'implementazione della logica applicativa. Inoltre, sono stati definiti i moduli per eseguire i vari test unitari e di integrazione. In primis, è stato sviluppato lo stage di **build**, poi seguito dalla fase relativa agli **unit-test**, fino ad arrivare all'esecuzione dei **test di integrazione** per verificare che l'interazione tra lato client e database funzionasse in modo coeso e corretto rispettando la logica applicativa.
Attualmente, il team è focalizzato sullo sviluppo della pipeline relativa all'implementazione degli stage di **release**, **package** e della risoluzione di errori in fase **verify**.
Gli stage per ora completati sono: build, unit-test, integration-test e docs. Lo stage di verify sta subendo delle modifiche a causa del fallimento in fase di run della pipeline. La problematica sorta in questa fase sembra essere dovuta ad un errore interno di prospector (probabilmente dovuto ad incompatibilità tra versioni).
La documentazione creata nello stage **docs** rappresenta solo una versione iniziale, essa sarà terminata alla fine della fase implementativa dell'applicativo. È stata comunque automatizzata la generazione di quest'ultima tramite pipeline GitLab.
La pipeline finora sviluppata, anche se nelle sue parti funzionante, non è da considerarsi definitiva. Infatti meccanismi di caching e l'utilizzo di variabili d'ambiente necessarie all'ottimizzazione del codice devono ancora essere implementate.
