# post-covid-metadatenkatalog


## Dependency Installation

The respository is implemented with poetry for dependency management. To use please install poetry and then execute these commands in your terminal in the project. See the [official Poetry documentation](https://python-poetry.org/docs/basic-usage/) for more information.

```sh
$ poetry install # will install dependencies from the pyproject.toml file and add a poetry.lock file
$ poetry shell # will activate the virtual environment that has all dependencies installed
```

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

:::info
**Hinweis:**
Die frictionless data Metadaten wurden für den Piloten nur exemplarisch erstellt und validiert. Ob eine vollständige Integration in die bestehende Infrastruktur sinnvoll ist, sollte im Rahmen einer zukünftigen Entwicklung geprüft werden.
:::

1. **Erstellung der Frictionless Data Metadaten**:  
   Zur Strukturierung haben wir eine `datapackage.json` erstellt und darin die relevanten Metadatenfelder aufgenommen:
   - **Name**, **Titel** und **Beschreibung** geben grundlegende Informationen zum Datensatz.
   - **Lizenzen** und **Quellen** bieten rechtliche Klarheit und Dokumentation der Datenherkunft.
   - Unter **contributors** wurden alle beteiligten Teams und Personen verzeichnet.
   - Im Abschnitt **resources** mit **schema** haben wir detaillierte Informationen zu allen Feldern, Datentypen und Beschreibungen jeder Datentabelle festgehalten.

2. **Validierung**:  
   Die Metadaten können mit der frictionless CLI oder der Python-Bibliothek validiert werden. Dazu haben wir die `datapackage.json` mit dem Befehl `frictionless validate metadata/frictionless/datapackage.json --type package` geprüft.

   Für eine zukünftige Entwicklung müsste festgelegt werden, wie genau frictionless Data in die bestehende Infrastruktur integriert werden soll. Dementsprechend müssten Anpassungen an den Metadaten vorgenommen werden (z.B. spezifische Abfragen der APIs) und eine Umstrukturierung der Daten als vollständige Data Packages.



Durch die strukturierte Erstellung und Validierung nach DCAT-AP.de- und Frictionless-Standards sind die Metadaten nun gut auffindbar und beschrieben. Dies erleichtert die Nutzung und Weiterverwendung der Daten für unterschiedliche Zwecke.

