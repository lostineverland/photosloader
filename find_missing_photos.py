'''An extensive photo import went wrong (missing photos), and I'm selecting the files which were imported.
The list added_paths matches the correct timestamp for the import. It was generated from this command:

ll /Users/Shared/Photo\ Library/Family\ Photo\ Library.photoslibrary/Masters/2015/08/25/

Then, culled for timestamp and to pick the right paths.

The actual files from this import are culled from the file 'added.files' by comparing them to 'added_paths'. The
file 'added.files' was generated with:

find /Users/Shared/Photo\ Library/Family\ Photo\ Library.photoslibrary/Masters/2015/08/25/ -type f > added.files
find /Users/Shared/Photo\ Library/Family\ Photo\ Library.photoslibrary/Masters/2015/08/26/ -type f >> added.files
'''
import os
from collections import Counter

base_path = '/Users/Shared/Photo\ Library/Family\ Photo\ Library.photoslibrary/Masters/2015/08/25'

added_paths = '''
    20150825-221320
    20150825-221433
    20150825-221636
    20150825-221655
    20150825-221741
    20150825-222610
    20150825-225512
    20150825-225537
    20150825-225746
    20150825-225911
    20150825-230054
    20150825-230216
    20150825-230306
    20150825-230659
    20150825-232830
    20150825-233258
    20150825-234029
    /26/
'''.split()

containsPath = lambda s: max(map(lambda x: x in s, added_paths))
fileIsValid = lambda s: containsPath(s)
imported_images = []
with open('select_added_files.txt', 'w') as g:
    with open('added.files') as f:
        for line in f:
            if fileIsValid(line):
                # print line
                imported_images.append(line.rsplit('/', 1)[-1])
                g.write(line)

dest_images = Counter(imported_images)

''' By the same token, the list of files that were imported come from the 'import.log'
  The import.log lists all of the paths that were used, so we then follow the same measure
  to obtain the source_files by filtering source.files with source_paths

 find /Users/Shared/Reconcile_Photos/Masters/2010 -type f > source.files
 find /Users/Shared/Reconcile_Photos/Masters/2011 -type f >> source.files

'''

source_paths = map(lambda x: x[4:], '''
    /Users/Shared/Reconcile_Photos/Masters/2010/CLE ROSE
    /Users/Shared/Reconcile_Photos/Masters/2010/Dec 1, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Dec 12, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Dec 2, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Dec 28, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Dec 4, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Dec 8, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Feb 1, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/I01CANON
    /Users/Shared/Reconcile_Photos/Masters/2010/I02CANON
    /Users/Shared/Reconcile_Photos/Masters/2010/I03CANON
    /Users/Shared/Reconcile_Photos/Masters/2010/I04CANON
    /Users/Shared/Reconcile_Photos/Masters/2010/Jan 2, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Jul 14, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Jul 14, 2010_2
    /Users/Shared/Reconcile_Photos/Masters/2010/Jul 18, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Jul 30, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Jul 31, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Jul 7, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Jul 7, 2010_2
    /Users/Shared/Reconcile_Photos/Masters/2010/Jul 8, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Jun 12, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Jun 19, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Jun 22, 2009
    /Users/Shared/Reconcile_Photos/Masters/2010/Jun 25, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/MachuPicchu
    /Users/Shared/Reconcile_Photos/Masters/2010/May 15, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/May 23, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/May 24, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/May 9, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Mi disco
    /Users/Shared/Reconcile_Photos/Masters/2010/Navidades con Abuelos
    /Users/Shared/Reconcile_Photos/Masters/2010/Nov 14, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Nov 14, 2010_2
    /Users/Shared/Reconcile_Photos/Masters/2010/Nov 2, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Nov 26, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Oct 10, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Oct 20, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Oct 30, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Oct 31, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Oct 31, 2010_2
    /Users/Shared/Reconcile_Photos/Masters/2010/Sep 11, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Sep 12, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Sep 17, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Sep 6, 2010
    /Users/Shared/Reconcile_Photos/Masters/2010/Washington DC- Visas
    /Users/Shared/Reconcile_Photos/Masters/2011/03/09/20110309-182049
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-232308
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234211
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234219
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234222
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234226
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234229
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234233
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234237
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234240
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234244
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234248
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234338
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234343
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234347
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234351
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234355
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234401
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234409
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234412
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234416
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234422
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234427
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234430
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234434
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234437
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234441
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234445
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234448
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234452
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234456
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234500
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234504
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234508
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234512
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234517
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234522
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234526
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234531
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234535
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234541
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234546
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234550
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234554
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234559
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234603
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234607
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234612
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234615
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234619
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234623
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234628
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234631
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234849
    /Users/Shared/Reconcile_Photos/Masters/2011/03/13/20110313-234853
    /Users/Shared/Reconcile_Photos/Masters/2011/03/15/20110315-111242
'''.split('\n')[1:-1])

containsPath = lambda s: max(map(lambda x: x in s, source_paths))
original_images = []
with open('select_source_files.txt', 'w') as g:
    with open('source.files') as f:
        for line in f:
            if fileIsValid(line):
                original_images.append(line.rsplit('/', 1)[-1])
                g.write(line)

source_images = Counter(original_images)

missing = set(source_images.keys()) - set(dest_images.keys())
common = set(source_images.keys()) - missing
source_common_count = sum(map(source_images.get, common))
dest_common_count = sum(map(source_images.get, common))
print "source common count: {0}".format(source_common_count)
print "destination common count: {0}".format(dest_common_count)
print "The only missing files are contained in the 'missing' variable", source_common_count == dest_common_count

'''This doesn't add up, according to the count in photos app, there are 342 photos missing,
but looking at the discrepancy in the files contained in the 'Family Photos Library' Masters
folder, there are only 24 files missing. all of them MOVs (the var 'missing' above). And the source_images counter
shows that there's only one of each of the missing files.

    ['100_6823.MOV\n',
     '100_6825.MOV\n',
     '100_6826.MOV\n',
     '100_6827.MOV\n',
     '100_6828.MOV\n',
     '100_6829.MOV\n',
     '100_6854.MOV\n',
     '100_6900.MOV\n',
     '100_6906.MOV\n',
     '102_6907.MOV\n',
     '102_6908.MOV\n',
     '102_6912.MOV\n',
     '102_6915.MOV\n',
     '102_7032.MOV\n',
     '102_7033.MOV\n',
     '102_7034.MOV\n',
     '102_7035.MOV\n',
     '102_7036.MOV\n',
     '102_7037.MOV\n',
     '102_7063.MOV\n',
     '102_7158.MOV\n',
     '102_7376.MOV\n',
     '103_7445.MOV\n',
     '103_7498.MOV\n']
'''

containsPath = lambda s: max(map(lambda x: x in s, missing))
with open('source.files') as f:
    for line in f:
        if fileIsValid(line):
            print line

'''The missing MOVs were quite inconsequential and, in facts, did not belong to me. These were files copied
from someone else's camera, and I didn't care to have them.
'''
