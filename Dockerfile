FROM ubuntu:16.04

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN ./install_software.sh

# Set the python path
ENV PYTHONPATH /app/lib/python3.5/site-packages/:/app/lib/
# Allow incoming connections on port 8888
EXPOSE 8888

# Run app.py when the container launches
CMD ["/bin/bash"]