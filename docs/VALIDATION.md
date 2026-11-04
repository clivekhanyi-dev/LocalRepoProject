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
