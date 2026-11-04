# Automation Engineering Academy — Version 6.0

## Open and upgrade

Download https://github.com/clivekhanyi-dev/LocalRepoProject/archive/refs/tags/standalone-v6.0.0.zip . In Windows, right-click → Extract All, open the extracted folder and double-click **Automation-Academy-V6.html** in Chrome or Edge. The ZIP contains only V6 HTML, with no previous versions or source folders. No VS Code, Python, installation or server is needed.

Open V5 → Projects → Export backup. Open V6 → Projects → Import backup, and select that JSON. The versions have separate local browser storage; V6 does not automatically read projects from another file. Keep the HTML in a permanent folder and export backups regularly. Browser/profile changes, file moves, private browsing and clearing browser data can remove access to local storage. Runtime power, outputs, active diagnostic case and motion progress reset on reopen.

Home retains all earlier tools. **V6 practical training workshop** opens six choices: wiring/meter practice, motion, terminal configuration, site survey, complete engineering projects and manufacturer evidence.

## Wiring challenges

1. Open Guided wiring & simulation, choose one of the three example panels, and expand **V6 · Wiring challenges and diagnostic cases**.
2. Click **Start a challenge from unwired**. Use terminal dropdowns/dots, the component explanations and the guided connection button as needed.
3. Click **Test my wiring**. Checks run a separate deterministic training attempt without changing your displayed power state: no pre-Start energisation, Start response, release/sequence behaviour, ordinary Stop, supply loss and required paths.
4. Read each failed check for a useful next step. Undo/Redo fixes mistakes. Editing the wiring invalidates the displayed result; run the checks again.

A pass is a named-model training result, not circuit safety approval, certification or a general electrical validation. Learning records are historical attempts and should be rerun after changes. The ordinary Stop is not a safety-rated function. The PLC feedback remains virtual. Exit diagnostic mode before grading wiring.

## Virtual multimeter

Expand **V6 · Virtual multimeter**. Select DC voltage, resistance or continuity, choose red/black terminal probes and click **Take & record a measurement**. Readings are sampled, not a continuously refreshed display. They use the actual current wires and contact states; the log records terminal names and supply state.

- Voltage is red minus black, so swapping probes reverses the sign. An unreferenced node reads Floating/indeterminate. Ideal wires/closed contacts have zero voltage drop.
- Switch simulated power OFF before resistance/continuity; the app blocks these modes when power is ON. On real equipment isolate, prove dead and discharge stored energy using appropriate competent procedures and rated equipment.
- The teaching solenoid has 240 Ω, and relay K has 480 Ω. In-circuit parallel paths affect readings: the relay example can show 160 Ω across the shared command loads rather than an isolated 240 Ω coil. These values are assumed, not manufacturer data. Continuity beeps below 30 Ω; a healthy 240 Ω coil is not a short.
- PLC PNP outputs source +24 V only with a powered/healthy controller and command in this model. Off outputs, internal electronics, leakage, suppression, contact resistance, measurement impedance and actual supply internals are simplified. For DC voltage the disabled ideal supply is clamped to zero; for resistance its internal source is excluded. No mains or current-range measurements are simulated.

A missing return can leave both coil terminals near +24 V relative to 0 V through the coil resistance, while the voltage across the coil is zero. This is why a single voltage reading cannot establish that the load has a complete circuit.

## Diagnostic cases

Load a case, read the symptom, then operate Start and take appropriate measurements. The four cases cover missing coil return, open branch fuse, open coil and missing pneumatic supply. The fuse's explicit fault label is hidden during the exercise. Use the hint when needed. Record at least one meter observation, choose a diagnosis and check it. Correct answers are authored teaching cases, not automated real-machine diagnosis. **Return to normal trainer** clears injected faults and reloads the selected example. Case loading replaces the current training wiring, so save a workspace/backup first if it must be kept.

## Load and flow motion experiment

The separate motion lab responds to bore/rod/stroke, opposing external load and friction, supply/back pressure, actual tube ID/length, valve reference flow/test pressure drop and opening fraction. The worked example is a guided horizontal 50/20 × 200 mm cylinder at 6 bar, 500 N opposing load and 30 N friction. Try a smaller opening, longer/narrower tube, retract stroke, full closure or overload. Closed flow control or insufficient force stalls the preview.

