

from pylab import *


lw=1
ms=6
fontsize = 8

matplotlib.rcParams['lines.linewidth'] = lw
matplotlib.rcParams['axes.linewidth'] = lw
matplotlib.rcParams['lines.markeredgewidth'] = lw
matplotlib.rcParams['lines.markersize'] = 6
matplotlib.rcParams['font.size'] = fontsize
matplotlib.rcParams['font.weight'] = 'normal'
matplotlib.rcParams['figure.figsize'] = 2, .2
matplotlib.rcParams['legend.fontsize'] = fontsize


pk_fmts = {"simple_key_value": 'o-', "unique_key_value": 's-'}
pk_colors = {"simple_key_value": 'blue', "unique_key_value": 'green'}
fk_fmts = {"simple": 'o-', "belongs_to": 's-'}
fk_colors = {"simple": 'blue', "belongs_to": 'green'}

relabel = {"simple_key_value": "No validation",
           "unique_key_value": "Validation",
           "simple": "No validation",
           "belongs_to": "Validation"}


cla()
axis('off')
text(0, 0, "Size of Key Domain")
savefig("pk-workload-xlabel.pdf", bbox_inches=0)

cla()
axis('off')
text(0, 0, "Number of Duplicate Records")
savefig("pk-workload-ylabel.pdf")
    
fig = figure()
figlegend = figure(figsize=(2.4, .3))
ax = fig.add_subplot(111)

lines = []
for k in pk_fmts:
    l, = ax.plot([0],[0], pk_fmts[k], label=relabel[k], color=pk_colors[k], markeredgecolor=pk_colors[k], markersize=8, markerfacecolor='None')
    lines.append(l)
figlegend.legend(lines, [relabel[k] for k in pk_fmts], loc="right", ncol=2, frameon=False, numpoints=1, labelspacing=1, handlelength=2)
figlegend.savefig('pk-legend-oneline.pdf', transparent=True, pad_inches=.05)
