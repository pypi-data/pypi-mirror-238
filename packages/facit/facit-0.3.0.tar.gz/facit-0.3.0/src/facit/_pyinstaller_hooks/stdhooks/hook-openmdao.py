from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("openmdao")
hiddenimports = [
    "numpy.distutils.ccompiler",
    "numpy.distutils.log",
    "numpy.distutils.misc_util",
    "numpy.distutils.npy_pkg_config",
    "numpy.distutils.unixccompiler",
    "distutils.unixccompiler",
]
