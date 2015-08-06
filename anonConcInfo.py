#!/usr/bin/env python

__author__ = 'waldo'

import pickle, csv, random, sys

def get_anon_id(huid, id_dict, id_view):
    """
    Return an anonymized id for the supplied HUID.

    This routine will look for a particular huid to see if there has already been an anonymized id generate for it; if
    not a new anonymized id will be generated and added to the huid->anon_id dictionary. The anonymized id will
    then be returned.
    :param huid:  huid to be matached with an anonymized, random id
    :param id_dict:  Dictionary of existing huid->anon_id values
    :param id_view: A view into the values of the id_dict, insuring that new values generated are not re-uses of old values
    :return: the anonymized id that is associated with the huid
    """
    anon_id = ''
    if huid in id_dict:
        anon_id = id_dict[huid]
    else:
        anon_id = random.randint(1,1000000)
        while anon_id in id_view:
            anon_id = random.randint(1, 1000000)
        id_dict[huid] = anon_id

    return anon_id

def strip_prefix(huid):
    """
    Strip the alphabetic prefix on the HUIDs

    The HUIDs supplied were prefixed with either a "U" or "HU"; this routine strips those
    :param huid:  the HUID supplied in the .csv file
    :return: the numeric portion of the id
    """
    if huid[0] == 'U':
        return huid[1:]
    elif huid[0] == 'H':
        return huid[2:]
    else:
        return huid

def main(infile_name, outfile_name, id_fname, id_outname):
    """
    Driver program for the file conversion

    Taking the names of the input file, the output file, and the file containing the pickle of the id_dictionary, this
    routine will open the files, recreate the dictionary, write the header (without the name portion ) to the oubput
    file, and then take each line from the input file, replace the huid with the anonymized id, and delete the student
    name, and write the result to the output file. The pickle file is written as well, to deal with any new ids that
    get generated.
    :param infile_name: Name of the data file to be converted
    :param outfile_name: Name of the file to contain the anonymized information. If the file already exists, it will
    be over-written
    :param id_fname: Name of the file containing the pickle of the dictionary from huid->anonymized_id
    :param id_outname: Name of the file that will contain the pickle of the resulting huid->anonymized_id dictionary
    :return: None
    """
    fin = csv.reader(open(infile_name, 'rU'))
    fout = csv.writer(open(outfile_name, 'w'))

    id_dict = pickle.load(open(id_fname, 'rU'))
    id_view = id_dict.viewvalues()

    header = fin.next()
    header.pop(1)
    fout.writerow(header)

    for l in fin:
        huid = strip_prefix(l[0])
        l[0] = get_anon_id(huid, id_dict, id_view)
        l.pop(1)
        fout.writerow(l)

    pickle.dump(id_dict, open(id_outname, 'w'))

if __name__ == '__main__':
    infile_name = sys.argv[1]
    outfile_name = sys.argv[2]
    pickle_file = sys.argv[3]
    pickle_out = sys.argv[4]
    main(infile_name, outfile_name, pickle_file, pickle_out)
