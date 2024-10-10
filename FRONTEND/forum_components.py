import flet as ft
import requests
import forum

#CONSTANTS

#COLORS:
#GREENS:
BACKGROUND_COLOR = ft.colors.GREEN_200
CONTAINER_COLOR = ft.colors.GREEN_600
BACKGROUND_COLOR_BUTTON = ft.colors.GREEN_200
LETTERS_COLOR_BUTTON = ft.colors.GREEN_600

#REDS:

BACKGROUND_RED_COLOR_BUTTON = ft.colors.RED_200
LETTERS_RED_COLOR_BUTTON = ft.colors.RED_600

#SIZES:
START_COLUMN_WIDTH = 800
MIDDLE_COLUMN_WIDTH = 150
FINNISH_COLUMN_WIDTH = 350
MAX_WIDTH = 1200

#### PANTALLA INICIAL DEL FORO #### ------------------------------------------------------------------------------------------------------------------------------------

#### PANTALLA DE TEMAS | TOPICS DE UN TEMA #### ------------------------------------------------------------------------------------------------------------------------------------

## MANIPULAR DATOS PROVENIENTES DE LA BD

data_rows=forum.data_rows


def close_anchor(e):
    text = f"Color {e.control.data}"
    print(f"closing view from {text}")
    anchor.close_view(text)

def handle_change(e):
    print(f"handle_change e.data: {e.data}")
    filter_data(e.data)


def handle_submit(e):
    print(f"handle_submit e.data: {e.data}")
    filter_data(e.data)

def handle_tap(e):
    print(f"handle_tap")
    anchor.open_view()

    
# Filtra los datos de la DataTable en función de la entrada del usuario
def filter_data(query):
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    data_table.rows = create_data_rows(filtered_df)
    data_table.update()
    

anchor = ft.SearchBar(
    view_elevation=4,
    divider_color=BACKGROUND_COLOR,
    bar_hint_text="Buscar Temas...",
    view_hint_text="Sugerencias encontradas...",
    on_change=handle_change,
    on_submit=handle_submit,
    on_tap=handle_tap,
    controls=[
        ft.ListTile(title=ft.Text(f"Color {i}"), on_click=close_anchor, data=i)
        for i in range(10)
    ],
)

# Envuelve la SearchBar en un contenedor para hacerla responsiva
search_bar_container = ft.Container(
    content=anchor,
    expand=True,
)

topic_menu = ft.Container(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text("Foro General de Discusión",
                                          size=25,
                                          weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(
                                "Este es el lugar ideal para aprender y crecer. ¡Explora los temas que te interesan y participa en las discusiones!"
                            ),
                        ),  
                    ]
                ),
            ),
            alignment=ft.alignment.center,
            expand=True
        )
## ------------------------------------------------------------------------------------------------------------------------------------
## TOPIC CONTAINER --------------------------------------------------------------------------------------------------------------------
topic_container = ft.Container(
    content=ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("TITULO")),
            ft.DataColumn(ft.Text("CONTENIDO")),
            ft.DataColumn(ft.Text("AUTOR")),
            ft.DataColumn(ft.Text("ID_INSECTO")),
            ft.DataColumn(ft.Text("COMENTARIOS"))
        ],
        rows=data_rows,
        data_row_min_height=60,
        data_row_max_height=110,
    ),
    alignment=ft.alignment.center,
    expand=True,
    padding=10,
    bgcolor=CONTAINER_COLOR,
    width=MAX_WIDTH,
    border_radius=10,
    shadow=ft.BoxShadow(
        blur_radius=10,
        spread_radius=2,
    ),
)

## ------------------------------------------------------------------------------------------------------------------------------------
## MENSAJE CONTAINER -------------------------------------------------------------------------------------------------------------------- 

def create_mensaje_container(mensaje):
    mensaje_id = mensaje['_id']
    mensaje_data = mensaje['data']
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(value=f"Título: {mensaje_data['title']}",
                                    size=24, 
                                    weight=ft.FontWeight.BOLD),
                            ft.Text(value=f"{mensaje_data['content']}"),
                            ft.Text(value=f"Autor ID: {mensaje_data['author_id']}"),
                            ft.Text(value=f"ID del Insecto: {mensaje_data['user_insect_id']}"),
                            ft.Text(value=f"Comentarios: {mensaje_data['comments']}"),
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton(
                                        "COMENTAR",
                                        icon='add',
                                        icon_color=LETTERS_COLOR_BUTTON,
                                        color=LETTERS_COLOR_BUTTON,
                                        bgcolor=BACKGROUND_COLOR_BUTTON,
                                    ),
                                    ft.ElevatedButton(
                                        "ELIMINAR",
                                        icon="DELETE_SHARP",
                                        icon_color=LETTERS_RED_COLOR_BUTTON,
                                        color=LETTERS_RED_COLOR_BUTTON,
                                        bgcolor=BACKGROUND_RED_COLOR_BUTTON,
                                        on_click=lambda e: eliminar_registro(mensaje_id)
                                    ),
                                ]
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,  # Alinea el contenido al inicio
                        horizontal_alignment=ft.CrossAxisAlignment.START,  # Alinea el contenido al inicio horizontalmente
                    ),

                    bgcolor=CONTAINER_COLOR,
                    border_radius=10,
                    padding=10,
                    shadow=ft.BoxShadow(
                        blur_radius=10,
                        spread_radius=2,
                    ),
                    expand=True,
                    width=MAX_WIDTH,
                    
                ),
                
            ]
        ),
        alignment=ft.alignment.center,
    )


## ------------------------------------------------------------------------------------------------------------------------------------
## NUEVO MENSAJE BUTTON --------------------------------------------------------------------------------------------------------------------

# Define the function to handle the button click
def eliminar_registro(_id):
    url = f"https://insectid-api-1086245255634.us-central1.run.app/forum/post/{_id}/delete"
    try:
        response = requests.delete(url)
        if response.status_code == 200:
            print("Registro eliminado exitosamente")
        else:
            print(f"Error al eliminar el registro: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as err:
        print(f"Error de red: {err}")

# Create the button and assign the click event handler
# Assuming _id is obtained from somewhere in your application
eliminar_button = ft.ElevatedButton(
    "ELIMINAR",
    icon="DELETE_SHARP",
    icon_color=LETTERS_RED_COLOR_BUTTON,
    color=LETTERS_RED_COLOR_BUTTON,
    bgcolor=BACKGROUND_RED_COLOR_BUTTON,
    on_click=lambda e: eliminar_registro(mensaje_id)
)

'''# New code block
def obtener_id():
    url = "https://insectid-api-1086245255634.us-central1.run.app/forum/posts/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Suponiendo que el _id está en el primer registro de la lista de posts
        _id = data[0]['_id']
        return _id
    else:
        raise Exception("Error al obtener el _id de la API")

# Obtener el _id desde la API
_id = obtener_id()

# Llamar a la función eliminar_registro con el _id obtenido
eliminar_registro(_id)'''

