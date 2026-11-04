# Automation Engineering Academy — Version 3.0

## Open and upgrade

Download/extract the `standalone-v3.0.0` ZIP and double-click **Automation-Academy-V3.html** in Chrome or Edge. No VS Code, Python, terminal or server is needed for the standalone app. Before upgrading, open V2 → Projects → Export backup; open V3 → Projects → Import backup and select that JSON. V1/V2 HTML files remain unchanged. V3 uses a separate `automation-academy-v3` local-storage key and adds a `designV3` object to the existing project/backup schema.

Keep the file in a permanent location and export backups regularly. Moving the file, changing browser/profile, clearing browser data or using private mode can make browser-local data unavailable. The HTML is the app; exported JSON is your portable project data. Runtime PLC outputs still reset on reopen.

Home now links to **V3 panel design**, **SANS / IEC review**, and **Engineering mastery path**. All V2 tools and the original learning/project features remain available.

## Integrated panel design studio

Start with one of three illustrative packages:

1. Pneumatic transfer and guarded conveyor cell.
2. Hydraulic clamp, pneumatic loader and motorised process.
3. VFD conveyor and proportional hydraulic positioning.

Each package contains a provisional backplate layout, component/function list, I/O schedule, power/control/bonding allocation schedule, coordinated state sequence, hazard/energy discussion, build stages, FAT/recovery matrix and fault-finding exercises. The schedules are internally referenced and illustrate an integrated design package. They are **not construction-ready electrical/fluid drawings, a verified/purchasable BOM, actual equipment pinouts, a complete cell PLC program or a validated protective-function circuit**. Related V2 circuit/PLC buttons open subsystem learning exercises. Develop actual drawings, device selections and software from the requirements.

### Lay out and check the entered plan

- Select a rectangle and edit its function label, X/Y, physical dimensions, depth, reserved clearance, internal DC load and heat loss.
- Drag with mouse/touch or enter numeric X/Y positions. The device selector and View arrows reach parts beyond the visible drawing without requiring a touch-scroll gesture. Selecting without moving does not change the draft revision. The drawing snaps drag positions to a 5 mm planning grid.
- Add generic device rectangles or remove devices. Reference package schedules are not auto-rewired; missing referenced devices are reported for reconciliation.
- Enter available backplate width/height, available depth to obstructions and extra wiring-depth allowance. These are internal planning dimensions, not an automatic external enclosure selection.
- Checks detect overlap of physical/reserved rectangles, boundary overruns and device depth plus the entered wiring allowance. Two reserved areas touching is allowed; overlap is flagged. This conservative uniform-clearance model does not interpret manufacturer-specific directional clearance instructions.
- Default dimensions, losses and clearances are hypothetical. Record the actual datasheet/installation-manual revision/pages and the review of entered values. Changing those values removes their source-review flag. This flag is self-reported, not independently verified.

Colours distinguish functional planning groups (power, control, protective-function allocation, terminals/bonding). They do **not** establish EMC segregation or safety separation. A geometry result is never a conformity decision. Internal DC/heat subtotals exclude unentered external field loads, inrush and unknown losses. Use V2's budgeting tools with actual load/thermal assumptions.

The app does not assess supply fault level, conductor ampacity, protective-device coordination, disconnection times, protective bonding, EMC, IP, thermal performance, complete safety-function architecture or assembly/machine conformity from rectangles.

## South Africa / SANS with IEC context

The default context is South Africa / SANS with IEC. The guide explicitly asks you to establish the relevant legal/contractual requirements, responsibilities, applicability and exact adopted editions.

SANS 10142-1 concerns low-voltage installation wiring in its scope; it is not treated as the sole machinery/panel or functional-safety standard. The scope library includes ISO 12100, IEC 60204-1, scope-dependent IEC 61439, ISO 13849/IEC 62061, ISO 4413/4414, IEC 60529, IEC 61800-5-2, documentation/symbol references and IEC 62443. Use the SABS/IEC/ISO catalogues and the actual licensed applicable documents. **Current editions, SANS adoptions, exact clauses and legal applicability have not been verified here.** The guide provides no copied normative requirements, universal electrical test values or automatic safety-rating calculation.

For each reference, record your applicability decision, exact adopted designation/edition/amendments, the source you checked and the scope rationale/open decisions. The app can count entered/incomplete records, not verify the source, edition or correctness. Official links need Internet only when followed; core learning/design work stays offline.

