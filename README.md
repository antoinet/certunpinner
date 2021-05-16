# What is this?
Script used to perform automatic certificate unpinning of an APK by adding a custom [network security configuration](https://developer.android.com/training/articles/security-config) that permits user-added CA certificates.

# Prerequisites
 * [Apktool](https://ibotpeaches.github.io/Apktool/)
 * [Android Debug Bridge (adb)](https://developer.android.com/studio/command-line/adb), get it from the [SDK platform tools](https://developer.android.com/studio/releases/platform-tools#downloads) or bundled with [Android Studio](https://developer.android.com/studio/)
 * [keytool](https://docs.oracle.com/en/java/javase/16/docs/specs/man/keytool.html) and [jarsigner](https://docs.oracle.com/en/java/javase/16/docs/specs/man/jarsigner.html), get them with the latest [Java Development Kit (jdk)](https://www.oracle.com/java/technologies/javase-jdk16-downloads.html)

# Usage
```
$ python3 certunpinner.py --help
usage: certunpinner.py [-h] [--path-apktool PATH_APKTOOL] [--path-adb PATH_ADB] [--path-keytool PATH_KEYTOOL]
                       [--path-jarsigner PATH_JARSIGNER] [--outfile OUTFILE]
                       apkfile

Certificate Unpinner

positional arguments:
  apkfile               Path to the APK file

optional arguments:
  -h, --help            show this help message and exit
  --path-apktool PATH_APKTOOL
                        Path to the apktool executable
  --path-adb PATH_ADB   Path to the adb executable
  --path-keytool PATH_KEYTOOL
                        Path to the keytool executable
  --path-jarsigner PATH_JARSIGNER
                        Path to the jarsigner executable
  --outfile OUTFILE     Output file
```
