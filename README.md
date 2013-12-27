# download_subtitle KDE service menu #

## Description ##

This is a service menu to download subtitles from opensubtitle.org

Just right click on a video file -> actions -> download subtitle, it will show
you a list of subtitles. Select one and it will be downloaded and saved with
the same name as the video (with a subtitle extension of course), so your
player will detect automatically the subtitle

The search is done extracting a hash from the file, this way you will get the
correct subtitle for sure (no more async problems)

The default language is english, you can change it in the python file

Thank you to opensubtitles.org for that great service.

## Install ##

KDE3: Copy download_subtitle.desktop to ~/.kde/share/apps/konqueror/servicemenus

KDE4: Copy download_subtitle.desktop to ~.kde/share/kde4/services/ServiceMenus

Copy download_subtitle.py to some dir of your path.

For the lazy there are two scripts to install and uninstall the needed files in
the right folder for KDE4. The scripts use sudo to allow the copy of the python
script into a system folder included in PATH.

## Dependencies ##

- python
- wget
- kdialog

## Changelog ##

- 2013-12-27: Updated to work with the changed opensubtitles.org API
- Added suport for kde4, you will find the correct desktop file for your kde
    inside the package