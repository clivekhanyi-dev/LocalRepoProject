# Automation Engineering Academy

**Version 4: open `Automation-Academy-V4.html` directly in Chrome or Edge.** This is the single-file offline desktop edition; no Python or VS Code is needed. See [Version 4 instructions](docs/VERSION-4.md) for saving, backups and transferring existing projects. Server/Android instructions below still apply to the original hosted edition.


An automation learning workspace spanning pneumatics, hydraulics, electrical engineering and CODESYS / IEC 61131-3 programming. Existing accounts, projects, product comparisons and notes remain compatible. Independent of manufacturers.

## Run locally

Requires Python 3.12+; no third-party runtime dependencies or paid APIs.

```sh
cd /workspace/LocalRepoProject
python3 server.py
```

Open the application on port 8000 through your hosting provider's supported route. Create an account with a password of at least 12 characters. Accounts and saved projects use SQLite (`academy.sqlite3`, ignored by Git). Guest users can explore; saving requires sign-in. Projects include circuit topology, notes, lesson completion, entered product evidence and calculator inputs. Saving an existing name replaces that account's project with the same name.

## First workflow

The example connects supply → valve 1, valve 2 → cylinder cap end, and valve 4 → rod end. Ports 3 and 5 exhaust to atmosphere. Run or step to extend; energise Y1 to retract. Click a hose to remove it, then click two ports to reconnect. Drag component bodies to reposition. The V4 studio also offers seven starters and broader ideal-air connectivity; hydraulic and electrical drawings do not run a physical simulator.

The simulator is a discrete state teaching model, not a sizing or fluid-dynamics tool. Its motion speed is illustrative. The studio and symbol library use original vector drawings following conventional fluid-power notation. They are not a certified ISO/IEC symbol library. The calculator displays ideal force; friction and exhaust back pressure reduce available force.

The product workbench accepts UTF-8 text excerpts and manual specification entry. It does not parse PDFs, decode manufacturer codes or retrieve catalogues. Source references are entered by the user, not independently verified. Comparison checks text agreement and missing fields; it cannot establish interchangeability. The circuit coach uses authored guidance, not a generative AI model. A separate PLC teaching lab now supports editable boolean rungs and TON; full PLC/runtime emulation, broader fluid-power circuit simulation and a verified catalogue remain future work.

## Validate

```sh
python3 -m unittest discover -s tests -v
node --test tests/model.test.cjs
```

Node 18+ is needed only for the model tests. Integration tests use a temporary database and verify registration, login, account isolation, project round trips, logout and HTML serving.

## Remote deployment

Use a Python-capable VM or container host with persistent disk. Hosting may cost money; no hosting account is provisioned by this repository.

1. Put this checkout on the host and mount persistent storage for SQLite.
2. Run `HOST=0.0.0.0 PORT=8000 ACADEMY_DB=/data/academy.sqlite3 ACADEMY_SECURE_COOKIE=1 python3 server.py` under a process supervisor.
3. Terminate HTTPS at a reverse proxy, preserve the original Host header, and forward traffic to port 8000. Expose only HTTPS publicly. Configure request limits and login rate limiting at that proxy before public access; the standard-library server is a small pilot backend, not a hardened production gateway.
4. Back up the database using SQLite's backup API and protect the disk and backups. Session cookies expire after 24 hours. Account recovery, email verification and MFA are not implemented.
5. Verify registration, save/reload, and account isolation through the deployed HTTPS address. The current development instance does not establish public hosting.

Set `ACADEMY_SECURE_COOKIE=1` only when accessed through HTTPS; local HTTP uses the default. The server defaults to loopback. Do not commit the database or credentials. No real-machine control is included.

## Android on Windows / Samsung

The existing frontend now has a responsive mobile dashboard with Lessons, Calculators, Products, Projects and Profile navigation; Circuit Studio remains accessible from Home. A native Android WebView client is in `android/`. It connects to this same Python backend, preserving same-origin authentication and server-side storage. Python does not run inside the APK.

See [the complete Windows build, USB installation and remote-hosting guide](docs/ANDROID-WINDOWS.md). For the first phone installation, run Python on Windows and use `adb reverse tcp:8000 tcp:8000`; set the debug app's server address to `http://localhost:8000`. Away from the laptop, configure an HTTPS-hosted backend. No public deployment has been created automatically.

Optional mobile end-to-end test: install Playwright in your test environment and run `python3 tests/mobile_smoke.py` with Chromium available at `/usr/bin/chromium` (Linux test environment). The test uses a temporary database and does not touch real accounts.


## Advanced automation workspace

Home opens the **CODESYS / PLC lab**, **Engineering symbols**, and **Advanced learning tracks**. Lessons can be filtered by Pneumatics, Hydraulics, Electrical, PLC / CODESYS and Integration. Twenty-one advanced modules include worked engineering challenges, saved reasoning and a commissioning notebook. Five original refresher lessons remain available in the foundation section; existing numeric completion IDs are unchanged. New module progress uses stable string IDs.

