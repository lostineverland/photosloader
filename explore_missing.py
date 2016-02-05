import os, sys, json, toolz

src = sys.argv[-1]
os.mkdir(src)

def make_links(paths, i):
    dest = '{0}/{1}'.format(src, i)
    # os.mkdir(dest)
    map(lambda (j, path): os.link(path, '{0}_img_{1}.{2}'.format(dest, j, path[-3:])), enumerate(paths))
    with open('{0}/files.txt'.format(src), 'a') as f:
        f.write('\n'.join(paths) + '\n')

with open('missing_data.json') as f:
    notCounter = lambda k: k != 'counter'
    lines = toolz.keyfilter(notCounter, json.loads(f.read())).values()
    lines.sort()
    for i, line in enumerate(lines):
        pics = line
        make_links(pics, i)