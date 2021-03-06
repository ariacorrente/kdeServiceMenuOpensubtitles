# KDE ServiceMenu OpenSubtitles #

## Description ##

This is a KDE service menu to download subtitles from [OpenSubtitles.org][0].

1. right click on a video file in Dolphin
2. open the "Actions" submenu
3. select the "download from OpenSubtitles.org" action , it will show you a
    list of subtitles
4. select one subtitle from the list and it will be downloaded

The subtitle file will be saved with the same name as the video but keeping the
subtitle extension, so your player will detect automatically the subtitle. The
search is done extracting an hash from the file, this way you will get the
correct subtitle for sure.

The default language is english, you can change it in the python file.

Thank you to [OpenSubtitles.org][0] for that great service, it's also possible
to help them [uploading subtitles][1].

Original code is from [download_opensubtitle][2], I only fixed some stuff and
made some little changes here and there.

## Install ##

KDE3: Copy download_subtitle.desktop to ~/.kde/share/apps/konqueror/servicemenus

KDE4: Copy download_subtitle.desktop to ~/.kde/share/kde4/services

KDE5: Copy download_subtitle.desktop to ~/.local/share/kservices5/ServiceMenu

Copy download_subtitle.py to some dir of your PATH.

## Dependencies ##

If you have KDE installed all the required tools are usually already installed:

- python
- wget
- kdialog
    In debian based distros kdialog is usually available inside the 
    `kde-baseapps-bin` package.
- qdbus

## Contacts ##

This software is published on the following services:

- [source of kdeServiceMenuOpenSubtitles][3] on GitHub 
- [releases of kdeServiceMenuOpenSubtitles][4] on KDE Store

## Changelog ##

- 2017-04-24: specified python2 as interpreter, fixed --geometry parameter not
    supported by current kdialog, added a progress bar for the login phase,
    fixed info about installation paths in the readme and removed the
    installation and uninstallation script because they where not reliable
    for KDE5.
- 2015-08-13: fix detection of missing dependency. The script is working fine
    in KDE5.
- 2015-03-12: add a real user agent authorized by [OpenSubtitles.org][0] so the
    script will be more reliable.
- 2013-12-27: Updated to work with the changed opensubtitles.org API and some
    dialogs to have a better feeling about what the script is doing. Added
    support for kde4, you will find the correct desktop file for your kde
    version inside the package

[0]: http://www.opensubtitles.org/  "OpensSubtitles.org website"
[1]: http://www.opensubtitles.org/upload  "Upload subtitles to OpenSubtitles.org"
[2]: https://store.kde.org/p/998446 "download_opensubtitle original code"
[3]: https://github.com/ariacorrente/kdeServiceMenuOpensubtitles "kdeServiceMenuOpensubtitles GitHub repository" 
[4]: https://store.kde.org/p/998190 "kdeServiceMenuOpensubtitles on KDE store"
