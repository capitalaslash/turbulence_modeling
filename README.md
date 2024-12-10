# Installation instructions for OpenFOAM-11 on OpenSUSE Leap 15.6

## System requirements

Install some required packages
```bash
sudo zypper install \
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
    zlib-devel
```

and create links to set `gcc-10` as default version
```bash
sudo ln -s /usr/bin/gcc-13 /usr/local/bin/gcc
sudo ln -s /usr/bin/g++-13 /usr/local/bin/g++
sudo ln -s /usr/bin/gfortran-13 /usr/local/bin/gfortran
```

## Install `openmpi` via `spack`

### Install `spack`

Set `spack` installation folder
```bash
export SPACK_ROOT=~/platform_tm/spack
```

clone `spack-0.23`
```bash
mkdir -p $SPACK_ROOT
cd $SPACK_ROOT
git clone https://github.com/spack/spack.git . -b releases/v0.23
```

set environment to operate with `spack`
```bash
source $SPACK_ROOT/share/spack/setup-env.sh
```
### Install `openmpi`

install `openmpi` via spack
```bash
spack install openmpi@4.1.7
```

enable the `openmpi` installation
```bash
spack load openmpi@4.1.7
```

### Environment setup for later usage

```bash
export SPACK_ROOT=~/platform_tm/spack
source $SPACK_ROOT/share/spack/setup-env.sh
spack load openmpi@4.1.7
```

### Automatic environment setup

Run this **once**

```bash
cat <<EOF >>~/.bashrc
# setup spack and load openmpi
export SPACK_ROOT=~/platform_tm/spack
source $SPACK_ROOT/share/spack/setup-env.sh
spack load openmpi@4.1.7
EOF
```

## Install `OpenFOAM-12`

Set the installation location
```bash
export OPENFOAM_ROOT=~/platform_tm/openfoam
```

Clone the source files
```bash
mkdir -p $OPENFOAM_ROOT
cd $OPENFOAM_ROOT
git clone https://github.com/OpenFOAM/OpenFOAM-dev.git -b version-12
git clone https://github.com/OpenFOAM/ThirdParty-dev.git -b version-12
source $OPENFOAM_ROOT/OpenFOAM-dev/etc/bashrc
```

Disable `zoltan` and `paraview`
```bash
mkdir -p $HOME/.OpenFOAM
echo "export ZOLTAN_TYPE=none" >> $HOME/.OpenFOAM/prefs.sh
echo "export ParaView_TYPE=none" >> $HOME/.OpenFOAM/prefs.sh
```

Compile third party software
```bash
cd $OPENFOAM_ROOT/ThirdParty-dev
./Allwmake -j
```

Compile OpenFOAM
```bash
cd $OPENFOAM_ROOT/OpenFOAM-dev
./Allwmake -j
```

### Test installation

Copy and run the `cavity` tutorial
```bash
mkdir ~/sandbox
cd ~/sandbox
cp -r $FOAM_TUTORIALS/incompressibleFluid/cavity .
cd cavity
blockMesh
foamRun
```


### Environment setup for later usage

```bash
export OPENFOAM_ROOT=~/platform_tm/openfoam
source $OPENFOAM_ROOT/OpenFOAM-dev/etc/bashrc
```

### Automatic environment setup

Run this **once**
```bash
cat <<EOF >>~/.bashrc
# configure openfoam
export OPENFOAM_ROOT=~/platform_tm/openfoam
source $OPENFOAM_ROOT/OpenFOAM-dev/etc/bashrc
EOF
```
