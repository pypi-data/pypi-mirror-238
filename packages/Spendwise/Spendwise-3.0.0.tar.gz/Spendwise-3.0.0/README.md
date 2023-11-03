# spendwise
## Descrizione app
L'app spendwise è una semplice applicazione scritta in python per la gestione delle spese quotidiane.
Essa segue un architettura app+db. Il db è composto da una singola tabella spese contentente tutti i dettagli delle spese.
L'applicazione permette all'utente di aggiungere, modificare o eliminare una spesa dal db. Una volta inserite le spese, permette di conoscere il totale delle spese effettuate, stampandole in una tabella.

## Breve descrizione pipeline
La nostra pipeline è divisa nei seguenti stage:
* __Build__: Installa le dipendenze del progetto
* __Verify__: Esegue prospector e bandit in due job differenti, per eseguire l'analisi statica e dinamica del codice    
          python.
* __unit-test__: Esegue i test d'unità sull'applicazione usando la libreria pytest.
* __integration-test__: Esegue i test d'Integrazione sull'applicazione usando la libreria pytest.
* __package__: Crea il pacchetto che verrà poi rilasciato negli stage successivi, utilizzando la libreria setuptools e 
           wheel.
* __release__: Rilascia il pacchetto utilizzando twine su PyPi.
* __docs__: Crea la documentazione del progetto utilizzando mkdocs e la pubblica su gitlab pages.

## Condizioni di esecuzione degli stage della pipeline
* __Build__: sempre.
* __Verify__: Quando viene modificato un file all'interno della directory app/* o un file di configurazione prospector o 
         bandit.
* __unit-test__: Quando viene modificato un file all'interno della directory app/* .
* __integration-test__: Quando viene modificato un file all'interno della directory app/* .
* __package__: Quando viene effettuato un commit con un tag associato.
* __release__: Quando viene effettuato un commit con un tag associato.
* __docs__: Quando viene modificato un file nella directory docs, o un file di configurazione mkdocs.yml

## Altre istruzioni
* __before_script__: viene eseguito prima di ogni stage eccetto il build e serve per installare le dipendenze presenti nella cache. 
* __variables__: dichiarazione delle variabili globali utilizzate nella pipeline
* __cache__: vengono specificate le directory usate per salvare i dati nella cache.

## Descrizione dettagliata pipeline
La nostra pipeline di integrazione continua è stata progettata per automatizzare il processo di sviluppo e distribuzione del nostro progetto in modo efficace e affidabile. Di seguito le ragioni dietro le scelte implementative per ciascuno dei nostri stage:
* __Build__: In questa fase iniziale della pipeline, prepariamo l'ambiente di sviluppo eseguendo una serie di azioni chiave. Verifichiamo la versione di Python, creiamo un ambiente virtuale isolato, installiamo le dipendenze dal file requirements.txt, e verifichiamo la presenza degli strumenti essenziali come pytest, bandit e prospector. Questo ci permette di assicurarci che l'ambiente sia pronto per la compilazione e l'esecuzione del progetto.
* __Verify__: Nella fase "Verify," abbiamo diviso l'analisi statica e dinamica del codice in due job distinti: "Prospector" e "Bandit," al fine di eseguire una revisione approfondita del nostro codice Python. "Prospector" opera all'interno della directory 'app', valutando il nostro codice in modo completo. Al contrario, "Bandit" opera sulla stessa directory 'app', ma con un'importante eccezione: escludiamo i file di test. Questa decisione è basata sul fatto che i file di test spesso contengono asserzioni e logiche specifiche del test, le quali solitamente non presentano rilevanza per la sicurezza dell'applicazione. Escludendo i file di test, riduciamo i falsi positivi nell'analisi di sicurezza, concentriamo l'attenzione sulla sicurezza del codice di produzione e risparmiamo tempo ed elaborazione. Questa suddivisione ci permette di identificare e migliorare la qualità del codice, rilevando potenziali problematiche sia statiche che dinamiche.
* __unit-test__ e integration-test: I test d'unità e di integrazione, eseguiti con pytest, sono essenziali per garantire la qualità e la robustezza del nostro codice. Questi test verificano che il codice funzioni correttamente, individuando eventuali problemi precocemente e assicurandoci che le diverse parti del software siano compatibili tra loro. 
* __package e release__: La creazione del pacchetto e il rilascio sono legati all'uso di tag associati ai commit. Questo ci permette di creare pacchetti distribuibili solo quando si effettua un rilascio, garantendo che le versioni pubblicate siano stabili.
* __docs__: L'automazione della generazione e pubblicazione della documentazione garantisce che sia sempre aggiornata ed è facilmente accessibile tramite GitLab Pages. Questo risparmia tempo, mantiene la documentazione accurata.

Per ridurre i tempi di esecuzione e ottimizzare l'utilizzo delle risorse, utilizziamo la sezione "before_script" per installare le dipendenze presenti nella cache. Inoltre, dichiariamo le variabili globali utilizzate nella pipeline nella sezione "variables" e configuriamo la cache per memorizzare i dati di cui il nostro flusso di lavoro ha bisogno.
Abbiamo anche definito le condizioni di esecuzione per ciascuno stage, in modo da evitare esecuzioni inutili e consentire un flusso di lavoro efficiente. In questo modo, la nostra pipeline di integrazione continua supporta uno sviluppo continuo, il testing approfondito e il rilascio affidabile del nostro progetto.

## Membri progetto
* Alberto Varisco 866109
* Mattia Milanese 869161
* Oscar Sacilotto 866040

## Link vari
   repository: https://gitlab.com/2023_assignment1_spendwise/spendwise  
   docs: https://spendwise-2023-assignment1-spendwise-db02e21ef2c47c900d1903f51e.gitlab.io