The estimate balances a constant opposing load against chamber pressure, then solves approximate series tube/valve loss for reference flow and displacement speed. Air assumptions: 20 °C, 1 bar absolute reference, isothermal tube loss with friction and K=3. Valve loss scales with entered test Δp × (flow / rated flow / opening)² under assumed matching inlet conditions. This is an empirical quasi-steady experiment, not ISO 6358 modelling or a validated compressible transient simulator. Large pressure ratios/high speeds are flagged; choked flow can invalidate time estimates. Chamber filling, acceleration, leakage, gravity, cushions and exhaust dynamics are excluded. It compares trends and does not determine a safe installed design. Settings do not change the existing fixed-speed wiring trainer.

## Configure a valve terminal

Apply a station count from one to eight, then choose each station's load label, 5/2 spring, 3/2 NC, 5/3 or spare function and zone 1/2. Export the functional tubing/output schedule. A 5/3 allocation uses two output channels and explicitly leaves centre function to be specified. A spare needs correct gallery sealing. Distinct zone numbers are planning intentions: actual supply/exhaust separation and appropriate plates must be verified. The total steady current screen conservatively sums all allocated coils; 5/3 opposing coils must not energise together, and actual simultaneity, inrush, group limits and interlocking require design.

Output labels Q0… are planning labels, not connector pins or verified fieldbus mapping. Actual voltage/common polarity, pilot supply, manual overrides, exhaust and manufacturer drawings remain necessary. Custom schedules are not automatically converted to a runnable circuit. A button opens the existing fixed two-station 5/2 simulation for comparison.

## Site survey and photos

Record the site/equipment tag, survey date/reviewer, nameplate, unknown dimensions and isolation/environment observations. The existing cylinder worksheet still distinguishes confirmed bore from outside barrel measurements; it calculates stroke and preliminary forces and exports an enquiry.

Attach up to three JPEG/PNG/WebP photos, each source no larger than 8 MB. The browser resizes them locally to at most 1000 pixels on the longest edge and compresses to JPEG; each stored image is capped at 180,000 data-URL characters. Keep original images separately, especially for fine nameplate detail. No catalogue service receives the images. They are stored in the project and portable JSON backup. Multiple photo-heavy projects can exhaust browser storage; export backups if autosave reports a quota problem.

Download an illustrated HTML site report for viewing/printing. It includes existing cylinder enquiry fields and embeds the photos without external files; user-entered text is escaped. This report is a reference copy, not an editable backup. Use Projects → Export backup for editable records/photos.

## Engineering projects and manufacturer evidence

Three briefs combine requirements, sizing, schematics/control interpretation, testing and self-reported evidence: product reject station, relay pneumatic fixture and two-cylinder indexing unit. Each links to its named running control subsystem. Write expected and observed results, hazards, energy/restart concerns and outstanding requirements; export the portfolio. These are learning packages, not complete construction-ready machine designs or protective-function circuits. Earlier SANS/IEC review and CODESYS examples remain available.

The Festo/SMC evidence register records exact model/revision, official datasheet source/page, reviewer/date, ratings/test conditions and outstanding differences. The completeness button counts empty record fields. It does not retrieve or independently verify datasheets, establish current catalogue validity or approve substitution. No new verified product database is claimed. Use the existing comparison tool with actual evidence.

## Validation

51 model cases and the temporary-database account/project integration test pass. Exact offline V5→V6 browser tests cover real challenge editing/grading/stale results, voltage/ohms interlock, all four diagnostic cases, motion/closed valve/stall/retract behaviour, terminal functions/zones, photo upload/resize/report rendering, escaped text, learning/source records, restart, JSON recovery/rejection and 360/412/768/1600 layouts. Existing server/mobile regression passes. No JavaScript page errors or external runtime resources were observed.

Managed Chromium blocks file URLs, so these tests fulfill a loopback URL with the exact bundled HTML bytes while offline. Windows double-click and physical Samsung operation remain unverified here. No real equipment, standards editions, protective function, manufacturer pinout or CODESYS compilation is validated.
