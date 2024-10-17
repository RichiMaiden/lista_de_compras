import flet as ft

def main(page: ft.Page):
    # Definir ancho y alto de la ventana
    page.window_width = 450  # ancho de la ventana
    page.window_height = 650  # alto de la ventana
    page.title = "Lista de Compras"

    def add_clicked(e):
        item = create_item(new_task.value)
        page.add(item)
        new_task.value = ""
        new_task.focus()

    def create_item(text):
        checkbox = ft.Checkbox(label=text)
        edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_clicked(e, checkbox, item))
        delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_clicked(e, item))
        item = ft.Row([checkbox, edit_button, delete_button])
        return item

    def edit_clicked(e, checkbox, item):
        new_value = ft.TextField(value=checkbox.label, width=300)
        save_button = ft.IconButton(icon=ft.icons.SAVE, on_click=lambda e: save_clicked(e, checkbox, new_value, item))
        cancel_button = ft.IconButton(icon=ft.icons.CANCEL, on_click=lambda e: cancel_clicked(e, checkbox, item))
        item.controls = [new_value, save_button, cancel_button]
        page.update()

    def save_clicked(e, checkbox, new_value, item):
        checkbox.label = new_value.value
        edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_clicked(e, checkbox, item))
        delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_clicked(e, item))
        item.controls = [checkbox, edit_button, delete_button]
        page.update()

    def cancel_clicked(e, checkbox, item):
        edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_clicked(e, checkbox, item))
        delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_clicked(e, item))
        item.controls = [checkbox, edit_button, delete_button]
        page.update()

    def delete_clicked(e, item):
        page.controls.remove(item)
        page.update()

    new_task = ft.TextField(hint_text="¿Qué necesitas comprar?", width=300)

    # Usar una ruta relativa para la imagen
    logo = ft.Image(src="home/kaalinux/Documentos/proyecto/image/logo1.png", width=200, height=150)
    header_text = ft.Text("Bienvenidos a la App de Lista de Compras", size=20, weight=ft.FontWeight.BOLD)

    # Organizamos cabecera en una columna
    header = ft.Column([
        logo,
        header_text
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Añadimos elementos a la aplicación
    page.add(
        header,  # Para que muestre el texto primero
        ft.Divider(height=20),  # Agrega un divisor para separar el logo de la sección
        ft.Row([new_task, ft.ElevatedButton("Agregar", on_click=add_clicked)])
    )

ft.app(target=main)