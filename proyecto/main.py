import flet as ft
import os

def main(page: ft.Page):
    # Establecemos el color de fondo en verde agua (verde claro)
    page.bgcolor = "#34495e"  # Color verde agua

    # Definimos una lista para almacenar los ítems
    shopping_list = []

    logo_path = os.path.join(os.path.dirname(__file__), "image/logo1.png")
    logo = ft.Image(src=logo_path, width=200, height=150)

    # Definir ancho y alto de la ventana
    page.window_width = 450  # ancho de la ventana
    page.window_height = 650  # alto de la ventana
    page.title = "Lista de Compras"

    # Función para mostrar un cuadro de diálogo con un mensaje de error
    def show_error_dialog():
        def close_dlg(e):
            page.dialog.open = False  # Cerrar el diálogo
            page.update()  # Actualizar la página

        page.dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text("No puedes agregar un ítem en blanco."),
            actions=[ft.TextButton("OK", on_click=close_dlg)],  # Llama a la función para cerrar
            open=True
        )
        page.update()

    # Función para agregar un nuevo ítem
    def add_clicked(e):
        # Validar que no esté vacío el campo de texto
        if not new_task.value.strip():  # Comprobamos si el campo está vacío
            show_error_dialog()  # Mostrar el cuadro de diálogo
            return

        # Crear y agregar el ítem si no está vacío
        item = create_item(new_task.value)
        shopping_list.append(new_task.value)  # Añadir el texto a la lista de compras
        page.add(item)
        new_task.value = ""
        new_task.focus()

        # Actualizar los controles para mostrar el botón de exportar si hay ítems en la lista
        update_buttons()

    # Crear el ítem con checkbox y botones de edición/eliminación
    def create_item(text):
        checkbox = ft.Checkbox(label=text)
        edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_clicked(e, checkbox, item))
        delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_clicked(e, item, text))
        item = ft.Row([checkbox, edit_button, delete_button])
        return item

    # Función para editar un ítem
    def edit_clicked(e, checkbox, item):
        new_value = ft.TextField(value=checkbox.label, width=300)
        save_button = ft.IconButton(icon=ft.icons.SAVE, on_click=lambda e: save_clicked(e, checkbox, new_value, item))
        cancel_button = ft.IconButton(icon=ft.icons.CANCEL, on_click=lambda e: cancel_clicked(e, checkbox, item))
        item.controls = [new_value, save_button, cancel_button]
        page.update()

    # Función para guardar cambios en un ítem
    def save_clicked(e, checkbox, new_value, item):
        checkbox.label = new_value.value
        edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_clicked(e, checkbox, item))
        delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_clicked(e, item, checkbox.label))
        item.controls = [checkbox, edit_button, delete_button]
        page.update()

    # Función para cancelar la edición
    def cancel_clicked(e, checkbox, item):
        edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_clicked(e, checkbox, item))
        delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_clicked(e, item, checkbox.label))
        item.controls = [checkbox, edit_button, delete_button]
        page.update()

    # Función para eliminar un ítem
    def delete_clicked(e, item, text):
        shopping_list.remove(text)  # Remover de la lista de compras
        page.controls.remove(item)
        page.update()
        update_buttons()  # Actualizar los botones si la lista está vacía

    # Función para exportar la lista a un archivo .txt y permitir que el usuario lo descargue
    def export_list(e):
        if shopping_list:  # Verificar que haya ítems en la lista
            # Creamos el archivo .txt
            file_path = "lista_de_compras.txt"
            with open(file_path, "w") as file:
                for item in shopping_list:
                    file.write(f"{item}\n")

            # Mostrar cuadro de diálogo con el enlace de descarga
            download_link = ft.TextButton("Descargar archivo", on_click=lambda e: page.launch_url(f"/{file_path}"))
            
            page.dialog = ft.AlertDialog(
                title=ft.Text("Éxito"),
                content=ft.Text("Haz clic en el siguiente enlace para descargar la lista:"),
                actions=[download_link],
                open=True
            )
            page.update()

    # Función para actualizar los botones (Agregar y Exportar)
    def update_buttons():
        button_row.controls = [
            new_task,
            ft.ElevatedButton("Agregar", on_click=add_clicked),
        ]

        # Si la lista no está vacía, agregamos el botón de exportar
        if shopping_list:
            button_row.controls.append(ft.ElevatedButton("Exportar Lista a .txt", on_click=export_list))
        
        page.update()

    # Campo de entrada para nuevo ítem
    new_task = ft.TextField(hint_text="¿Qué necesitas comprar?", width=250)
    
    # Creamos una cabecera con el logo y el texto de bienvenida
    header_text = ft.Text("Bienvenidos a la App de Lista de Compras", size=20, weight=ft.FontWeight.BOLD)

    # Organizamos cabecera en una columna
    header = ft.Column([
        logo,
        header_text
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Definimos una fila para los botones
    button_row = ft.Row([
        new_task,
        ft.ElevatedButton("Agregar", on_click=add_clicked)  # Botón para agregar ítems
    ])

    # Añadimos elementos a la aplicación
    page.add(
        header,  # Para que muestre el texto primero
        ft.Divider(height=20),  # Agrega un divisor para separar el logo de la sección
        button_row  # Fila de botones
    )

ft.app(target=main)

