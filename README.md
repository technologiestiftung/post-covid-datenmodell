# Post-Covid Metadatenkatalog
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Über dieses Projekt

tbd - Text von Seiten Technologiestiftung?

Inhalt

1. [Projekt-Struktur](#projekt-struktur)
2. [Quick-Start](#quick-start)
3. [Benutzte Datenquellen](#benutze-datenquellen)
4. [Erstellen und Validieren von Metadaten: Vorgehen und Ergebnisse](#erstellen-und-validieren-von-metadaten-vorgehen-und-ergebnisse)
5. [Geographisches Mapping](#geographisches-mapping)
6. [Autoren, Mehr Informationen](#autoren-mehr-informationen)

## Projekt-Struktur

Dieses GitHub-Repository benutzt synthetische MII-Daten (mehr dazu [hier](https://www.medizininformatik-initiative.de/de/der-kerndatensatz-der-medizininformatik-initiative)) und andere Datenquellen, wie z.B. Wetterdaten um Forscher:innen Informationen zu Patient:innen bereitzustellen.

Die synthetischen Daten der MII-Patient:innen sind in [data/raw/](data/raw/) zu finden. Eine Übersicht zu benutzten (externen) Daten folgt in [Tabelle 1](#benutze-datenquellen).

Für die externen Datenquellen wurde jeweils ein Skript/ eine Klasse erstellt, diese sind in [src/download](src/download) hinterlegt. Dort befindet sich auch ein Skript um die Patient:innen aus den synthetischen Daten zu extrahieren [src/download/patient.py](src/download/patients.py).

Use-Cases für jede Abfrage der Daten können in Juypter-Notebooks in dem Ordner [src/use_cases](/src/use_cases/) durchgeführt werden. Folgen Sie dafür dem [Quick Start](#quick-start).

## Quick Start

Dieses Projekt wurde mit Hilfe von poetry aufgesetzt. Poetry übernimmt das Management der benötigten Pakete/ Libraries für die Skripte in python. Bitte Stellen Sie sicher, dass Sie poetry installiert haben bevor Sie das Projekt lokal ausführen. Siehe hier: [Poetry Website / Installation](https://python-poetry.org/docs/).

Um das Projekt lokal aufzusetzen und alle dependencies zu installieren führen Sie bitte folgende Terminal-Befehle innerhalb des Projekts aus. Siehe auch [offizielle Poetry Dokumentation](https://python-poetry.org/docs/basic-usage/) für mehr Informationen.

```sh
$ poetry install # installiert dependencies von der Datei 'pyproject.toml' und erstellt eine Datei 'poetry.lock'
$ poetry shell # Aktiviert das virtual environment (mit dependencies)
```

Das Projekt ist anhand von 'Use Cases' aufgebaut. Für jeden Datensatz gibt es ein Jupyter Notebook.

Für eine Auflistung der verfügbaren Skripte und abgedeckten Use Cases gibt es eine erweiterte Dokumentation: [Tabelle 3: Auflistung abgedeckte Use Cases](src/use_cases/README.md). Bitte stellen Sie sicher, dass Sie beim Ausführen der Skripte innerhalb des Poetry Enviroments sind.

## Benutze Datenquellen

Für das Projekt wurden mehrere (öffentliche) Datensätze benutzt um mehr Informationen an die MII-Daten (Patient:innen-Daten zu spielen).

| Datensatz                                 | Kurzbeschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Link                                                                          | Metaden-Beschreibung                                                                                                                                    |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Luftdaten (Umweltbundesamt)               | Die API des Umwelt Bundesamtest gibt für verschiedene Stationen in Deutschland Luftdaten an. Es gibt einen Luftindex (generelle Angabe zu der Luftqualität), man kann aber auch einzelne Schadstoffe (z.B. Feinstaub PM₁₀) und deren stündliche Werte abfragen.                                                                                                                                                                                                                            | https://www.umweltbundesamt.de/daten/luft/luftdaten/doc                       | [Frictionless Metadaten](metadata/frictionless/luftqualitaet-datapackage.json), [DCAT Metadaten](/metadata/dcat/luftqualitaet.jsonld)                   |
| Wetterdaten (Bright Sky)                  | Die API für Wetterdaten sellt die Daten des Deutschen Wetter Dienstes bereit. Das Wetter (Eigenschaften wie Niederschlag, Sonnenstunden, Temperatur) können mit einem Standort (Breitengrad, Längengrad) stündlich abgefragt werden.                                                                                                                                                                                                                                                       | https://brightsky.dev/                                                        | [Frictionless Metadaten](metadata/frictionless/wetter-datapackage.json), [DCAT Metadaten](/metadata/dcat/dwd_wetter.jsonld)                             |
| Abwasserdaten (Viruslast im Wasser) - RKI | Die Daten stammen aus dem Projekt Abwassersurveillance AMELAG vom RKI und enthält Daten von Abwasser-Stationen in Deutschland. Der Datensatz wird während der Projektlaufzeit von AMELAG wöchentlich aktualisiert und ist über GitHub zugänglich. Auf Nachfrage bei dem RKI wurden auch die Standorte der Stationen angegeben um ein besseres Matching von Patient:innen auf die relevante Station zu garantieren. Todo: dürfen wir die Daten mit den Standorten öffentlich im Repo haben? | https://github.com/robert-koch-institut/Abwassersurveillance_AMELAG/tree/main | [Frictionless Metadaten](metadata/frictionless/rki_abwasser_viruslast_datapackage.json), [DCAT Metadaten](/metadata/dcat/rki_abwasser_viruslast.jsonld) |
| POST-Covid Ambulanzen / Kliniken          | Die Daten für POST-Covid Ambulanzen stammen von der BMG Initiative Long Covid. Die Daten aus der dort aufgelisteten Tabelle wurden zuletzt am 02.12.2024 abgefragt und befinden sich in der Datei data/raw/2022-12-02_post_covid_ambulanzen_kliniken.json                                                                                                                                                                                                                                  | https://www.bmg-longcovid.de/service/buergertelefon-und-regionale-kliniksuche |
| POST-Covid Reha Angebote                  | Die Daten für POST-Covid Reha Angebote stammen von der Bundesarbeitsgemeinschaft für Rehabilitation (BAR). In der Suche wurden alle Reha Angebote gezogen die mit der Auswahl 'Rehabilitation bei Long/Post COVID' zu finden sind. Dabei sind stationäre und ambulante Reha Angebote enthalten.                                                                                                                                                                                            | https://www.reha-einrichtungsverzeichnis.de/index.html                        |
| SARS-CoV-2-Infektionen in Deutschland     | Der Datensatz stammt vom RKI und enthält 'umfassende Informationen zu SARS-CoV-2-Infektionen in Deutschland, die gemäß dem Infektionsschutzgesetze (IfSG) von den Gesundheitsämtern an das Robert Koch-Institut (RKI) gemeldet wurden.' - GitHub Beschreibung des RKIs                                                                                                                                                                                                                     | https://github.com/robert-koch-institut/SARS-CoV-2-Infektionen_in_Deutschland | [Frictionless Metadaten](metadata/frictionless/rki_covid_faelle_datapackage.json), [DCAT Metadaten](/metadata/dcat/rki_covid_faelle.jsonld)             |

Tabelle 1: Übersicht der benutzten Datenquellen

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

### Geographisches Mapping

Die benutzten Datenquellen und die synthetischen MII-Daten arbeiten mit verschiedenen geographischen Angaben, wie Postleitzahl, Breitengrad/ Längengrad. Es wurden daher Skripte / Dokumente erstellt die helfen zwischen den Angaben zu mappen. Skripte für geographisches Mapping sind unter [address_transformation.py](src/geolocation/address_transformation.py) zu finden.

| Datensatz / Quelle                                                                                                                                                                                                                  | Kurzbeschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Beispiel                                                                                                                      |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Mapping von Breitengrad (Lat) und Längengrad (Lng) zu einer Postleitzahl.<li> [2024-11-14_plz_geocoord.csv](data/raw/2024-11-14_plz_geocoord.csv)</li>                                                                              | Wurde hier aufgerufen: [Geokoordinaten für Postleitzahlen](https://github.com/WZBSocialScienceCenter/plz_geocoord/tree/master) und ursprünglich von der Google Cloud Geocoding API (in 2019) abgefragt.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Wird benutzt um für unvollständige Postleitzahlen einen geschätzten Mittelpunkt zu finden (in Breitengrad / Längengrad)       |
| Mapping von Postleitzahl auf IdLandkreis <li>[2024-12-03_postleitzahlen_kreis_id.csv](data/raw/2024-12-03_postleitzahlen_kreis_id.csv)</li><li>[2024-12-03_berlin_plz_mapping.csv](data/raw/2024-12-03_berlin_plz_mapping.csv)</li> | Wird benutzt um bei den Covid-Daten von dem RKI die sogenannte IdLandkreis zu generieren. Basiert auf einer Veröffentlichung von [Opendatasoft; BKG](https://public.opendatasoft.com/explore/dataset/georef-germany-postleitzahl/information/?dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6Imdlb3JlZi1nZXJtYW55LXBvc3RsZWl0emFobCIsIm9wdGlvbnMiOnt9fSwiY2hhcnRzIjpbeyJhbGlnbk1vbnRoIjp0cnVlLCJ0eXBlIjoiY29sdW1uIiwiZnVuYyI6IkNPVU5UIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiI0ZGNTE1QSJ9XSwieEF4aXMiOiJwbHpfbmFtZSIsIm1heHBvaW50cyI6NTAsInNvcnQiOiIifV0sInRpbWVzY2FsZSI6IiIsImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWV9&location=11,51.6931,8.28335&basemap=jawg.light) mit Angaben zu Land- und Kreiscode für Postleitzahlen in Deutschland. Für die Generierung des Mappings Postleitzahl -> IdLandkreis wurde Landcode und Kreiscode benutzt. für Berlin gelten vom RKI definierte Sonderregelungen (Anpassung der Id),d iese wurde manuell erstellt und ist in [2024-12-03_berlin_plz_mapping.csv](data/raw/2024-12-03_berlin_plz_mapping.csv) festgehalten. Manuell meint hier: Das RKI hat in ihrere Dokumentation [siehe GitHub Repo RKI](https://github.com/robert-koch-institut/SARS-CoV-2-Infektionen_in_Deutschland/blob/main/%5BDokumentation%5D_SARS-CoV-2-Infektionen_in_Deutschland.pdf) festgehalten werlche Bezirke in Berlin welche Id bekommen. Es wurden dann manuell (per google) die Postleitzahlen für diese Bezirke gesucht und den jeweiligen Ids zugeordnet. | wird benutzt um bei der Abfrage der Covid-Daten die richtige id in den Daten für die Postleitzahl der Patient:innen zu finden |
| Bundesland-Abkürzungsverzeichnis <li>[2024-11-13_federal_state_mapper.xlsx](data/raw/2024-11-13_federal_state_mapper.xlsx)</li>                                                                                                     | Wurde manuell erstellt. Enthält Bundesland Abkürzungen und die ausgeschriebenen Namen der Bundesländer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Kann beispielsweise verwendet werden um Bundesländer-Abkürzungen in den Covid-Daten zu 'übersetzen' .                         |

Tabelle 2: Geographisches Mapping

### Utils / Hilfsfunktionen

Für die verschiedenen Use Cases wurden Hilfsfunktionen, wie z.B. Berechnung des Alters der Patient:innen erstellt. Diese sind in dem Ordner [src/utils](src/utils) zu finden. In dem Skript [graph_configurations.py](src/utils/graph_configurations.py) wurden für die verschiedenen Use Cases Funktionen für die Datenvisualisierung erstellt. So können einfache Timeline Plots erstellt werden. Das Skript [time_age_calculation.py](src/time_age_calculation.py) enthält Hilfsfunktion um beispielsweise die Altersgruppe der Patient:innen (benutzt für die Covid Cases) zu finden oder den Zeitraum X Monate vor- und nach einem Datum zu finden.

### Autoren, Mehr Informationen

tbd: Hinweise von Seiten Technologiestiftung, weiterfürhrende Informationen zu dem Projekt?

Dieses Repository wurde in Kollaboration der Technologiestiftung Berlin und [&effect](https://www.and-effect.com/) erstellt.

tbd: Lizenz?m Hinweise zur Veröffentlichung?

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/bauerfriederike"><img src="https://avatars.githubusercontent.com/u/141726622?v=4?s=100" width="100px;" alt="bauerfriederike"/><br /><sub><b>bauerfriederike</b></sub></a><br /><a href="https://github.com/technologiestiftung/post-covid-datenmodell/commits?author=bauerfriederike" title="Code">💻</a> <a href="https://github.com/technologiestiftung/post-covid-datenmodell/commits?author=bauerfriederike" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!