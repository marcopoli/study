# 🎓 Manuale Utente: Univox Study Assistant

Benvenuto in **Univox**, il tuo assistente intelligente basato su IA progettato per supportare lo studio universitario attraverso il Retrieval-Augmented Generation (RAG). Questo manuale ti guiderà attraverso le funzionalità del sistema, sia come partecipante a uno studio che come sviluppatore.

---

## 🚀 1. Avvio Rapido

Per avviare il sistema su Windows:
1.  Assicurati di avere Python installato.
2.  Esegui il file `start_univox.bat` situato nella cartella principale.
3.  L'applicazione si aprirà automaticamente nel tuo browser all'indirizzo `http://localhost:8501`.

---

## 🔬 2. Modalità Partecipante (User Study)

Questa modalità è dedicata alla valutazione del sistema. Segue un flusso guidato:

### A. Consenso Informato
Prima di iniziare, dovrai leggere l'informativa sulla privacy. È necessario selezionare **"acconsento"** al primo blocco obbligatorio per procedere. Puoi scaricare l'informativa completa in PDF direttamente dalla schermata.

### B. Selezione Materia e Scenario
Dovrai scegliere una tra le materie disponibili (es. **MRI**, **SIIA**, **LP**, **Calculus**). Il sistema ti assegnerà uno **scenario di studio** casuale con un obiettivo specifico (es. chiarire un concetto, trovare una differenza tra due tecnologie).

### C. La Chat di Studio
*   **Domande Libere**: Interroga il tutor sui materiali del corso. L'IA utilizzerà le slide e i libri caricati per risponderti.
*   **Fonti**: Sotto ogni risposta, potrai vedere quali documenti sono stati utilizzati (🔧 **Strumenti**).
*   **Materiale Didattico**: Nella sidebar sinistra troverai un menu a tendina per scaricare le slide e i libri relativi alla materia scelta.

### D. Conclusione
Una volta raggiunto l'obiettivo, clicca su **"Concludi e Compila Questionario"** nella sidebar. Rispondi alle domande (scala SUS e feedback qualitativo) e clicca su "Invia". Riceverai un codice di completamento univoco.

---

## 🛠️ 3. Modalità Sviluppatore (Dev Mode)

Accessibile selezionando "Avvia Dev Mode" nella schermata iniziale.
*   **Password**: La password predefinita è `admin123`.

### Funzionalità Esclusive:
*   **Gestione Chat**: Puoi creare nuove chat con nomi personalizzati e navigare tra lo storico delle conversazioni.
*   **Configurazione Avanzata (Sidebar)**:
    *   **Provider LLM**: Scegli tra *Google Gemini* o *Together AI*.
    *   **Livello di Complessità**: Imposta il tono della risposta (Base, Intermediate, Advanced).
    *   **Selezione Corso**: Forza il sistema a concentrarsi su una materia specifica.
    *   **Streaming**: Attiva o disattiva la visualizzazione della risposta in tempo reale.

---

## 🎙️ 4. Funzionalità Avanzate

### 🎤 Comandi Vocali
Clicca sull'icona del microfono (🎤) nella barra di input per attivare la modalità vocale. Registra la tua domanda e il sistema la trascriverà automaticamente. Puoi anche ascoltare le risposte dell'IA cliccando sull'icona dell'altoparlante (🔊).

### 🖼️ Analisi Immagini
Puoi trascinare immagini (PNG, JPG) nella chat. L'IA utilizzerà strumenti come **Google Lens** o **Mathpix** per analizzare grafici, esercizi scritti a mano o diagrammi.

### 📄 Caricamento Documenti
Puoi caricare i tuoi file PDF o TXT. Il sistema li analizzerà temporaneamente per rispondere a domande specifiche sul loro contenuto.

---

## 📁 5. Folder & Risultati

Se sei un ricercatore, ecco dove trovare i dati raccolti:
*   **Risultati Questionari**: `userstudy/results/results.csv`
*   **Log delle Sessioni**: `userstudy/logs/` (File JSONL con ogni interazione)
*   **Grafici di Analisi**: `userstudy/results/plots/`

---

> [!TIP]
> Per garantire le migliori prestazioni, assicurati di aver inserito tutte le chiavi API necessarie nel file `.env` all'interno della cartella `system/`.
