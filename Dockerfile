
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in pyproject.toml
# We use pip to install the package in editable mode or just dependencies
RUN pip install --no-cache-dir .

# Make port 80 available to the world outside this container (if we add HTTP later)
# For Stdio MCP, we don't strictly need EXPOSE, but good practice
# EXPOSE 8000

# Define environment variable
ENV NAME DataGovernance

# Run data-gov-server when the container launches
CMD ["data-gov-server"]
