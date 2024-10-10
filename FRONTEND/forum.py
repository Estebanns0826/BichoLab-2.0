import flet as ft
import forum_components as fc
import pandas as pd
import temas
import json



### ------------------------------------------------------------------------------------------------------------------------------------###
### LECTURA DE DATOS DESDE JSON

# Convierte los datos del archivo JSON en filas de DataTable
def create_data_rows(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    df = pd.DataFrame(data)
    
    rows = []
    for _, row in df.iterrows():
        cells = [ft.DataCell(ft.Text(str(cell))) for cell in row]
        rows.append(ft.DataRow(cells=cells))
    
    return rows

# Uso de la función con la ruta especificada
json_path = "forum_db/forum_test.json"
data_rows = create_data_rows(json_path)

### ------------------------------------------------------------------------------------------------------------------------------------###


def start_forum(page: ft.Page):
    page.add(
        ft.Column(
            [
                ft.Text("FORO", size=30, weight=ft.FontWeight.BOLD),
                fc.container_anuncios,
                fc.container_primeros_pasos,
                fc.container_funcionalidades,
                fc.container_comunidad
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )
    )

# Ejemplo de cómo iniciar la aplicación
if __name__ == "__main__":
    ft.app(target=start_forum)