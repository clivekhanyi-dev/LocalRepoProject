# Install on a Samsung phone from Windows

## Architecture and choice

This is the existing project with a native Android WebView shell in `android/`, not a replacement application. The WebView loads the existing Python-served HTML, CSS and JavaScript. The same Python API and SQLite database continue to own accounts, projects, lesson completion and saved notes. This avoids a separate API origin, cross-origin cookies, and duplicating the frontend. Capacitor is useful when native plugins or bundled offline assets become necessary; it is not needed for this first remote client. Bundling Python inside Android would add substantial runtime and persistence complexity.

**The APK requires a reachable server.** It does not contain Python or a copy of your database, and does not provide offline startup. Frontend changes are served by the backend, so updating HTML/CSS does not require rebuilding the APK. Native wrapper changes do require an APK update. Existing cloud-instance accounts do not automatically appear on your Windows server: those are separate databases. To preserve data, stop Python and securely transfer your existing SQLite database to the Windows project directory before starting the Windows server. Keep it out of Git.

## Install once on Windows

1. Install **Python 3.12 or newer** from python.org (include the Python launcher).
2. Install **Android Studio** from developer.android.com/studio. Complete its setup wizard.
3. In Android Studio's **SDK Manager**, install **Android SDK Platform 35**, **Android SDK Build-Tools 35.0.0**, and **Android SDK Platform-Tools**. Install Android SDK Command-line Tools (latest) if using the command line. You do not need an emulator for your own phone.
4. Use Android Studio's bundled JDK (normally Java 21) as the Gradle JDK, or install JDK 17+. This project pins Android Gradle Plugin 8.9.2 and Gradle 8.11.1. No Node.js or Capacitor installation is required to build the APK. Node 18+ is optional for the existing JavaScript tests.
5. Copy the **whole existing project**, including `server.py`, `web/`, and `android/`, onto your laptop, for example `C:\Projects\LocalRepoProject`. A Git clone alone will not include changes that have not yet been committed or downloaded.

## Start the existing backend

Open PowerShell in the project folder:

```powershell
cd C:\Projects\LocalRepoProject
py -3 server.py
```

Leave this terminal running. Check the app in your laptop browser at `http://localhost:8000`. Python has no pip dependencies. If port 8000 is already in use, close the other instance first. The default database is `academy.sqlite3` beside `server.py` and persists after restart. Back it up before replacing your laptop or project folder.

## If you use the prebuilt debug APK

Download `pneumatic-academy-debug.apk` supplied with this work and save it on Windows. You can skip rebuilding for your first test. Start Python as above, enable USB debugging as below, run `adb reverse tcp:8000 tcp:8000`, and install the downloaded file with `adb install -r C:\path\to\pneumatic-academy-debug.apk`. Replace that path with the actual download location. The prebuilt APK still needs your Python server; it does not contain your account database or frontend assets. Android Studio is needed to build your own updates; its Platform-Tools supply ADB for the USB test.

## Build the debug APK

In Android Studio, **Open** `C:\Projects\LocalRepoProject\android` and allow Gradle sync to complete. Accept the requested SDK licences. Set the Gradle JDK under Settings → Build, Execution, Deployment → Build Tools → Gradle if prompted. Choose **Build → Build App Bundle(s) / APK(s) → Build APK(s)** (the exact wording varies by Studio version), or use this PowerShell command:

```powershell
cd C:\Projects\LocalRepoProject\android
.\gradlew.bat assembleDebug
```

If running from PowerShell without Android Studio's configured Java, set `JAVA_HOME` to its bundled runtime for that terminal:

```powershell
$env:JAVA_HOME = 'C:\Program Files\Android\Android Studio\jbr'
```

Android Studio creates `android/local.properties` with the local SDK path; do not copy another machine's file. If building only from the terminal, set `$env:ANDROID_HOME = "$env:LOCALAPPDATA\Android\Sdk"`. The wrapper downloads the pinned Gradle distribution on first use. First build needs Internet access to Google's Maven repository and Maven Central.

