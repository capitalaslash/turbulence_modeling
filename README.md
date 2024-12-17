# Support files for Turbulence Modeling course at unibo

Content:

* OpenFOAM installation instuctions

* `docker` container with OpenFOAM

* OpenFOAM cases with templates

* TODO: merge adv1d python code


## Installation instructions for OpenFOAM-12

### System requirements

#### Xubuntu 22.04

```bash
sudo apt install \
    bash \
    bzip2 \
    cmake \
    flex \
    gcc \
    g++ \
    git \
    gzip \
    libopenmpi-dev \
    make \
    openmpi-bin \
    paraview \
    patch \
    tar \
    vim \
    wget \
    xz-utils
```

#### OpenSUSE-Leap 15.6

Install some required packages
```bash
sudo zypper install \
    bzip2 \
    cmake \
    flex \
    gcc \
    gcc-c++ \
    gcc-fortran \
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

### Install `openmpi` via `spack`

#### Install `spack`

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

#### Install `openmpi`

install `openmpi` via spack
```bash
spack install openmpi@4.1.7
```

enable the `openmpi` installation
```bash
spack load openmpi@4.1.7
```


#### Environment setup for later usage

```bash
export SPACK_ROOT=~/platform_tm/spack
source $SPACK_ROOT/share/spack/setup-env.sh
spack load openmpi@4.1.7
```


#### Automatic environment setup

Run this **once**

```bash
cat <<EOF >> ~/.bashrc
# setup spack and load openmpi
export SPACK_ROOT=~/platform_tm/spack
source \$SPACK_ROOT/share/spack/setup-env.sh
spack load openmpi@4.1.7
EOF
```


### Install `OpenFOAM-12`

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
source $OPENFOAM_ROOT/OpenFOAM-dev/etc/bashrc
./Allwmake -j
```

Compile OpenFOAM
```bash
cd $OPENFOAM_ROOT/OpenFOAM-dev
source $OPENFOAM_ROOT/OpenFOAM-dev/etc/bashrc
./Allwmake -j
```


#### Test installation

Copy and run the `cavity` tutorial
```bash
mkdir ~/sandbox
cd ~/sandbox
cp -r $FOAM_TUTORIALS/incompressibleFluid/cavity .
cd cavity
blockMesh
foamRun
```


#### Environment setup for later usage

```bash
export OPENFOAM_ROOT=~/platform_tm/openfoam
source $OPENFOAM_ROOT/OpenFOAM-dev/etc/bashrc
```


#### Automatic environment setup

Run this **once**
```bash
cat <<EOF >> ~/.bashrc
# configure openfoam
export OPENFOAM_ROOT=~/platform_tm/openfoam
source \$OPENFOAM_ROOT/OpenFOAM-dev/etc/bashrc
EOF
```

