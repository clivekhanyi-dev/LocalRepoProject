# Android conversion validation

The existing Python server and data schema are retained. No user database was reset or included in downloadable source archives.

Verified in this cloud workspace:

- Five JavaScript model tests: valid/disconnected/reversed circuits, ideal force calculation and invalid dimensions, valve movement direction/bounds, incomplete evidence and product function conflicts.
- Python HTTP integration test: registration, sign-in, logout, account isolation, project persistence round trip, and HTML serving, using a temporary database.
- Chromium mobile browser end-to-end check: dashboard/navigation, PLC lesson availability, lesson completion, notes, calculator changes, text datasheet upload, comparison missing-evidence feedback, registration, save/reload, cylinder coil state and restoration of saved notes/product excerpt/calculator inputs. No JavaScript page errors. Page overflow checked at widths 360, 412, 768 and 1280 pixels.
- Android debug APK built with the included Gradle 8.11.1 wrapper, Android Gradle Plugin 8.9.2, SDK 35 and a complete JDK 21. Min Android API 26, target API 35, package `com.pneumatic.academy`.
- Android lint: no errors. JavaScript-enabled WebView warning is expected and retained: the existing simulator needs JavaScript. The wrapper exposes no JavaScript/native bridge, restricts navigation to the selected origin, and uses default TLS verification. Only connect to a backend you trust.
- APK signature verified using Android SDK `apksigner`; package metadata checked using `aapt`.

A compiler note flags compatibility APIs deprecated on newer Android versions. The installed command-line SDK metadata is newer than the pinned Android Gradle Plugin's metadata parser; it prints an SDK XML version warning but the APK compiles successfully. These are distinct from application runtime failures.

Not verified here: installation or execution on a physical Samsung, Android document picker behaviour on that device, native lifecycle/keyboard/insets on that device, USB forwarding from the user's Windows laptop, public HTTPS hosting, or Google Play release. Follow the phone checklist in ANDROID-WINDOWS.md. This is a network-dependent client; unsaved edits are not durable offline. The existing pilot backend still needs public-hosting hardening and operational configuration before broad deployment.


## Advanced automation update

Five additional model tests verify boolean precedence and rejection, unknown tags, seal-in/dropout, TON timing/reset, sequential scan behaviour, SET/RESET ordering and hydraulic/electrical units. The expanded mobile end-to-end test verifies advanced module answers/progress/notebook, uploaded text evidence and old notes across project save/load, editable PLC presets, timer completion, stop dropout, compiler diagnostics, symbols and the new calculators. Responsive views include the PLC lab and symbols at 360/412/768/1280 pixels. Python account/project integration remains passing. The title expectation changed to Automation Engineering Academy.

CODESYS compilation, full ST execution, general hydraulic/electrical circuit simulation and certification of the authored symbols have not been performed or claimed. Existing Android native packaging is unchanged by this web update.


## Version 1 standalone HTML

The existing frontend is bundled with inline styles/scripts and the ST example as a data URL. Only this generated edition injects a browser-local store; the original backend authentication is retained for server clients. The exact HTML passes offline Chromium tests for local profile/project persistence, autosave, browser restart, JSON backup recovery/rejection, unfinished PLC drafts and export when browser storage is blocked. The managed browser blocks file:// navigation; these tests use a loopback URL fulfilled with the bundled bytes from memory and do not establish a real Windows double-click test. See VERSION-1.md for that limitation and browser-storage behaviour. The server-app regression also passes after adding shared backup support.


## Version 2

Ten additional model tests cover directional bore sizing with pressure/efficiency/margin, absolute-pressure/temperature air conversion, travel-time consistency, tube-ID units, DC/thermal budgeting, uniform-module layout, all five supplied PLC examples, a complete two-sensor sequence, timeout and edge-reset recovery, reversing neutral time and load/gravity/return-flow calculations. Together with the existing ten tests, 20 model tests pass.

