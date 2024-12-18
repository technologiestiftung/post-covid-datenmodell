# Post-Covid Metadatenkatalog
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Über dieses Projekt

Die Technologiestiftung Berlin entwickelt im Rahmen der Post-COVID-Challenge des Dateninstituts des Bundes ein Datenmodell zur Post-COVID-Forschung. Dieses ermöglicht es Medizinforschenden, Gesundheitsdaten mit offenen Daten zu kombinieren. Aktuell befinden wir uns in der zweiten von drei Challenge-Stufen. Ziel ist es, eine Datengrundlage für gesellschaftlich relevante Forschungsfragen zu schaffen, unterstützt durch Tools zur Verschneidung und Analyse medizinischer und offener Daten.

Inhalt

1. [Projekt-Struktur](#projekt-struktur)
2. [Quick-Start](#quick-start)
3. [Benutzte Datenquellen](#benutze-datenquellen)
4. [Erstellen und Validieren von Metadaten: Vorgehen und Ergebnisse](#erstellen-und-validieren-von-metadaten-vorgehen-und-ergebnisse)
5. [Geographisches Mapping](#geographisches-mapping)
6. [Autoren, Mehr Informationen](#autoren-mehr-informationen)

## Projekt-Struktur

Dieses GitHub-Repository benutzt synthetische MII-Daten (mehr dazu [hier](https://www.medizininformatik-initiative.de/de/der-kerndatensatz-der-medizininformatik-initiative)) und andere offenen Datenquellen, wie z.B. Wetterdaten, um Forscher:innen Informationen zu Patient:innen bereitzustellen.

Die synthetischen Daten der MII-Patient:innen sind in [data/raw/](data/raw/) zu finden. Eine Übersicht zu benutzten (externen) Daten folgt in [Tabelle 1](#benutze-datenquellen).

Für die externen Datenquellen wurde jeweils ein Skript/eine Klasse erstellt, diese sind in [src/download](src/download) hinterlegt. Dort befindet sich auch ein Skript, um die Patient:innen aus den synthetischen Daten zu extrahieren [src/download/patient.py](src/download/patients.py).

Use-Cases für jede Abfrage der Daten können in Juypter-Notebooks in dem Ordner [src/use_cases](/src/use_cases/) durchgeführt werden. Folgen Sie dafür dem [Quick Start](#quick-start).

## Quick Start

Dieses Projekt wurde mit Hilfe von poetry aufgesetzt. Poetry übernimmt das Management der benötigten Pakete/ Libraries für die Skripte in python. Bitte Stellen Sie sicher, dass Sie poetry installiert haben, bevor Sie das Projekt lokal ausführen. Siehe hier: [Poetry Website / Installation](https://python-poetry.org/docs/).

Um das Projekt lokal aufzusetzen und alle dependencies zu installieren, führen Sie bitte folgende Terminal-Befehle innerhalb des Projekts aus. Siehe auch [offizielle Poetry Dokumentation](https://python-poetry.org/docs/basic-usage/) für mehr Informationen.

```sh
$ poetry install # installiert dependencies von der Datei 'pyproject.toml' und erstellt eine Datei 'poetry.lock'
$ poetry shell # Aktiviert das virtual environment (mit dependencies)
```

Das Projekt ist anhand von 'Use Cases' aufgebaut. Für jeden 'Use Case' und den darin verarbeiteten Datensatz gibt es ein Jupyter Notebook.

Für eine Auflistung der verfügbaren Skripte und abgedeckten Use Cases gibt es eine erweiterte Dokumentation: [Tabelle 3: Auflistung abgedeckte Use Cases](src/use_cases/README.md). Bitte stellen Sie sicher, dass Sie beim Ausführen der Skripte innerhalb des Poetry Enviroments sind.

## Benutzte Datenquellen

Für das Projekt wurden mehrere (öffentliche) Datensätze benutzt, um weitere Informationen an die Patient:innen-Daten zu spielen.

| Datensatz                                 | Kurzbeschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Link                                                                          | Metaden-Beschreibung                                                                                                                                    |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Luftdaten (Umweltbundesamt)               | Die API des Umweltbundesamt gibt für verschiedene Stationen in Deutschland Luftdaten an. Es gibt einen Luftindex (generelle Angabe zu der Luftqualität), sowie stündliche Werte für einzelne Schadstoffe (z.B. Feinstaub PM₁₀).                                                                                                                                                                                                                            | https://www.umweltbundesamt.de/daten/luft/luftdaten/doc                       | [Frictionless Metadaten](metadata/frictionless/luftqualitaet-datapackage.json), [DCAT Metadaten](/metadata/dcat/luftqualitaet.jsonld)                   |
| Wetterdaten (Bright Sky)                  | Die API für Wetterdaten sellt die Daten des Deutschen Wetterdienstes bereit. Wettereigenschaften wie Niederschlag, Sonnenstunden, Temperatur, können mit einem Standort (Breitengrad, Längengrad) stündlich abgefragt werden.                                                                                                                                                                                                                                                       | https://brightsky.dev/                                                        | [Frictionless Metadaten](metadata/frictionless/wetter-datapackage.json), [DCAT Metadaten](/metadata/dcat/dwd_wetter.jsonld)                             |
| Abwasserdaten (Viruslast im Wasser) - RKI | Die Daten stammen aus dem Projekt Abwassersurveillance AMELAG vom Robert-Koch-Institut (RKI) und enthalten Daten über Infektionserreger im Wasser von Klärwerken in Deutschland. Der Datensatz wird während der Projektlaufzeit von AMELAG wöchentlich aktualisiert und ist über GitHub zugänglich. Auf Nachfrage bei dem RKI wurden auch die Standorte der Stationen angegeben, um ein besseres Matching von Patient:innen auf die relevante Station zu garantieren. | https://github.com/robert-koch-institut/Abwassersurveillance_AMELAG/tree/main | [Frictionless Metadaten](metadata/frictionless/rki_abwasser_viruslast_datapackage.json), [DCAT Metadaten](/metadata/dcat/rki_abwasser_viruslast.jsonld) |
| Post-COVID Ambulanzen / Kliniken          | Die Daten für Post-COVID Ambulanzen stammen von der Initiative Long Covid des Bundesgesundheitsministeriums. Die Daten aus der dort aufgelisteten Tabelle wurden zuletzt am 02.12.2024 abgefragt und befinden sich in der folgenden [Datei](data/raw/2024-12-02_post_covid_ambulanzen_kliniken.json).                                                                                                                                                                                                                                 | https://www.bmg-longcovid.de/service/buergertelefon-und-regionale-kliniksuche |
| Post-COVID Reha Angebote                  | Die Daten für Post-COVID Reha Angebote stammen von der Bundesarbeitsgemeinschaft für Rehabilitation (BAR). In der Suche wurden alle Reha Angebote ausgewählt und gescraped, die mit der Auswahl 'Rehabilitation bei Long/Post COVID' zu finden sind. Dabei sind stationäre und ambulante Reha Angebote enthalten.                                                                                                                                                                                            | https://www.reha-einrichtungsverzeichnis.de/index.html                        |
| SARS-CoV-2-Infektionen in Deutschland     | Der Datensatz stammt vom RKI und enthält 'umfassende Informationen zu SARS-CoV-2-Infektionen in Deutschland, die gemäß dem Infektionsschutzgesetze (IfSG) von den Gesundheitsämtern an das Robert Koch-Institut (RKI) gemeldet wurden.' - GitHub Beschreibung des RKIs                                                                                                                                                                                                                     | https://github.com/robert-koch-institut/SARS-CoV-2-Infektionen_in_Deutschland | [Frictionless Metadaten](metadata/frictionless/rki_covid_faelle_datapackage.json), [DCAT Metadaten](/metadata/dcat/rki_covid_faelle.jsonld)             |

Tabelle 1: Übersicht der benutzten Datenquellen

## Erstellen und Validieren von Metadaten: Vorgehen und Ergebnisse

### DCAT-AP.de

1. **Erstellung der DCAT-AP.de-Metadaten**:  
   Wir haben die zentralen Felder nach DCAT-AP.de-Standard definiert, um eine optimale Auffindbarkeit und klare Struktur sicherzustellen. Dabei haben wir:

   - Je nachdem ob ein Datensatz oder eine API (Datenservice) beschrieben wird, die entsprechenden **Klassen** (`dcat:Dataset` oder `dcat:DataService`) verwendet.
   - **Titel** (`dct:title`), **Beschreibung** (`dct:description`), und **Herausgeber** (`dct:publisher`) festgelegt, um die Identität und den Kontext des Datensatzes zu beschreiben.
   - **Kontaktinformationen** (`dcat:contactPoint`) sowie **Lizenzdetails** (`dct:license`) aufgenommen, um rechtliche und Support-Angaben einzubinden.
   - **Schlagwörter** (`dcat:keyword`) und **Themenbereiche** (`dcat:theme`) hinzugefügt, um die thematische Zuordnung und Suchbarkeit zu verbessern.
   - Unter **Verteilung** (`dcat:distribution`) Zugangs-URLs und Dateiformate beschrieben, um Nutzenden einen direkten Zugriff zu ermöglichen.

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

Die benutzten Datenquellen und die synthetischen MII-Daten arbeiten mit verschiedenen geographischen Angaben, wie Postleitzahl, Breitengrad/ Längengrad. Es wurden daher Skripte / Dokumente erstellt, die helfen zwischen den Angaben zu mappen. Skripte für geographisches Mapping sind unter [address_transformation.py](src/geolocation/address_transformation.py) zu finden.

| Datensatz / Quelle                                                                                                                                                                                                                  | Kurzbeschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Beispiel                                                                                                                      |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Mapping von Breitengrad (Lat) und Längengrad (Lng) zu einer Postleitzahl.<li> [2024-11-14_plz_geocoord.csv](data/raw/2024-11-14_plz_geocoord.csv)</li>                                                                              | Wurde hier aufgerufen: [Geokoordinaten für Postleitzahlen](https://github.com/WZBSocialScienceCenter/plz_geocoord/tree/master) und ursprünglich von der Google Cloud Geocoding API (in 2019) abgefragt.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Wird benutzt um für unvollständige Postleitzahlen einen geschätzten Mittelpunkt zu finden (in Breitengrad / Längengrad)       |
| Mapping von Postleitzahl auf IdLandkreis <li>[2024-12-03_postleitzahlen_kreis_id.csv](data/raw/2024-12-03_postleitzahlen_kreis_id.csv)</li><li>[2024-12-03_berlin_plz_mapping.csv](data/raw/2024-12-03_berlin_plz_mapping.csv)</li> | Wird benutzt um bei den Covid-Daten von dem RKI die sogenannte IdLandkreis zu generieren. Basiert auf einer Veröffentlichung von [Opendatasoft; BKG](https://public.opendatasoft.com/explore/dataset/georef-germany-postleitzahl/information/?dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6Imdlb3JlZi1nZXJtYW55LXBvc3RsZWl0emFobCIsIm9wdGlvbnMiOnt9fSwiY2hhcnRzIjpbeyJhbGlnbk1vbnRoIjp0cnVlLCJ0eXBlIjoiY29sdW1uIiwiZnVuYyI6IkNPVU5UIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiI0ZGNTE1QSJ9XSwieEF4aXMiOiJwbHpfbmFtZSIsIm1heHBvaW50cyI6NTAsInNvcnQiOiIifV0sInRpbWVzY2FsZSI6IiIsImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWV9&location=11,51.6931,8.28335&basemap=jawg.light) mit Angaben zu Land- und Kreiscode für Postleitzahlen in Deutschland. Für die Generierung des Mappings Postleitzahl -> IdLandkreis wurde Landcode und Kreiscode benutzt. für Berlin gelten vom RKI definierte Sonderregelungen (Anpassung der ID),diese wurde manuell erstellt und ist in [2024-12-03_berlin_plz_mapping.csv](data/raw/2024-12-03_berlin_plz_mapping.csv) festgehalten. Manuell meint hier: Das RKI hat in seiner Dokumentation [siehe GitHub Repo RKI](https://github.com/robert-koch-institut/SARS-CoV-2-Infektionen_in_Deutschland/blob/main/%5BDokumentation%5D_SARS-CoV-2-Infektionen_in_Deutschland.pdf) festgehalten, welche Bezirke in Berlin welche ID bekommen. Es wurden dann manuell (per Google) die Postleitzahlen für diese Bezirke gesucht und den jeweiligen IDs zugeordnet. | wird benutzt um bei der Abfrage der Covid-Daten die richtige ID in den Daten für die Postleitzahl der Patient:innen zu finden |
| Bundesland-Abkürzungsverzeichnis <li>[2024-11-13_federal_state_mapper.xlsx](data/raw/2024-11-13_federal_state_mapper.xlsx)</li>                                                                                                     | Wurde manuell erstellt. Enthält Bundesland Abkürzungen und die ausgeschriebenen Namen der Bundesländer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Kann beispielsweise verwendet werden um Bundesländer-Abkürzungen in den Covid-Daten zu 'übersetzen' .                         |

Tabelle 2: Geographisches Mapping

### Utils / Hilfsfunktionen

Für die verschiedenen Use Cases wurden Hilfsfunktionen, wie z.B. Berechnung des Alters der Patient:innen erstellt. Diese sind in dem Ordner [src/utils](src/utils) zu finden. In dem Skript [graph_configurations.py](src/utils/graph_configurations.py) wurden für die verschiedenen Use Cases Funktionen für die Datenvisualisierung erstellt. So können einfache Timeline Plots erstellt werden. Das Skript [time_age_calculation.py](src/time_age_calculation.py) enthält Hilfsfunktion um beispielsweise die Altersgruppe der Patient:innen (benutzt für die Covid Cases) zu finden oder den Zeitraum X Monate vor- und nach einem Datum zu finden.

## Autoren, Mehr Informationen

Weiterführende Informationen zum Projekt, sowie der Challenge zur Gründung des Dateninstitutes finden Sie auf der Seite der [Technologiestiftung Berlin](https://www.technologiestiftung-berlin.de/projekte/post-covid-datenmodell).

Dieses Repository wurde in Kollaboration der Technologiestiftung Berlin und [&effect](https://www.and-effect.com/) erstellt.


### Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/bauerfriederike"><img src="https://avatars.githubusercontent.com/u/141726622?v=4?s=100" width="100px;" alt="bauerfriederike"/><br /><sub><b>bauerfriederike</b></sub></a><br /><a href="https://github.com/technologiestiftung/post-covid-datenmodell/commits?author=bauerfriederike" title="Code">💻</a> <a href="https://github.com/technologiestiftung/post-covid-datenmodell/commits?author=bauerfriederike" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ckeuss"><img src="https://avatars.githubusercontent.com/u/147528104?v=4?s=100" width="100px;" alt="ckeuss"/><br /><sub><b>ckeuss</b></sub></a><br /><a href="https://github.com/technologiestiftung/post-covid-datenmodell/commits?author=ckeuss" title="Documentation">📖</a> <a href="https://github.com/technologiestiftung/post-covid-datenmodell/pulls?q=is%3Apr+reviewed-by%3Ackeuss" title="Reviewed Pull Requests">👀</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/m-b-e"><img src="https://avatars.githubusercontent.com/u/36029603?v=4?s=100" width="100px;" alt="Max B. Eckert"/><br /><sub><b>Max B. Eckert</b></sub></a><br /><a href="#projectManagement-m-b-e" title="Project Management">📆</a> <a href="https://github.com/technologiestiftung/post-covid-datenmodell/commits?author=m-b-e" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jjmllr"><img src="https://avatars.githubusercontent.com/u/68501961?v=4?s=100" width="100px;" alt="jjmllr"/><br /><sub><b>jjmllr</b></sub></a><br /><a href="https://github.com/technologiestiftung/post-covid-datenmodell/commits?author=jjmllr" title="Code">💻</a> <a href="https://github.com/technologiestiftung/post-covid-datenmodell/commits?author=jjmllr" title="Documentation">📖</a> <a href="#projectManagement-jjmllr" title="Project Management">📆</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

### Credits

<table>
  <tr>
    <td>
      <a href="https://www.technologiestiftung-berlin.de/">
        <br />
        <br />
        <img width="200" src="https://logos.citylab-berlin.org/logo-technologiestiftung-berlin-de.svg" />
      </a>
    </td>
    <td>
      In Zusammenarbeit mit: <a href="https://www.bihealth.org/en/">
        <br />
        <br />
        <img width="200" src="https://www.bihealth.org/_assets/6cb4206c3a065969362f190803612019/Frontend/Build/assets/images/bih-logo.svg" />
      </a>
    </td>
    <td>
      und: <a href="https://www.and-effect.com/de/">
        <br />
        <br />
        <svg viewBox="0 0 410.1 103" id="logo" class="h-full" data-v-b21d18f4="" width="200">
          <path fill="#fe563e" d="M20.6,41.5c-1.5-2.8-2.2-5.9-2.2-9.3c0-5.1,1.6-9.3,4.8-12.4c3.2-3.1,7.5-4.7,12.7-4.7
	c3.6,0,6.8,0.8,9.6,2.5c2.8,1.7,5.3,4.1,7.4,7.2l4.8-4.6c-1.5-2.4-3.3-4.5-5.5-6.2c-2.2-1.7-4.6-3-7.4-4c-2.7-1-5.8-1.4-9.1-1.4
	c-4.7,0-8.9,1-12.6,3c-3.7,2-6.5,4.8-8.6,8.2c-2.1,3.5-3.1,7.5-3.1,12.2c0,4,0.9,7.8,2.6,11.4c0.9,1.9,2.1,3.7,3.5,5.6
	c-4.4,2.4-7.9,5.7-10.6,9.9c-3,4.7-4.5,9.8-4.5,15.2c0,5.1,1.2,9.7,3.7,13.6c2.4,3.9,5.8,7,10,9.3c4.2,2.3,9.1,3.4,14.6,3.4
	c3.8,0,7.3-0.5,10.7-1.6c3.4-1.1,6.4-2.7,9.2-4.7c2-1.5,3.8-3.2,5.2-5.2l9.9,10.2h8.8L28,51.1C24.5,47.5,22,44.3,20.6,41.5
	 M43.9,90.7C40,92.9,35.7,94,31,94c-4.2,0-7.9-0.9-11.2-2.6c-3.3-1.7-5.8-4-7.7-7c-1.9-3-2.8-6.4-2.8-10.3c0-4.7,1.2-9,3.7-12.9
	c2.2-3.4,4.9-6,8.2-7.9c0.3,0.3,0.6,0.7,1,1l29,29.9C49.4,86.8,47,89,43.9,90.7 M120.3,38.1c-4.8-2.7-10.4-4.1-16.8-4.1
	c-6.5,0-12.3,1.4-17.4,4.3c-5.1,2.9-9.2,6.8-12.2,11.8c-3,5-4.4,10.7-4.4,16.9c0,6.5,1.5,12.2,4.6,17.3c3.1,5.1,7.2,9,12.6,11.8
	c5.3,2.8,11.4,4.3,18.3,4.3c5.4,0,10.3-0.9,14.8-2.7c4.4-1.8,8.2-4.6,11.4-8.3l-11.1-11c-1.9,2.2-4.1,3.8-6.7,4.9
	c-2.5,1.1-5.3,1.6-8.4,1.6c-3.4,0-6.3-0.7-8.8-2.2c-2.5-1.4-4.4-3.5-5.8-6.2c-0.4-0.8-0.8-1.7-1.1-2.7l45.5-0.2
	c0.4-1.6,0.7-3,0.9-4.3c0.1-1.3,0.2-2.5,0.2-3.7c0-6.2-1.4-11.7-4.2-16.5C128.9,44.6,125.1,40.8,120.3,38.1 M95.6,51.6
	c2.3-1.5,5-2.2,8.2-2.2c2.9,0,5.3,0.7,7.4,2c2,1.3,3.6,3.2,4.6,5.6c0.4,0.9,0.8,2,1,3.1l-27.5,0.2c0.3-0.9,0.6-1.7,0.9-2.4
	C91.5,55.1,93.3,53.1,95.6,51.6 M208.9,29.5c0-2.7,0.8-4.8,2.4-6.4c1.6-1.6,3.8-2.4,6.5-2.4c1.5,0,2.7,0.2,3.8,0.7
	c1,0.5,2,1.2,2.9,2l12.6-12.8c-2.4-2.4-5.3-4.4-8.6-5.9c-3.3-1.5-7.1-2.2-11.5-2.2c-5.7,0-10.6,1.2-14.9,3.7
	c-2.2,1.2-4.1,2.7-5.7,4.4c-1.2-1.1-2.5-2.1-4-3c-4-2.5-9-3.7-14.9-3.7c-5.9,0-11.1,1.3-15.4,3.8c-4.4,2.5-7.7,6-10,10.4
	c-2.3,4.4-3.5,9.4-3.5,14.9v2.6h-14.1v17.1h14.1v46.5h20V52.6h20.3v46.5h20V52.6h18.3V35.5h-18.3V29.5z M168.6,35.5v-4.1
	c0-3.2,0.9-5.7,2.7-7.5c1.8-1.8,4.3-2.7,7.5-2.7c3.2,0,5.7,0.9,7.5,2.7c1.8,1.8,2.6,4.4,2.6,7.6v3.9H168.6z M278.2,38.1
	c-4.8-2.7-10.4-4.1-16.8-4.1c-6.5,0-12.3,1.4-17.4,4.3c-5.1,2.9-9.2,6.8-12.2,11.8c-3,5-4.4,10.7-4.4,16.9c0,6.5,1.5,12.2,4.6,17.3
	c3.1,5.1,7.2,9,12.6,11.8c5.3,2.8,11.4,4.3,18.3,4.3c5.4,0,10.3-0.9,14.8-2.7c4.4-1.8,8.2-4.6,11.4-8.3l-11.1-11
	c-1.9,2.2-4.1,3.8-6.7,4.9c-2.5,1.1-5.3,1.6-8.4,1.6c-3.4,0-6.3-0.7-8.8-2.2c-2.5-1.4-4.4-3.5-5.8-6.2c-0.4-0.8-0.8-1.7-1.1-2.7
	l45.5-0.2c0.4-1.6,0.7-3,0.9-4.3c0.1-1.3,0.2-2.5,0.2-3.7c0-6.2-1.4-11.7-4.2-16.5C286.7,44.6,283,40.8,278.2,38.1 M253.5,51.6
	c2.3-1.5,5-2.2,8.2-2.2c2.9,0,5.3,0.7,7.4,2c2,1.3,3.6,3.2,4.6,5.6c0.4,0.9,0.8,2,1,3.1l-27.5,0.2c0.3-0.9,0.6-1.7,0.9-2.4
	C249.4,55.1,251.2,53.1,253.5,51.6 M338.9,80.9c2-0.9,3.8-2.1,5.3-3.8l13,12.8c-3.4,3.5-7.2,6.1-11.3,7.9c-4.1,1.8-8.8,2.7-14.1,2.7
	c-6.6,0-12.6-1.4-17.9-4.3c-5.3-2.9-9.5-6.8-12.5-11.9c-3-5.1-4.5-10.7-4.5-17c0-6.4,1.5-12.1,4.6-17.1c3.1-5,7.2-9,12.6-11.8
	c5.3-2.9,11.3-4.3,17.9-4.3c5.1,0,9.7,0.9,13.8,2.6c4.1,1.7,7.8,4.2,11.1,7.5l-13,13.1c-1.5-1.7-3.2-2.9-5.2-3.7
	c-2-0.8-4.2-1.2-6.7-1.2c-2.8,0-5.3,0.6-7.5,1.9c-2.2,1.3-4,3-5.2,5.2c-1.3,2.2-1.9,4.8-1.9,7.7c0,3,0.6,5.6,1.9,7.9
	c1.3,2.3,3,4,5.3,5.3c2.3,1.3,4.8,1.9,7.5,1.9C334.6,82.2,336.9,81.8,338.9,80.9 M407.6,52.6h-14.4v46.5h-20.2V52.6h-14.3V35.5h14.3
	V9.2h20.2v26.3h14.4V52.6z" data-v-b21d18f4="">
        </path>
	    </svg>
      </a>
    </td>
    <td>
      Im Auftrag des: <a href="https://www.bmi.bund.de/DE/startseite/startseite-node.html">
        <br />
        <br />
        <img width="150" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/BMI_Logo.svg/320px-BMI_Logo.svg.png" />
      </a>
    </td>
  </tr>
</table>