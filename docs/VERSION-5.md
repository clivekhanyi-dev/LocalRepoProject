# Automation Engineering Academy — Version 5.0

## Open and transfer your work

Download https://github.com/clivekhanyi-dev/LocalRepoProject/archive/refs/tags/standalone-v5.0.0.zip . Extract All in Windows, open the extracted folder and double-click **Automation-Academy-V5.html** in Chrome or Edge. This distribution contains only the V5 HTML. No Python, VS Code, server or installation is needed. The standalone file has no external runtime dependencies.

Before upgrading: open V4 → Projects → Export backup. In V5 → Projects → Import backup, select that JSON. Previous releases remain available in the repository but are not in the V5 distribution. V5 uses separate browser storage; it does not automatically read another file's local projects. Keep the HTML in a permanent folder and export JSON backups regularly. Browser/profile changes, file moves, private mode or clearing browser data can remove access to local data.

## Start with a completely wired panel

1. Home → **Guided wiring & simulation**.
2. Choose the hold-to-run, relay seal-in or PLC/two-station terminal example. Click **Open fully wired example**.
3. Use **Trace one wire** to highlight a connection and read its purpose. Select a component to learn what its terminals do. Expand **Connection schedule** for every wire explanation.
4. Switch **24 V supply ON**, leave **Air supply ON**, then select **Hold Start**. Click **Run simulation** to animate; **Step 100 ms** advances deterministic simulated time. Uncheck Start to release the button.
5. In the direct example, releasing Start drops the coil. In the relay example, the wired K auxiliary contact holds K until Stop is pressed. In the PLC example, a fresh Start edge commands A+ → B+ → B− → A−.
6. The ordinary Stop clears PLC outputs. Release Start before Reset or a new start. A state that cannot reach its virtual end feedback within ten simulated seconds faults and drops outputs.
7. Practise fault finding with an open fuse/coil, Air OFF or a removed return wire. Pause to inspect. Changing wiring resets power/runtime; it never automatically starts equipment.

The Run button is paused when leaving the guided screen; its supply/commands reset. Coil states, relay latch, faults and motion positions are not saved. Wires, notes and worksheets are saved with the project and autosaved in the offline edition. Use **Save this workspace** to open Projects, then name/save or export a portable backup.

## Wire it yourself

Choose **Practise from unwired**, then **Add the next guided connection**. The coach explains each connection. Alternatively select two terminals using the large dropdowns or click their dots. Undo/Redo restores wiring; the connection schedule lets you remove individual wires. Fit view shows the whole plan; Large view allows scrolling to larger dots. Crossing lines do not mean an electrical junction.

This is a named-model ideal-contact DC trainer, not a general electrical solver. It checks terminal existence, polarity, duplicate links and direct source/output conflicts; a connected schedule is not a safe-design verdict. Custom bypasses can change behaviour. It does not calculate coil transients, contact welding, resistance, voltage drop, actual fault current, protective-device coordination, conductor sizing or equipment ratings. The Stop is ordinary control, not an emergency-stop or protective function. The supply's mains input is outside the model.

The pneumatic terminal uses shared prepared-air port 1 and exhausts 3/5. Each station has cap-side 4/A and rod-side 2/B tubing. The chosen trainer spool retracts OFF and extends ON; other actual spool/rest functions differ. Y1/Y2 refer to separate 24 V DC coils, with generic A1/A2 terminal names. Real multi-pin or fieldbus terminals need their actual connector mapping, load-supply groups, commons, module limits and manufacturer data. Virtual PLC end sensors are derived from cylinder position; physical sensor wiring is explained conceptually but not simulated. Air OFF holds position in this ideal model; real loads can drift or move. Motion is fixed-speed and does not use the sizing worksheet.

Pneumatic and hydraulic valve terminals are also selectable in the general Circuit Builder. Hydraulic terminals are drawing-only; V5's new runnable circuits focus on pneumatics and DC electrical control. Circuit Builder has 55 component kinds and the symbol reference adds ten original schematic/functional drawings. These are conventional educational drawings, not a certified standards symbol library.

## Measure a cylinder for a customer

Home → **Measure a cylinder / size tubing**. The worked example uses a 50 mm bore, 20 mm rod and 200 mm stroke. Record both readings from the same datums; stroke is the fully extended reading minus the fully retracted reading. Measurements must come from safely isolated, depressurised equipment with stored energy controlled. Do not move live machinery to obtain readings.

Bore remains UNKNOWN unless confirmed from a drawing/nameplate or safe internal measurement. Outside barrel diameter is recorded separately and never converted into bore. Enter mount/pin sizes, rod-end and port threads, cushioning/load/speed, sensor, environmental and existing-code references. Available-force estimates include entered opposing back pressure and efficiency; they do not establish a rated allowable load or interchangeability. Download the text site enquiry with measurements and unknowns for supplier review.

## Tubing and solenoid selection

Copy confirmed measurements into the tubing worksheet or enter dimensions directly. Enter travel time, simultaneous cylinders, developed tube length and your velocity/loss limits. The screen converts swept displacement flow using absolute pressure and explicit reference temperature/pressure. Retraction demand is shown at the same speed. Example OD/ID pairs are illustrative: real tubing walls vary.

Approximate line loss uses isothermal ideal air: p₁² − p₂² = (fL/D + K) ṁ²RT/A², SI units, estimated viscosity/friction and small commercial-tube roughness. This is steady, unchoked screening. Large drops, high speeds, actual fittings, branch distribution, valve/pilot/exhaust characteristics, transient cylinder demand, dead volumes and leakage require supplier curves or detailed engineering. The smallest listed size within entered screens is not a guaranteed installed selection.

The valve worksheet compares entered shared-supply flow against demand with your allowance, conditional on matching reference/test conditions. It also reports individual/total steady DC coil current and flags a voltage mismatch with the 24 V trainer. Published per-channel limits, group limits, inrush, suppression, duty, pilot pressure, IP/environment and spool function must all be verified. Example flow/current values are unverified training assumptions. Record a datasheet reference; it is not fetched or independently verified. The 3/2 or 5/3 selection does not automatically redesign the 5/2 simulation.

## Validation and remaining checks

44 JavaScript model tests and the temporary-database Python integration test pass. Exact bundled offline Chromium tests cover V4 migration, wire/dot/selector editing, tracing/history, direct/relay/PLC operation, missing-wire and air timeout behaviour, measurement/flow/RFQ downloads, new terminal parts, persistence/restart, malformed backup rejection, and layouts at 360/412/768/1600 pixels. The existing server/mobile regression passes. No external runtime resources or JavaScript page errors were observed.

Managed Chromium blocks file URLs, so these browser tests fulfill a loopback URL with the exact bundled HTML bytes while offline. Windows double-click and physical Samsung operation remain unverified. No physical hardware, actual manufacturer pinouts, standards editions, CODESYS compilation or safety function is validated. Existing SANS/IEC evidence review remains available.
