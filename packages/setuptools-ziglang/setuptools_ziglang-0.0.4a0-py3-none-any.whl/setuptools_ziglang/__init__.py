from setuptools_ziglang import zigcompiler

import os
import sys

# Add the Zig language and compiler to the list of compilers
def patch_distutils_ccompiler(module):
    module.ccompiler.compiler_class['zig'] = ("zigcompiler", "ZigCompiler", "The Zig language compiler")
    module.ccompiler.CCompiler.language_map[".zig"] = "zig"
    module.ccompiler.CCompiler.language_order.insert(0, "zig")
    module.zigcompiler = zigcompiler
    # Users can set this if they want Zig as the default compiler. May be useful if the compiler mutates
    # because of other extensions
    if os.getenv("SETUPTOOLS_FORCE_ZIG", None):
        module.ccompiler._default_compilers = (
            ('cygwin.*', 'zig'),
            ('posix', 'zig'),
            ('nt', 'zig'),
        )



import setuptools._distutils as dist_module
patch_distutils_ccompiler(dist_module)

# Patch distutils stdlib unless we're in a Python version where they've been removed (>= 3.12)
if sys.version_info[1] >= 12:
    try:
        import distutils
        patch_distutils_ccompiler(distutils)
    except (ModuleNotFoundError, ImportError) as ModuleImportError:
        pass


