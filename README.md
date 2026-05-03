# Individuell Labb 1: Centraliserad säkerhetsövervakning med AI-stödd hotdetektion

Denna labb demonstrerar uppsättningen av en komplett säkerhetspipeline (SIEM + SOAR) – från logginsamling via Wazuh, till visuell analys i Dashboards, vidare till AI-baserad anomalidetektion och slutligen automatiserad incidentrespons i Linux-brandväggen.

## Steg 19: Arkitekturdokumentation och Sammanfattning

Det övervakningssystem som byggts upp under denna labb följer ett tydligt och automatiserat dataflöde:

1. **Datainsamling (Wazuh Agent):** En Wazuh-agent körs lokalt på maskinen (`debian-fajk`) och övervakar systemet i realtid. Den samlar in systemloggar, autentiseringsförsök och övervakar kritiska filer via File Integrity Monitoring (FIM).
2. **Centraliserad Analys (Wazuh Manager):** Agenten skickar datan till en central Wazuh-manager (kursens server). Här normaliseras datan, matchas mot säkerhetsregler och visualiseras i anpassade Dashboards.
3. **AI-stödd Hotdetektion (Machine Learning):** Istället för att enbart förlita sig på statiska regler, exporteras loggdata till en lokal AI-motor skriven i Python (`anomaly_detector.py`). Med hjälp av algoritmen *Isolation Forest* identifieras avvikande beteendemönster baserat på en statistisk baslinje.
4. **Automatiserad Larmhantering:** Skriptet `alert_manager.py` klassificerar AI-motorns poäng och genererar formaterade larm (Medium, High, Critical) som matas tillbaka in i systemet.
5. **Automatiserad Incidentrespons (SOAR):** Skriptet `response_playbook.py` fungerar som sista försvarslinje. Den agerar omedelbart på genererade larm och integrerar direkt med Linux-kärnan (`iptables`) för att blockera angriparens IP-adress, helt utan mänsklig inblandning.

### Reflektion och Utmaningar
Genom att kombinera traditionell regelbaserad övervakning (som direkt fångar kända hot, t.ex. brute-force) med AI-stödd anomalidetektering (som kan hitta okända avvikelser) skapas ett mycket robust försvar. Den största lärdomen är kraften i automatiserad incidentrespons; att låta ett skript blockera en attack i brandväggen tar millisekunder, vilket minimerar skadan avsevärt jämfört med om en människa manuellt hade behövt analysera larmet och agera.

**Utmaningar under labben:**
En specifik utmaning jag stötte på var vid insamlingen av baslinjedata (Steg 11). Eftersom OpenSearch-databasens port (9200) var blockerad utifrån av säkerhetsskäl på kurs-managern, kunde jag inte köra `curl`-kommandot för att exportera loggarna. Jag löste detta genom att simulera och skapa en egen formaterad `baseline_alerts.json` med realistisk testdata. Detta var otroligt lärorikt då det tvingade mig att förstå exakt hur OpenSearch strukturerar sin JSON-data, och det gjorde att jag ändå kunde bygga, träna och verifiera min AI-modell lokalt.

---

## Bevis och Skärmdumpar

### 1. Bekräftad anslutning & Händelseflöde
*Wazuh tar emot data från agenten `debian-fajk` och identifierar olika MITRE ATT&CK-taktiker.*
![Wazuh Agent Ansluten](https://github.com/user-attachments/assets/844d2f65-452e-47b5-94bf-0d56f81bf9e8)

### 2. Detektion av simulerade attacker (FIM)
*Realtidsövervakningen (FIM) upptäcker framgångsrikt när en fil skapas och raderas i den övervakade mappen.*
![FIM Detektion](https://github.com/user-attachments/assets/c8874a08-986c-409e-a405-512d0cf0124f)

### 3. Anpassad Säkerhetsöversikt (Dashboard)
*Visualisering av de senaste 24 timmarnas loggar, fördelat på larmkategori, IP-adresser och tid.*
![Säkerhetsöversikt Dashboard](https://github.com/user-attachments/assets/ea087edb-2f30-4904-8895-6f653e923bf9)

### 4. AI-detektion och Larmgenerering
*Python-skripten analyserar loggdata, hittar en anomali (z=1.79) och konverterar det till ett larm som skrivs tillbaka till systemet.*
![AI Detektion](https://github.com/user-attachments/assets/eb0b294b-5e5b-4bc3-80fc-815cceaf64db)

### 5. Automatiserad Incidentrespons (Blockering i brandvägg)
*Playbook-skriptet reagerar på AI-larmet och lägger automatiskt till en DROP-regel i iptables för den misstänkta IP-adressen (8.8.8.8).*
![Iptables blockering](https://github.com/user-attachments/assets/ce4841de-b693-4cc8-909f-735c9f0f98a6)
