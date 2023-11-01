#!/bin/sh
export TBBROOT="D:/a/Maud/Maud/build/lib.win-amd64-cpython-39/maud/stan/cmdstan-2.33.1/stan/lib/stan_math/lib/tbb_2020.3"
export TBB_ARCH_PLATFORM="intel64\mingw8.3.0"
export TBB_TARGET_ARCH="intel64"
export CPATH="${TBBROOT}/include;$CPATH"
export LIBRARY_PATH="D:/a/Maud/Maud/build/lib.win-amd64-cpython-39/maud/stan/cmdstan-2.33.1/stan/lib/stan_math/lib/tbb;$LIBRARY_PATH"
export PATH="D:/a/Maud/Maud/build/lib.win-amd64-cpython-39/maud/stan/cmdstan-2.33.1/stan/lib/stan_math/lib/tbb;$PATH"
export LD_LIBRARY_PATH="D:/a/Maud/Maud/build/lib.win-amd64-cpython-39/maud/stan/cmdstan-2.33.1/stan/lib/stan_math/lib/tbb;$LD_LIBRARY_PATH"
