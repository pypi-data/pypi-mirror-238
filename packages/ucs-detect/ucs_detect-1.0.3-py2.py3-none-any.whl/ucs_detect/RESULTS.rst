iTerm2
------

At time of this writing, iTerm2 has mixed version support, most of the unicode
tables are based on unicode version 12, but emoji characters up to unicode
release 15 were recently added.

- https://github.com/gnachman/iTerm2/blob/a98871deaf3f534e1057d1fe3339bb14a083ccba/sources/NSCharacterSet%2BiTerm.m#L1936C10-L1936C10


BiDi support
------------

- https://terminal-wg.pages.freedesktop.org/bidi/
- https://gist.github.com/XVilka/a0e49e1c65370ba11c17

mlterm
------

Although it scores very well, almost all fonts are missing, installing 'Noto
Mono' and etc.  is not much help, it seems I have to select an individual font
for every unicode plane/language grouping, very weird. I think only on Linux, it
is common to configure a terminal emulator for only a single language (Devangani
is popular), something about size constraints.