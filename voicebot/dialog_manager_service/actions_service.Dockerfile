# Extend the official Rasa SDK image
FROM python:3.8-buster

# Use subdirectory as working directory
WORKDIR /app

# Copy any additional custom requirements
COPY ./dialog_manager_service/actions/requirements-actions.txt ./

# Change back to root user to install dependencies
USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install -r requirements-actions.txt

# Copy actions folder to working directory
COPY ./dialog_manager_service/actions /app/actions

# Copy utilities folder to working directory
COPY ./dialog_manager_service/utilities /app/utilities

# Copy configuration
COPY ./dialog_manager_service/config/config.docker.yml /app/config/config.yml

# Copy module file
COPY ./dialog_manager_service/__init__.py ./

# By best practices, don't run the code with root user
USER 1001

CMD ["python", "-m", "rasa_sdk", "--actions", "actions.actions"]
