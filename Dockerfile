FROM sonarqube:latest

# Download and install SonarScanner
RUN wget https://binaries.sonarsource.com/?prefix=Distribution/sonar-scanner-cli/sonar-scanner-cli-6.0.0.4432-linux.zip && \
    unzip sonar-scanner-cli-6.0.0.4432-linux.zip -d /opt/sonarqube/ && \
    rm sonar-scanner-cli-6.0.0.4432-linux.zip

# Set environment variable
ENV SONAR_SCANNER_HOME=/opt/sonarqube/sonar-scanner-cli-4.8.0.12008-linux

# Add SONAR_SCANNER_HOME/bin to PATH
ENV PATH=$SONAR_SCANNER_HOME/bin:$PATH
