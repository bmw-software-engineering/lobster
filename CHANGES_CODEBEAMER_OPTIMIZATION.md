# Änderungsdokumentation: Codebeamer-Tool Optimierung und Erweiterungen

**Datum:** April 2026  
**Autor:** GitHub Copilot  
**Status:** Abgeschlossen und validiert  
**Betroffene Versionen:** Lobster 2.x und nachfolgende

---

## 1. Übersicht

Diese Dokumentation beschreibt die tatsächlich umgesetzten Änderungen rund um Codebeamer-Extraktion, Datenmodell, Report/HTML-Ausgabe, TRLC-Import, Testabdeckung und Packaging.

### Hauptziele
- Sichtbarkeit zusätzlicher Requirement-Felder im HTML-Report
- Erweiterung um ASIL-Weitergabe in den relevanten Verarbeitungspfaden
- Ergänzung von Konfigurationsoptionen für Codebeamer Baselines

---

## 2. Motivation für Änderung

### 2.1 ASIL Attribuierung der Anforderungen
Der ASIL-Wert einer Anforderung wurde bisher nicht aus Codebeamer extrahiert und nicht im Lobster-Datenmodell gespeichert. Er war daher weder in `report.lobster` noch im HTML-Report sichtbar.

Änderungen:
- Auslesen des ASIL-Werts aus nativen Codebeamer-Feldern und aus `customFields`
- Erweiterung des Requirement-Datenmodells um das Attribut `asil`
- Übernahme des ASIL-Werts im TRLC-Importpfad
- Anzeige von ASIL im HTML-Report

### 2.2 Argumentation im `ver_Val`-Attribut
Die Felder `ver_ValSetup` und `ver_ValRationalargumentation` wurden nicht aus Codebeamer extrahiert. Ursache war, dass WikiText-Felder den Wert in `customFields[].value` statt in `customFields[].values[]` ablegen. Die Felder fehlten dadurch in `report.lobster` und im HTML-Report.

Änderungen:
- Extraktion mit Fallback auf `value` zusätzlich zu `values[]`
- Unterstützung unterschiedlicher Feldnamenvarianten
- Explizite Serialisierung in `report.lobster`
- Anzeige im HTML-Report

### 2.3 Codebeamer Query auf Baseline einschränken
Ohne Baseline-Bezug liefert eine Codebeamer-Query stets den aktuellen Stand, der sich zwischen zwei Ausführungen unterscheiden kann. Es gab keine Möglichkeit, eine Abfrage auf einen definierten Baseline-Stand zu fixieren.

Änderungen:
- Neuer Config-Parameter `baseline_id` (positive Integer)
- Übergabe von `baselineId` an die Codebeamer-Query-Endpunkte

---

## 3. Durchgeführte Änderungen

### 3.1 Datei: `lobster/tools/codebeamer/codebeamer.py`

#### 3.1.1 Feldextraktion robuster gemacht
- Erweiterte Extraktionslogik für `ver_ValSetup` und `ver_ValRationalargumentation`
- Fallbacks für unterschiedliche Feldnamenvarianten
- Unterstützung für Werte in `value`, `values[]` sowie rekursive Schlüsselauflösung

#### 3.1.2 Detail-Fetches optimiert
- `to_lobster(..., fetch_missing_details=True)` eingeführt
- Detailaufrufe werden nur dann erzwungen, wenn relevante Felder fehlen
- Query-Importpfad verarbeitet Report-Wrapper-Felder gezielt (Merge ohne Überschreiben nicht-nulliger Werte)

#### 3.1.3 ASIL-Unterstützung ergänzt
- ASIL-Auslese aus nativen Feldern (`aSIL`) und aus `customFields`
- Weitergabe in die Erzeugung von Requirement-Objekten

#### 3.1.4 Konfiguration erweitert
- Neuer Config-Key `baseline_id` inkl. Validierung (positive Integer)
- `baselineId` wird an Query-Endpunkte angehängt, wenn konfiguriert
- `verify_ssl` akzeptiert jetzt `bool` oder PEM-Pfad (`str`)
- Verbesserte Fehlermeldungen für SSL-/Verbindungsprobleme

### 3.2 Datei: `lobster/tools/codebeamer/config.py`

- Config-Typen erweitert:
- `baseline_id: Optional[int]`
- `verify_ssl: Union[bool, str]`

### 3.3 Datei: `lobster/common/items.py`

- Requirement-Datenmodell erweitert um:
- `asil`
- `ver_ValSetup`
- `ver_ValRationalargumentation`
- JSON-Serialisierung und Deserialisierung (`to_json`/`from_json`) entsprechend angepasst

### 3.4 Datei: `lobster/common/report.py`

- Report-Export nutzt nun einen dedizierten Mapping-Pfad (`_item_to_report_json`)
- Requirement-spezifische Felder werden explizit in `report.lobster` erhalten

### 3.5 Datei: `lobster/tools/core/html_report/html_report.py`

- Rendering um zusätzliche Requirement-Attribute ergänzt:
- `ASIL`
- `Ver_Val setup`
- `Ver_Val rational/argumentation`

### 3.6 Datei: `lobster/tools/trlc/converter.py`

- ASIL-Wert aus TRLC-Objekten wird in Requirement-Objekte übernommen

---

## 4. Testing und Validierung

