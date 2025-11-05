# lógica que envía el email

def send_email(to_address: str, subject: str, body: str) -> None:
    print(f"Sending email to {to_address} with subject '{subject}'")
    # Aquí iría la lógica real para enviar el email

# traer template en html y pasarle los parámetros necesarios // mejor almacenar en base de datos los templates

# entidad: id, nombre, descripción, template_html, módulo al que pertenece (usuarios, notificaciones, etc).

# v1 controllers/mail.py
# v2 modules/file_storage/application/service/file_storage.py