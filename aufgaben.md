# GUI Ladesäule Aufgabenpakete:

## wichtig
___
### ~~1. Tastatur Eingaben Crashs **(Marius)**~~
	- das Einlesen beim Karte Scannen führt bei manchen Tastatureingaben zu Crashs
		--> Checken bei welchen Eingaben das Problem auftritt und Crashs verhindern

	Lösung: Errors werden über try-except abgefangen
	
### ~~2. GUI Anpassungen: **(Markus)**~~
	- Emil E-Ladesäulen Benutzer gefällt die Ansicht vom MainScreen noch nicht
	- die Knöpfe haben unterschiedliche Abstände zueinander, schicker würde es aussehen, wenn
	überall gleiche Abstände herrschen
	- Wenn die Aufgabe "Reservierungen anders managen" fertig bearbeitet ist, kann auch der Reservierung Button
	vom MainScreen verschwinden

### ~~3. Reservierungen anders managen **(Marius)**~~
	- Aktuell: muss man um an eine reservierte Station zu kommen einen Button betätigen
	- zukünftig: soll der User (der eine Station reserviert hat) nur noch seine Karte an den RFID Reader halten,
	über die eingelesene ID kann der PI dem User die richtige Station zuordnen
		--> um das umzusetzen muss der PI im Mainscreen ständig auf Input bereit sein
		--> das darf aber Touch Eingaben von Usern nicht beeinträchtigen die an eine freie Station wollen,
		also nicht vergessen das Einlesen auszuschalten, wenn es nicht mehr benötigt wird

### ~~4. unendliche Reservierungen vermeiden **(Marius)**~~
    - wenn ein User eine Ladestation reserviert soll ein Timer gestartet werden (z.b. 20min)
    - läuft der Timer ab, wird die Ladestation wieder freigegeben  --> verhindert das Ladestationen ewig reserviert bleiben

### 5. Bezahl-Info-Fenster nach Checkout: **(Marius)**
	- Nachdem der Kunde ausgecheckt hat, soll er für ein paar Sekunden in einem Popup angezeigt bekommen
	wie viel "€" er für den Ladevorgang bezahlt
	- in dem Fenster sollten keine Eingaben zugelassen werden -> stellt sicher dass User die Anzeige liest

### 6. Socket Verbindung implementieren **(Marius+Markus)**
	- Python Socket muss eingebunden werden, er soll Nachrichten vom Broker empfangen können
	- erstmal soll es 4 Topis geben die reinkommen, und 1 Topic das rausgeht
	- 4 Topic: sind die Ladesäulen 1-4, die als Data alle ihre Daten gebündelt übermitteln
	(Data Format können wir erstmal festlegen)
	- 1 Topic: vom RFID Reader eingescannte ID soll an Broker geschickt werden
	- Topics müssen beim Start der GUI abonniert werden (noch Unklar wie das geht -> in Niklas Programm gucken)
	- PI mit HMI muss sich zuallererst anmelden über Set_name und abfragen ob es geklappt hat mit Get_name

### 9. Dokumentation schreiben + Code Dokumentation **Markus+Marius**
	- kurze knappe Doku schreiben
	- wichtig, nicht aufblasen
___
## mittelwichtig

### 7. Main.py in Module aufsplitten
	- bis jetzt ist das gesamte Programm in einer Datei implementiert (ca 1000 Zeilen und wird mehr)
	- um wieder Übersicht zu schaffen sollten die einzelnen Teile der Main in Module aufgesplittet werden
___
### unwichtig
### 8. Zeitberechnung bis Ladevorgang fertig ist:
	- wenn wir diese Information nicht haben -> Anzeige ausblenden
	- kriegen wir die Information überhaupt mitgeteilt
	- oder berechnen schätzen wir die Zeit nur aus den verfügbaren Daten (Kapazität vom Auto und Ladeleistung 22kW)?