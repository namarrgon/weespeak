# weespeak - espeak in weechat

weespeak will output the incoming messages on the current channel-buffer through espeak.

## Source

* http://github.com/namarrgon/weespeak

 ```git clone git://github.com/namarrgon/weespeak.git weespeak```

## Dependencies

* weechat http://weechat.org/
* python-espeak https://launchpad.net/python-espeak

## Usage:
* If you copied _weespeak.py_ to _~/.weechat/python/_, you load it by running:

 ```/python load weespeak.py```

* Otherwise load it from any path:

 ```/python load /path/to/script/weespeak.py```

* List muted Nicks:

 ```/weespeak list_muted```

* Mute Nick:

 ```/weespeak mute elvis```

* Nicks are whitespace separated:

 ```/weespeak mute elvis rob```
* The same rules apply to unmute:

 ```/weespeak unmute elvis```

 ```/weespeak unmute elvis rob```

## TODO
## License
