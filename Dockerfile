# Use the official Ubuntu base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install prerequisites
RUN apt-get update && \
    apt-get install -y \
    software-properties-common \
    wget \
    build-essential \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update

# Install Python 3.12.9
RUN apt-get install -y python3.12 python3.12-distutils

# Install pip for Python 3.12
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3.12 get-pip.py && \
    rm get-pip.py

# Install the required Python libraries
RUN pip install --no-cache-dir \
    joblib \
    numpy \
    scipy \
    scikit-learn \
    setuptools \
    threadpoolctl \
    wheel

# Set the default command to run when starting the container
CMD ["python3.12"]