import struct
from app_paths import DefinePathsClass
import configparser
from os import path

#reutilizado de:
#https://github.com/Scondo/purepng/blob/master/png/iccp.py


class GetICCtags(object):

    #def __init__(self, filename, string):

    def __init__(self):

        self.config = configparser.ConfigParser()
        path_conf_file = DefinePathsClass.create_configuration_paths("configuration.ini")
        if path.exists(path_conf_file):
            self.config.read(path_conf_file)
            self.default_gamma = float(self.config['SAMPLING']['DEFAULT_GAMMA'])
        else:
            self.default_gamma = 2.2

    def group(self, s, n):
        """Repack iterator items into groups"""
        # See http://www.python.org/doc/2.6/library/functions.html#zip
        return zip(*[iter(s)] * n)

    def readICCdatetime(self, s):
        """Convert from 12 byte ICC representation of dateTimeNumber to
        ISO8601 string. See [ICC 2004] 5.1.1"""
        return '%04d-%02d-%02dT%02d:%02d:%02dZ' % struct.unpack('>6H', s)

    def readICCXYZNumber(self, s):
        """Convert from 12 byte ICC representation of XYZNumber to (x,y,z)
        triple of floats.  See [ICC 2004] 5.1.11"""
        return self.s15f16l(s)

    def s15f16l(self, s):
        """Convert sequence of ICC s15Fixed16 to list of float."""

        # Note: As long as float has at least 32 bits of mantissa, all
        # values are preserved.
        n = len(s) // 4
        t = struct.unpack('>%dl' % n, s)
        return map((2**-16).__mul__, t)

    def fromFile(self, inp, name='<unknown>'):
        # See [ICC 2004]
        profile = inp.read(128)
        if len(profile) < 128:
            print("too short")
        size, = struct.unpack('>L', profile[:4])
        profile += inp.read(size - len(profile))
        return self.fromString(profile, name)

    def readICCFile(self, filename):

        with open(filename, 'rb') as f:
            buffer = f.read()
            return self.fromString(buffer)

    def getGamma(self,file):
        gamma = self.default_gamma
        if file is not None:
            tag = self.fromString(file)
            if 'rTRC' in tag:
                gamma = tag['rTRC'][1]['gamma']
        return float(gamma)

    def fromString(self, profile, name='<unknown>'):
        d = dict()
        if len(profile) < 128:
            print("ICC Profile is too short.")
        d.update(dict(
          zip(['size', 'preferredCMM', 'version',
               'profileclass', 'colourspace', 'pcs'],
              struct.unpack('>L4sL4s4s4s', profile[:24]))))
        if len(profile) < d['size']:
            print(
              'Profile size declared to be %d, but only got %d bytes' %
              (d['size'], len(profile)))
        d['version'] = '%08x' % d['version']
        d['created'] = self.readICCdatetime(profile[24:36])
        d.update(dict(
          zip(['acsp', 'platform', 'flag', 'manufacturer', 'model'],
              struct.unpack('>4s4s3L', profile[36:56]))))
        if d['acsp'] != self.strtobytes('acsp'):
            print('acsp field not present (not an ICC Profile?).')
        d['deviceattributes'] = profile[56:64]
        d['intent'], = struct.unpack('>L', profile[64:68])
        d['pcsilluminant'] = self.readICCXYZNumber(profile[68:80])
        d['creator'] = profile[80:84]
        d['id'] = profile[84:100]
        ntags, = struct.unpack('>L', profile[128:132])
        d['ntags'] = ntags
        fmt = '4s2L' * ntags
        # tag table
        tt = struct.unpack('>' + fmt, profile[132:132 + 12 * ntags])
        tt = self.group(tt, 3)

        # Could (should) detect 2 or more tags having the same sig.  But
        # we don't.  Two or more tags with the same sig is illegal per
        # the ICC spec.

        # Convert (sig,offset,size) triples into (sig,value) pairs.
        rawtag = list(map(lambda x: (x[0], profile[x[1]:x[1] + x[2]]), tt))
        rawtagtable = rawtag
        rawtagdict = dict(rawtag)
        tag = dict()
        # Interpret the tags whose types we know about
        for sig, v in rawtag:
            sig = self.bytestostr(sig)
            if sig in tag:
                print("Duplicate tag %r found.  Ignoring." % sig)
                continue
            v = self.ICCdecode(v)
            if v is not None:
                tag[sig] = v

        return tag

    def ICCdecode(self, s):
        """Take an ICC encoded tag, and dispatch on its type signature
        (first 4 bytes) to decode it into a Python value.  Pair (*sig*,
        *value*) is returned, where *sig* is a 4 byte string, and *value* is
        some Python value determined by the content and type.
        """
        sig = self.bytestostr(s[0:4].strip())
        f = dict(text=self.RDtext,
                 XYZ=self.RDXYZ,
                 curv=self.RDcurv,
                 #vcgt=self.RDvcgt,
                 sf32=self.RDsf32,
                 )
        if sig not in f:
            return None
        return (sig, f[sig](s))


    def RDtext(self, s):
        """Convert ICC textType to Python string."""

        # Note: type not specified or used in [ICC 2004], only in older
        # [ICC 2001].
        # See [ICC 2001] 6.5.18
        assert s[0:4] == self.strtobytes('text')
        return s[8:-1]


    def RDcurv(self, s):
        """Convert ICC curveType."""

        # See [ICC 2001] 6.5.3
        assert s[0:4] == self.strtobytes('curv')
        count, = struct.unpack('>L', s[8:12])
        if count == 0:
            return dict(gamma=1)
        table = struct.unpack('>%dH' % count, s[12:])
        if count == 1:
            return dict(gamma=table[0] * 2 ** -8)
        return table


    def RDvcgt(self, s):
        """Convert Apple CMVideoCardGammaType."""

        # See
        # http://developer.apple.com/documentation/GraphicsImaging/Reference/
        #         ColorSync_Manager/Reference/reference.html#//apple_ref/c/
        #         tdef/CMVideoCardGammaType
        assert s[0:4] == self.strtobytes('vcgt')
        tagtype, = struct.unpack('>L', s[8:12])
        if tagtype != 0:
            return s[8:]
        if tagtype == 0:
            # Table.
            _, count, size = struct.unpack('>3H', s[12:18])
            if size == 1:
                fmt = 'B'
            elif size == 2:
                fmt = 'H'
            else:
                return s[8:]
            l = len(s[18:]) // size
            t = struct.unpack('>%d%s' % (l, fmt), s[18:])
            t = self.group(t, count)
            return size, t
        return s[8:]

    def RDXYZ(self, s):
        """Convert ICC XYZType to rank 1 array of trimulus values."""

        # See [ICC 2001] 6.5.26
        assert s[0:4] == self.strtobytes('XYZ ')
        return self.readICCXYZNumber(s[8:])


    def RDsf32(self, s):
        """Convert ICC s15Fixed16ArrayType to list of float."""

        # See [ICC 2004] 10.18
        assert s[0:4] == self.strtobytes('sf32')
        return self.s15f16l(s[8:])


    def bytestostr(self, x): return str(x, 'iso8859-1')  # noqa
    def strtobytes(self, x): return bytes(x, 'iso8859-1')  # noqa
