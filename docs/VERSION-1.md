# Automation Engineering Academy — Version 1.0

## Open it on Windows

1. On GitHub select the `android-mobile-app` branch and open **Automation-Academy-V1.html** at the repository root.
2. Click **Download raw file** (the download arrow above the file). Alternatively choose Code → Download ZIP and extract it.
3. Put `Automation-Academy-V1.html` in a permanent folder, such as Documents → Automation Academy.
4. Double-click the HTML. If Windows opens VS Code, right-click → Open with → Microsoft Edge or Google Chrome.
5. Use the app. No Python, VS Code, server, terminal, package installation or Internet connection is required for its learning tools.

The single HTML contains the CSS, JavaScript, lessons, drawings and CODESYS example. Links to external standards/documentation still require Internet when you choose to follow them. The browser edition retains the existing simulator, PLC scan lab, technical symbols, lesson challenges, calculators and manual comparison tool. General hydraulic/electrical circuit simulation and a full CODESYS runtime remain outside V1.

## Saving and backups

- **Save current workspace** creates/updates a named project in this browser. **Open saved project** loads it.
- A local draft is autosaved every 1.5 seconds, with a status message at the top. A final save is attempted when the page closes, but browser shutdown may interrupt it. Use explicit save/export for important work.
- Runtime outputs and timer values reset on reopen. Your PLC program, inputs, notes, lesson progress, product evidence and calculator settings are retained.
- **Projects → Export backup** downloads a JSON file containing saved projects and the current workspace, including edits not yet explicitly saved. Keep this outside the browser, ideally on a backed-up drive.
- **Import backup** restores those projects. Matching names are replaced only after confirmation. A malformed backup is rejected before any import changes.
- If the browser blocks local storage or its quota is full, the app shows an error instead of claiming a successful save. Export backup remains available.

Local-file browser storage is implementation-dependent and is not embedded back into the HTML. Moving or renaming the HTML, changing browsers, using private mode or clearing browser data can make local projects unavailable. Export before any of those actions and before replacing V1 with a future version. Keep using the same browser and file location. A local profile is only a display name; it does not provide password protection, user isolation or cloud sync.

## Existing server accounts and projects

The original Python app and SQLite database remain unchanged. The standalone HTML does not read SQLite or carry over server passwords. If you want existing projects in V1:

1. Update the original app's `web` folder from this branch while keeping `academy.sqlite3` untouched.
2. Open the original server app, sign in and select Projects → Export backup.
3. Open Version 1 HTML and select Projects → Import backup.
4. Check the restored notes/projects before retiring the server copy. Keep a backup of the original database.

Starting V1 without this import gives you a separate local workspace.

## Future updates and development

We can improve V1 incrementally while retaining the JSON backup format. The existing web source remains in `web/`; `tools/build_standalone.py` bundles it reproducibly into the root HTML. Developers can regenerate it with `python3 tools/build_standalone.py`. End users do not run this command.

Do not manually edit the generated HTML for development: change the source and rebuild. The normal Python/Android clients continue using the original server-based authentication; only the standalone HTML injects the local-store adapter.

## Verification and limits

The exact generated HTML was tested in Chromium with networking disabled, including PLC behaviour, profile/project saving, autosave, browser-process restart, backup export/import, invalid-backup rejection, unfinished PLC draft recovery and storage-blocked export. It requests no external scripts, styles or data. Existing server-app mobile regression remains passing.

The managed test browser blocks `file://` navigation by administrative policy. Therefore the bundled bytes were loaded through a loopback URL fulfilled from memory for those tests, with no web server or external network. Direct double-click launch on the user's Windows browser has not been tested here. Chrome/Edge normally support local HTML; company-managed browser policies may restrict it. File-local persistence remains browser-dependent, so JSON backups are the reliable transfer mechanism.