### Geänderte/erweiterte Testdateien
- `tests_unit/lobster_codebeamer/test_codebeamer.py`
- `tests_unit/lobster_report/test_report.py`
- `tests_unit/lobster_html_report/test_html_report.py`
- `tests_unit/lobster_trlc/test_converter.py`
- `tests_unit/test_items.py`

### Inhaltlich abgedeckte Punkte
- Extraktion von WikiText-ähnlichen Feldern aus `value` und `values[]`
- Verhinderung unnötiger Detail-API-Aufrufe
- Merge-Verhalten (nicht-nullige Werte bleiben erhalten)
- ASIL-Propagation in Codebeamer-, TRLC- und Datenmodell-Pfaden
- Persistenz neuer Requirement-Felder in Report-JSON
- Sichtbarkeit der neuen Felder im HTML-Report

### Validierungs-Zusammenfassung
- Code- und Teständerungen für alle betroffenen Pfade vorhanden
- Dokumentation auf tatsächliche geänderte Dateien abgeglichen

---

## 5. Abhängigkeits- und Packaging-Änderungen

### Laufzeitabhängigkeiten
- Keine neuen fachlichen Runtime-Abhängigkeiten im Codepfad erforderlich

### Packaging/Build-Artefakte ergänzt
- Neuer Hook: `hooks/hook-certifi.py`
- Neue PyInstaller-Spec-Dateien:
- `lobster-codebeamer.spec`
- `lobster-html-report.spec`
- `lobster-pkg.spec`
- `lobster-report.spec`
- `lobster-trlc.spec`
- `lobster-trlc-cli.spec`
- `lobster-trlc-full.spec`

Hinweis: Diese Änderungen betreffen Build/Bundling und sollten bei Release/Distribution berücksichtigt werden.

---

## 6. Performance-Auswirkungen

### API-Anrufe
- Detail-Fetches werden bedarfsorientiert ausgeführt
- Im Query-Importpfad sinkt die Anzahl unnötiger Item-Detailaufrufe

### Erwartete Wirkung
- Geringere API-Last
- Kürzere Laufzeiten bei größeren Importen

---

## 7. Migrations-Guide

### Für Endbenutzer
1. Keine zwingenden manuellen Schritte für bestehende Basisfunktionalität.
2. Neue Felder erscheinen nach erneuter Extraktion/Report-Erzeugung in den Ausgaben.

### Für Entwickler
1. Optionales Verhalten in `to_lobster` beachten:
```python
item = to_lobster(cb_config, cb_item, fetch_missing_details=False)
```
2. Neue Config-Optionen möglich:
```yaml
baseline_id: 123456
verify_ssl: true
# oder
verify_ssl: C:/certs/company-root-ca.pem
```
3. Packaging-Prozesse bei Bedarf auf neue `.spec`-Dateien umstellen.

---

## 8. Bekannte Einschränkungen und Future Work

### Aktuelle Limitationen
1. Feldsemantik und Namensvarianten hängen weiterhin von Codebeamer-Instanzkonfigurationen ab.
2. Kein allgemeines Caching-/Batching-Konzept für alle API-Pfade implementiert.

### Mögliche nächste Schritte
- Batch-Endpoints nutzen, wo möglich
- Caching für häufig abgefragte Items
- Erweiterte Retry-/Backoff-Strategien
- Weitere Harmonisierung von Feldnamen und Typkonvertierungen

---

## 9. Rollback-Anleitung

Bei Bedarf können Änderungen selektiv per Git-Revert zurückgenommen werden.

Empfohlene Reihenfolge für gezielten Rollback:
1. `lobster/tools/codebeamer/codebeamer.py`
2. `lobster/common/items.py`
3. `lobster/common/report.py`
4. `lobster/tools/core/html_report/html_report.py`
5. `lobster/tools/trlc/converter.py`
6. `lobster/tools/codebeamer/config.py`
7. Packaging-Dateien (`hooks/` und `*.spec`)

---

## 10. Kontakt und Support

Bei Fragen:
- Diese Änderungsdokumentation prüfen
- Unit-Tests in `tests_unit/` als Referenz verwenden
- Packaging-Themen in `hooks/` und den `.spec`-Dateien nachvollziehen

---

## Anhang A: Betroffene Dateien

### Modifiziert
1. `lobster/common/items.py`
2. `lobster/common/report.py`
3. `lobster/tools/codebeamer/codebeamer.py`
4. `lobster/tools/codebeamer/config.py`
5. `lobster/tools/core/html_report/html_report.py`
6. `lobster/tools/trlc/converter.py`
7. `tests_unit/lobster_codebeamer/test_codebeamer.py`
8. `tests_unit/lobster_html_report/test_html_report.py`
9. `tests_unit/lobster_report/test_report.py`
10. `tests_unit/lobster_trlc/test_converter.py`
11. `tests_unit/test_items.py`

### Neu angelegt
1. `CHANGES_CODEBEAMER_OPTIMIZATION.md`
2. `hooks/hook-certifi.py`
3. `lobster-codebeamer.spec`
4. `lobster-html-report.spec`
5. `lobster-pkg.spec`
6. `lobster-report.spec`
7. `lobster-trlc.spec`
8. `lobster-trlc-cli.spec`
9. `lobster-trlc-full.spec`

---

**Dokumentations-Version:** 1.1  
**Letzte Aktualisierung:** April 2026  
**Status:** Produktiv
