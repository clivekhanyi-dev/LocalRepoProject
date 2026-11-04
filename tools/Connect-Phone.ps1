# Run from PowerShell after starting server.py and authorising USB debugging.
param([string]$Serial = '')
$ErrorActionPreference = 'Stop'
$adb = Join-Path $env:LOCALAPPDATA 'Android\Sdk\platform-tools\adb.exe'
if (!(Test-Path $adb)) { throw 'Install Android SDK Platform-Tools in Android Studio first, or use your custom SDK adb path manually.' }
$deviceArgs = @()
if ($Serial) { $deviceArgs = @('-s', $Serial) }
& $adb devices
& $adb @deviceArgs reverse tcp:8000 tcp:8000
if ($LASTEXITCODE -ne 0) { throw 'USB forwarding failed. Unlock the phone, authorise USB debugging, and select a device serial if needed.' }
$apk = Join-Path $PSScriptRoot '..\android\app\build\outputs\apk\debug\app-debug.apk'
if (!(Test-Path $apk)) { throw 'Build the APK in Android Studio or run android\gradlew.bat assembleDebug first.' }
& $adb @deviceArgs install -r $apk
if ($LASTEXITCODE -ne 0) { throw 'APK installation failed. Read the adb error above.' }
Write-Host 'Open Pneumatic Academy on your phone. Set Server settings to http://localhost:8000. Keep Python running and USB connected.'
