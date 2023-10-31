# Client-Server Network

## Team:
Composizione del team (sdona):
- Satriano Daniel (MAT = 919053)
- Cavallini Francesco (MAT = 920835)


## Repository:
Di seguito viene linkata la repository di Git-Lab:
1. Prima repo (tempo terminato)
    https://gitlab.com/processo-e-sviluppo-software/2023_assignment1_PythonPipeline.git
2. Seconda repo (completato progetto)
    https://gitlab.com/FCavallini303/2023_assigment1_pythonpipeline_2.git


## Bibliografia:
Per eseguire l'assignment abbiamo optato di reperire il codice di un applicazione open-source. Il seguente link contiene il codice originale per l'implementazione dei file `client.py` e `server.py`: https://github.com/katmfoo/python-client-server

Dal link è possibile visualizzare il file [README.md](https://github.com/katmfoo/python-client-server/blob/master/README.md) nel quale vengono illustrate le funzionalità del programma.


## Stato di sviluppo
Vengono di seguito riportati gli obbiettivi per il completamento del progetto
### To-do:
- [x] `before_script`: Installazione di python sul git-lab
    
    Step necessario per l'installazione di:
    - *venv* 
        necessario per la creazione ed attivazione dell'ambiente virtuale python e l'esecuzione del codice. (sempre eseguito nella sezione di `before_script`)
    - *pip*. 
        necessario ad installare le dependencies
    
    Vengono poi aggiornate ed installate le librerie di sistema con `upgrade` e `update`.
- [x] `Build-job`: build del progetto
    
    Stage del progetto necessario per l'installazione delle dependencies dal file `requirements.txt`. 
    
    In questo job vengono installate le librerie tramite il comando `pip install` e dove gli script Python verranno eseguiti.
    
    Al momento il file delle dependencies contiene esclusivamente la dependency di `pytest`, questo perchè gli import utilizzati sono tutte librerie base di python, queste infatti sono:
    - `socket`
    - `threading`
    - `sys`
    
    Caso in cui verrebbe modificato il progetto rendendo necessario l'inserimento di altre dependencies sarà semplicemente possibile modificare il file `requirements.txt`
    
- [x] `Verify-job`: eseguire *Prospector* e *Bandit*
    
    Step necessario per il miglioramento del codice. 
    - L'esecuzione del prospector ci aiuta garantire il rispetto degli standard di codifica e fornisce approfondimenti su potenziali problemi prima di eseguire il codice. È uno strumento prezioso per mantenere la qualità del codice nei progetti Python.
    - L'esecuzione di bandit serve per rilevare e di conseguenza migliorare le possibili vulnerabilità del codice.
    Al momento si è solo provato a runnare il job ma non si sono apportate ancora modifiche per superare i controlli di *Prospector* e *Bandit*.
- [x] `Unit-test-job`: eseguire *pytest*
    
    Vengono eseguiti gli unit test sui metodi di entrambi client e server. Per far ciò è stato eseguito il comando `pytest` su 2 job differenti (`unit-test-job-client` e `unit-test-job-server`) che fanno sempre parte dello stage `unit test`. 
    
    Il comando eseguito andrà a runnare entrambi i file di test `test_client.py` e `test_server.py` per andare ad eseguire i seguenti metodi:
    - nel file `test_client.py`:
        - esecuzione del metodo `test_send_message`:
            All'interno di questa funzione di test, vengono utilizzati diversi contesti di patching (utilizzando i blocchi `with mock.patch.object`) per simulare il comportamento delle funzioni di rete nel modulo `socket`. Dopo aver creato il contesto di patching, viene chiamata la funzione `send_message` con alcuni parametri di test e verificato che si ottenga il comportamento aspettato (ossia che il metodo ritorni 0).
    - nel file `test_server.py`:
        - esecuzione del metodo `test_handle_client`:
            Questa funzione è responsabile per testare la funzione `handle_client` nel modulo `server`. Infatti viene configurato il comportamento dell'oggetto simulato `client_socket` per simulare l'invio dei messaggi dal client. Dopo aver configurato il comportamento dell'oggetto simulato `client_socket`, viene chiamata la funzione `handle_client` con l'oggetto simulato come argomento. Infine dopo l'esecuzione di `handle_client`, viene verificato se il metodo `close` sull'oggetto simulato `client_socket` è stato chiamato una volta utilizzando `assert_called_once`, questa verifica assicura che la funzione `handle_client` abbia chiuso correttamente il socket del client dopo aver gestito i messaggi.
        - esecuzione del metodo `test_start_server`:
            il codice fornito esegue un test per la funzione `start_server` nel modulo `server`. Utilizza il modulo `mock` per creare oggetti simulati per le funzioni di rete e di stampa durante il test. Viene eseguito il server in un thread separato e vengono verificati i risultati della sua esecuzione utilizzando gli oggetti simulati.
- [x] `Integration-test-job`: eseguire *pytest*
    
    Per eseguire il test di integrazione è stato creato un solo file (`test_integration.py`) dedicato al testing del comportamento simultaneo del funzionamento di entrambi i client e server. All'interno di questo file sono infatti presenti i metodi:
    - `start_server_thread`
        
        serve per avviare il server (con il metodo `star_server` importato dal `server.py`) sotto forma di thread e arrestarlo solo una volta che i test vengono terminati
    - `test_server_client_communication`
        
        metodo di test per il metodo `send_message` del client. Viene testato che il comportamento del metodo funzioni sia nel caso di
        - utilizzo porta corretta 
            
            in questo caso abbiamo che utilizziamo la porta aspettata dal server (8080) per eseguire l'invio del messaggio (ci aspettiamo quindi che il metodo ritorni 0, di modo che possiamo fare nel file di test `assert!=-1`)
        - utilizzo porta non corretta 
            
            in questo caso abbiamo che utilizziamo una porta diversa dal server (la 8081) per eseguire l'invio del messaggio (ci aspettiamo quindi che il metodo ritorni 1 in quanto fallisca la comunicazione, di modo che possiamo fare nel file di test `assert==-1`)
- [x] `Package-job`: usare *setuptools* e *wheel* per creare Source Archive e Built Distribution
    
    In questo job vengono quindi installati setuptools e wheel ed eseguiti. Questi servono per eseguire il comando python `setup.py sdist bdist_wheel`, che viene utilizzato per creare un pacchetto di distribuzione (file `tar.gz`) e il source archive (file `*.whl`) per il nostro progetto Python. 
    Poi il job che esegue questo comando salva tutti gli artifact citati nella cartella `dist`
    
- [x] `Release-job`: Pubblicare la Build Distribution a *PyPI* con *twine*
    
    Per permettere il funzionamento di questo job è stato inserito all'interno delle variabili di sistema del progetto git-lab la variabile `$PIPY_TOKEN` che contiene ora il token per il caricamento di file all'interno del sito PiPy.
    
    Questo Job esegue l'upload dei file presenti nella cartella "dist" su PyPI utilizzando il comando `twine upload`. Viene utilizzato il flag `--non-interactive` per eseguire l'upload in modalità non interattiva, il flag `--skip-existing` per ignorare i file già presenti su PyPI e il flag `-u` per specificare il nome utente (in questo caso `__token__`) e il flag `-p` per specificare il token di accesso (in questo caso prelevato dalla variabile di sistema grazie alla dicitura `$PIPY_TOKEN`).
    
    Nota che è stato necessario specificare sotto la voce `dependencies` il `package job` in quanto questo job deve caricare i file generati appunto dal package job su PiPy
- [x] `Docs-job` --> diventato `Pages`: scrittura manuale md + generazione sito web
      
    Il job ha diversi passaggi definiti nel campo "script". Questi passaggi sono i seguenti:
    1. `pip install mkdocs-material`: 
        Questo passaggio installa il tema "material design" per Mkdocs. 
    2. `cd documentazione`: 
        Questo passaggio cambia la directory corrente alla cartella "documentazione". Questa cartella contiene i file Markdown che verranno utilizzati per generare la documentazione.
    4. `mkdocs build`: 
        Questo passaggio esegue il comando per generare la documentazione. Viene utilizzato il flag `--clean` per rimuovere eventuali file generati in precedenza e il flag `-d` per specificare la directory di destinazione in cui verrà generata la documentazione (in questo caso, `../public`).
      
    è stato necessario modificare il nome del job a `pages` di modo tale che dopo la generazione delle pagine del sito dai nostri file md git-lab si accorgesse della presenza delle nuove pagine generate e ne caricasse il contenuto sul sito al seguente url:
    - url:
        https://2023-assigment1-pythonpipeline-2-fcavallini303-156898af8445920c.gitlab.io/


### Criticità
- Per la creazione dei file di unit-test ed la loro successiva esecuzione è stato necessario apportare modifiche al codice di entrambi i file `server.py` e `client.py` in quanto questi file originariamente erano pensati creare thread e girare all'infinito per permettere comunicazione continua. Per poter però effettuare sia unit test che integration test è necessario che i programmi terminino: sia per dare il risultato dei test sia per poi liberare la console dalle istanze di client e server che altrimenti girerebbero all'infinito. Nell'implementazione attuale abbiamo che:
  - viene avviato il server
  - un client si connette, invia un messaggio programmatico e termina
  - il server termina
