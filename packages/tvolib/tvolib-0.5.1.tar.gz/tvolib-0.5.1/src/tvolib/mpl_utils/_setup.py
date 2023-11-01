__all__ = ["setup"]

import atexit
import os
import shutil
import tempfile
from importlib.resources import files

import matplotlib as mpl
import matplotlib.pyplot as plt


def _checkdep_usetex(s):
    return s and shutil.which("tex")


def setup(tex=False, cache=False, **kw):
    plt.style.use(files("tvolib.mpl_utils") / "data" / "mpl_utils.mplstyle")
    plt.rc("text", usetex=_checkdep_usetex(tex))
    if cache:
        # Quick fix for matplotlib's tex cache in multiprocessing
        mpldir = tempfile.mkdtemp()
        atexit.register(shutil.rmtree, mpldir)
        umask = os.umask(0)
        os.umask(umask)
        os.chmod(mpldir, 0o777 & ~umask)
        os.environ["HOME"] = mpldir
        os.environ["MPLCONFIGDIR"] = mpldir

        class TexManager(mpl.texmanager.TexManager):
            texcache = os.path.join(mpldir, "tex.cache")

        mpl.texmanager.TexManager = TexManager
