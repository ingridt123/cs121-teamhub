import connexion

# Initialize application from specification
app = connexion.App(__name__)
app.add_api("../openapi.yaml", options={"swagger_ui": False})
