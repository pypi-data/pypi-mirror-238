#!/bin/csh
setenv TBBROOT "D:\a\Maud\Maud\build\lib.win-amd64-cpython-39\maud\stan\cmdstan-2.33.1\stan\lib\stan_math\lib\tbb_2020.3"
setenv TBB_ARCH_PLATFORM "intel64\mingw8.3.0"
setenv TBB_TARGET_ARCH "intel64"
setenv CPATH "${TBBROOT}\include;$CPATH"
setenv LIBRARY_PATH "D:\a\Maud\Maud\build\lib.win-amd64-cpython-39\maud\stan\cmdstan-2.33.1\stan\lib\stan_math\lib\tbb;$LIBRARY_PATH"
setenv PATH "D:\a\Maud\Maud\build\lib.win-amd64-cpython-39\maud\stan\cmdstan-2.33.1\stan\lib\stan_math\lib\tbb;$PATH"
setenv LD_LIBRARY_PATH "D:\a\Maud\Maud\build\lib.win-amd64-cpython-39\maud\stan\cmdstan-2.33.1\stan\lib\stan_math\lib\tbb;$LD_LIBRARY_PATH"
