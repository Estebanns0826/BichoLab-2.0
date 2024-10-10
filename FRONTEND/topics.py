import flet as ft
import forum_components as fc

def start_topics(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    page.add(
        ft.Column(
            [
                fc.topic_menu,
                fc.topic_container  # Asegúrate de que topic_container es un objeto de control de Flet
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
    ft.app(target=start_topics)