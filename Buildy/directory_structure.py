# directory_structure.py

# Defines the project's directory structure
directory_structure = {
    "root": {
        "home": {
            "auth": {
                "docker-compose.yml": {},
                "authelia": {
                    "configuration.yml": {},
                    "db.sqlite3": {},
                    "user_database.yml": {},
                    "certificates": {
                        # ...empty...
                    },
                    "logs": {
                        "authelia.log": {},
                        "notification.txt": {}
                    }
                },
                "mysql": {
                    # ...more...
                },
                "redis": {
                    # ...more...
                },
                "traefik": {
                    "acme.json": {},
                    "traefik.log": {},
                    "traefik.yml": {},
                    "config.yml": {},
                    "certificates": {
                        # ...empty...
                    }
                }
            },
            # ...more folders...
        }
    }
}
