import flet as ft
import flet.map as map
from PIL import Image, ImageDraw, ImageFont
import urllib.parse  
import os
import shutil
from datetime import datetime
import requests
import json
import cloudinary
import cloudinary.uploader
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import temas
import forum_components as fc

urlapi = "https://insectid-api-1086245255634.us-central1.run.app/"


def add_watermark(image_path, coordinates):
    try:
        # Cargamos la imagen original
        original = Image.open(image_path)
        
        # Creamos un objeto de dibujo
        draw = ImageDraw.Draw(original)
        
        # Definimos el tamaño de la fuente en función del tamaño de la imagen
        width, height = original.size
        font_size = int(height * 0.05)  # Ajusta el tamaño de la fuente al 5% de la altura de la imagen
        font = ImageFont.truetype("arial.ttf", font_size)
        
        # Texto de la marca de agua
        watermark_text = "Tomado y clasificado con Bicho Lab\n"
        
        # Agregamos la fecha y hora
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        watermark_text += f"Fecha y Hora: {current_time}\n"
        
        if coordinates:
            watermark_text += f"Coordenadas: {coordinates.latitude}_{coordinates.longitude}"
        
        # Cargamos el icono
        icon_path = "public/ICONO.png"
        icon = Image.open(icon_path)
        
        # Redimensionamos el icono en función de la imagen
        icon_size = (int(width * 0.2), int(height * 0.2))  # Ajusta el icono al 20% del ancho de la imagen
        icon = icon.resize(icon_size, Image.LANCZOS)
        
        # Posición para el icono (inferior)
        icon_position = (width - icon.width - 20, height - icon.height - 20)  # 20 píxeles de margen desde la parte inferior y derecha
        
        # Dibujamos el icono en la imagen
        original.paste(icon, icon_position, icon.convert("RGBA"))
        
        # Posición de la marca de agua (más arriba de la esquina inferior izquierda)
        text_x = int(width * 0.02)  # 2% del ancho desde la izquierda
        text_y = height - int(height * 0.15)  # Mueve el texto más arriba, ajusta según sea necesario
        
        # Dibujamos la marca de agua en la imagen
        text_color = (0, 0, 0, 128)  # Negro con transparencia
        draw.text((text_x, text_y), watermark_text, font=font, fill=text_color)
        
        # Generamos un nombre de archivo único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        
        # Reemplazamos espacios y caracteres no deseados
        safe_base_name = base_name.replace(" ", "_").replace(":", "").replace(",", "_")
        watermarked_image_path = f"{safe_base_name}_watermarked_{timestamp}.jpg"
        
        # Guardamos la imagen con la marca de agua
        original.save(watermarked_image_path)
        
        return watermarked_image_path
    except Exception as e:
        print(f"Error al agregar marca de agua: {e}")
        return None



