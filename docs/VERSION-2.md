# Automation Engineering Academy — Version 2.0

## Open and upgrade

Download the Version 2 ZIP from the `standalone-v2.0.0` GitHub tag, extract it, put **Automation-Academy-V2.html** in a permanent folder and double-click it. Use Microsoft Edge or Google Chrome. No Python, VS Code, terminal, server, account registration or installation is required for the standalone edition. The HTML includes its scripts, styles, drawings, lessons and ST reference text. External documentation links require Internet only when followed.

Before switching, open V1 → Projects → Export backup. Open V2 → Projects → Import backup and select that JSON file. V1's HTML and version tag are unchanged. V2 uses its own local browser storage key, so V1 data is not silently overwritten or automatically assumed present. Both use backup schema version 1; V2 adds a `designV2` worksheet and additional PLC inputs. Do not assume the V1 PLC runtime understands new V2 programs; forward migration is the supported workflow.

Keep the file at the same path and use the same browser profile. Clearing browser data, moving the HTML or changing browsers can hide local projects. Export a backup before those actions and future updates. Backup files, not the HTML itself, contain your portable saved projects. Browser-local saving/autosave and the original profile/project features remain available. Runtime outputs are reset when a project reopens.

## What's new

Home has shortcuts for **Cylinder sizing & airflow**, **Complete circuit examples**, and **Panel workshop**. Calculators also links to the new sizing tools. Lessons now has 21 advanced modules plus the five original refreshers. The searchable symbol library contains 36 original vector drawings with explanations of their conventions and limits.

### Cylinder design and air worksheet

1. Build a load case in newtons from moving mass, acceleration, process resistance, guide friction and horizontal/vertical-lift orientation. This simple model is not a linkage, descending-load or impact solver.
2. Enter the loaded motion, design multiplier, minimum drive pressure, opposing chamber pressure, provisional rod diameter and mechanical efficiency. Inspect required force, minimum equivalent bore and a common-bore candidate.
3. Copy the candidate into the air worksheet or enter a catalogue-supported bore/rod combination yourself. A candidate in the app is not a verified Festo/SMC selection. Check real rod availability, stroke, mounting, side loads, buckling, cushioning and dimensional drawings.
4. Enter useful travel and stroke allowance, extend/retract times, cycles per minute, gauge/ambient/reference pressures, chamber/reference temperatures, fixed dead volume vented/recharged per cycle and reserve.
5. Compare reference litres/cycle, average reference demand, average plus reserve and travel-time displacement demand. The app flags cycle rates incompatible with the specified travel times. Actual swept-volume flow is separately displayed.
6. Tube-ID estimation uses actual local L/min and a chosen velocity. It is a velocity screen only. It does not solve compressible pressure loss, valve sonic conductance, fitting losses or initial charging.

Pressure reference and kelvin conversion are explicit. Swept volume uses the absolute-pressure ratio. Fixed dead volume is assumed vented to ambient between charges at the same chamber temperature, so its incremental consumption uses gauge-pressure/reference-absolute-pressure × temperature ratio. The result is **reference L/min at the stated conditions**, not an unspecified normal-flow rating. Do not enter reference L/min into the actual-flow tube calculator. Stroke is travel plus allowance, not an estimate of a manufacturer's installed cylinder length.

### Complete worked circuits

Four functional examples include schematic, component/function list, port/I/O mapping, operating sequence and fault discussion:

- Monostable electropneumatic hold-to-extend, with work lines deliberately mapped 4→cap and 2→rod so Y1 energised extends. Meter-out/check paths and signal links are shown.
- Dual-solenoid automatic extend/retract with endpoint feedback, pressure permissive, independent timers and fault reset. The matching 15-rung program loads into the PLC lab.
- Fixed-pump hydraulic power unit, pressure gauge/relief path, 4/3 closed-centre valve, cylinder and return filter. Closed-centre relief heating is an explicit analysis problem, not a finished energy-efficient design.
- Three-phase motor starter power circuit and separate 24 V hardwired seal-in control circuit.

