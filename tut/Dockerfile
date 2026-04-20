FROM andrewosh/binder-base

MAINTAINER Philipp Gadow <philipp@pgadow.de>

USER root

# Add dependency
RUN apt-get update

# Install requirements for Python
RUN pip install --upgrade pip
RUN pip install numpy sympy matplotlib plotly ipywidgets

USER main