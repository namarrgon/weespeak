# -*- coding: utf-8 -*-

#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#
# Copyright (c) Alexander Schnaidt <alex.schnaidt@gmail.com>
#

SCRIPT_NAME    = "weespeak"
SCRIPT_AUTHOR  = "Alexander Schnaidt <alex.schnaidt@gmail.com>"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL2"
SCRIPT_DESC    = "Outputs messages in current irc-buffer through espeak."
SCRIPT_COMMAND = "weespeak"

try:
    import weechat
    from weechat import WEECHAT_RC_OK as W_OK
except ImportError:
    raise ImportError("Load this script from inside weechat (http://weechat.org)."
                      "Run '/python load /path/to/script/weespeak.py' from weechat.")

try:
    from espeak import espeak
except ImportError:
    raise ImportError("This script requires python-espeak: https://launchpad.net/python-espeak")

syntax = "{who} says {what}"
ignore = []
max_message_length = 500

def own_nick(server):
    """this users nick"""
    return weechat.info_get("irc_nick", server)

def buffer_current():
    """current buffer pointer as string"""
    return weechat.current_buffer()

def buffer(server, channel):
    """buffer pointer as string"""
    return weechat.info_get("irc_buffer", ",".join( [server, channel] ) )

def parse_message(data, signal, signal_data):
    """ parse the data in the three strings and return a dict """
    # info_get_hashtable docs:
    # http://www.weechat.org/files/doc/devel/weechat_scripting.en.html#irc_message_parse
    hm = weechat.info_get_hashtable("irc_message_parse", {"message":signal_data})
    # servername where the message came from signal, for irc => "
    hm["server"] = signal.split(",")[0]
    # strip channel-name from arguments and then the leading colon
    hm["message"] = hm["arguments"].lstrip(hm["channel"]).lstrip()[1:]
    return hm

def mute(nicks):
    if nicks:
        [ignore.append(nick) for nick in nicks if nick not in ignore]

def unmute(nicks):
    if nicks:
        [ignore.remove(nick) for nick in nicks if nick in ignore]

def cmd(rc, from_buffer, arg):
    
    arguments = arg.split()

    if arguments[0] == "mute":
        mute( arguments[1:] )
    elif arguments[0] == "unmute":
        unmute( arguments[1:] )
    elif arguments[0] == "list_muted":
        weechat.prnt("", "muted nicks: {}".format(" ".join(ignore)))
    else:
        weechat.prnt("", "unknown command: '{}'".format(arguments[0]))
        return weechat.WEECHAT_RC_ERROR
 
    return W_OK

def speak_out(data, signal, signal_data):

    msg = parse_message(data, signal, signal_data)

    # filter out message that would take to long to synthesize by espeak
    if len(msg["message"]) > max_message_length:
        return W_OK

    # you don't want to hear your own messages
    elif msg["nick"] == own_nick(msg["server"]):
        return W_OK

    # don't speak out if nick is in ignore list
    elif msg["nick"] in ignore:
        return W_OK

    # only speak out the current buffer
    elif buffer_current() != buffer(msg["server"], msg["channel"]):
        return W_OK

    # build sentence
    sentence = syntax.format(who = msg["nick"], what = msg["message"])

    # run it through espeak
    espeak.synth(sentence)

    return W_OK

# weechat.register(name, author, version, 
#                  license, description, shutdown_function, charset)
weechat.register(SCRIPT_NAME,
                 SCRIPT_AUTHOR,
                 SCRIPT_VERSION,
                 SCRIPT_LICENSE,
                 SCRIPT_DESC, "", "")

# run speak_out() AFTER the message got processed => irc_in2_privmsg;
# run BEFORE => irc_in_privmsg
weechat.hook_signal("*,irc_in2_privmsg", "speak_out", "")

weechat.hook_command("weespeak",
                     "adjust the weespeak configuration",
                     "[mute | unmute] [nick(s)] | [list_muted]", # example syntax
                     "list_muted: prints out nicks that are ignored by weespeak\n"
                     "mute      : puts a nick / list of nicks on ignore\n"
                     "unmute    : removes a nick / list of nicks from ignore\n\n"
                     " Example:\n"
                     "  /weespeak mute elvis\n"
                     "   puts the nick 'elvis' on the ignore list\n\n"
                     "  /weespeak unmute elvis phrik\n"
                     "   removes the nicks 'elvis' and 'phrik' from the ignore list\n\n"
                     "  /weespeak list_muted\n"
                     "   prints the muted nicks to the core-buffer\n", # desc of args
                     " || mute %(nicks)"
                     " || unmute %(nicks)"
                     " || list_muted",
                     "cmd", "")
