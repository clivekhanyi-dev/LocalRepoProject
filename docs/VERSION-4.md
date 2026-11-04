# Automation Engineering Academy — Version 4.0

## Open the app

1. Download https://github.com/clivekhanyi-dev/LocalRepoProject/archive/refs/tags/standalone-v4.0.0.zip .
2. In Windows, right-click the ZIP → Extract All.
3. Open the extracted folder and double-click **Automation-Academy-V4.html** using Chrome or Edge. No VS Code, Python, terminal or installation is needed.

Before upgrading, open your old version → Projects → Export backup. In V4 → Projects → Import backup, select that JSON file. Previous HTML versions are preserved. Keep V4 in one permanent folder; browser/profile changes, file moves or clearing browser data can affect local storage. Export JSON backups regularly. The HTML contains the app, not your saved projects. Accounts remain local profiles in the standalone edition; the server edition retains server accounts.

## Build a circuit

1. On Home choose **Build circuit**.
2. Choose a starter, or start blank. Seven starters cover basic and prepared air, spring return, two cylinders, hydraulics, relay control and electropneumatics.
3. Search the toolbox or filter its categories. Click to add a part, then drag it into place. There are 48 component kinds across fluid power, electrical and PLC/sensing.
4. Click one connection dot and a matching dot on another part. Large connection buttons provide the same action without needing to hit a tiny dot. Lines route automatically.
5. Select a part to label, rotate, duplicate or remove it. Undo/Redo fixes mistakes. Cancel connection clears an unfinished link. Zoom and view arrows reach other areas; selecting a part brings it into view.
6. Check the drawing. Supported ideal-air circuits offer Run/Step; select a valve to operate that valve. Hydraulic, electrical and mixed circuits are drawing-only and say so.
7. Save through Projects. Export SVG produces a viewing/printing copy; export JSON backup preserves editable project data.

Pneumatic animation traces simplified pressure and exhaust paths. It does not calculate real pressures, timing, friction, flow or dynamics. Components use original conventional schematic drawings, not a certified or exhaustive standards symbol library.

## Assemble a panel on screen

1. Choose **Build panel** from Home. Start with a reference panel or blank backplate.
2. Add illustrated devices from the searchable toolbox: supplies, switching/protection, PLC, drive, HMI, terminals, bonding, valve bank and sensor hub are among 14 generic types.
3. Drag parts onto planning rows, rotate or duplicate them, and connect compatible functional dots using the large terminal buttons. Undo/Redo restores placement and wiring edits.
4. Name and save the project. Use **More options** for exact geometry, device information and the existing SANS/IEC review workflow. Layout edits advance the revision so earlier review evidence becomes stale.
5. Export the panel SVG or a report when you want a reference to study or print.

These are virtual assembly exercises. The device fronts and connection dots describe functions, not actual manufacturer pinouts, terminal counts or connection instructions. Optional example power links show functional distribution only: they do not design phase/pole wiring, protective devices or safety circuits. Real construction requires verified datasheets, coordinated protection and wiring drawings, applicable South African/SANS/IEC requirements and competent review. No conformity, safety rating or construction approval is generated.

All earlier lessons, calculations, PLC examples, comparisons, notes, projects, advanced panel planning and engineering development exercises remain available.

## Verified and remaining limits

36 model tests and the Python account/project integration test pass. The exact bundled HTML passes offline Chromium checks for actual V3 backup migration, starter circuits, component placement/rotation, independent valve operation, functional panel connections, Undo/Redo, SVG downloads, advanced-view synchronization, save/reopen, backup rejection and responsive widths 360/412/768/1600. The existing server/mobile regression also passes.

Managed Chromium blocks file URLs in this cloud workspace, so browser tests fulfill a loopback URL with the exact HTML bytes from memory while offline. A Windows double-click and physical Samsung operation have not been verified here. No real equipment, CODESYS compilation, normative standard edition/adoption or safety function has been tested.
