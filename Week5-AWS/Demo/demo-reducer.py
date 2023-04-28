#!/usr/bin/python3

import sys

#  Current key being processed, and accumulated counts
current_docid = None
current_longest_term = None
current_count_all = 0
current_count_filtered = 0

for line in sys.stdin:
    docid, term = line.strip('\n').split('\t')

    if current_docid == docid:
        current_count_all += 1
        if (len(term) == 0):
            current_count_filtered += 1
        if len(term) > len(current_longest_term):
            current_longest_term = term
    else:
        # Seeing either a new different key, or the first one
        if current_docid:
            print('%s\t%s\t%s\t%s' % (docid,
                                      current_longest_term,
                                      len(current_longest_term),
                                      1.0 * current_count_filtered/current_count_all))
        current_docid = docid
        current_count_all = 1
        if len(term) == 0:
            current_count_filtered = 1
        else:
            current_count_filtered = 0
        current_longest_term = term
            
if current_count_all > 0:
    print('%s\t%s\t%s\t%s' % (docid,
                              current_longest_term,
                              len(current_longest_term),
                              1.0* current_count_filtered/current_count_all))