async def main(page: ft.Page):
    page.scroll = ft.ScrollMode.ALWAYS
    page.title = "Clasificador de Insectos"
    page.bgcolor = ft.colors.WHITE
    page.window_width = 410  # Ancho inicial de la ventana
    page.window_height = 700  # Altura inicial de la ventana


    def on_file_picked(e):
        if e.files:
            file_path = e.files[0].path
            print(f"Cargando imagen: {file_path}")

            # Añadir la marca de agua y cargar la nueva imagen
            image_with_watermark = add_watermark(file_path, None)  # Añadimos marca de agua
            print(f"Imagen con marca de agua: {image_with_watermark}")  # Verifica la ruta

            # Actualiza el src de la imagen
            image.src = image_with_watermark
            
            # Hacer la imagen visible
            image.visible = True

            # Actualiza la página para reflejar el cambio
            page.update()  # Asegúrate de que esto se llame después de hacer cambios en la UI


    async def cargar_imagen_con_gps(e):
        global location_gl
        file_picker.pick_files()
        location = await handle_get_current_position(e)
        location_gl = location
        add_marker(location, e)
        
    
    def classify_insect(e):
        page.controls.clear()  # Clear the page before adding new content
        insect_info_page(page)
        page.update()

    def borrar_imagen(e):
        # Lógica para borrar la imagen actual
        image.visible = False  # Oculta la imagen actual
        classification_label.text = ""  # Limpiar la etiqueta de clasificación

        # Eliminar la imagen temporal si existe
        temp_image_path = "temp_watermarked_image.jpg"
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
            print(f"Imagen temporal {temp_image_path} eliminada.")

        # Actualiza la página para reflejar el cambio
        page.update()



       

   

        # Función para mostrar contenido educativo
    def mostrar_contenido_educativo(page):
        # Limpiar la pantalla actual
        page.clean()

        # Crear contenido educativo
        contenido = ft.Column(
            [
                ft.Text("Contenido Educativo", size=30, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Ofrece recursos educativos, como artículos, videos e infografías sobre insectos y su rol en los ecosistemas.",
                    size=20
                ),
                ft.Divider(),
                # Agregar un enlace al video
                ft.Text(
                    "Mira este video sobre insectos:",
                    size=20
                ),
                ft.ElevatedButton(
                    text="Ver Video",
                    on_click=lambda e: page.launch_url("https://www.youtube.com/watch?v=1XbWlt2xJnE"),  # Reemplaza con tu URL de video
                ),
                ft.Divider(),
                # Agregar un botón para redirigir a una URL externa
                ft.ElevatedButton(
                    text="Leer más sobre Insectos", 
                    on_click=lambda e: page.launch_url("https://www.ambientum.com/ambientum/biodiversidad/cual-es-la-importancia-de-los-insectos-en-el-ecosistema.asp"),  # Reemplaza con tu URL
                ),
                ft.Divider(),
                ft.ElevatedButton("Volver", on_click=show_image_upload_screen)  # Botón para volver
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )

        # Agregar contenido a la página
        page.add(contenido)

    # Configuración de la ventana
    def main(page: ft.Page):
        page.window.width = 410  # Ancho inicial de la ventana
        page.window.height = 700  # Altura inicial de la ventana
        
        # Otros códigos para iniciar la aplicación...
        page.add(ft.ElevatedButton("Contenido Educativo", on_click=lambda e: mostrar_contenido_educativo(page)))


    # Función para mostrar la pantalla de carga de imágenes
    def show_image_upload_screen(e):
        # Limpiar la pantalla actual
        page.clean()
        
        # Agregar el file picker si es necesario
        page.add(file_picker)

        # Crear la columna para cargar y clasificar imágenes
        page.add(
            ft.Column(
                [
                    ft.Text("Bienvenido al BichoIdentifyLab", size=30, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text("Cargar y Clasificar Imagen de Insecto", size=20),

                    # Columna para alinear los botones verticalmente
                    ft.Column(
                        [
                            ft.ElevatedButton("Cargar Imagen", on_click=cargar_imagen_con_gps),
                            # Mover la imagen aquí
                            image,
                            ft.ElevatedButton("Clasificar Insecto", on_click=classify_insect),
                            ft.ElevatedButton("Borrar Imagen", on_click=borrar_imagen),
                            ft.ElevatedButton("Mostrar Imágenes Guardadas", on_click=show_saved_images),
                            ft.ElevatedButton("Atrás", on_click=show_login_screen),
                            ft.ElevatedButton("Entra al foro", on_click=forum_post),
                            ft.ElevatedButton("Contenido Educativo", on_click=lambda e: mostrar_contenido_educativo(page)),  # Nuevo botón
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centra horizontalmente
                        spacing=10,  # Espaciado uniforme entre botones
                    ),

                    classification_label,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )



        # Centrar el contenedor del mapa
        page.add(
            ft.Text("Ubicación de la fotografía", size=30, weight=ft.FontWeight.BOLD),
            ft.Column(
                [
                    map_container,
                    ft.Row(),  # Si necesitas una fila vacía para el espaciado, déjala aquí
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )

        page.update()



    def show_saved_images(e):
        page.clean()
        
        # Crear un contenedor para las imágenes con scroll
        images_container = ft.Column(
            spacing=4,
            scroll=ft.ScrollMode.AUTO
        )

        # URL de la API
        api_url = urlapi + f"/users/{myid}/insects/"

        def fetch_images():
            try:
                response = requests.get(api_url)
                response.raise_for_status()  # Lanza un error si la respuesta es un error HTTP
                return response.json()
            except requests.RequestException as e:
                print(f"Error al obtener las imágenes: {e}")
                return []

        def delete_image(user_insect_id):
            images_container.controls.clear()
            print(user_insect_id)
            # Aquí puedes agregar la lógica para eliminar la imagen si es necesario.
            response = requests.delete(urlapi+f'users/{myid}/insects/delete',params={'user_insect_id':user_insect_id})
            if response.status_code == 200:
                print(f"Eliminar imagen con ID: {user_insect_id}")
                show_saved_images(e)
                
                page.update()

            else:
                print('No se encontro el insecto')

        def update_images_container():
            images_container.controls.clear()  # Limpiar el contenedor antes de llenarlo
            insects_data = fetch_images()

            for insect in insects_data:
                image_url = insect['data']["image"]
                insect_id = insect['data']["insect_id"]
                user_insect_id = insect['_id']
                image_url = urlapi + f"insects/download/image/{image_url}"
                insect_data = requests.get(urlapi + f'insects/{insect_id}')
                data_json = insect_data.json().get('data')

                common_name = ft.Text(value=f"{data_json.get('common_name', 'Desconocido')}", size=20, weight="bold", color='black')
                scientific_name = ft.Text(value=f"{data_json['taxonomy']['specie']}", size=15, weight="italic", color='black')

                img_widget = ft.Image(src=image_url, width=300, height=300)

                # Crear un contenedor para la imagen y los nombres
                image_info_column = ft.Column(
                    controls=[
                        img_widget,
                        common_name,
                        scientific_name
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
                
                delete_button = ft.IconButton(
                    icon=ft.icons.CLOSE,
                    on_click=lambda e: delete_image(user_insect_id),
                )

                img_row = ft.Row(
                    controls=[image_info_column, delete_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
                images_container.controls.append(img_row)

            page.add(images_container)
            page.update()

        update_images_container()  # Llenar el contenedor por primera vez

        page.add(ft.ElevatedButton("Atrás", on_click=show_image_upload_screen))
        page.update()



    ############ TOCA METER ESTO A LA APP PARA INGRESAR AL FORO ##############
    def forum_post(e):
        
        page.clean()

        page.scroll = ft.ScrollMode.ALWAYS
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        def close_dialog(dialog):
            dialog.open = False
            page.update()

        def publicar_mensaje(e):
            title = title_field.value
            content = content_field.value
            author_id = author_id_field.value
            user_insect_id = user_insect_id_field.value

            if not title or not content or not author_id or not user_insect_id:
                print("Todos los campos son obligatorios.")
                return

            data = {
                "title": title,
                "content": content,
                "author_id": author_id,
                "user_insect_id": user_insect_id,
                "comments": []
            }

            url = "https://insectid-api-1086245255634.us-central1.run.app/forum/post/"
            
            try:
                response = requests.post(url, json=data)
                response.raise_for_status()
            except requests.exceptions.RequestException as err:
                print("Error al publicar el mensaje:", err)
                return
            
            
            #visualizar_registros(page)
            forum_post(e)
            page.add(nuevo_mensaje)
            page.update()

                # Botón para ir atrás a la pantalla show_image_upload_screen
        back_button = ft.ElevatedButton(
            text="Ir atrás",
            on_click=show_image_upload_screen
        )

        page.add(back_button)


        def get_mensaje_data():
            response = requests.get("https://insectid-api-1086245255634.us-central1.run.app/forum/posts/")
            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list):
                    return data
            return []

        def visualizar_registros(page: ft.Page, intervalo=60):
            mensajes = get_mensaje_data()
            mensaje_containers = []
            for mensaje in mensajes:
                try:
                    mensaje_container = fc.create_mensaje_container(mensaje)
                    mensaje_containers.append(mensaje_container)
                except KeyError as e:
                    print(f"Error: Falta la clave {e} en el mensaje {mensaje}")

            page.add(
                ft.Column(
                    mensaje_containers,
                    scroll=ft.ScrollMode.AUTO
                )
            )
            page.update()





        def show_mensaje_form(e):
            
            dialog = ft.AlertDialog(
                content=mensaje_form,
                actions=[
                    ft.ElevatedButton("CERRAR", on_click=lambda e: close_dialog(dialog)),
                    ft.ElevatedButton("PUBLICAR", on_click =lambda e: publicar_y_cerrar(dialog)),
                ],
                modal=True
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()


        def publicar_y_cerrar(dialog):
            close_dialog(dialog)
            publicar_mensaje(e)

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

        visualizar_registros(page)






    def show_login_screen(e):
        page.clean()

        # Cargar el icono
        icono = ft.Image(src="public/ICONO.png", width=250, height=250)



        def signup(e):
            
            global myid
            username = username_input.value
            password = password_input.value
            print(username,password)
            url = "https://insectid-api-1086245255634.us-central1.run.app/auth/signup"
            datos = {
                "username": username,
                "password": password,
                "insects": []
            }

            try:
                respuesta = requests.post(url, json=datos)

                if respuesta.status_code == 200:
                    print("Usuario creado:", respuesta.json())
                    myid=respuesta.json().get('id')
                    show_image_upload_screen(e)
                    
                else:
                    print("Error al crear usuario:", respuesta.json())

            except Exception as e:
                print("Error de conexión:", e)





        # Función para manejar el inicio de sesión con usuario y contraseña
        def login(e):
            global myid
            username = username_input.value
            password = password_input.value

            url = "https://insectid-api-1086245255634.us-central1.run.app/auth/signin"
            datos = {
                "username": username,
                "password": password,
                "insects": []
            }

            try:
                respuesta = requests.post(url, json=datos)

                if respuesta.status_code == 200:
                    print("Sesión Iniciada:", respuesta.json())
                    myid=respuesta.json().get('id')
                    show_image_upload_screen(e)
                    
                else:
                    print("Error al iniciar sesión:", respuesta.json())

            except Exception as e:
                print("Error de conexión:", e)
            

        # Establecer la imagen de fondo
        try:
            page.background_image = ft.Image(src="public/FONT.png", fit=ft.ImageFit.COVER)
        except Exception as error:
            print(f"Error al cargar la imagen de fondo: {error}")

        # Campos para usuario y contraseña
        username_input = ft.TextField(label="Usuario", width=300)
        password_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
        error_message = ft.Text("", size=14, color="red")

        # Agregar los elementos a la página
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Text("Bienvenido a BichoLab", size=30, weight=ft.FontWeight.BOLD, color="black"),
                            alignment=ft.alignment.center
                        ),
                        icono,
                      
                        
                        username_input,
                        password_input,
                        error_message,
                        ft.ElevatedButton("Iniciar Sesión", on_click=login, style=ft.ButtonStyle(
                            bgcolor="blue", color="white")),
                        ft.ElevatedButton("Crear Cuenta", on_click=signup, style=ft.ButtonStyle(
                            bgcolor="blue", color="white")),
                        ft.Text("© 2024 Bicholab", size=12, color="black", italic=True)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                alignment=ft.alignment.center,
                padding=20,
                bgcolor="rgba(0, 0, 0, 0.5)"  # Fondo semitransparente para resaltar el contenido
            )
        )

        # Actualizar la página para reflejar los cambios
        page.update()









    async def handle_get_current_position(e):
        p = await gl.get_current_position_async()
        return p

    username_input = ft.TextField(label="Usuario")
    password_input = ft.TextField(label="Contraseña", password=True)
    error_text = ft.Text(color="red")
    classification_label = ft.Text("")

    copyright_text = ft.Container(
        content=ft.Text("Con todos los derechos reservados", italic=True, size=14, color=ft.colors.WHITE),
        bgcolor=ft.colors.GREEN,
        padding=10,
        alignment=ft.alignment.center
    )

    # Elementos de la UI
    file_picker = ft.FilePicker(on_result=on_file_picked)
    image = ft.Image(width=300, height=300, fit=ft.ImageFit.CONTAIN, visible=False)

    # Mapa
    marker_layer_ref = ft.Ref[map.MarkerLayer]()
    map_ref = ft.Ref[map.Map]()

    def add_marker(location, e):
        try:
            lat = location.latitude
            lon = location.longitude
            print(f"Adding marker at: {lat}, {lon}")  # Verifica los valores

            marker_layer_ref.current.markers.append(
                map.Marker(
                    content=ft.Icon(ft.icons.LOCATION_ON, color=ft.cupertino_colors.DESTRUCTIVE_RED),
                    coordinates=map.MapLatitudeLongitude(lat, lon),
                )
            )
            map_ref.current.center = map.MapLatitudeLongitude(lat, lon)
            map_ref.current.zoom = 10
            map_ref.current.update()  
            page.update()  
            
        except ValueError:
            print("Por favor, ingrese valores válidos para la latitud y longitud.")

    gl = ft.Geolocator(
        location_settings=ft.GeolocatorSettings(
            accuracy=ft.GeolocatorPositionAccuracy.LOW
        ),
    )
    page.overlay.append(gl)

    map_container = ft.Container(
        map.Map(
            ref=map_ref,
            expand=True,
            configuration=map.MapConfiguration(
                initial_center=map.MapLatitudeLongitude(3, -70),
                initial_zoom=4.2,
                interaction_configuration=map.MapInteractionConfiguration(
                    flags=map.MapInteractiveFlag.ALL
                ),
            ),
            layers=[
                map.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    on_image_error=lambda e: print("TileLayer Error"),
                ),
                map.MarkerLayer(ref=marker_layer_ref, markers=[]),
            ],
        ),
        width=500,
        height=500,
    )

 




    def insect_info_page(page: ft.Page):
        page.title = "Insect Information"
        

        # Contenedor para los mensajes
        message_container = ft.Column()

        # Enviar la imagen al backend al cargar la página
        def send_image_to_backend():
            global insect_id_gl
            if hasattr(image, 'src') and image.src:
                try:
                    if not image.src.startswith("http"):
                        with open(image.src, 'rb') as img_file:
                            image_data = img_file.read()
                            response = requests.post(urlapi + "classify/", files={'image': (os.path.basename(image.src), image_data)})
                    else:
                        image_data = requests.get(image.src).content
                        response = requests.post(urlapi + "classify/", files={'image': (os.path.basename(image.src), image_data)})
                    
                    if response.status_code == 200:
                        insect_id_gl = response.json().get('_id')
                        data = response.json().get('data', {})
                        display_insect_info(data)
                    else:
                        message_container.controls.append(ft.Text("Error en la clasificación.", color="red"))
                        page.update()
                except Exception as e:
                    message_container.controls.append(ft.Text(f"Error al enviar la imagen: {e}", color="red"))
                    page.update()
            else:
                message_container.controls.append(ft.Text("No hay imagen para enviar.", color="red"))
                page.update()

        # Función para guardar la imagen
        def save_insect(e):
            if hasattr(image, 'src') and image.src:
                try:
                    # Comprobar si la imagen es local o una URL
                    if not image.src.startswith("http"):
                        local_image_path = image.src
                        with open(local_image_path, 'rb') as img_file:
                            response = requests.post(
                                "https://insectid-api-1086245255634.us-central1.run.app/insects/upload/image/",
                                headers={'accept': 'application/json'},
                                files={'image': (os.path.basename(local_image_path), img_file, 'image/jpeg')}
                            )

                    else:
                        # Descargar y subir imagen desde una URL
                        response = requests.get(image.src)
                        if response.status_code == 200:
                            response = requests.post(
                                "https://insectid-api-1086245255634.us-central1.run.app/insects/upload/image/",
                                headers={'accept': 'application/json'},
                                files={'image': ('image.jpg', response.content, 'image/jpeg')}
                            )
                        else:
                            message_container.controls.append(ft.Text("No se pudo descargar la imagen desde la URL.", color="red"))
                            page.update()
                            return
                    
                    # Verificar si la subida fue exitosa
                    if response.status_code == 200:
                        image_name = response.json().get("image_name", "desconocido")
                        message_container.controls.append(ft.Text(f"Imagen guardada con éxito como: {image_name}", color="green"))
                        
                        # Preparar los datos del insecto
                        datos = {
                            "insect_id": insect_id_gl,
                            "image": image_name,
                            "location": {
                                "latitude": location_gl.latitude,
                                "longitude": location_gl.longitude
                            }
                        }
                        response_insect = requests.post(urlapi + f'users/{myid}/insects/add', json=datos)

                        # Diagnóstico
                        print(f"Response Status Code: {response_insect.status_code}")
                        print(f"Response Content: {response_insect.text}")
                        
                        if response_insect.status_code == 200:
                            print('Insecto guardado exitosamente')
                        else:
                            print('Error al guardar insecto')

                    else:
                        message_container.controls.append(ft.Text(f"Error al subir la imagen: {response.text}", color="red"))

                    page.update()

                except requests.RequestException as req_err:
                    message_container.controls.append(ft.Text(f"Error de conexión: {req_err}", color="red"))
                    page.update()
                except Exception as e:
                    message_container.controls.append(ft.Text(f"Error: {e}", color="red"))
                    page.update()
            else:
                message_container.controls.append(ft.Text("No hay imagen para guardar.", color="red"))
                page.update()

        # Función para mostrar la información del insecto
        def display_insect_info(data):
            common_name = ft.Text(value=f"Common Name: {data.get('common_name', 'Desconocido')}", size=20, weight="bold")
            taxonomy = ft.Column([
                ft.Text(value="Taxonomy:", size=18, weight="bold"),
                ft.Text(value=f"Order: {data['taxonomy']['order']}"),
                ft.Text(value=f"Family: {data['taxonomy']['family']}"),
                ft.Text(value=f"Genus: {data['taxonomy']['genus']}"),
                ft.Text(value=f"Species: {data['taxonomy']['specie']}")
            ])
            characteristics = ft.Column([
                ft.Text(value="Characteristics:", size=18, weight="bold"),
                ft.Text(value=f"Habitat: {data['characteristics']['habitat']}"),
                ft.Text(value=f"Diet: {data['characteristics']['diet']}"),
                ft.Text(value=f"Life Cycle: {data['characteristics']['life_cycle']}"),
                ft.Text(value=f"IUCN Status: {data['characteristics']['IUCN_status']}")
            ])
            description = ft.Text(value=f"Description: {data['description']}")
            image_json = ft.Column([
                ft.Text(value="Imagen de Base de Datos", size=18, weight="bold"),
                ft.Image(src=data['image'], width=300, height=300)
            ])
            uploaded_image = ft.Column([
                ft.Text(value="Imagen Fotografiada", size=18, weight="bold"),
                ft.Image(src=image.src, width=300, height=300)
            ])

            page.add(
                ft.Column(
                    [
                        common_name,
                        taxonomy,
                        characteristics,
                        description,
                        ft.Divider(height=20, thickness=2),
                        uploaded_image,
                        image_json,
                        share_buttons,
                        ft.ElevatedButton("Guardar este recuerdo", on_click=save_insect),
                        ft.ElevatedButton("Regresar", on_click=lambda e: show_image_upload_screen(e)),
                        message_container  # Agrega el contenedor de mensajes aquí
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                )
            )
            page.update()

        def share_facebook(e):
            cloudinary.config(
                cloud_name='dtmchrmdg',
                api_key='881676981548729',
                api_secret='L46w1mjbt65-3p-LVfKPZ7IlQIs'
            )

            def upload_image_to_cloudinary(image_path):
                try:
                    response = cloudinary.uploader.upload(image_path)
                    return response['secure_url']
                except Exception as ex:
                    print(f"Error al subir la imagen a Cloudinary: {ex}")
                    return None

            if hasattr(image, 'src') and image.src:
                image_path = image.src if not image.src.startswith("http") else None
                if image_path:
                    image_url = upload_image_to_cloudinary(image_path)

                    if image_url:
                        facebook_share_url = f"https://www.facebook.com/sharer/sharer.php?u={image_url}"
                        try:
                            page.launch_url(facebook_share_url)
                        except Exception as ex:
                            print(f"Error al abrir la URL de compartir en Facebook: {ex}")

        def share_instagram(e):
            message = "Para compartir en Instagram, guarda la imagen y utiliza el siguiente texto:\n\nMira he tomado esta foto con Bicho Lab:"
            snackbar = ft.SnackBar(ft.Text(message), action="OK")
            page.show_snack_bar(snackbar)

        # Botones de compartir
        share_buttons = ft.Row(
            [
                ft.IconButton(icon=ft.icons.ADD_A_PHOTO, on_click=share_instagram, tooltip="Compartir en Instagram"),
                ft.IconButton(icon=ft.icons.FACEBOOK, on_click=share_facebook, tooltip="Compartir en Facebook")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )


        

        # Llamar a la función para enviar la imagen al backend al cargar la página
        send_image_to_backend()


    # Suponiendo que `show_login_screen` es una función válida en tu código
    show_login_screen(None)

    
# Iniciar la aplicación
ft.app(target=main)
