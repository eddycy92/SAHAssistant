import os
import yaml
import json
import re

def parse_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def analyze_traefik_config(traefik_config):
    errors = []
    
    https_entrypoint = traefik_config.get('entryPoints', {}).get('https', {})
    if not https_entrypoint.get('address'):
        errors.append("HTTPS entrypoint address not defined in Traefik configuration.")
    if 'tls' not in https_entrypoint:
        errors.append("TLS configuration missing in HTTPS entrypoint.")

    # Check for correct HTTPS redirection from HTTP
    http_entrypoint = traefik_config.get('entryPoints', {}).get('http', {})
    http_redirections = http_entrypoint.get('http', {}).get('redirections', {}).get('entryPoint', {})
    if http_redirections.get('to') != 'https' or http_redirections.get('scheme') != 'https':
        errors.append("HTTP to HTTPS redirection is not correctly configured.")

    # Add more checks as necessary based on your traefik.yml content
    return errors

def analyze_authelia_config(authelia_config):
    errors = []
    
    if authelia_config.get('authentication_backend', {}).get('ldap', {}).get('url') is None:
        errors.append("Authelia LDAP URL is not configured.")
    
    # Add more checks as necessary for Authelia's configuration
    return errors

def analyze_docker_compose(docker_compose_config):
    errors = []

    # Check for port bindings and network settings
    services = docker_compose_config.get('services', {})
    for service_name, service_config in services.items():
        ports = service_config.get('ports', [])
        if any(port.endswith(":80") or port.endswith(":443") for port in ports):
            errors.append(f"Port conflict detected in service: {service_name}")

    # Check for necessary labels in services like Authelia
    if service_name == 'authelia':
        labels = service_config.get('labels', [])
        if "traefik.http.routers.authelia.entrypoints=https" not in labels:
            errors.append("Authelia service missing HTTPS entrypoint label.")

    return errors

def analyze_acme_json(acme_json_path):
    try:
        with open(acme_json_path, 'r') as file:
            acme_data = json.load(file)
            if not acme_data:
                return ["acme.json is empty, SSL/TLS certificates may be missing."]
    except Exception as e:
        return [f"Error reading acme.json: {e}"]
    return []

def analyze_logs(log_file_path):
    errors = []
    try:
        with open(log_file_path, 'r') as file:
            for line in file:
                if "error" in line.lower():
                    errors.append(line.strip())
    except Exception as e:
        return [f"Error reading log file: {e}"]
    return errors

def main():
    traefik_config = parse_yaml_file('/home/auth/traefik/traefik.yml')
    docker_compose_config = parse_yaml_file('/home/auth/docker-compose.yml')
    authelia_config = parse_yaml_file('/home/auth/authelia/configuration.yml')
    
    traefik_errors = analyze_traefik_config(traefik_config)
    docker_errors = analyze_docker_compose(docker_compose_config)
    authelia_errors = analyze_authelia_config(authelia_config)
    acme_errors = analyze_acme_json('/home/auth/traefik/acme.json')
    analyze_logs('/home/auth/traefik/traefik.log')

    # Output findings
    print("Analysis Complete.")
    print("Traefik Analysis:", traefik_errors)
    print("Docker Compose Analysis:", docker_errors)
    print("Authelia Analysis:", authelia_errors)
    print("ACME JSON Analysis:", acme_errors)
    print("Log Analysis:", log_errors)

if __name__ == "__main__":
    main()