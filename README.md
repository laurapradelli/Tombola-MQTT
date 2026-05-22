# Tombola MQTT

Un'implementazione del gioco della Tombola, sviluppata in Python utilizzando il protocollo di messaggistica MQTT. 

Il progetto sfrutta il pattern Publish/Subscribe per separare la logica di estrazione dei numeri e la notifica degli eventi di vittoria (ambo, terna, ecc.).

## Architettura del Progetto

Il sistema è composto da diversi script che interagiscono tra loro tramite un broker MQTT:

* **L'estrattore (`pub_numbers.py`)**: Si occupa di mescolare i numeri da 1 a 90 e pubblicarne uno al secondo sul topic dedicato alle estrazioni.
* **Il motore di gioco (`tombola.py`)**: Gestisce l'iscrizione dei giocatori, genera le cartelle valide secondo le regole della tombola (15 numeri per cartella, 5 per riga), ascolta le estrazioni e verifica automaticamente le vincite. Quando rileva una vincita, pubblica l'evento sul topic corrispondente.
* **I visualizzatori degli eventi**: Script singoli (`ambo.py`, `terna.py`, `quaterna.py`, `cinquina.py`, `vittoria.py`) che restano in ascolto sui rispettivi topic e notificano a schermo quando un giocatore raggiunge quel traguardo.

## Requisiti di Sistema

* Python 3.x
* Libreria `paho-mqtt`
* Un Broker MQTT (già utilizzato `test.mosquitto.org`)

### Installazione delle dipendenze

Installa la libreria MQTT necessaria tramite pip:

```bash
pip install paho-mqtt
```
### Avvio del progetto
1. Avvio del motore di gioco (`tombola.py`) e iscrizione dei giocatori
2. Avvio di tutti i subscriber per i relativi topic (`ambo.py`, `terna.py`, `quaterna.py`, `cinquina.py`, `vittoria.py`)
3. Avvio dell'estrattore (`pub_numbers.py`)
