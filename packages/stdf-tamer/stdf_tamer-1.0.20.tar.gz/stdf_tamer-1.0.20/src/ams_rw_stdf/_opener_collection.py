import bz2
import gzip
import lzma

_opener = {".bz2": bz2.open, ".gz": gzip.open, ".stdf": open, ".xz": lzma.open, ".std": open}
