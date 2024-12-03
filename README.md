# Post-Covid Metadatenkatalog

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

Use-Cases für jede Abfrage der Daten können in Juypter-Notebooks in dem Ordner [notebooks](/notebooks/) durchgeführt werden. Folgen Sie dafür dem [Quick Start](#quick-start).

## Quick Start

Dieses Projekt wurde mit Hilfe von poetry aufgesetzt. Poetry übernimmt das Management der benötigten Pakete/ Libraries für die Skripte in python.

Um das Projekt lokal aufzusetzen und alle dependencies zu installieren führen Sie bitte folgende Terminal-Befehle innerhalb des Projekts aus. Siehe auch [offizielle Poetry Dokumentation](https://python-poetry.org/docs/basic-usage/) für mehr Informationen.

```sh
$ poetry install # installiert dependencies von der Datei 'pyproject.toml' und erstellt eine Datei 'poetry.lock'
$ poetry shell # Aktiviert das virtual environment (mit dependencies)
```

## Benutze Datenquellen

Für das Projekt wurden mehrere (öffentliche) Datensätze benutzt um mehr Informationen an die MII-Daten (Patient:innen-Daten zu spielen).

| Datensatz                                 | Kurzbeschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Link                                                                          |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| Luftdaten (Umweltbundesamt)               | Die API des Umwelt Bundesamtest gibt für verschiedene Stationen in Deutschland Luftdaten an. Es gibt einen Luftindex (generelle Angabe zu der Luftqualität), man kann aber auch einzelne Schadstoffe (z.B. Feinstaub PM₁₀) und deren stündliche Werte abfragen.                                                                                                                                                                                                                            | https://www.umweltbundesamt.de/daten/luft/luftdaten/doc                       |
| Wetterdaten (Bright Sky)                  | Die API für Wetterdaten sellt die Daten des Deutschen Wetter Dienstes bereit. Das Wetter (Eigenschaften wie Niederschlag, Sonnenstunden, Temperatur) können mit einem Standort (Breitengrad, Längengrad) stündlich abgefragt werden.                                                                                                                                                                                                                                                       | https://brightsky.dev/                                                        |
| Abwasserdaten (Viruslast im Wasser) - RKI | Die Daten stammen aus dem Projekt Abwassersurveillance AMELAG vom RKI und enthält Daten von Abwasser-Stationen in Deutschland. Der Datensatz wird während der Projektlaufzeit von AMELAG wöchentlich aktualisiert und ist über GitHub zugänglich. Auf Nachfrage bei dem RKI wurden auch die Standorte der Stationen angegeben um ein besseres Matching von Patient:innen auf die relevante Station zu garantieren. Todo: dürfen wir die Daten mit den Standorten öffentlich im Repo haben? | https://github.com/robert-koch-institut/Abwassersurveillance_AMELAG/tree/main |
| POST-Covid Ambulanzen / Kliniken          | Die Daten für POST-Covid Ambulanzen stammen von der BMG Initiative Long Covid. Die Daten aus der dort aufgelisteten Tabelle wurden zuletzt am 02.12.2024 abgefragt und befinden sich in der Datei data/raw/2022-12-02_post_covid_ambulanzen_kliniken.json                                                                                                                                                                                                                                  | https://www.bmg-longcovid.de/service/buergertelefon-und-regionale-kliniksuche |
| POST-Covid Reha Angebote                  | Die Daten für POST-Covid Reha Angebote stammen von der Bundesarbeitsgemeinschaft für Rehabilitation (BAR). In der Suche wurden alle Reha Angebote gezogen die mit der Auswahl 'Rehabilitation bei Long/Post COVID' zu finden sind. Dabei sind stationäre und ambulante Reha Angebote enthalten.                                                                                                                                                                                            | https://www.reha-einrichtungsverzeichnis.de/index.html                        |
| SARS-CoV-2-Infektionen in Deutschland     | Der Datensatz stammt vom RKI und enthält 'umfassende Informationen zu SARS-CoV-2-Infektionen in Deutschland, die gemäß dem Infektionsschutzgesetze (IfSG) von den Gesundheitsämtern an das Robert Koch-Institut (RKI) gemeldet wurden.' - GitHub Beschreibung des RKIs                                                                                                                                                                                                                     | https://github.com/robert-koch-institut/SARS-CoV-2-Infektionen_in_Deutschland |

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

1. **Erstellung der Frictionless Data Metadaten**:  
   Zur Strukturierung haben wir eine `datapackage.json` erstellt und darin die relevanten Metadatenfelder aufgenommen:

   - **Name**, **Titel** und **Beschreibung** geben grundlegende Informationen zum Datensatz.
   - **Lizenzen** und **Quellen** bieten rechtliche Klarheit und Dokumentation der Datenherkunft.
   - Unter **contributors** wurden alle beteiligten Teams und Personen verzeichnet.
   - Im Abschnitt **resources** mit **schema** haben wir detaillierte Informationen zu allen Feldern, Datentypen und Beschreibungen jeder Datentabelle festgehalten.

2. **Validierung**:  
   TODO: Validierung der Frictionless Data Metadaten

Durch die strukturierte Erstellung und Validierung nach DCAT-AP.de- und Frictionless-Standards sind die Metadaten nun gut auffindbar und beschrieben. Dies erleichtert die Nutzung und Weiterverwendung der Daten für unterschiedliche Zwecke.

### Geographisches Mapping

Die benutzten Datenquellen und die synthetischen MII-Daten arbeiten mit verschiedenen geographischen Angaben, wie Postleitzahl, Breitengrad/ Längengrad. Es wurden daher Skripte / Dokumente erstellt die helfen zwischen den Angaben zu mappen. Skripte für geographisches Mapping sind unter [address_transformation.py](src/geolocation/address_transformation.py) zu finden.

| Datensatz / Quelle                                                        | Kurzbeschreibung                                                                                                                                                                                        | Beispiel                                                                                                               |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Mapping von Breitengrad (Lat) und Längengrad (Lng) zu einer Postleitzahl. | Wurde hier aufgerufen: [Geokoordinaten für Postleitzahlen](https://github.com/WZBSocialScienceCenter/plz_geocoord/tree/master) und ursprünglich von der Google Cloud Geocoding API (in 2019) abgefragt. | Wird benutz um für unvollständige Postleitzahlen einen geschätzten Mittelpunkt zu finden (in Breitengrad / Längengrad) |
| tbd                                                                       | tbd                                                                                                                                                                                                     | tbd                                                                                                                    |

Tabelle 2: Geographisches Mapping

### Autoren, Mehr Informationen

tbd: Hinweise von Seiten Technologiestiftung, weiterfürhrende Informationen zu dem Projekt?

Dieses Repository wurde in Kollaboration der Technologiestiftung Berlin und [&effect](https://www.and-effect.com/) erstellt.

tbd: Lizenz?m Hinweise zur Veröffentlichung?