The editable ladder lab supports AND/OR/NOT, ordinary coils, SET/RESET and TON with a scan trace. Edit rungs and compile before scanning. Tags are validated; no user code is executed through JavaScript eval. Input sampling and sequential assignments are modelled explicitly. A TON begins at ET=0 on its first TRUE call, resets when false, and finishes at the first simulated scan at/after PT. The lab advances deterministic virtual time, not real hardware timing. The three inputs are Start, StopHealthy and OverloadHealthy; other tags are internal outputs or TON instance `.Q` fields. SET/RESET multiple writers demonstrate scan order; ordinary duplicate coil writers are rejected.

Generated Structured Text and `web/examples/AutomationCell.st` are CODESYS learning examples, not certified/import-ready projects. Paste declarations and implementation into a new POU, resolve standard TON/R_TRIG libraries, configure the task, and test with simulation before any physical mapping. CODESYS compilation and device execution have not been performed here. Ordinary PLC permissives are not safety-rated functions.

Calculators now include hydraulic force/speed/power and balanced three-phase motor current, with displayed formulas, units and assumptions. The symbol reference covers directional valves, fluid-power cylinders/pumps/motors, restrictions/check valves, relay/contact logic, motor and protective earth. It distinguishes physical contacts from PLC Boolean instructions. Drawings use conventional ISO 1219/IEC-style notation without claiming certification or covering every standard variant.

Advanced lesson answers, notes, calculator inputs, PLC program, input selections and scan interval are included in the existing project save. Runtime coils/timer elapsed values are deliberately reset on load. Nothing is written to the server until you save a project. Broad hydraulics/electrical network simulation, full ST execution and a complete manufacturer catalogue are not implemented.

Run additional model tests with `node tests/automation.test.cjs`. The mobile smoke test also exercises PLC timer/stop/compiler behaviour, technical symbols, new calculators and advanced project persistence.

For existing Windows ZIP installations: download the updated `android-mobile-app` branch and copy its `web` folder into the project that actually contains `server.py`. Preserve your `academy.sqlite3` and existing project files. Refresh the browser with Ctrl+F5; no database migration or pip installation is required. The Android WebView receives these frontend updates from whichever backend it is configured to use; no native wrapper update is needed for these features.


## Version 2 engineering workbenches

V2 extends the single-file V1 app with cylinder/load/bore/stroke and air-flow worksheets, tube-ID screening, a DC panel/thermal budget and uniform-module layout tool, 36 symbols, four worked functional circuits, five runnable PLC examples, additional simulated inputs and two full CODESYS ST references. See [Version 2 guide](docs/VERSION-2.md) for assumptions and limitations. V1 HTML is preserved unchanged; export a V1 backup and import it into V2.

`python3 tools/build_standalone.py` builds the current V4 HTML. The historical V1 generator/source is retained by the standalone-v1.0.0 tag. Run `node tests/design.test.cjs` for the ten new model/example tests and `python3 tests/version2_smoke.py` for the offline migration/workbench regression.


## Version 3 integrated panel / engineering pathway

The historical V3 release contains `Automation-Academy-V3.html`. V1/V2 files and tags remain unchanged. V3 adds a draggable entered-geometry panel planner, three integrated reference packages (pneumatic conveyor, hydraulic clamp/pneumatic loader, VFD/proportional axis), South Africa/SANS-with-IEC scope and source records, revision-attributed review evidence, printable reports and an eight-part practical engineering portfolio path.

These are learning/preliminary-design tools and self-reported evidence inventories, not standards verification, actual device pinouts, validated protective-function wiring, construction approval or certification. Current editions/adoptions must be checked against the applicable sources. See [V3 guide](docs/VERSION-3.md).

Additional checks: `node tests/panel.test.cjs` and `python3 tests/version3_smoke.py`. The browser regression includes actual V2 backup migration and preserves all earlier project fields.


## Version 4 easy circuit and panel building

Home opens **Build circuit** and **Build panel**. The searchable studio offers 48 component kinds across pneumatics, hydraulics, electrical and PLC/sensing, seven starter circuits, orthogonal connection routing, rotation, duplication, Undo/Redo and SVG export. Four starters support ideal pneumatic animation; three are explicitly drawing-only. The illustrated panel builder offers 14 generic device types, row snapping, functional connection dots/buttons, zoom, templates and project saving. Detailed V3 settings and SANS/IEC review remain available under More options.

See [V4 opening, backup and build instructions](docs/VERSION-4.md). V1/V2/V3 HTML files remain unchanged; their tagged sources retain their respective builders. Run `node --test tests/*.test.cjs` and `python3 tests/version4_smoke.py` for model and offline UI checks.
