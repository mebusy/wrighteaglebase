#!/bin/bash

set -e

# brew install boost automake bison qt@5
# for librcsc doc
# brew install doxygen


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

BOOST_PREFIX="$(brew --prefix boost)"
export CPPFLAGS="-I${BOOST_PREFIX}/include"
export LDFLAGS="-L${BOOST_PREFIX}/lib"

if [ $step -le 2 ]; then
    rm -rf rcssserver-19.0.0
    # unzip the downloaded file
    tar -xvzf rcssserver.tar.gz

    pushd rcssserver-19.0.0

#     python3 - <<'PY'
# PY
    python3 - < ../fixBoostLib.py

    autoreconf -fi
    rm -f config.cache

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

    # autoreconf -fi
    # rm -f config.cache

    ./configure --with-boost="${BOOST_PREFIX}" --prefix=${curDir}/../bin/

    PATH="$(brew --prefix bison)/bin:$PATH" make install -j1

    popd

fi

# https://github.com/helios-base/librcsc.git
if [ $step -le 5 ]; then
    wget -O librcsc.tar.gz https://github.com/helios-base/librcsc/archive/refs/tags/support-v18.tar.gz
fi


# gcc -std=gnu23
# 从 C23 开始，旧式 K&R 函数定义不再是标准语法。
# macOS 上的 gcc 通常实际指向 Apple Clang，因此它拒绝了这些旧式函数定义。
# 最简单的解决方案：强制使用 GNU C17
export CFLAGS="-std=gnu17 -O2"
export CXXFLAGS="-std=c++17 -O2 -fno-typed-cxx-new-delete"

if [ $step -le 6 ]; then
    rm -rf librcsc-support-v18
    # unzip the downloaded file
    tar -xvzf librcsc.tar.gz

    pushd librcsc-support-v18

    python3 - < ../fixBoostLib.py

    autoreconf -fi
    rm -f config.cache


    ./bootstrap

    ./configure --with-boost="${BOOST_PREFIX}" --prefix=${curDir}/../bin/ --disable-unit-test

    PATH="$(brew --prefix bison)/bin:$PATH" make install -j1

    sed -i '' -E \
    's/^[[:space:]]*#?[[:space:]]*OUTPUT_LANGUAGE[[:space:]]*=.*/OUTPUT_LANGUAGE = Chinese/' Doxyfile
    make doc

    popd
fi

# https://github.com/helios-base/helios-base/archive/refs/tags/support-v18.tar.gz
if [ $step -le 7 ]; then
    wget -O helios-base.tar.gz https://github.com/helios-base/helios-base/archive/refs/tags/support-v18.tar.gz
fi

if [ $step -le 8 ]; then
    rm -rf helios-base-support-v18
    # unzip the downloaded file
    tar -xvzf helios-base.tar.gz

    pushd helios-base-support-v18

    python3 - < ../fixBoostLib.py

    autoreconf -fi
    rm -f config.cache

    ./bootstrap


    ./configure --with-boost="${BOOST_PREFIX}" --prefix=${curDir}/../bin/ --with-librcsc=${curDir}/../bin/


    python3 - --apply < ../fixHeliosSytax.py
    PATH="$(brew --prefix bison)/bin:$PATH" make install -j1

    popd
fi

