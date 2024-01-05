from tkinter import ttk 
from tkinter import *
import sqlite3

class VentanaPrincipal:

    DB_PATH = 'database/productos.db'

    def __init__(self, root):
        self.db = self.DB_PATH
        self.ventana = root
        self.ventana.title('App Gestor de Productos')
        self.ventana.resizable(1, 1)
        self.ventana.wm_iconbitmap('static/ico.ico')

        frame = LabelFrame(self.ventana, text='Registrar un nuevo Producto',font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=20, pady=20)

        self.etiqueta_nombre = Label(frame, text='Nombre: ',font=('Calibri', 13))
        self.etiqueta_nombre.grid(row=1, column=0)
        self.nombre = Entry(frame, font=('Calibri', 13))
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        self.etiqueta_precio = Label(frame, text='Precio: ',font=('Calibri', 13))
        self.etiqueta_precio.grid(row=2, column=0)
        self.precio = Entry(frame, font=('Calibri', 13))
        self.precio.grid(row=2, column=1)

        self.etiqueta_categoria = Label(frame, text='Categoría: ',font=('Calibri', 13))
        self.etiqueta_categoria.grid(row=3, column=0)
        self.categoria = Entry(frame, font=('Calibri', 13))
        self.categoria.grid(row=3, column=1)

        self.etiqueta_stock = Label(frame, text='Stock: ',font=('Calibri', 13))
        self.etiqueta_stock.grid(row=4, column=0)
        self.stock = Entry(frame, font=('Calibri', 13))
        self.stock.grid(row=4, column=1)

        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, style='my.TButton')
        self.boton_aniadir.grid(row=5, columnspan=2, sticky=W + E)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.tabla = ttk.Treeview(height=20, columns=('Nombre', 'Precio', 'Categoría', 'Stock'), style="mystyle.Treeview")
        self.tabla.grid(row=6, column=0, columnspan=2)

        self.tabla.heading('Nombre', text='Nombre', anchor=CENTER)
        self.tabla.heading('Precio', text='Precio', anchor=CENTER)
        self.tabla.heading('Categoría', text='Categoría', anchor=CENTER)
        self.tabla.heading('Stock', text='Stock', anchor=CENTER)

        self.mensaje = Label(text='', fg='red')
        self.mensaje.grid(row=5, column=0, columnspan=2, sticky=W + E)

        self.get_productos()

        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto, style='my.TButton')
        boton_eliminar.grid(row=7, column=0, sticky=W + E)
        boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto, style='my.TButton')
        boton_editar.grid(row=7, column=1, sticky=W + E)

    def db_consulta(self, consulta, parametros=()):
        try:
            with sqlite3.connect(self.db) as con:
                cursor = con.cursor()
                cursor.execute(consulta, parametros)
                con.commit()

            # Devolver los resultados de la consulta
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en la consulta: {e}")
            return None

    def get_productos(self):
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        registros_db = self.db_consulta(query)

        if registros_db is not None:  # Añadida comprobación para evitar el error 'NoneType'
            for fila in registros_db:
                if len(fila) >= 4:
                    self.tabla.insert('', 0, values=(fila[1], fila[2], fila[3], fila[4]))
                else:
                    print(f"La fila {fila} no tiene suficientes elementos.")
    def validacion_nombre(self):
        return len(self.nombre.get()) != 0

    def validacion_precio(self):
        return len(self.precio.get()) != 0

    def validacion_categoria(self):
        return len(self.categoria.get()) != 0

    def validacion_stock(self):
        return len(self.stock.get()) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() and self.validacion_stock():
            query = 'INSERT INTO producto VALUES(NULL, ?, ?, ?, ?)'
            parametros = (self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get())
            self.db_consulta(query, parametros)
            self.mensaje['text'] = f'Producto {self.nombre.get()} añadido con éxito'
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
            self.categoria.delete(0, END)
            self.stock.delete(0, END)
        else:
            self.mensaje['text'] = 'Todos los campos son obligatorios'

        self.get_productos()

    def del_producto(self):
        self.mensaje['text'] = ''
        try:
            seleccion = self.tabla.selection()
            if not seleccion:
                raise IndexError("No se ha seleccionado un producto")
            
            nombre = self.tabla.item(seleccion)['values'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        query = 'DELETE FROM producto WHERE nombre = ?'
        self.db_consulta(query, (nombre,))
        self.mensaje['text'] = f'Producto {nombre} eliminado con éxito'
        self.get_productos()

    def edit_producto(self):
        self.mensaje['text'] = ''
        try:
            seleccion = self.tabla.selection()
            if not seleccion:
                raise IndexError("No se ha seleccionado un producto")
            
            nombre = self.tabla.item(seleccion)['values'][0]
            old_precio = self.tabla.item(seleccion)['values'][1]
            old_categoria = self.tabla.item(seleccion)['values'][2]
            old_stock = self.tabla.item(seleccion)['values'][3]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Producto")
        self.ventana_editar.resizable(1, 1)
        self.ventana_editar.wm_iconbitmap('static/ico.ico')

        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto")
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        etiqueta_nombre_anituguo = Label(frame_ep, text="Nombre antiguo: ", font=('Calibri', 16, 'bold'))
        etiqueta_nombre_anituguo.grid(row=2, column=0)

        input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly', font=('Calibri', 13))
        input_nombre_antiguo.grid(row=2, column=1)

        etiqueta_precio_anituguo = Label(frame_ep, text="Precio antiguo: ", font=('Calibri', 16, 'bold'))
        etiqueta_precio_anituguo.grid(row=4, column=0)

        input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio), state='readonly', font=('Calibri', 13))
        input_precio_antiguo.grid(row=4, column=1)

        etiqueta_categoria_antigua = Label(frame_ep, text="Categoría antigua: ", font=('Calibri', 16, 'bold'))
        etiqueta_categoria_antigua.grid(row=5, column=0)

        input_categoria_antigua = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria), state='readonly', font=('Calibri', 13))
        input_categoria_antigua.grid(row=5, column=1)

        etiqueta_stock_antiguo = Label(frame_ep, text="Stock antiguo: ", font=('Calibri', 16, 'bold'))
        etiqueta_stock_antiguo.grid(row=6, column=0)

        input_stock_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_stock), state='readonly', font=('Calibri', 13))
        input_stock_antiguo.grid(row=6, column=1)

        etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ")
        etiqueta_nombre_nuevo.grid(row=3, column=0)

        input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        input_nombre_nuevo.grid(row=3, column=1)
        input_nombre_nuevo.focus()

        etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13))
        etiqueta_precio_nuevo.grid(row=7, column=0)

        input_precio_nuevo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio), font=('Calibri', 13))
        input_precio_nuevo.grid(row=7, column=1)

        etiqueta_categoria_nueva = Label(frame_ep, text="Categoría nueva: ", font=('Calibri', 13))
        etiqueta_categoria_nueva.grid(row=8, column=0)

        input_categoria_nueva = Entry(frame_ep, font=('Calibri', 13))
        input_categoria_nueva.grid(row=8, column=1)

        etiqueta_stock_nuevo = Label(frame_ep, text="Stock nuevo: ", font=('Calibri', 13))
        etiqueta_stock_nuevo.grid(row=9, column=0)

        input_stock_nuevo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_stock), font=('Calibri', 13))
        input_stock_nuevo.grid(row=9, column=1)

        # Boton Actualizar Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto",
                                    style='my.TButton',
                                    command=lambda:
                                    self.actualizar_productos(input_nombre_nuevo.get(),
                                                                input_nombre_antiguo.get(),
                                                                input_precio_nuevo.get(),
                                                                input_precio_antiguo.get(),
                                                                input_categoria_nueva.get(),
                                                                input_categoria_antigua.get(),
                                                                input_stock_nuevo.get(),
                                                                input_stock_antiguo.get()))

        boton_actualizar.grid(row=10, columnspan=2, sticky=W + E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio, nueva_categoria, antigua_categoria, nuevo_stock, antiguo_stock):
        query = 'UPDATE producto SET nombre = ?, precio = ?, categoria = ?, stock = ? WHERE nombre = ? AND precio = ? AND categoria = ? AND stock = ?'
        if (nuevo_nombre != antiguo_nombre or nuevo_precio != antiguo_precio or nueva_categoria != antigua_categoria or nuevo_stock != antiguo_stock):
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            self.db_consulta(query, parametros)
            self.ventana_editar.destroy()
            self.mensaje['text'] = f'El producto {antiguo_nombre} ha sido actualizado con éxito'
            self.ventana.update()  # Refrescar la interfaz
            self.get_productos()  # Intenta obtener los datos actualizados
        else:
            self.ventana_editar.destroy()
            self.mensaje['text'] = f'El producto {antiguo_nombre} NO ha sido actualizado'
            self.ventana.update()  # Refrescar la interfaz
            self.get_productos()  # Intenta obtener los datos actualizados


if __name__ == '__main__':
    root = Tk()
    app = VentanaPrincipal(root)
    root.mainloop()