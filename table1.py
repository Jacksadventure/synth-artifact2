#!/usr/bin/env python3
import sys
import allfiles as files
import Levenshtein
import pudb

class Dist:
    def __init__(self, n1, n2):
        #if '6234' in n1: pudb.set_trace()
        with open(n1, 'rb') as f1: t1 = f1.read()
        with open(n2, 'rb') as f2: t2 = f2.read()
        self.d1 = len(t1)
        self.d2 = len(t2)
        self.editops = Levenshtein.editops(t1,t2)
        self.delops = [c for c in self.editops if c[0] == 'delete']

tool_names='bRepair DDMin DDMaxG Antlr DDMax'.split(' ')
formats = ['ini', 'json', 'sexp', 'tinyc']

print_format = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"

#print(print_format % ('tool', 'fmt',
#                  'valid', 'invalid', 'repaired',
#                  'len_valid', 'len_invalid', 'len_repaired',
#                  'ops_valid_to_invalid',
#                  'ops_valid_to_repaired',
#                  'ops_invalid_to_repaired',
#                  'delops_valid_to_invalid',
#                  'delops_valid_to_repaired',
#                  'delops_invalid_to_repaired',
#                      ))

my_repaired = {k: {v:0 for v in formats} for k in tool_names}
my_notrepaired = {k: {v:0 for v in formats} for k in tool_names}

for ntool in tool_names:
    for fmt in formats:
        for valid, invalid, result in files.produce_files(ntool, fmt):
            tool, repaired = result
            l0 = Dist(valid, invalid)
            len_valid = l0.d1
            len_invalid = l0.d2
            l1 = Dist(valid, repaired)
            len_repaired = l1.d2
            l2 = Dist(invalid, repaired)
            if len_repaired > 0:
                my_repaired[ntool][fmt] += 1
            else:
                my_notrepaired[ntool][fmt] += 1
            #print(print_format % (tool, fmt,
            #      valid, invalid, repaired,
            #      len_valid, len_invalid, len_repaired,
            #      len(l0.editops),
            #      len(l1.editops),
            #      len(l2.editops),
            #      len(l0.delops),
            #      len(l1.delops),
            #      len(l2.delops)))

print('' + '\t|' + '\t'.join(formats))
for tool in tool_names:
    print(tool + '\t|' + '\t'.join([str(my_repaired[tool][t]) for t in formats]))
    #print('\t'.join([my_repaired[tool][t] for t in formats]))
    #print()
