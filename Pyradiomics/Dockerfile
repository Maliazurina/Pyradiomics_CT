FROM nvidia/cuda:11.0-base-ubuntu18.04

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential libgl1-mesa-glx libglib2.0-0 \
  curl sudo git wget htop \
  && rm -rf /var/lib/apt/lists/*

# Create a non-root user and switch to it
ARG USER_NAME="mbsaad"
RUN adduser --disabled-password --gecos '' --shell /bin/bash ${USER_NAME}
RUN echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USER_NAME}
USER ${USER_NAME}
ENV HOME=/home/${USER_NAME}
RUN chmod 777 /home/${USER_NAME}
WORKDIR /home/${USER_NAME}

# Install Miniconda
RUN curl -LO http://repo.continuum.io/miniconda/Miniconda3-py37_4.8.3-Linux-x86_64.sh \
 && bash ~/Miniconda3-py37_4.8.3-Linux-x86_64.sh -p ~/miniconda -b \
 && rm ~/Miniconda3-py37_4.8.3-Linux-x86_64.sh
ENV PATH=/home/${USER_NAME}/miniconda/bin:$PATH
## Create a Python 3.7.0 environment
RUN /home/${USER_NAME}/miniconda/bin/conda install conda-build \
 && /home/${USER_NAME}/miniconda/bin/conda create -y --name py37 python=3.7.0 \
 && /home/${USER_NAME}/miniconda/bin/conda clean -ya
ENV CONDA_DEFAULT_ENV=py37
ENV CONDA_PREFIX=/home/${USER_NAME}/miniconda/envs/$CONDA_DEFAULT_ENV
ENV PATH=$CONDA_PREFIX/bin:$PATH

# Python packages installation
## Common packages
RUN pip install gpustat==0.6.0 setuptools==45
RUN pip install numpy==1.19.2 scipy==1.6.0 matplotlib==3.3.2
RUN pip install scikit-image==0.17.2 opencv-python==4.4.0.44 scikit-learn==0.23.2

## Install pytorch
RUN conda update -n base -c defaults conda
RUN conda install pytorch torchvision torchaudio cudatoolkit=11.0 -c pytorch
RUN pip install tensorboard==2.4.0
RUN pip install pytorch-msssim
RUN pip install tqdm
RUN pip install nibabel
RUN pip install SimpleITK
RUN pip install napari
RUN pip install ipywidgets==7.4.2
RUN pip install albumentations
RUN pip install torchtuples
RUN pip install pycox
RUN pip install monai
RUN pip install pyradiomics
RUN pip install -U pip setuptools



RUN mkdir -p /home/${USER_NAME}/miniconda/envs/py37/lib/python3.7/site-packages/pycox/datasets/data
WORKDIR /home/${USER_NAME}