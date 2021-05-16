#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import shutil
import subprocess
import tempfile
import xml.dom.minidom
from pathlib import Path


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Executable:
    def __init__(self, name):
        if not shutil.which(name):
            raise FileNotFoundError(name)
        self.name = name

    def run(self, args):
        cmdline = [self.name] + args
        pcmdline = ' '.join(cmdline)
        print(f'{bcolors.WARNING}{bcolors.BOLD}[*] {pcmdline}{bcolors.ENDC}{bcolors.OKGREEN}')
        res = subprocess.run(cmdline)
        print(bcolors.ENDC, end='')
        return res


class Apk:
    def __init__(self, args):
        self.apkfile = Path(args.apkfile)
        if not self.apkfile.is_file():
            raise FileNotFoundError(args.apkfile)
        self.apktool = Executable(args.path_apktool)
        self.adb = Executable(args.path_adb)
        self.keytool = Executable(args.path_keytool)
        self.jarsigner = Executable(args.path_jarsigner)
        self.tempdir = tempfile.TemporaryDirectory()
        self.apkdir = self.tempdir.name + '/apkdir'
        self.keystore = self.tempdir.name + '/release.keystore'
        self.outfile = args.outfile

    def apktool_decode(self):
        res = self.apktool.run(['d', '-f', '-o', self.apkdir, str(self.apkfile)])
        res.check_returncode()

    def apktool_build(self):
        res = self.apktool.run(['b', '-f', '-o', self.outfile, self.apkdir])
        res.check_returncode()

    def keytool_generate(self):
        res = self.keytool.run(['-v', '-genkeypair', '-noprompt', '-keyalg', 'RSA', '-keysize', '2048',
            '-keypass', 'passw0rd', '-storepass', 'passw0rd', '-validity', '10000',
            '-keystore', self.keystore, '-dname', 'CN=Unknown', '-destalias', 'mykey'])
        res.check_returncode()

    def jarsigner_signapk(self):
        res = self.jarsigner.run(['-sigalg', 'MD5withRSA', '-digestalg', 'SHA1',
            '-storepass', 'passw0rd', '-keypass', 'passw0rd', '-keystore', self.keystore,
            self.outfile, 'mykey'])
        res.check_returncode()

    def patch_manifest(self):
        print(f'{bcolors.WARNING}{bcolors.BOLD}[*] Patch AndroidManifest.xml{bcolors.ENDC}{bcolors.OKGREEN}')
        with xml.dom.minidom.parse(self.apkdir + '/AndroidManifest.xml') as dom:
            application = dom.getElementsByTagName('application')[0]
            application.setAttribute('android:networkSecurityConfig', '@xml/network_security_config')
            print(application.toprettyxml().splitlines()[0] + bcolors.ENDC)
            with open('/Users/antoinet/git/publibike/app/PubliBike_v1.57.0_apkpure.com/AndroidManifest.xml', 'w') as xmlout:
                dom.writexml(xmlout)

    def patch_ressources(self):
        print(f'{bcolors.WARNING}{bcolors.BOLD}[*] Patch res/xml/network_security_config.xml{bcolors.ENDC}{bcolors.OKGREEN}')
        xml = """<?xml version="1.0" encoding="utf-8"?>
<network-security-config xmlns:android="http://schemas.android.com/apk/res/android">
    <base-config>
        <trust-anchors>
            <certificates src="system"/>
            <certificates src="user"/>
        </trust-anchors>
    </base-config>
</network-security-config>"""
        print(xml + bcolors.ENDC)
        with open(self.apkdir + '/res/xml/network_security_config.xml', 'w') as outfile:
            outfile.write(xml)

    def cleanup(self):
        self.tempdir.cleanup()


def main(argv):
    parser = argparse.ArgumentParser(description='Certificate Unpinner')
    parser.add_argument('--path-apktool', default='apktool', help='Path to the apktool executable')
    parser.add_argument('--path-adb', default='adb', help='Path to the adb executable')
    parser.add_argument('--path-keytool', default='keytool', help='Path to the keytool executable')
    parser.add_argument('--path-jarsigner', default='jarsigner', help='Path to the jarsigner executable')
    parser.add_argument('--outfile', default='unpinned.apk', help='Output file')
    parser.add_argument('apkfile', help='Path to the APK file')

    args = parser.parse_args(argv)
    apk = Apk(args)
    apk.apktool_decode()
    apk.patch_manifest()
    apk.patch_ressources()
    apk.apktool_build()
    apk.keytool_generate()
    apk.jarsigner_signapk()
    apk.cleanup()

if __name__ == '__main__':
    main(sys.argv[1:])
