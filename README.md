# weespeak - espeak in weechat

weespeak will output the incoming messages on the current channel-buffer through espeak.

## Source

* [http://github.com/namarrgon/weespeak](http://github.com/namarrgon/weespeak)

```git clone git://github.com/namarrgon/weespeak.git weespeak```

## Dependencies

* weespeak https://github.com/namarrgon/weespeak
* python-espeak https://launchpad.net/python-espeak

## Usage
* Load the script into weechat:

 ```/python load /path/to/script/weespeak.py```

* List muted Nicks:

 ```/weespeak list_muted```

* mutet Nick(s):

 ```/weespeak mute elvis```

* nicks are whitespace separated:

 ```/weespeak mute elvis rob```
* The same rules apply to unmute:

 ```/weespeak unmute elvis```

 ```/weespeak unmute elvis rob```

## TODO
## License
