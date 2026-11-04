# Pneumatic Automation Academy

A first educational web application for a Festo/SMC sales engineer studying electrical engineering. Independent of both manufacturers.

## Run locally

Requires Python 3.12+; no third-party runtime dependencies or paid APIs.

```sh
cd /workspace/LocalRepoProject
python3 server.py
```

Open the application on port 8000 through your hosting provider's supported route. Create an account with a password of at least 12 characters. Accounts and saved projects use SQLite (`academy.sqlite3`, ignored by Git). Guest users can explore; saving requires sign-in. Projects include circuit topology, notes, lesson completion, entered product evidence and calculator inputs. Saving an existing name replaces that account's project with the same name.

## First workflow

The example connects supply → valve 1, valve 2 → cylinder cap end, and valve 4 → rod end. Ports 3 and 5 exhaust to atmosphere. Run or step to extend; energise Y1 to retract. Click a hose to remove it, then click two ports to reconnect. Drag component bodies to reposition. The foundation validator deliberately supports this single topology; other valid pneumatic designs are outside this version.

The simulator is a discrete state teaching model, not a sizing or fluid-dynamics tool. Its motion speed is illustrative. Symbols are simplified educational drawings, not certified ISO 1219 symbols. The calculator displays ideal force; friction and exhaust back pressure reduce available force.

The product workbench accepts UTF-8 text excerpts and manual specification entry. It does not parse PDFs, decode manufacturer codes or retrieve catalogues. Source references are entered by the user, not independently verified. Comparison checks text agreement and missing fields; it cannot establish interchangeability. The circuit coach uses authored guidance, not a generative AI model. Broader components, PLC simulation and a verified catalogue remain future work.

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
