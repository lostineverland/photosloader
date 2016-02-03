import os, hashlib, json

def hash_dir(path_to_files, hash_list={}, total=0):
    filenames = os.listdir(path_to_files)
    total += len(filenames)
    print "count: {0}, path: {1}".format(total, path_to_files)
    for filename in filenames:
        filename_full_path = '/'.join([path_to_files, filename])
        with open('/'.join([path_to_files, filename])) as f:
            ss = f.read()
            sha1 = hashlib.sha1(ss).hexdigest()
            md5 = hashlib.md5(ss).hexdigest()
            hash_list.setdefault(sha1 + md5, []).append(filename_full_path)
    return hash_list, total

with open('path_list.txt') as f:
    hash_list = {}
    total = 0
    for i, path in enumerate(f):
        print i,
        hash_list, total = hash_dir(path[:-1], hash_list, total)

with open('duplicates.txt', 'w') as f:
    for i in hash_list.values():
        if len(i) >= 2:
            f.write(json.dumps(i) + '\n')

with open('data.json', 'w') as f:
    f.write(json.dumps(hash_list))
