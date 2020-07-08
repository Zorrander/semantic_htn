FROM python:3.7.1

# Install prerequisite Ubuntu packages
#RUN apt-get install -y <REQUIRED UBUNTU PACKAGES> \
# && apt-get clean \
# && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip3 install -r ../cobowl/

# Copy the application into the image
ADD . /app

# Run the app setup script
# RUN /app/setup.sh

# Specify the application startup script
CMD ["pytest", "./tests/compound_task_test.py"]
