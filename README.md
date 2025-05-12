# 🧮 PyCalculator - Calcolatrice Scientifica con Python e Tkinter 🧪💻

Benvenuto nella mia Calcolatrice Scientifica! 🌟 
Questo progetto è un'applicazione desktop creata interamente in Python, utilizzando la libreria `tkinter` (con `ttk` per widget migliorati) per l'interfaccia grafica. 
È stata sviluppata per offrire un'ampia gamma di funzionalità matematiche in un formato intuitivo e facile da usare.

## ✨ Funzionalità Implementate

La calcolatrice supporta le seguenti operazioni e caratteristiche:

* **Operazioni Aritmetiche di Base:** ➕➖✖️➗
    * Addizione (`+`), Sottrazione (`-`), Moltiplicazione (`*`), Divisione (`/`)
* **Gestione dell'Espressione:**
    * Parentesi `(` `)` per controllare l'ordine delle operazioni.
    * Il display 🖥️ visualizza l'intera espressione man mano che viene digitata.
* **Pulsanti di Controllo:**
    * `C`: Cancella completamente l'espressione e resetta. 🧹
    * `CE`: Cancella l'input corrente (attualmente resetta l'espressione).
    * `←` (Backspace): Cancella l'ultimo carattere inserito.
    * `+/-`: Cambia il segno dell'ultimo numero inserito o del risultato.
* **Funzioni Scientifiche Unarie:**
    * `x²`: Elevamento al quadrato.
    * `x³`: Elevamento al cubo.
    * `√`: Radice quadrata (gestisce errore per input negativi).
    * `1/x`: Reciproco (gestisce divisione per zero).
    * `%`: Percentuale (calcola `numero / 100`).
    * `n!`: Fattoriale (gestisce input non interi e negativi, e overflow).
* **Operatore di Potenza:**
    * `xʸ`: Eleva una base (x) a un esponente (y) (usando `**`).
* **Costanti Matematiche:**
    * `π`: Inserisce il valore di Pi greco.
    * `e`: Inserisce il valore del numero di Eulero.
* **Funzioni Trigonometriche:** 📐
    * `sin`, `cos`, `tan`
    * Modalità angolare selezionabile: `deg` (gradi) e `rad` (radianti), con indicazione visiva del modo attivo.
    * Gestione del caso `tan` indefinita (es. tan(90°)).
* **Funzioni Trigonometriche Inverse:**
    * `sin⁻¹` (arcoseno), `cos⁻¹` (arcocoseno), `tan⁻¹` (arcotangente)
    * Risultato in base alla modalità angolare selezionata.
    * Controllo del dominio per `sin⁻¹` e `cos⁻¹`.
* **Funzioni Iperboliche:**
    * `sinh`, `cosh`, `tanh`
* **Funzioni Logaritmiche:**
    * `log`: Logaritmo in base 10.
    * `ln`: Logaritmo naturale (base *e*).
    * Controllo del dominio (input > 0).
* **Funzioni di Memoria:** 💾
    * `MC`: Memory Clear (azzera la memoria).
    * `MR`: Memory Recall (richiama il valore dalla memoria al display).
    * `MS`: Memory Store (salva il valore del display in memoria).
    * `M+`: Memory Add (somma il valore del display a quello in memoria).
    * `M-`: Memory Subtract (sottrae il valore del display da quello in memoria).
* **Interfaccia Utente:** 🎨
    * Layout chiaro e organizzato, ottimizzato per l'uso.
    * Display ampio per visualizzare le espressioni.
    * Stili personalizzati per i pulsanti (`ttk`) per una migliore leggibilità e feedback visivo (incluso l'effetto hover e l'indicazione della modalità angolare attiva).
    * Utilizzo del tema `clam` di `ttk` per una maggiore flessibilità stilistica.
    * Input numerico validato per prevenire l'inserimento di caratteri non validi.
    * Finestra a dimensione fissa.
* **Gestione Errori:** ⚠️
    * Visualizzazione di messaggi di errore specifici (es. "Errore: Divisione per 0", "Errore Sintassi", "Errore: Dominio...").

## 🚀 Installazione e Avvio

1.  **Python:** 🐍 Assicurati di avere Python 3 installato sul tuo sistema. Puoi scaricarlo da [python.org](https://www.python.org/).
2.  **Tkinter:** La libreria Tkinter (incluso il modulo `ttk`) è parte della libreria standard di Python, quindi non sono necessarie installazioni aggiuntive. 👍
3.  **Scarica il Progetto:** 📂
    * Scarica o clona questo repository.
4.  **Esegui l'Applicazione:** ▶️
    * Apri un terminale o prompt dei comandi nella cartella del progetto.
    * Esegui lo script Python:
        ```bash
        python main.py
        ```

## 🎮 Come Usare

* Utilizza i pulsanti numerici 🔢 e degli operatori per costruire la tua espressione matematica sul display.
* Le funzioni scientifiche (sin, cos, log, √, x², ecc.) si applicano generalmente al numero o all'espressione corrente visualizzata.
* Usa `(` e `)` per definire l'ordine delle operazioni.
* Premi `=` per calcolare il risultato dell'espressione.
* Usa `deg` o `rad` per cambiare la modalità di input/output degli angoli per le funzioni trigonometriche.
* I pulsanti di memoria (`MC`, `MR`, `MS`, `M+`, `M-`) funzionano come nelle calcolatrici standard.
* `C` cancella tutto, `CE` cancella l'input corrente (attualmente resetta), `←` cancella l'ultimo carattere.
