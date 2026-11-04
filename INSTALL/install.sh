#!/bin/bash

# brew install boost automake bison qt@5


# let step = first argument
step=$1

# if $1 is not provided, set step to 0
if [ -z "$step" ]; then
  step=0
fi

# download the rcssserver from github iff step <= 1
if [ $step -le 1 ]; then
    echo "Downloading rcssserver..."
    wget -O rcssserver.tar.gz https://github.com/rcsoccersim/rcssserver/releases/download/rcssserver-19.0.0/rcssserver-19.0.0.tar.gz

fi

curDir=$(pwd)

if [ $step -le 2 ]; then
    rm -rf rcssserver-19.0.0
    # unzip the downloaded file
    tar -xvzf rcssserver.tar.gz

    pushd rcssserver-19.0.0

    python3 - <<'PY'
from pathlib import Path

p = Path("m4/ax_boost_system.m4")
s = p.read_text()

old = """            if test "x$ax_lib" = "x"; then
                AC_MSG_ERROR(Could not find a version of the Boost::System library!)
            fi
"""

new = """            if test "x$ax_lib" = "x"; then
                dnl Modern Boost.System is header-only (Boost >= 1.69).
                BOOST_SYSTEM_LIB=""
                AC_SUBST(BOOST_SYSTEM_LIB)
                AC_MSG_NOTICE([Using header-only Boost.System])
            fi
"""

if old not in s:
    raise SystemExit("ERROR: Original code not found; no changes made.")

p.write_text(s.replace(old, new, 1))
print("Patched:", p)
PY

    autoreconf -fi
    rm -f config.cache

    BOOST_PREFIX="$(brew --prefix boost)"

    CPPFLAGS="-I${BOOST_PREFIX}/include" \
    LDFLAGS="-L${BOOST_PREFIX}/lib" \
    ./configure --with-boost="${BOOST_PREFIX}" --prefix=${curDir}/../bin/

    PATH="$(brew --prefix bison)/bin:$PATH" make install -j1

    popd
fi


if [ $step -le 3 ]; then
    wget -O rcssmonitor.tar.gz https://github.com/rcsoccersim/rcssmonitor/releases/download/rcssmonitor-19.0.1/rcssmonitor-19.0.1.tar.gz
fi


if [ $step -le 4 ]; then
    rm -rf rcssmonitor-19.0.1
    # unzip the downloaded file
    tar -xvzf rcssmonitor.tar.gz

    pushd rcssmonitor-19.0.1

    # 已知的 Clang 19 与旧版 simdjson 的兼容性问题，不是 M4 芯片的问题。
    # simdjson 上游已经有修复提交：5d35e7c，修复方式正好对应你遇到的三个错误：把 this->print_xxx() 改为 static_cast<formatter*>(this)->print_xxx()。
    
perl -pi -e \
's/this->print_newline\(\)/static_cast<formatter*>(this)->print_newline()/g;
 s/this->print_indents\(depth\)/static_cast<formatter*>(this)->print_indents(depth)/g;
 s/this->print_space\(\)/static_cast<formatter*>(this)->print_space()/g' \
rcss/rcg/simdjson/simdjson.h

    autoreconf -fi
    rm -f config.cache

    BOOST_PREFIX="$(brew --prefix boost)"

    CPPFLAGS="-I${BOOST_PREFIX}/include" \
    LDFLAGS="-L${BOOST_PREFIX}/lib" \
    ./configure --with-boost="${BOOST_PREFIX}" --prefix=${curDir}/../bin/

    PATH="$(brew --prefix bison)/bin:$PATH" make install -j1

    popd

fi

