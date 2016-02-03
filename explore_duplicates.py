import os, json

os.mkdir('duplicates')

def make_links(paths, i):
    dest = 'duplicates/{0}'.format(i)
    # os.mkdir(dest)
    map(lambda (j, path): os.link(path, '{0}_img_{1}'.format(dest, j)), enumerate(paths))
    with open('duplicates/files.txt'.format(dest), 'a') as f:
        f.write('\n'.join(paths) + '\n')

with open('duplicates.txt') as f:
    for i, line in enumerate(f):
        pics = json.loads(line)
        make_links(pics, i)