The exact V2 HTML passes offline browser tests for actual V1 backup migration, sizing/air/panel inputs and notes, 36 symbols, four functional diagrams, the 15-rung cylinder example, text/ST downloads, process restart, backup recovery and 360/412/768/1280 layouts. Existing server/mobile regression remains passing. The V1 HTML is unchanged. File URL policy, CODESYS execution, physical equipment, catalogue selection and symbol-certification limitations remain as documented in VERSION-2.md.


## Version 3

Eight new panel-model tests cover integrated template references/geometry, entered keep-outs, depth/source assumptions, revision-bound evidence and non-applicability inventory, standards-record completeness, learning prerequisites and malformed import rejection. Twenty earlier model tests remain passing.

The exact V3 bundle passes offline V2→V3 migration tests, actual pointer/numeric panel manipulation, source/review/standards/learning persistence, stale-evidence behaviour, escaped script-free HTML report generation, browser restart, backup recovery, invalid panel rejection and 360/412/768/1500 layouts. Existing server/mobile regression passes. These tests do not verify standard editions/adoptions, actual equipment/PL/SIL, conformity or a Windows file double-click. See VERSION-3.md for those limits.


## Version 4 broad studio and easy assembly

Eight additional model cases cover all 48 catalogue entries and seven starter connections/routes, graph-based ideal-air behaviour, spring return and independent cylinders, reverse-check/exhaust faults, drawing-only domain gating, rotated ports and import schema, panel type/backfeed rejection and orthogonal routing. All 36 model tests pass, as does Python account/project integration.

The exact offline V4 bundle passes actual V3 backup migration, toolbox and dot connections, independent valve controls, drawing-only gating, rotation/duplication, Undo/Redo, SVG downloads, panel functional links and type rejection, pointer movement, synchronization with the advanced V3 plan, persistence/restart, malformed import rejection and 360/412/768/1600 layouts without JavaScript errors or external assets. The server/mobile regression passes. File-URL policy, physical-device, manufacturer-pinout, hydraulic/electrical-simulation and conformity limits are recorded in VERSION-4.md.


## Version 5 guided wiring and site worksheets

Eight new model cases verify all three complete schedules, return-path behaviour, relay seal-in/dropout, four-stage PLC motion/rearm/Stop, missing-coil/air timeout, unknown-bore handling and force units, absolute-reference/group tube flow/loss and guarded imports. All 44 model cases and backend account/project integration pass.

The exact V5 bundle passes offline V4→V5 migration, actual terminal-dot/dropdown connections, trace/Undo/Redo/removal, direct/relay/PLC simulation and fault timeout, measurement unknowns and worked example, tubing screens, voltage mismatch, enquiry/report downloads, all seven added Circuit Builder parts and hydraulic panel bank, save/restart/backup recovery/rejection, duplicate-ID absence and 360/412/768/1600 layouts. Existing mobile/server regression passes. The distribution ZIP contains only V5 HTML; earlier HTMLs remain unchanged. File-URL/physical-device, named-model scope, product-data and actual construction limits are documented in VERSION-5.md.


## Version 6 practical training and diagnostics

Seven new model cases exercise voltage/sign/floating/open-return behaviour, powered-ohms interlock, coil/parallel resistance and continuity, PLC output supply dependency, all three behavioural grades and bypass rejection, load/flow/line/stall motion trends, unique terminal output allocation and guarded photo/evidence import. All 51 model cases plus temporary-database account/project integration pass.

Exact offline V5→V6 browser checks cover guided wiring/grading/stale results, actual meter controls and all four diagnostic cases, motion/closed-flow/overload/retract controls, terminal function/zone exports, uploaded/resized JPEG photos and rendered embedded-image reports, escaped source text, portfolio/manufacturer records, browser restart, backup recovery/malformed-image rejection and responsive 360/412/768/1600 layouts without JS errors or external resources. Existing server/mobile regression passes. Prior V1–V5 HTMLs remain unchanged; the V6 distribution contains only V6 HTML. See VERSION-6.md for ideal circuit/estimate, hardware, normative and file-URL limitations.
