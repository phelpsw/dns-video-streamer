import base64
import struct
import time

import dns.resolver

parser = argparse.ArgumentParser()
parser.add_argument("--host", help="Server containing file of interest",
                    type=str, default='caramelsundae.williamslabs.com'))
parser.add_argument("--outfile", help="Output file",
                    type=str, default='out.mp4')
args = parser.parse_args()

uri = args.host

answer = dns.resolver.query('manifest.' + uri, 'TXT')
for data in answer:
    (segments,) = struct.unpack('!I', base64.b64decode(data.strings[0]))

payload = []
i = 0
while i < segments:
    print i
    complete = False
    while not complete:
        try:
            answer = dns.resolver.query('{}.{}'.format(i, uri), 'TXT')
            for data in answer:
                seg = base64.b64decode(data.strings[0])
                payload.append(seg)
                complete = True
                i += 1
        except dns.resolver.NoNameservers:
            print('Retrying {}'.format(i))
            time.sleep(5)
            pass


with open(args.outfile, 'wb') as fp:
    for i in range(len(payload)):
        fp.write(payload[i])
