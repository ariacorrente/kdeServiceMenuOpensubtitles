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

Copy download_subtitle.py to some dir of your path.

For the lazy there are two scripts to install and uninstall the needed files in
the right folder for KDE4. The scripts will use sudo to allow the copy of the
python script into a system folder included in PATH.

## Dependencies ##

If you have KDE installed all the required tools are usually already installed:

- python
- wget
- kdialog
- qdbus

## Changelog ##

- 2015-03-12: add a real user agent authorized by [OpenSubtitles.org][0] so the
    script will be more reliable.
- 2013-12-27: Updated to work with the changed opensubtitles.org API and some
    dialogs to have a better feeling about what the script is doing. Added
    support for kde4, you will find the correct desktop file for your kde
    version inside the package

[0]: http://www.opensubtitles.org/  "OpensSubtitles.org website"
[1]: http://www.opensubtitles.org/upload  "Upload subtitles to OpenSubtitles.org"
[2]: http://kde-look.org/content/show.php/download_opensubtitle?content=65444 "download_opensubtitle original code"
