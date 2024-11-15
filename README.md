# post-covid-metadatenkatalog

## Erstellen und Validieren von Metadaten: Vorgehen und Ergebnisse

### DCAT-AP.de

1. **Erstellung der DCAT-AP.de-Metadaten**:  
   Wir haben die zentralen Felder nach DCAT-AP.de-Standard definiert, um eine optimale Auffindbarkeit und klare Struktur sicherzustellen. Dabei haben wir:
   - Je nachdem ob ein Datensatz oder eine API (Datenservice) beschrieben wird, haben wir die entsprechenden **Klassen** (`dcat:Dataset` oder `dcat:DataService`) verwendet.
   - **Titel** (`dct:title`), **Beschreibung** (`dct:description`), und **Herausgeber** (`dct:publisher`) festgelegt, um die Identität und den Kontext des Datensatzes zu beschreiben.
   - **Kontaktinformationen** (`dcat:contactPoint`) sowie **Lizenzdetails** (`dct:license`) aufgenommen, um rechtliche und Support-Angaben einzubinden.
   - **Schlagwörter** (`dcat:keyword`) und **Themenbereiche** (`dcat:theme`) hinzugefügt, um die thematische Zuordnung und Suchbarkeit zu verbessern.
   - Unter **Verteilung** (`dcat:distribution`) haben wir Zugangs-URLs und Dateiformate beschrieben, um Nutzern einen direkten Zugriff zu ermöglichen.

2. **Validierung**:  
   Die erstellten Metadaten haben wir im [DCAT-AP.de Validator](https://www.itb.ec.europa.eu/shacl/dcat-ap.de/upload) geprüft. Der Validator bestätigte die Konformität unserer Metadaten. Über den DCAT-AP.de-Validator können bei Bedarf auch SHACL-Shapes erstellt werden.

### Frictionless Data

1. **Erstellung der Frictionless Data Metadaten**:  
   Zur Strukturierung haben wir eine `datapackage.json` erstellt und darin die relevanten Metadatenfelder aufgenommen:
   - **Name**, **Titel** und **Beschreibung** geben grundlegende Informationen zum Datensatz.
   - **Lizenzen** und **Quellen** bieten rechtliche Klarheit und Dokumentation der Datenherkunft.
   - Unter **contributors** wurden alle beteiligten Teams und Personen verzeichnet.
   - Im Abschnitt **resources** mit **schema** haben wir detaillierte Informationen zu allen Feldern, Datentypen und Beschreibungen jeder Datentabelle festgehalten.

2. **Validierung**:  
   TODO: Validierung der Frictionless Data Metadaten

Durch die strukturierte Erstellung und Validierung nach DCAT-AP.de- und Frictionless-Standards sind die Metadaten nun gut auffindbar und beschrieben. Dies erleichtert die Nutzung und Weiterverwendung der Daten für unterschiedliche Zwecke.