### Project evidence register and draft changes

Eleven review areas cover scope, risk/safety requirements, protection, bonding, power/thermal/environment, layout, wiring/documentation, control/restart, fluid/mechanical interfaces, verification/validation and handover/recovery.

For each record enter status, responsible author/reviewer and criterion/method/result/document references (or exclusion rationale). Click **Record against current draft** to attribute it to the current draft revision. Records without meaningful evidence and attribution stay open. Editing evidence requires attribution again. Changing plan/spec/device data or risk/standards-basis entries makes earlier review records stale through the draft revision.

These are self-reported evidence records, not authenticated signatures or proof that a test/review occurred. Even if every record is entered, **the app does not approve a panel, determine PLr/PL/SIL/category, validate a safety function, verify an edition or issue a certificate of compliance**. Identify the actual competent/authorised people and obligations for the work.

## Complete-example workflow

1. Record requirements, machine/assembly boundary and utilities.
2. Determine hazards, energy paths and required risk-reduction/protective functions before choosing an architecture.
3. Replace generic parts with verified actual equipment and develop power/control/fluid drawings, protection/thermal basis, terminal/I/O lists and layout.
4. Use the build stages for a controlled assembly/inspection plan under actual device requirements.
5. Prepare suitable authorised verification, FAT/SAT and required safety-function validation plans; do not apply generic tests to connected electronics.
6. Record normal/fault/restart results and as-built changes. A stopped pump, false PLC output or drive status bit does not prove controlled residual energy or machine safety.
7. Reconcile the final design with documentation, settings, software, backups, operating/maintenance information and open-action records.

The hydraulic clamp case deliberately combines pneumatics, hydraulics, electrical equipment and software. Example faults ask for measurements/reasoning, then reveal a comparison explanation. Your answers are saved per package. Loading another package replaces its plan/risk/review records after confirmation while keeping the development portfolio and fault-study notes.

## Engineering development path

Eight self-assessed practice areas build toward a multidisciplinary portfolio:

- Testable customer requirements and acceptance criteria.
- Physical process, force/flow/power and stored-energy reasoning.
- Traceable electrical/panel design package.
- Maintainable PLC software and fault testing.
- HMI, networking, units/data validity and communication-loss behaviour.
- Measured commissioning and FAT/SAT evidence.
- Cybersecurity, lifecycle/change control and tested recovery.
- An integrated capstone defended to an experienced reviewer.

Each area supplies a task, deliverable, prerequisite and stretch exercise. Record a self-assessed level, evidence and reviewer feedback. Next-practice suggestions require level 3+ plus a meaningful evidence description and follow the pathway prerequisites. The app cannot verify that the artefacts or reviewer exist and does not certify competence or guarantee professional standing.

Useful habits: keep requirements measurable; calculate and state assumptions; test failure/recovery paths; measure actual behaviour; use version control and reversible changes; maintain as-built drawings; ask an experienced engineer to challenge the weakest assumption; record what changed and why.

## Saving and reports

Named project saves, draft autosave and JSON exports include the V3 plan, standards records, reviews, notes, fault-study answers and development portfolio along with all earlier project fields. **Download design/review report (.html)** creates a local printable report with the layout, entered data/findings, references, evidence, schedules and test matrix. Open it in a browser and use Print → Save as PDF if needed. The report is not a certificate or verified as-built package. User text is escaped; the exported report contains no scripts.

## Validation

Eight new model tests exercise the three packages/reference consistency, geometry/clearance/depth behaviour, datasheet-source recording, evidence attribution/staleness, standards-record completeness, learning prerequisites and malformed design rejection. Twenty existing model tests remain applicable.

The exact bundled V3 HTML passes offline browser tests that export from the actual V2 app, import into V3, manipulate devices by pointer/numeric input, record data references and review/standards/learning evidence, invalidate old evidence, download an escaped report, restart the browser, recover a V3 backup, reject invalid panel data and check layouts at 360/412/768/1500 pixels. Existing server/mobile workflows also pass.

The managed test browser blocks file:// navigation. Tests fulfil the exact bundled document through an in-memory loopback route with networking disabled; they do not constitute a direct Windows double-click test. No actual panel, CODESYS runtime, normative-standards compliance or safety function has been built/verified by these software tests.
