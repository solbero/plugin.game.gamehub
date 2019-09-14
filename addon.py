# -*- coding: utf-8 -*-
# Module: default
# Author: solbero
# Created on: 14.09.2019
# License: GPL v.2 https://www.gnu.org/licenses/old-licenses/gpl-2.0.html

from __future__ import unicode_literals
import os
import xbmc
import xbmcaddon
from distutils.spawn import find_executable

# Get the addon id
addon = xbmcaddon.Addon()
# Get the addon name
addon_name = addon.getAddonInfo('name')
# Get the localized strings
language = addon.getLocalizedString


def log(msg, level=xbmc.LOGDEBUG):
    """
    Output message to kodi.log file.

    :param msg: message to output
    :param level: debug levelxbmc. Values:
    xbmc.LOGDEBUG = 0
    xbmc.LOGERROR = 4
    xbmc.LOGFATAL = 6
    xbmc.LOGINFO = 1
    xbmc.LOGNONE = 7
    xbmc.LOGNOTICE = 2
    xbmc.LOGSEVERE = 5
    xbmc.LOGWARNING = 3
    """
    # Decode message to UTF8
    if isinstance(msg, str):
        msg = msg.decode('utf-8')
    # Write message to kodi.log
    log_message = '{0}: {1}'.format(addon_name, msg)
    xbmc.log(log_message.encode('utf-8'), level)


def inhibit_shutdown(bool):
    """
    Enable or disable the built in kodi idle shutdown timer.

    :param bool: true or false boolean
    :type bool: bool
    """
    # Convert bool to lowercase string
    str_bool = str(bool).lower
    # Send bool to kodi
    xbmc.executebuiltin('InhibitIdleShutdown({0})'.format(str_bool))


def executable_path():
    """
    Find the path to the gamehub executable .

    :return: path to executable
    :rtype: list
    """
    # Check if the user has specified a custom path
    if addon.getSetting('use_custom_path') == 'true':
        # Get the custom path from addon settings
        path = addon.getSetting('gamehub_executable').decode('utf-8')
    # Find the path to the gamehub executable
    else:
        try:
            path = find_executable('com.github.tkashkin.gamehub').decode('utf-8')
        # Log if executable is not found
        except Exception as e:
            log('{0}').format(e)
    return path


def launch():
    """Launch the GameHub executable."""
    # Stop playback if Kodi is playing any media
    if xbmc.Player().isPlaying():
        xbmc.Player().stop()
    # Disable the idle shutdown timer
    inhibit_shutdown(True)
    # Launch gamehub executable
    try:
        os.system(executable_path().encode('utf-8'))
    # Log if executable is not found
    except Exception as e:
        log('{0}').format(e)
    # Enable the idle shutdown timer
    inhibit_shutdown(False)

if (__name__ == '__main__'):
    launch()
