#!/usr/bin/env python
"""
admin.py - Jenni Admin Module
Copyright 2010-2011, Sean B. Palmer (inamidst.com) and Michael Yanovich (yanovich.net)
Licensed under the Eiffel Forum License 2.

More info:
 * Jenni: https://github.com/myano/jenni/
 * Phenny: http://inamidst.com/phenny/
"""

import os

def join(jenni, input):
   """Join the specified channel. This is an admin-only command."""
   # Can only be done in privmsg by an admin
   if input.sender.startswith('#'): return
   if input.admin:
      channel, key = input.group(1), input.group(2)
      if not key:
         jenni.write(['JOIN'], channel)
      else: jenni.write(['JOIN', channel, key])
join.rule = r'\.join (#\S+)(?: *(\S+))?'
join.priority = 'low'
join.example = '.join #example or .join #example key'

def part(jenni, input):
   """Part the specified channel. This is an admin-only command."""
   # Can only be done in privmsg by an admin
   if input.sender.startswith('#'): return
   if input.admin:
      jenni.write(['PART'], input.group(2))
part.commands = ['part']
part.priority = 'low'
part.example = '.part #example'

def quit(jenni, input):
   """Quit from the server. This is an owner-only command."""
   # Can only be done in privmsg by the owner
   if input.sender.startswith('#'): return
   if input.owner:
      jenni.write(['QUIT'])
      __import__('os')._exit(0)
quit.commands = ['quit']
quit.priority = 'low'

def msg(jenni, input):
   # Can only be done in privmsg by an admin
   if input.sender.startswith('#'): return
   a, b = input.group(2), input.group(3)
   if (not a) or (not b): return
   if input.admin:
      jenni.msg(a, b)
msg.rule = (['msg'], r'(#?\S+) (.+)')
msg.priority = 'low'

def me(jenni, input):
   # Can only be done in privmsg by an admin
   if input.sender.startswith('#'): return
   if input.admin:
      msg = '\x01ACTION %s\x01' % input.group(3)
      jenni.msg(input.group(2), msg)
me.rule = (['me'], r'(#?\S+) (.*)')
me.priority = 'low'

def defend_ground(jenni, input):
    """
    This function monitors all kicks across all channels jenni is in. If she
    detects that she is the one kicked she'll automatically join that channel.

    WARNING: This may not be needed and could cause problems if jenni becomes
    annoying. Please use this with caution.
    """
    channel = input.sender
    jenni.write(['JOIN'], channel)
defend_ground.event = 'KICK'
defend_ground.rule = '.*'
defend_ground.priority = 'low'

def blocks(jenni, input):
    if not input.admin: return

    STRINGS = {
            "success_del" : "Successfully deleted block: %s",
            "success_add" : "Successfully added block: %s",
            "no_nick" : "No matching nick block found for: %s",
            "no_host" : "No matching hostmask block found for: %s",
            "invalid" : "Invalid format for %s a block. Try: .blocks add (nick|hostmask) jenni",
            "invalid_display" : "Invalid input for displaying blocks.",
            }

    if not os.path.isfile("blocks"):
        blocks = open("blocks", "w")
        blocks.write('gateway/freenode/\n')
        blocks.write('jenni')
        blocks.close()

    blocks = open("blocks", "r")
    contents = blocks.readlines()
    blocks.close()

    masks = contents[0].replace("\n", "").split(',')
    nicks = contents[1].replace("\n", "").split(',')

    text = input.group().split()

    if text[1] == "list" and len(text) == 3:
        if text[2] == "hostmask":
            for each in masks:
                jenni.say(each)
        elif text[2] == "nick":
            for each in nicks:
                jenni.say(each)
        else:
            jenni.reply(STRINGS['invalid_display'])

    elif text[1] == "add" and len(text) == 4:
        if text[2] == "nick":
            nicks.append(text[3])
        elif text[2] == "hostmask":
            masks.append(text[3])
        else:
            jenni.reply(STRINGS['invalid'] % ("adding"))
            return

        jenni.reply(STRINGS['success_add'] % (text[3]))

    elif text[1] == "del" and len(text) == 4:
        if text[2] == "nick":
            try:
                nicks.remove(text[3])
                jenni.reply(STRINGS['success_del'] % (text[3]))
            except:
                jenni.reply(STRINGS['no_nick'] % (text[3]))
                return
        elif text[2] == "hostmask":
            try:
                masks.remove(text[3])
                jenni.reply(STRINGS['success_del'] % (text[3]))
            except:
                jenni.reply(STRINGS['no_host'] % (text[3]))
                return
        else:
            jenni.reply(STRINGS['invalid'] % ("deleting"))
            return

    os.remove("blocks")
    blocks = open("blocks", "w")
    masks_str = ",".join(masks)
    blocks.write(masks_str)
    blocks.write("\n")
    nicks_str = ",".join(nicks)
    blocks.write(nicks_str)
    blocks.close()

blocks.commands = ['blocks']
blocks.priority = 'low'
blocks.thread = False

if __name__ == '__main__':
   print __doc__.strip()

