import flet as ft
import os

def main(page: ft.Page):
    page.bgcolor = "#FFF0F5"
    lista_de_compras = []
    page.scroll = ft.ScrollMode.ALWAYS

    logo_path = os.path.join(os.path.dirname(__file__), "img/LOGO.png")
    logo = ft.Image(src=logo_path, width=200, height=150)

    page.window.width = 600
    page.window.height = 400
    page.window.resizable = False
    page.title = "Lista de Compras"

    selector_archivos = ft.FilePicker(on_result=lambda e: guardar_archivo(e))
    page.overlay.append(selector_archivos)

    def mostrar_dialogo_error():
        def cerrar_dialogo(e):
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Error", color="#D1478B"),
            content=ft.Text("No puedes agregar un ítem en blanco.", color="#FF69B4"),
            actions=[ft.TextButton("OK", on_click=cerrar_dialogo, style=ft.ButtonStyle(bgcolor="#FFB6C1"))],
            open=True
        )
        page.update()

    def agregar_clic(e):
        if not nueva_tarea.value.strip():
            mostrar_dialogo_error()
            return

        item = crear_item(nueva_tarea.value)
        lista_de_compras.append(nueva_tarea.value)
        vista_lista.controls.append(item)
        nueva_tarea.value = ""
        nueva_tarea.focus()
        page.update()
        actualizar_botones()

    def crear_item(texto):
        checkbox = ft.Checkbox(label=texto, fill_color="#FF69B4")
        boton_editar = ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: editar_clic(e, checkbox, item), icon_color="#D1478B")
        boton_eliminar = ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: eliminar_clic(e, item, texto), icon_color="#D1478B")
        item = ft.Row([checkbox, boton_editar, boton_eliminar], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        return item

    def editar_clic(e, checkbox, item):
        nuevo_valor = ft.TextField(value=checkbox.label, width=300, bgcolor="#FFD1DC")
        boton_guardar = ft.IconButton(icon=ft.icons.SAVE, on_click=lambda e: guardar_clic(e, checkbox, nuevo_valor, item), icon_color="#D1478B")
        boton_cancelar = ft.IconButton(icon=ft.icons.CANCEL, on_click=lambda e: cancelar_clic(e, checkbox, item), icon_color="#D1478B")
        item.controls = [nuevo_valor, boton_guardar, boton_cancelar]
        page.update()

    def guardar_clic(e, checkbox, nuevo_valor, item):
        checkbox.label = nuevo_valor.value
        item.controls = [
            checkbox,
            ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: editar_clic(e, checkbox, item), icon_color="#D1478B"),
            ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: eliminar_clic(e, item, checkbox.label), icon_color="#D1478B")
        ]
        page.update()

    def cancelar_clic(e, checkbox, item):
        item.controls = [
            checkbox,
            ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: editar_clic(e, checkbox, item), icon_color="#D1478B"),
            ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: eliminar_clic(e, item, checkbox.label), icon_color="#D1478B")
        ]
        page.update()

    def eliminar_clic(e, item, texto):
        lista_de_compras.remove(texto)
        vista_lista.controls.remove(item)
        page.update()
        actualizar_botones()

    def exportar_lista(e):
        # Configurar el FilePicker para permitir seleccionar varios formatos
        selector_archivos.save_file(allowed_extensions=["txt", "csv", "json"])

    def guardar_archivo(e):
        if e.path:
            _, extension = os.path.splitext(e.path)
            with open(e.path, "w") as file:
                if extension == ".txt":
                    for item in lista_de_compras:
                        file.write(f"{item}\n")
                elif extension == ".csv":
                    file.write("Ítem\n")
                    for item in lista_de_compras:
                        file.write(f"{item}\n")
                elif extension == ".json":
                    import json
                    json.dump({"lista_de_compras": lista_de_compras}, file, indent=4)

            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Lista guardada como {extension}."),
                bgcolor="#FFB6C1"
            )
            page.snack_bar.open = True
            page.update()

    def limpiar_lista(e):
        lista_de_compras.clear()
        vista_lista.controls.clear()
        page.update()
        actualizar_botones()

    def actualizar_botones():
        fila_botones.controls = [
            nueva_tarea,
            ft.ElevatedButton("Agregar", on_click=agregar_clic, bgcolor="#FF69B4", color="white")
        ]
        if lista_de_compras:
            fila_botones.controls.append(
                ft.ElevatedButton(
                    "Descargar", on_click=exportar_lista, bgcolor="#FF1493", 
                    color="white", width=120, height=30
                )
            )
            boton_limpiar.visible = True
        else:
            boton_limpiar.visible = False
        page.update()

    nueva_tarea = ft.TextField(hint_text="¿Qué necesitas comprar?", width=250, bgcolor="#FFD1DC")

    boton_limpiar = ft.ElevatedButton(
        "Limpiar lista", on_click=limpiar_lista, bgcolor="#FF1493", 
        color="white", width=200, height=50, visible=False
    )

    texto_encabezado = ft.Text("Bienvenidos a tu lista de compras ROSA", size=20, weight=ft.FontWeight.BOLD, color="#D1478B")

    encabezado = ft.Column(
        [logo, texto_encabezado], 
        alignment=ft.MainAxisAlignment.CENTER, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    fila_botones = ft.Row(
        [nueva_tarea, ft.ElevatedButton("Agregar", on_click=agregar_clic, bgcolor="#FF69B4", color="white")],
        alignment=ft.MainAxisAlignment.CENTER
    )

    vista_lista = ft.Column([], expand=True, alignment=ft.MainAxisAlignment.START)

    contenedor = ft.Column(
        [encabezado, ft.Divider(height=20, color="#FFC0CB"), fila_botones, boton_limpiar, vista_lista],
        expand=True, alignment=ft.MainAxisAlignment.CENTER, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(contenedor)

ft.app(target=main)
