import numpy as np
import csv, re


# INITIALIZATION
html    = open('index.html', 'w')
html.write('\
    <!DOCTYPE html>\n\
    <html>\n\
    <head>\n\
    \t<title>Periodic table by Leonard Seydoux</title>\n\
    \t<meta charset="utf-8" />\n\
    \t<meta name="viewport" content="width=device-width, initial-scale=1" />\n\
    \t<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.1/css/font-awesome.min.css">\n\
    \t<link rel="stylesheet" href="style.css" />\n\
    </head>\n\n\
    <body>\n\n\
')

# MAIN TITLE
html.write('<h1>The interactive periodic table of the elements</h1>\n')
html.write('<h3>Hover your mouse pointer to reveal more information</h3>\n')


# TABLE INIT
html.write('<table>\n')
k = 0

def cell_definition(e):
    anum = "<span class='atomicnumber'> %s </span>"%e['Atomic Number']
    symb = "<span class='symbol'> %s </span>"%e['Symbol']
    name = "<span class='atomicnumber'> %s </span>"%e['Element']
    if e['Phase'] == 'gas':
        phase = '<i class="fa fa-fire"></i> Gas'
    if e['Phase'] == 'solid':
        phase = '<i class="fa fa-diamond"></i> Solid'
    if e['Phase'] == 'liq':
        phase = '<i class="fa fa-tint"></i> Liquid'
    if e['Phase'] == 'artificial':
        phase = '<i class="fa fa-flask"></i> Artificial'

    discoverer = '<i class="fa fa-graduation-cap"></i> %s - %s'%(e['Discoverer'], e['Year of Discovery'])
    electron = '<i class="fa fa-dot-circle-o"></i> %s'%(e['Electron Configuration'])

    meta = '<div class="bg"> <p class="title">%s </p>\
        <p><i class="fa fa-globe"></i> %s</br>\
        <i class="fa fa-balance-scale"></i> %s</br>\
        %s</br>\
        %s</br>\
        %s</br>\
        </p>\
        </div>'%(e['Element'], e['Type'], e['Atomic Weight'], phase, electron, discoverer)

    cell = '\t\t<td class="%s"><div class="cell-content">%s</br>%s</br>%s</div>%s</td>\n'\
        %(re.sub('[\s+]', '', e['Type']), name, symb, anum, meta)
    return cell



# CLASSICAL ELEMENTS
with open('periodic-table.csv') as ptable:
    ptable = csv.DictReader(ptable, delimiter=',')
    for e in ptable:

        cell = cell_definition(e)

        if int(e['Display Row']) < 8:

            for i in xrange(int(e['Group'])-k-1):
                html.write('\t\t<td class="empty"></td>\n')

            if int(e['Display Column']) == 1:
                html.write('\t<tr>\n')
                html.write(cell)

            elif int(e['Display Column']) == 18:
                html.write(cell)
                html.write('\t</tr>\n')

            else:
                html.write(cell)

            k = int(e['Group'])

# TRANSITION
html.write('\t<tr>\n')
for i in xrange(18):
    html.write('\t\t<td class="empty"></td>\n')
html.write('\t</tr>\n')
k = 0

# ARTIFICIAL ELEMENTS
with open('periodic-table.csv') as ptable:
    ptable = csv.DictReader(ptable, delimiter=',')
    for e in ptable:

        cell = cell_definition(e)

        if int(e['Display Row']) >= 8:

            if int(e['Display Column']) == 3:
                html.write('\t<tr>\n')
                for i in xrange(2):
                    html.write('\t\t<td class="empty"></td>\n')
                html.write(cell)

            elif int(e['Display Column']) == 17:
                html.write(cell)
                html.write('\t\t<td class="empty"></td>\n')
                html.write('\t</tr>\n')

            else:
                html.write(cell)


# CLOSE ALL
html.write('</table>\n')

html.write('<h4><a id="github" target="_blank" href="https://github.com/leonard-seydoux"><i class="fa fa-github"></i>leonard-seydoux</a></h4>\n')

html.write('</body>\n</html>')
html.close()
