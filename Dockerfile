FROM opensuse/leap:15.6

# install packages
RUN /bin/sh -c zypper ref && \
    zypper up -y && \
    zypper in -y \
    bzip2 \
    cmake \
    flex \
    gcc13 \
    gcc13-c++ \
    gcc13-fortran \
    git \
    gzip \
    paraview \
    patch \
    tar \
    vim-small \
    wget \
    xz \
    zlib-devel \
    && zypper clean

# set gcc 13 as default
RUN ln -s /usr/bin/gcc-13 /usr/local/bin/gcc && \
    ln -s /usr/bin/g++-13 /usr/local/bin/g++ && \
    ln -s /usr/bin/gfortran-13 /usr/local/bin/gfortran

ENV SPACK_ROOT=/opt/spack

# install spack
RUN mkdir -p $SPACK_ROOT && \
    cd $SPACK_ROOT && \
    git clone https://github.com/spack/spack.git . -b releases/v0.23 && \
    mkdir -p $SPACK_ROOT/opt/spack

# install openmpi
RUN $SPACK_ROOT/bin/spack install openmpi@4.1.7

ENV OPENFOAM_ROOT=/opt/openfoam

# clone OpenFOAM.org
RUN mkdir -p $OPENFOAM_ROOT && \
    cd $OPENFOAM_ROOT && \
    git clone https://github.com/OpenFOAM/OpenFOAM-dev.git -b version-12 && \
    git clone https://github.com/OpenFOAM/ThirdParty-dev.git -b version-12

# disable zoltan
RUN mkdir -p $HOME/.OpenFOAM && \
    echo "export ZOLTAN_TYPE=none" >> $HOME/.OpenFOAM/prefs.sh && \
    echo "export ParaView_TYPE=none" >> $HOME/.OpenFOAM/prefs.sh

# compile third parties
RUN source $SPACK_ROOT/share/spack/setup-env.sh && \
    spack load openmpi@4.1.7 && \
    source $OPENFOAM_ROOT/OpenFOAM-dev/etc/bashrc && \
    cd $OPENFOAM_ROOT/ThirdParty-dev && \
    ./Allwmake -j

# compile OpenFOAM
RUN source $SPACK_ROOT/share/spack/setup-env.sh && \
    spack load openmpi@4.1.7 && \
    source $OPENFOAM_ROOT/OpenFOAM-dev/etc/bashrc && \
    cd $OPENFOAM_ROOT/OpenFOAM-dev && \
    ./Allwmake -j

# open shell
RUN source $SPACK_ROOT/share/spack/setup-env.sh && \
    spack load openmpi@4.1.7 && \
    source $OPENFOAM_ROOT/OpenFOAM-dev/etc/bashrc && \
    /bin/bash

# TODO: replace shell with cavity test
