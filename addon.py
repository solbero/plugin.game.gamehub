# -*- coding: utf-8 -*-
# Module: default
# Author: solbero
# Created on: 14.09.2019
# License: GPL v.2 https://www.gnu.org/licenses/old-licenses/gpl-2.0.html

from __future__ import unicode_literals
import xbmc
import xbmcaddon
from subprocess import call
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
    # Convert bool argument to lowercase string
    str_bool = str(bool).lower
    # Send bool value to Kodi
    xbmc.executebuiltin('InhibitIdleShutdown({0})'.format(str_bool))


def get_path():
    """
    Find the path to the gamehub executable .

    :return: path to executable
    :rtype: list
    """
    # Check if the user has specified a custom path in addon settings
    if addon.getSetting('custom_path') == 'true':
        # Get the custom path from addon settings
        path = addon.getSetting('executable').decode('utf-8')
    else:
        # Find the path to the gamehub executable
        path = find_executable('com.github.tkashkin.gamehub').decode('utf-8')
    # Log lutris executable path to kodi.log
    log('Executable path is {}'.format(path))
    return path


def run():
    """Launch the gamehub executable."""
    # Add the path to the lutris executable to the command
    cmd = get_path()
    # Stop playback if Kodi is playing any media
    if xbmc.Player().isPlaying():
        xbmc.Player().stop()
    # Log command to kodi.log
    log('Launch command is {0}'.format(cmd))
    # Disable the idle shutdown timer
    inhibit_shutdown(True)
    # Convert command string to list
    cmd = cmd.split()
    # Launch gamehub with command. Subprocess.call waits for the game
    # to finish before continuing
    call(cmd)
    # Enable the idle shutdown timer after the user exits the game
    inhibit_shutdown(False)

if (__name__ == '__main__'):
    run()
