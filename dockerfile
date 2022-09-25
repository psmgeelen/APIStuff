FROM ubuntu:latest
WORKDIR /usr/app/src
# Add files
COPY main.py .
COPY APIStuff/. ./APIStuff/
COPY requirements.txt .

# Install base utilities
RUN apt update
#RUN apt install -y build-essentials
RUN apt install -y wget
# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH
# Create Environment based on the requirements txt
RUN conda create --name test_env --file requirements.txt
# Run main script whilst using the correct environment
RUN conda run -n test_env python main.py