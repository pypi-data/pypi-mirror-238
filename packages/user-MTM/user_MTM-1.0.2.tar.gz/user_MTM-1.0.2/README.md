Gruppo MTM:
Lorenzo	Molinari 911610
Massimo	Trippetta 869286
Lorenzo	Megna 868929

Link repository: https://gitlab.com/gruppomtm/assignment1/-/tree/main

Per questo progetto è stata sviluppata una semplice applicazione che conta gli accessi degli utenti contenuti in un Database, il quale è stato creato da noi tramite il software SQL, mentre l'applicazione  è stata scrittà in python.

Per la parte di build non ci sono stati molti problemi, ci è bastato installare tutte le dipendenze contenute all'interno del file 'requirements.txt', successivamente siamo passati allo stage verify nel quale prospector ci sta dando molti problemi ai quali non siamo ancora riusciti a trovare una soluzione, l'errore che ci viene ripetuto sempre è il seguente: '    pylint: astroid-error / /builds/gruppomtm/assignment1/main.py: Fatal error while checking '/builds/gruppomtm/assignment1/main.py'. Please open an issue in our bug tracker so we address this. There is a pre-filled template that you can use in '/root/.cache/pylint/pylint-crash-2023-10-17-10-54-57.txt'.'. 
Abbiamo quindi utilizzato momentaneamente il comando "allow_failure: true" e siamo passati allo stage successivo per poi tornare indietro quando avremo completato gli altri stage.