APK output: `android\app\build\outputs\apk\debug\app-debug.apk`. Debug builds are automatically signed for personal testing. Keep using the same laptop/debug key for updates, or Android will reject an update signed with a different key. A prebuilt APK from this cloud workspace and an APK built on Windows normally have different debug signing keys; uninstall the older app first if Android reports a signature mismatch. Uninstalling clears the wrapper's settings/cookies, but server-side projects remain in SQLite.

## Connect and install by USB (recommended first goal)

1. On Samsung: Settings → About phone → Software information → tap **Build number** seven times. Enter your device PIN if asked.
2. Enable **USB debugging** in Developer options. Connect using a data-capable USB cable. Unlock the phone and accept the computer's debugging prompt. Install Samsung's official Windows USB driver if the phone is not detected.
3. In a second PowerShell terminal:

```powershell
$adb = "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe"
& $adb devices
& $adb reverse tcp:8000 tcp:8000
& $adb install -r C:\Projects\LocalRepoProject\android\app\build\outputs\apk\debug\app-debug.apk
```

If more than one device is attached, add `-s DEVICE_SERIAL` after `$adb` for each command. `devices` must show `device`, not `unauthorized`.

4. Open **Pneumatic Academy** on the phone. In **Server settings**, enter **`http://localhost:8000`** and tap Connect. USB forwarding maps this phone address to the Python server on your Windows laptop. This is why localhost works in this specific test configuration; without `adb reverse`, localhost means the phone itself.
5. Register or sign in; save a project; close and reopen the app; load it again. Disconnecting USB or stopping Python makes this connection unavailable. Run `adb reverse` again after reconnecting or rebooting. Use Reload after restoring the connection.

A helper script is included: from the project folder run `.\tools\Connect-Phone.ps1` after building the APK and starting Python. It performs the forwarding and installation commands above. If your PowerShell policy blocks scripts, use the individual commands above.

You can also press Run in Android Studio to install on the selected phone; USB forwarding is still needed. If Samsung blocks installation, follow its displayed prompt for USB app installation/Auto Blocker on your device; change only what is required for this trusted test, then restore your preferred setting.

## Use away from your laptop

Deploy `server.py` and `web/` on a server with persistent storage, a process supervisor, and a real HTTPS domain. Configure `HOST=0.0.0.0`, the hosting platform's `PORT`, `ACADEMY_DB` pointing to persistent disk, and `ACADEMY_SECURE_COOKIE=1`. Terminate HTTPS at a reverse proxy and preserve the public Host header. Configure login rate limiting and database backups. The standard-library backend remains a pilot and needs production hardening before broad public use. The existing README has additional hosting details.

In the app, change Server settings to your HTTPS origin, for example `https://your-real-domain.example` (replace this placeholder; do not include a subpath). No domain or paid hosting has been provisioned automatically. An HTTPS tunnel to the laptop is another temporary option, but its lifetime, address and access protection depend on the provider; the laptop must remain awake.

HTTP LAN IP addresses are deliberately not enabled in the Android app. The debug APK permits HTTP only for localhost/127.0.0.1 and the Android emulator's 10.0.2.2. Release builds require HTTPS. TLS errors are not bypassed. No broad storage permission or JavaScript-to-native bridge is used; the system document picker supplies access to the selected text file.

## Checks and remaining limits

Automated frontend and backend checks are described in README. Mobile browser tests exercise narrow viewports; they do not substitute for a physical Samsung/WebView test. Confirm on your phone: keyboard and bottom navigation, circuit scrolling/port taps, drag and valve movement, text file selection, sign-in across restart, project and note reload, lost connection and recovery, and Android Back navigation. Save before reload, switching servers or leaving the app; unsaved work is not durably stored offline. Rotation keeps the current WebView. Android process termination or other Activity recreation can still reload the page.

Keep Android System WebView/Chrome updated through the Play Store. The APK supports Android 8+ (API 26); current WebView is required for modern browser APIs. Lessons include PLC foundations; a PLC editor/simulator is not yet implemented. Comparison is manual evidence matching, not a verified catalogue. No account recovery, email verification, MFA or generative AI service is configured. Google Play publication and release signing are separate future steps; no Play account is needed for USB installation.
