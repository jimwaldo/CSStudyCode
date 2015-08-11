__author__ = 'waldo'

import sys, csv
from anonConcInfo import strip_prefix

def build_id_set(from_file, with_filter = None):
    return_set = set()
    for l in from_file:
        rid = l[0]
        if None != with_filter:
            rid = with_filter(rid)
        return_set.add(rid)
    return return_set

def main(conc_info_1, conc_info_2, class_file):
    conc_info_1.next()
    conc_info_2.next()
    c1_set = build_id_set(conc_info_1)
    c2_set = build_id_set(conc_info_2, strip_prefix)

    class_file.next()

    for l in class_file:
        if (l[0] not in c1_set) and (l[0] not in c2_set):
            print l

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'need 3 file names'
        quit()

    c_info_1 = sys.argv[1]
    c_info_2 = sys.argv[2]
    classfile = sys.argv[3]

    c1_in = csv.reader(open(c_info_1, 'rU'))
    c2_in = csv.reader(open(c_info_2, 'rU'))
    class_in = csv.reader(open(classfile, 'rU'))
    main(c1_in, c2_in, class_in)
