#! /usr/bin/env python

import lxml.etree as et
import sys
import subprocess
import os
import shutil

if len(sys.argv) < 2:
    print('Usage: ' + sys.argv[0] + ' <musescore-fle.mscx>')
    sys.exit()

ms_file = sys.argv[1]

home = os.path.expanduser('~')
if os.path.exists(home + '/Documents/MuseScore2'):
	ms_user_folder = home + '/Documents/Musescore2'
elif os.path.exists(home + '/Dokumente/MuseScore2'):
	ms_user_folder = home + '/Dokumente/Musescore2'

mscx = et.parse(ms_file)
defaultstyle = et.parse(ms_user_folder + '/Stile/default.mss').getroot()

# Delete synthesizer tag
for synthesizer in mscx.xpath('/museScore/Score/Synthesizer'):
	synthesizer.getparent().remove(synthesizer)

# Remove old style
for style in mscx.xpath('/museScore/Score/Style'):
	style.getparent().remove(style)

# Add styles from .mss file
for score in mscx.xpath('/museScore/Score'):
	score.insert(0, defaultstyle[0])

# strip tags in lyrics
et.strip_tags(mscx, 'font', 'b', 'i')

# To get closing tag use method 'html'
tmp_file = ms_file.replace('.mscx', '_tmp.mscx')
mscx.write(tmp_file, pretty_print=True, xml_declaration=True, method='html', encoding='UTF-8')

bak_file = ms_file.replace('.mscx', '_bak.mscx')
shutil.copy2(ms_file, bak_file)

mac_ms = '/Applications/MuseScore 2.app/Contents/MacOS/mscore'
if os.path.exists(mac_ms):
	subprocess.call([mac_ms, "-o", ms_file, tmp_file])
else:
	subprocess.call(["mscore", "-o", ms_file, tmp_file])
