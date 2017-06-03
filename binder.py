import argparse
import base64
import struct

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="file to encode",
                    type=str)
parser.add_argument("out_file", help="Zone file",
                    type=str)
args = parser.parse_args()

_filename = args.input_file
record_size = 189

parts = []
with open(_filename, 'rb') as fp:
    complete = False
    while not complete:
        buf = fp.read(record_size)
        ebuf = base64.b64encode(buf)
        parts.append(ebuf)
        if len(buf) < record_size:
            complete = True

manifest = base64.b64encode(struct.pack('!I', len(parts)))

with open(args.out_file, 'w') as outfp:
    outfp.write('$TTL\t86400\n')
    outfp.write('@\tIN\tSOA\tmovies.zzyzxgazette.xyz. root.zzyzxgazette.xyz. (1 604800 86400 2419200 86400)\n')
    outfp.write('@\tIN\tNS\tmovies.zzyzxgazette.xyz.\n')
    outfp.write("@\tIN\tTXT\t\"v=spf1 -all\"\n")
    outfp.write('manifest\tIN TXT\t"{}"\n'.format(manifest))
    for index in range(len(parts)):
        outfp.write('{}\tIN TXT\t"{}"\n'.format(index, parts[index]))


