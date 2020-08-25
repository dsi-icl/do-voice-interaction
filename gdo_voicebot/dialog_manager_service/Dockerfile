# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:2.0.0a2

# Use subdirectory as working directory
WORKDIR /app

# Copy any additional custom requirements
COPY actions/requirements-actions.txt ./

# Change back to root user to install dependencies
USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install -r requirements-actions.txt

# Copy actions folder to working directory
COPY ./actions /app/actions

# Copy utilities folder to working directory
COPY ./utilities /app/utilities

# Copy configuration
COPY ./config/config.docker.yml /app/config/config.yml

# Copy module file
COPY __init__.py ./

# By best practices, don't run the code with root user
USER 1001

CMD ["start", "--actions", "actions.actions"]
