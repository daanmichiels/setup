#!/bin/sh
#
# ~/.xinitrc
#
# Executed by startx (run your window manager from here)

if [ -d /etc/X11/xinit/xinitrc.d ]; then
  for f in /etc/X11/xinit/xinitrc.d/*; do
    [ -x "$f" ] && . "$f"
  done
  unset f
fi

# load .Xresources
[[ -f ~/.Xresources ]] && xrdb -merge ~/.Xresources

# switch caps lock and excape
setxkbmap -option caps:swapescape

# run xmonad
exec xmonad