These are complete **functional examples**, not construction-ready CAD packages or a general multi-domain simulator. Some system functions, such as upstream pneumatic isolation/exhaust and the PLC control interface, remain functional callouts requiring device-specific detail. Hydraulic load holding, component ratings, electrical protection, wiring terminals and safety functions need engineering beyond the reference drawing. The original animated pneumatic core remains available and keeps its original port mapping (2→cap, 4→rod; OFF extends, ON retracts); do not confuse it with the separately labelled worked examples.

### PLC / CODESYS examples

The program selector loads delayed motor start, rising-edge pulse, timed forward/reverse commands, electropneumatic hold command or a two-sensor cylinder cycle. It confirms before replacing current rungs and resetting runtime. Each example explains inputs, expected trace and a fault/review exercise.

Additional simulated inputs are Reset, Extended, Retracted, PressureOK, PartPresent and Reverse. Existing three-input projects remain supported. The browser still executes only supported Boolean instructions, COIL/SET/RESET and TON, not arbitrary ST. The reversing example's neutral timer is a teaching value, not proof of motor stopping. Real hardware needs an engineered zero-speed/reversal design and appropriate interlocks.

Full ST references for analogue scaling and CASE sequencing can be read/downloaded offline. They are for a standard CODESYS PROGRAM POU with standard TON/R_TRIG library resolution, cyclic-task configuration and separately designed I/O mapping. They have not been compiled in CODESYS here. Ordinary PLC permissives are not safety-rated functions. The automatic example uses edge-triggered start and reset; a held reset must not repeatedly clear a fault when home feedback returns.

### Hydraulic flow from speed

Calculators also estimates supply and opposite-chamber return flow from bore, rod, target speed and direction. Q = Av gives ideal incompressible displacement flow; retraction return can exceed supply. Allow for leakage, transients, fluid viscosity and real pressure-drop curves.

### Panel workshop

- Build a DC steady-load budget from controller power, I/O current, sensor current, simultaneously energised coils and auxiliary power. Reserve is explicit; inrush, pickup, foldback, group limits, voltage drop and protection coordination still need checking.
- Enter internal dissipated heat separately. The ideal air-exchange estimate assumes 1.2 kg/m³ air density and 1005 J/(kg·K). It omits enclosure heat transfer, filter losses and real fan curves. Ventilation cannot cool below incoming ambient temperature.
- Try a uniform-module space check using available backplate dimensions, edge/duct/row allowances, module dimensions and count. It reserves 10 mm extra pitch and 50 mm depth as declared planning assumptions, not mandated clearances. It also reports provisional minimum row height/depth and one-column width under those assumptions. A FIT result checks that simplified geometry only.
- Follow the design-basis, drawings, zoning, selection, assembly and verification guidance. Record review steps and notes, then download a text worksheet if useful.

No breaker, mains conductor size, enclosure certification, protective bonding verification or safety category is inferred from a single calculated current. These depend on the actual supply/fault level, environment, installation, equipment and applicable requirements such as IEC 60204-1/IEC 61439 and local standards.

## Saving

The existing named-project save and autosave include V2 sizing inputs, notes, selected circuit/reference, panel checks, PLC program and inputs. Export backup includes the current workspace even before an explicit named save. Downloads for the design worksheet and ST examples are also offline. The original Python/Android server edition remains available for existing accounts; this standalone edition uses a local display-name profile.

## Verification and limits

20 deterministic model tests cover existing functions and new sizing/flow/panel calculations, the five PLC examples, sensor sequence, timeout and reset behaviour. Offline browser tests export from the actual V1 bundle, import into V2, run the cylinder sequence, exercise reports and ST downloads, restart the browser, restore V2 backups and check layouts at 360/412/768/1280 pixels. The existing server-app regression still passes.

As with V1, the managed test browser blocks file:// navigation. Tests load the exact single-HTML bytes through an in-memory loopback route with networking disabled; they do not constitute a physical Windows double-click test. No CODESYS runtime/compiler, actual machine or certified fluid-power solver has been used. Symbol drawings use conventional/educational notation and are not a certified standards library.


The current source builder now emits V3. This V2 HTML is preserved unchanged; use the standalone-v2.0.0 tag for its historical source/generator. See VERSION-3.md for the optional V3 upgrade.
