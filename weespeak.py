# -*- coding: utf-8 -*-

SCRIPT_NAME    = "weespeak"
SCRIPT_AUTHOR  = "Alexander Schnaidt <alex.schnaidt@gmail.com>"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL2"
SCRIPT_DESC    = "Outputs messages in current irc-buffer through espeak."
SCRIPT_COMMAND = "weespeak"

import sys

try:
    import weechat
    from weechat import WEECHAT_RC_OK as W_OK
except ImportError:
    raise ImportError("This script has to be run from inside weechat: '/python load /path/to/script/weespeak.py'")

try:
    from espeak import espeak
    weechat.prnt("", "imported espeak OK")
except ImportError:
    weechat.prnt("", "This script requires python-espeak: https://launchpad.net/python-espeak")
    raise

template = "{who} says {what}"
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

def speak_out(data, signal, signal_data):

    msg = parse_message(data, signal, signal_data)

    W_OK = WEECHAT_RC_OK

    # filter out message that would take to long to synthesize by espeak
    if len(msg["message"]) > max_message_length:
        return WOK

    # you don't want to hear your own messages
    elif msg["nick"] == own_nick(msg["server"]):
        return WEECHAT_RC_OK

    # don't speak out if nick is in ignore list
    elif msg["nick"] in ignore:
        return WEECHAT_RC_OK

    # only speak out the current buffer
    elif buffer_current() != buffer(msg["server"], msg["channel"]):
        return WEECHAT_RC_OK

    # build sentence
    sentence = syntax.format(who = msg["nick"], what = msg["message"])

    # run it through espeak
    espeak.synth(sentence)

    return WOK

# weechat.register(name, author, version, 
#                  license, description, shutdown_function, charset)
weechat.register(SCRIPT_NAME,
                 SCRIPT_AUTHOR,
                 SCRIPT_VERSION,
                 SCRIPT_LICENSE,
                 SCRIPT_DESC, "", "")

# hook into weechat:

# run speak_out() AFTER the message got processed => irc_in2_privmsg;
# run BEFORE => irc_in_privmsg
weechat.hook_signal("*,irc_in2_privmsg", "speak_out", "")

