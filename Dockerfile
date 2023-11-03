FROM opensuse/leap:15.5

RUN /bin/sh -c zypper ref && \
    zypper up -y && \
    zypper in -y \
    bzip2 \
    cmake \
    flex \
    gcc10 \
    gcc10-c++ \
    gcc10-fortran \
    git \
    gzip \
    paraview \
    patch \
    tar \
    wget \
    xz \
    zlib-devel \
    && zypper clean

RUN ln -s /usr/bin/gcc-10 /usr/local/bin/gcc && \
    ln -s /usr/bin/g++-10 /usr/local/bin/g++ && \
    ln -s /usr/bin/gfortran-10 /usr/local/bin/gfortran

ENV SPACK_ROOT=/opt/spack

RUN mkdir -p $SPACK_ROOT && \
    cd $SPACK_ROOT && \
    git clone https://github.com/spack/spack.git . -b releases/v0.20 && \
    mkdir -p $SPACK_ROOT/opt/spack

RUN $SPACK_ROOT/bin/spack install openmpi@4.1.5

ENV OPENFOAM_ROOT=/opt/openfoam

RUN mkdir -p $OPENFOAM_ROOT && \
    cd $OPENFOAM_ROOT && \
    git clone https://github.com/OpenFOAM/OpenFOAM-dev.git -b version-11 && \
    git clone https://github.com/OpenFOAM/ThirdParty-dev.git -b version-11

RUN source $SPACK_ROOT/share/spack/setup-env.sh && \
    spack load openmpi && \
    source $OPENFOAM_ROOT/OpenFOAM-dev/etc/bashrc && \
    cd $OPENFOAM_ROOT/ThirdParty-dev && \
    ./Allwmake && \
    cd $OPENFOAM_ROOT/OpenFOAM-dev && \
    ./Allwmake

RUN source $SPACK_ROOT/share/spack/setup-env.sh && \
    spack load openmpi && \
    source $OPENFOAM_ROOT/OpenFOAM-dev/etc/bashrc && \
    /bin/bash
