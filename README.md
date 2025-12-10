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
    openmpi4-devel \
    paraview \
    patch \
    tar \
    vim-small \
    wget \
    xz \
    zlib-devel
```


### Set up `openmpi`

#### Xubuntu 22.04

No additional operation required.

#### OpenSUSE-Leap 15.6

Select `openmpi` version
```bash
mpi-selector --set openmpi4
```

It is required to **log out and log in again** to activate `mpi`.


### Install `OpenFOAM-12`

Set the installation location
```bash
export OPENFOAM_ROOT=~/software/openfoam
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
export OPENFOAM_ROOT=~/software/openfoam
source $OPENFOAM_ROOT/OpenFOAM-dev/etc/bashrc
```


#### Automatic environment setup

Run this **once**
```bash
cat <<EOF >> ~/.bashrc
# configure openfoam
export OPENFOAM_ROOT=~/software/openfoam
source \$OPENFOAM_ROOT/OpenFOAM-dev/etc/bashrc
EOF
```

