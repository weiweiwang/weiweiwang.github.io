#!/usr/bin/python
# copy from import_sogou_celldict.py
# thanks for the reverse engineering efforts of following projects/peoples:
# http://code.google.com/p/imewlconverter
# http://code.google.com/p/ibus-cloud-pinyin
# http://forum.ubuntu.org.cn/viewtopic.php?f=8&t=250136&start=0

import struct
import os, sys
from optparse import OptionParser


def read_utf16_str (f, offset=-1, len=2):
    if offset >= 0:
        f.seek(offset)
    str = f.read(len)
    return str.decode('UTF-16LE')

def read_uint16 (f):
    return struct.unpack ('<H', f.read(2))[0]

def get_word_from_sogou_cell_dict (fname):
    f = open (fname, 'rb')
    file_size = os.path.getsize (fname)
    
    hz_offset = 0
    mask = struct.unpack ('B', f.read(128)[4])[0]
    if mask == 0x44:
        hz_offset = 0x2628
    elif mask == 0x45:
        hz_offset = 0x26c4
    else:
        sys.exit(1)
    
    title   = read_utf16_str (f, 0x130, 0x338  - 0x130)
    type    = read_utf16_str (f, 0x338, 0x540  - 0x338)
    desc    = read_utf16_str (f, 0x540, 0xd40  - 0x540)
    samples = read_utf16_str (f, 0xd40, 0x1540 - 0xd40)
    
    py_map = {}
    f.seek(0x1540+4)
    
    while 1:
        py_code = read_uint16 (f)
        py_len  = read_uint16 (f)
        py_str  = read_utf16_str (f, -1, py_len)
    
        if py_code not in py_map:
            py_map[py_code] = py_str
    
        if py_str == 'zuo':
            break
    
    f.seek(hz_offset)
    while f.tell() != file_size:
        word_count   = read_uint16 (f)
        pinyin_count = read_uint16 (f) / 2
    
        py_set = []
        for i in range(pinyin_count):
            py_id = read_uint16(f)
            py_set.append(py_map[py_id])
        py_str = "'".join (py_set)
    
        for i in range(word_count):
            word_len = read_uint16(f)
            word_str = read_utf16_str (f, -1, word_len)
            f.read(12)  # simply ignore word frequence info
            yield py_str, word_str

    f.close()

def batch_convert(sogou_dict_dir,mmseg_dict_dir,file_ext_list):
    print "batch converting:%s -> %s"% (sogou_dict_dir,mmseg_dict_dir)
    file_list = [os.path.normcase(f)
                for f in os.listdir(sogou_dict_dir)]
    file_list = [os.path.join(sogou_dict_dir, f)
                for f in file_list
                if os.path.splitext(f)[1] in file_ext_list]
    for file in file_list:
        print "converting:%s" %(file)
        generator = get_word_from_sogou_cell_dict (file)
        name=os.path.splitext(file)[0][len(sogou_dict_dir):]
        mmseg_dict_file=os.path.join(mmseg_dict_dir,"words-%s.dic"%(name))
        output=open(mmseg_dict_file,'w')
        for py_str,word_str in generator:
            output.write("%s\n"%(word_str.encode('utf-8')))
        output.close()
    print 'done~'
def main ():
    usage_str = "usage: %prog sogou_dict_dir mmseg_dict_dir"
    version_str = "%prog 1.0.0"
    parser = OptionParser(usage=usage_str, version=version_str)
#    parser.add_option("-f", "--from", dest="sender", default="",
#        help="set sender", type="string")
#    parser.add_option("-t", "--to", action="append", dest="receivers", default=[],
#        help="add receiver", type="string")
#    parser.add_option("-a", "--attach", action="append", dest="attachments", default=[],
#        help="add attachment", type="string")
#    parser.add_option("-b", "--body",dest="body", default="",
#        help="set mail body,read from stdin if not set", type="string")
#    parser.add_option("-r","--rich",dest="rich",default=False,action="store_true",help="send html body")
#    parser.add_option("-p","--plain",dest="rich",action="store_false",help="send plain body,default")

    (options, args) = parser.parse_args()
    if len (args) != 2:
        parser.error("missing required params")
        sys.exit (1)
    batch_convert(args[0],args[1],['.scel'])

if __name__ == "__main__":
    main()
