import requests
import time
import flet as ft
import forum_components as fc



def start_temas(page: ft.Page):
    page.scroll = ft.ScrollMode.ALWAYS
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def publicar_mensaje(e):
        # Extraer los valores de los TextFields
        title = title_field.value
        content = content_field.value
        author_id = author_id_field.value
        user_insect_id = user_insect_id_field.value

        # Construir el cuerpo de la solicitud POST
        data = {
            "title": title,
            "content": content,
            "author_id": author_id,
            "user_insect_id": user_insect_id,
            "comments": []
        }

        # Hacer una solicitud POST al backend
        url = "https://insectid-api-1086245255634.us-central1.run.app/forum/post/"
        response = requests.post(url, json=data)

        if response.status_code == 200:
            # Crear una nueva instancia de mensaje_container
            nuevo_mensaje = fc.create_mensaje_container(data)

            # Añadir la nueva instancia a la página
            page.add(nuevo_mensaje)
            page.update()
        else:
            print("Error al publicar el mensaje:", response.status_code)
            
    
    def get_mensaje_data():
        response = requests.get("https://insectid-api-1086245255634.us-central1.run.app/forum/posts/")
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list):
                return data  # Devolver todos los mensajes
        return []

    def visualizar_registros(page: ft.Page, intervalo=60):
        while True:
            # Obtener los datos de los mensajes
            mensajes = get_mensaje_data()

            # Crear un mensaje_container para cada mensaje
            mensaje_containers = []
            for mensaje in mensajes:
                try:
                    mensaje_container = fc.create_mensaje_container(mensaje)
                    mensaje_containers.append(mensaje_container)
                except KeyError as e:
                    print(f"Error: Falta la clave {e} en el mensaje {mensaje}")

            # Añadir los contenedores de mensajes a la página
            page.add(
                ft.Column(
                    scroll=ft.ScrollMode.AUTO  # Habilitar el modo de desplazamiento
                )
            )

            # Esperar el intervalo especificado antes de la siguiente actualización
            time.sleep(intervalo)
    
    
    

    def show_mensaje_form(e):
        dialog = ft.AlertDialog(
            content=mensaje_form,
            actions=[
                ft.ElevatedButton("CERRAR", on_click=lambda e: close_dialog(dialog)),
                ft.ElevatedButton("PUBLICAR", on_click=publicar_mensaje),
            ],
            modal=True
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        
    '''def forum_post(e):
        page.clean()
        
        try:
            # Ejecutar el script temas.py
            result = subprocess.run(['python', 'C:\\Users\\juanp\\Documents\\workspace\\BichoLabV1.0\\temas.py'], capture_output=True, text=True)
            
            # Mostrar la salida del script en la consola
            print(result.stdout)
            if result.stderr:
                print("Error:", result.stderr)
        except Exception as ex:
            print(f"Error al ejecutar el script: {ex}")'''

    # Definir los TextFields en mensaje_form
    title_field = ft.TextField(label="Título")
    content_field = ft.TextField(label="Escriba aquí el contenido de su mensaje", max_lines=1000)
    author_id_field = ft.TextField(label="Author ID")
    user_insect_id_field = ft.TextField(label="Insect ID")

    mensaje_form = ft.Column(
        [
            title_field,
            content_field,
            author_id_field,
            user_insect_id_field,
        ],
        width=450,
        height=550
    )

    page.add(
        ft.Column(
            [
                fc.topic_menu,
                ft.ElevatedButton(
                    "NUEVO MENSAJE",
                    icon='add',
                    icon_color=fc.LETTERS_COLOR_BUTTON,
                    color=fc.LETTERS_COLOR_BUTTON,
                    bgcolor=fc.BACKGROUND_COLOR_BUTTON,
                    on_click=show_mensaje_form,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
    )
    
    # Visualizar todos los registros disponibles
    ## ESTO ES IMPORTANTE COMO UN HIJUEPUTAS, GENERA LA VISTA DE LOS CONTENEDORES DE MENSAJES
    visualizar_registros(page)
    
# Ejemplo de cómo iniciar la aplicación
if __name__ == "__main__":
    ft.app(target=start_temas)