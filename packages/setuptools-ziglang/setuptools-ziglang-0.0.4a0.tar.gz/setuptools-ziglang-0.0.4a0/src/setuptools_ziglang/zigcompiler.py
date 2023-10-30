from setuptools._distutils.ccompiler import CCompiler, gen_preprocess_options, gen_lib_options
from setuptools._distutils.dep_util import newer
from setuptools._distutils.errors import DistutilsExecError, CompileError, LinkError, LibError

import os
import sys
import logging
from sysconfig import get_config_var, get_config_vars

_logger = logging.getLogger(__name__)

# Much of this code is copied from UnixCCompiler (from setuptools._distutils)
# TODO: Cleanup unneeded code (and make it look nicer)

class ZigCompiler(CCompiler):
    compiler_type = 'zig'
    
    # Prefer using the PyPI zig binary, else fall back to the system zig
    try:
        import ziglang #noqa
        zig_bin = [sys.executable, '-m', 'ziglang',]
        _logger.info("Using ziglang module for compilation.")
    except (ImportError, ModuleNotFoundError) as ziglang_error:
        _logger.info("ziglang python module not found. Attempting to use system zig...")
        zig_bin = ['zig']

    executables = {
        'preprocessor': None,
        'compiler': zig_bin + ["build-obj"],  
        'compiler_so': zig_bin + ["build-obj"],
        'compiler_cxx': zig_bin + ["build-obj"],
        'linker_so': zig_bin + ["build-lib"],
        'linker_exe': zig_bin + ["build-lib"],
        'archiver': zig_bin + ["ar", "-cr"],
        'ranlib': None,
    }

    if sys.platform[:6] == "darwin":
        executables['ranlib'] = [*zig_bin, "ranlib"]

    src_extensions = [".zig", ".c", ".C", ".cc", ".s", ".S", ".cxx", ".cpp", ".m", ".mm"]
    obj_extension = ".o"
    static_lib_extension = ".a"
    shared_lib_extension = ".so"
    dylib_lib_extension = ".dylib"
    xcode_stub_lib_extension = ".tbd"
    static_lib_format = shared_lib_format = dylib_lib_format = "lib%s%s"
    xcode_stub_lib_format = dylib_lib_format
    if sys.platform.startswith("cygwin") or sys.platform.startswith("win32"):
        exe_extension = ".exe"

    def preprocess(
        self,
        source,
        output_file=None,
        macros=None,
        include_dirs=None,
        extra_preargs=None,
        extra_postargs=None,
    ):
        fixed_args = self._fix_compile_args(None, macros, include_dirs)
        ignore, macros, include_dirs = fixed_args
        pp_opts = gen_preprocess_options(macros, include_dirs)
        pp_args = self.preprocessor + pp_opts
        if output_file:
            pp_args.extend(['-o', output_file])
        if extra_preargs:
            pp_args[:0] = extra_preargs
        if extra_postargs:
            pp_args.extend(extra_postargs)
        pp_args.append(source)

        # reasons to preprocess:
        # - force is indicated
        # - output is directed to stdout
        # - source file is newer than the target
        preprocess = self.force or output_file is None or newer(source, output_file)
        if not preprocess:
            return

        if output_file:
            self.mkpath(os.path.dirname(output_file))

        try:
            self.spawn(pp_args)
        except DistutilsExecError as msg:
            raise CompileError(msg)

    def compile(
        self,
        sources,
        output_dir=None,
        macros=None,
        include_dirs=None,
        debug=0,
        extra_preargs=None,
        extra_postargs=None,
        depends=None,
        ):
        macros, objects, extra_postargs, pp_opts, build = self._setup_compile(
            output_dir, macros, include_dirs, sources, depends, extra_postargs
        )

        cc_args = pp_opts
        if debug:
            cc_args[:0] = ['-g']
        if extra_preargs:
            cc_args[:0] = extra_preargs

        for obj in objects:
            try:
                src, ext = build[obj]
            except KeyError:
                continue
            self._compile(obj, src, ext, cc_args, extra_postargs, pp_opts)

        # Return *all* object filenames, not just the ones we just built.
        return objects

    def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
        compiler_so = self.executables['compiler_so']
        obj_path = '-femit-bin={0}'.format(obj)
        try:
            self.spawn(compiler_so + cc_args + [src, obj_path] + extra_postargs)
        except DistutilsExecError as msg:
            raise CompileError(msg)

    def create_static_lib(
        self, objects, output_libname, output_dir=None, debug=0, target_lang=None
    ):
        objects, output_dir = self._fix_object_args(objects, output_dir)

        output_filename = self.library_filename(output_libname, output_dir=output_dir)

        if self._need_link(objects, output_filename):
            self.mkpath(os.path.dirname(output_filename))
            self.spawn(self.archiver + [output_filename] + objects + self.objects)

            # Not many Unices required ranlib anymore -- SunOS 4.x is, I
            # think the only major Unix that does.  Maybe we need some
            # platform intelligence here to skip ranlib if it's not
            # needed -- or maybe Python's configure script took care of
            # it for us, hence the check for leading colon.
            if self.ranlib:
                try:
                    self.spawn(self.ranlib + [output_filename])
                except DistutilsExecError as msg:
                    raise LibError(msg)
        else:
            _logger.debug("skipping %s (up-to-date)", output_filename)

    def link(
        self,
        target_desc,
        objects,
        output_filename,
        output_dir=None,
        libraries=None,
        library_dirs=None,
        runtime_library_dirs=None,
        export_symbols=None,
        debug=0,
        extra_preargs=None,
        extra_postargs=None,
        build_temp=None,
        target_lang=None,
    ):
        objects, output_dir = self._fix_object_args(objects, output_dir)
        fixed_args = self._fix_lib_args(libraries, library_dirs, runtime_library_dirs)
        libraries, library_dirs, runtime_library_dirs = fixed_args

        lib_opts = gen_lib_options(self, library_dirs, runtime_library_dirs, libraries)
        if not isinstance(output_dir, (str, type(None))):
            raise TypeError("'output_dir' must be a string or None")
        if output_dir is not None:
            output_filename = os.path.join(output_dir, output_filename)

        if self._need_link(objects, output_filename):
            ld_args = objects + self.objects + lib_opts + ["-femit-bin={0}".format(output_filename)]
            if debug:
                ld_args[:0] = ['-g']
            if extra_preargs:
                ld_args[:0] = extra_preargs
            if extra_postargs:
                ld_args.extend(extra_postargs)
            self.mkpath(os.path.dirname(output_filename))
            try:
                # Select a linker based on context: linker_exe when
                # building an executable or linker_so (with shared options)
                # when building a shared library.
                building_exe = target_desc == CCompiler.EXECUTABLE
                linker = (self.linker_exe if building_exe else self.linker_so)[:]

                self.spawn(linker + ld_args)
            except DistutilsExecError as msg:
                raise LinkError(msg)
        else:
            _logger.debug("skipping %s (up-to-date)", output_filename)

    def library_dir_option(self, dir):
        return "-L" + dir

    def runtime_library_dir_option(self, dir):
        if sys.platform[:6] == "darwin":
            from distutils.util import get_macosx_target_ver, split_version

            macosx_target_ver = get_macosx_target_ver()
            if macosx_target_ver and split_version(macosx_target_ver) >= [10, 5]:
                return "-Wl,-rpath," + dir
            else:  # no support for -rpath on earlier macOS versions
                return "-L" + dir
        elif sys.platform[:7] == "freebsd":
            return "-Wl,-rpath=" + dir
        elif sys.platform[:5] == "hp-ux":
            return [
                "-Wl,+s" if self._is_gcc() else "+s",
                "-L" + dir,
            ]

        # For all compilers, `-Wl` is the presumed way to
        # pass a compiler option to the linker and `-R` is
        # the way to pass an RPATH.
        if get_config_var("GNULD") == "yes":
            # GNU ld needs an extra option to get a RUNPATH
            # instead of just an RPATH.
            return "-Wl,--enable-new-dtags,-R" + dir
        else:
            return "-Wl,-R" + dir

    def library_option(self, lib):
        return "-l" + lib

    def find_library_file(self, dirs, lib, debug=0):
        r"""
        Second-guess the linker with not much hard
        data to go on: GCC seems to prefer the shared library, so
        assume that *all* Unix C compilers do,
        ignoring even GCC's "-static" option.

        >>> compiler = UnixCCompiler()
        >>> compiler._library_root = lambda dir: dir
        >>> monkeypatch = getfixture('monkeypatch')
        >>> monkeypatch.setattr(os.path, 'exists', lambda d: 'existing' in d)
        >>> dirs = ('/foo/bar/missing', '/foo/bar/existing')
        >>> compiler.find_library_file(dirs, 'abc').replace('\\', '/')
        '/foo/bar/existing/libabc.dylib'
        >>> compiler.find_library_file(reversed(dirs), 'abc').replace('\\', '/')
        '/foo/bar/existing/libabc.dylib'
        >>> monkeypatch.setattr(os.path, 'exists',
        ...     lambda d: 'existing' in d and '.a' in d)
        >>> compiler.find_library_file(dirs, 'abc').replace('\\', '/')
        '/foo/bar/existing/libabc.a'
        >>> compiler.find_library_file(reversed(dirs), 'abc').replace('\\', '/')
        '/foo/bar/existing/libabc.a'
        """
        lib_names = (
            self.library_filename(lib, lib_type=type)
            for type in 'dylib xcode_stub shared static'.split()
        )

        roots = map(self._library_root, dirs)

        searched = (
            os.path.join(root, lib_name)
            for root, lib_name in itertools.product(roots, lib_names)
        )

        found = filter(os.path.exists, searched)

        # Return None if it could not be found in any dir.
        return next(found, None)
   
    def set_default_flags(self) -> None:
        (
            cflags,
            ccshared,
            ldshared,
            shlib_suffix,
            ar_flags,
        ) = get_config_vars(
            'CFLAGS',
            'CCSHARED',
            'LDSHARED',
            'SHLIB_SUFFIX',
            'ARFLAGS',
        )
        
        # ldshared includes the executable that was used, so we need to remove it.
        ldshared = ldshared.split()
        ldshared = ldshared[1:]
        ldshared = ' '.join(ldshared)

        ar = ' '.join(self.executables['archiver'])

        if 'LDFLAGS' in os.environ:
            ldshared = ldshared + ' ' + os.environ['LDFLAGS']
        if 'CFLAGS' in os.environ:
            cflags = cflags + ' ' + os.environ['CFLAGS']
            ldshared = ldshared + ' ' + os.environ['CFLAGS']
        if 'ARFLAGS' in os.environ:
            archiver = ar + ' ' + os.environ['ARFLAGS']
        else:
            archiver = ar + ' ' + ar_flags

        # TODO: These flags may be better off in a different place
        zig_flags = '-fPIC -dynamic -lc -Bsymbolic'
        ##zig_flags = '-fPIC -fallow-shlib-undefined -dynamic -lc -Bsymbolic'
        if sys.platform.startswith("win32"):
            zig_flags += " " + "-target x86_64-windows-msvc"

        zig_build_obj = ' '.join(self.executables['compiler'])
        zig_compile    = zig_build_obj  + ' ' + zig_flags + ' ' + '-cflags' + ' ' + cflags + ' ' + '--'
        zig_compile_so = zig_build_obj  + ' ' + zig_flags + ' ' + '-cflags' + ' ' + cflags + ' ' + ccshared + ' ' + '--'
        
        zig_build_lib = ' '.join(self.executables['linker_so'])
        zig_linker_so  = zig_build_lib + ' ' + zig_flags + ' ' + '-flld' + ' ' + '-cflags' + ' ' + ldshared + ' ' + '--' 

        self.executables['compiler'] = zig_compile.split()
        self.executables['compiler_so'] = zig_compile_so.split()
        self.executables['linker_so'] = zig_linker_so.split()
        self.executables['archiver'] = archiver.split()

        self.set_executables(
            compiler=zig_compile,
            compiler_so=zig_compile_so,
            linker_so=zig_linker_so,
            archiver=archiver,
        )

        self.shared_lib_extension = shlib_suffix

