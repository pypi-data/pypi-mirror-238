# -*- coding: utf-8 -*-

# Copyright (c) 2011 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Package implementing cryptography related functionality.
"""

import base64
import random

from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QInputDialog, QLineEdit

from eric7 import Preferences
from eric7.EricWidgets import EricMessageBox

###############################################################################
## password handling functions below
###############################################################################


EncodeMarker = "CE4"
CryptoMarker = "CR5"

Delimiter = "$"

MainPassword = None


def pwEncode(pw):
    """
    Module function to encode a password.

    @param pw password to encode (string)
    @return encoded password (string)
    """
    pop = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,;:-_!$?*+#"
    rpw = "".join(random.sample(pop, 32)) + pw + "".join(random.sample(pop, 32))
    return EncodeMarker + base64.b64encode(rpw.encode("utf-8")).decode("ascii")


def pwDecode(epw):
    """
    Module function to decode a password.

    @param epw encoded password to decode (string)
    @return decoded password (string)
    """
    if not epw.startswith(EncodeMarker):
        return epw  # it was not encoded using pwEncode

    return base64.b64decode(epw[3:].encode("ascii"))[32:-32].decode("utf-8")


def __getMainPassword():
    """
    Private module function to get the password from the user.
    """
    from .py3PBKDF2 import verifyPassword

    global MainPassword

    pw, ok = QInputDialog.getText(
        None,
        QCoreApplication.translate("Crypto", "Main Password"),
        QCoreApplication.translate("Crypto", "Enter the main password:"),
        QLineEdit.EchoMode.Password,
    )
    if ok:
        mainPassword = Preferences.getUser("MainPassword")
        try:
            if mainPassword:
                if verifyPassword(pw, mainPassword):
                    MainPassword = pwEncode(pw)
                else:
                    EricMessageBox.warning(
                        None,
                        QCoreApplication.translate("Crypto", "Main Password"),
                        QCoreApplication.translate(
                            "Crypto", """The given password is incorrect."""
                        ),
                    )
            else:
                EricMessageBox.critical(
                    None,
                    QCoreApplication.translate("Crypto", "Main Password"),
                    QCoreApplication.translate(
                        "Crypto", """There is no main password registered."""
                    ),
                )
        except ValueError as why:
            EricMessageBox.warning(
                None,
                QCoreApplication.translate("Crypto", "Main Password"),
                QCoreApplication.translate(
                    "Crypto",
                    """<p>The given password cannot be verified.</p>"""
                    """<p>Reason: {0}""".format(str(why)),
                ),
            )


def pwEncrypt(pw, mainPW=None):
    """
    Module function to encrypt a password.

    @param pw password to encrypt (string)
    @param mainPW password to be used for encryption (string)
    @return encrypted password (string) and flag indicating
        success (boolean)
    """
    from .py3AES import encryptData
    from .py3PBKDF2 import hashPasswordTuple

    if mainPW is None:
        if MainPassword is None:
            __getMainPassword()
            if MainPassword is None:
                return "", False

        mainPW = pwDecode(MainPassword)

    digestname, iterations, salt, pwHash = hashPasswordTuple(mainPW)
    key = pwHash[:32]
    try:
        cipher = encryptData(key, pw.encode("utf-8"))
    except ValueError:
        return "", False
    return (
        CryptoMarker
        + Delimiter.join(
            [
                digestname,
                str(iterations),
                base64.b64encode(salt).decode("ascii"),
                base64.b64encode(cipher).decode("ascii"),
            ]
        ),
        True,
    )


def pwDecrypt(epw, mainPW=None):
    """
    Module function to decrypt a password.

    @param epw hashed password to decrypt (string)
    @param mainPW password to be used for decryption (string)
    @return decrypted password (string) and flag indicating
        success (boolean)
    """
    from .py3AES import decryptData
    from .py3PBKDF2 import rehashPassword

    if not epw.startswith(CryptoMarker):
        return epw, False  # it was not encoded using pwEncrypt

    if mainPW is None:
        if MainPassword is None:
            __getMainPassword()
            if MainPassword is None:
                return "", False

        mainPW = pwDecode(MainPassword)

    hashParameters, epw = epw[3:].rsplit(Delimiter, 1)
    try:
        # recreate the key used to encrypt
        key = rehashPassword(mainPW, hashParameters)[:32]
        plaintext = decryptData(key, base64.b64decode(epw.encode("ascii")))
    except ValueError:
        return "", False
    return plaintext.decode("utf-8"), True


def pwReencrypt(epw, oldPassword, newPassword):
    """
    Module function to re-encrypt a password.

    @param epw hashed password to re-encrypt (string)
    @param oldPassword password used to encrypt (string)
    @param newPassword new password to be used (string)
    @return encrypted password (string) and flag indicating
        success (boolean)
    """
    plaintext, ok = pwDecrypt(epw, oldPassword)
    if ok:
        return pwEncrypt(plaintext, newPassword)
    else:
        return "", False


def pwRecode(epw, oldPassword, newPassword):
    """
    Module function to re-encode a password.

    In case of an error the encoded password is returned unchanged.

    @param epw encoded password to re-encode (string)
    @param oldPassword password used to encode (string)
    @param newPassword new password to be used (string)
    @return encoded password (string)
    """
    if epw == "":
        return epw

    if newPassword == "":
        plaintext, ok = pwDecrypt(epw)
        return pwEncode(plaintext) if ok else epw
    else:
        if oldPassword == "":
            plaintext = pwDecode(epw)
            cipher, ok = pwEncrypt(plaintext, newPassword)
            return cipher if ok else epw
        else:
            npw, ok = pwReencrypt(epw, oldPassword, newPassword)
            return npw if ok else epw


def pwConvert(pw, encode=True):
    """
    Module function to convert a plaintext password to the encoded form or
    vice versa.

    If there is an error, an empty code is returned for the encode function
    or the given encoded password for the decode function.

    @param pw password to encode (string)
    @param encode flag indicating an encode or decode function (boolean)
    @return encoded or decoded password (string)
    """
    if pw == "":
        return pw

    if encode:
        # plain text -> encoded
        if Preferences.getUser("UseMasterPassword"):
            epw = pwEncrypt(pw)[0]
        else:
            epw = pwEncode(pw)
        return epw
    else:
        # encoded -> plain text
        if Preferences.getUser("UseMasterPassword"):
            plain, ok = pwDecrypt(pw)
        else:
            plain, ok = pwDecode(pw), True
        return plain if ok else pw


def changeRememberedMain(newPassword):
    """
    Module function to change the remembered main password.

    @param newPassword new password to be used (string)
    """
    global MainPassword
    MainPassword = pwEncode(newPassword) if newPassword else None


def dataEncrypt(data, password, keyLength=32, hashIterations=10000):
    """
    Module function to encrypt a password.

    @param data data to encrypt (bytes)
    @param password password to be used for encryption (string)
    @param keyLength length of the key to be generated for encryption
        (16, 24 or 32)
    @param hashIterations number of hashes to be applied to the password for
        generating the encryption key (integer)
    @return encrypted data (bytes) and flag indicating
        success (boolean)
    """
    from .py3AES import encryptData
    from .py3PBKDF2 import hashPasswordTuple

    digestname, iterations, salt, pwHash = hashPasswordTuple(
        password, iterations=hashIterations
    )
    key = pwHash[:keyLength]
    try:
        cipher = encryptData(key, data)
    except ValueError:
        return b"", False
    return (
        CryptoMarker.encode("utf-8")
        + Delimiter.encode("utf-8").join(
            [
                digestname.encode("utf-8"),
                str(iterations).encode("utf-8"),
                base64.b64encode(salt),
                base64.b64encode(cipher),
            ]
        ),
        True,
    )


def dataDecrypt(edata, password, keyLength=32):
    """
    Module function to decrypt a password.

    @param edata hashed data to decrypt (string)
    @param password password to be used for decryption (string)
    @param keyLength length of the key to be generated for decryption
        (16, 24 or 32)
    @return decrypted data (bytes) and flag indicating
        success (boolean)
    """
    from .py3AES import decryptData
    from .py3PBKDF2 import rehashPassword

    if not edata.startswith(CryptoMarker.encode("utf-8")):
        return edata, False  # it was not encoded using dataEncrypt

    hashParametersBytes, edata = edata[3:].rsplit(Delimiter.encode("utf-8"), 1)
    hashParameters = hashParametersBytes.decode()
    try:
        # recreate the key used to encrypt
        key = rehashPassword(password, hashParameters)[:keyLength]
        plaintext = decryptData(key, base64.b64decode(edata))
    except ValueError:
        return "", False
    return plaintext, True
