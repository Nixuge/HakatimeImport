# Use the base image from the docker-compose file
FROM mujx/hakatime:v1.6.1

# Install necessary packages to handle certificates
# RUN apt-get update && apt-get install -y ca-certificates

# Copy the mitmproxy CA certificate into the container
COPY mitmproxy-ca-cert.pem /usr/local/share/ca-certificates/mitmproxy-ca-cert.crt

# Update the CA certificates
RUN update-ca-certificates
