import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import numpy as np
import main  

# -----------------------------
# Utilidades
# -----------------------------
def pil_to_np(img: Image.Image):
    return np.array(img.convert("RGB"))

def np_to_pil(arr: np.ndarray):
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

# -----------------------------
# Clase principal
# -----------------------------
class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes - Pablo Marín")
        self.root.geometry("1000x700")

        self.img = None
        self.img2 = None
        self.result = None

        self._crear_menu()
        self._crear_panel_controles()
        self._crear_canvas()

    # ----------------------------
    # Secciones de UI
    # ----------------------------
    def _crear_menu(self):
        menubar = tk.Menu(self.root)
        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Abrir imagen 1", command=self.abrir_imagen)
        archivo_menu.add_command(label="Abrir imagen 2", command=self.abrir_imagen2)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Guardar resultado", command=self.guardar_resultado)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        self.root.config(menu=menubar)

    def _crear_panel_controles(self):
        # Canvas para scroll
        panel_canvas = tk.Canvas(self.root, width=250)
        panel_canvas.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=panel_canvas.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        panel_canvas.configure(yscrollcommand=scrollbar.set)

        # Frame dentro del canvas
        frame = ttk.Frame(panel_canvas, padding=10)
        frame_id = panel_canvas.create_window((0,0), window=frame, anchor="nw")

        def on_frame_configure(event):
            panel_canvas.configure(scrollregion=panel_canvas.bbox("all"))
        frame.bind("<Configure>", on_frame_configure)

        # Habilitar scroll con la rueda del ratón
        def _on_mousewheel(event):
            panel_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        panel_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # --- Controles ---
        ttk.Label(frame, text="Brillo global").pack()
        self.brillo_scale = ttk.Scale(frame, from_=-1, to=1, orient=tk.HORIZONTAL, command=self.aplicar_brillo)
        self.brillo_scale.set(0)
        self.brillo_scale.pack(fill=tk.X, pady=5)

        ttk.Label(frame, text="Brillo por canal (R, G, B)").pack(pady=(10,0))
        self.entry_r = ttk.Entry(frame, width=5)
        self.entry_g = ttk.Entry(frame, width=5)
        self.entry_b = ttk.Entry(frame, width=5)
        self.entry_r.insert(0, "0")
        self.entry_g.insert(0, "0")
        self.entry_b.insert(0, "0")
        for e in (self.entry_r, self.entry_g, self.entry_b):
            e.pack(pady=2)
        ttk.Button(frame, text="Aplicar brillo por canal", command=self.aplicar_brillo_canal).pack(pady=5)

        ttk.Button(frame, text="Contraste logarítmico", command=self.aplicar_contraste_log).pack(fill=tk.X, pady=2)
        ttk.Button(frame, text="Contraste exponencial", command=self.aplicar_contraste_exp).pack(fill=tk.X, pady=2)
        ttk.Button(frame, text="Negativo", command=self.aplicar_negativo).pack(fill=tk.X, pady=2)
        ttk.Button(frame, text="Grises", command=self.aplicar_grises).pack(fill=tk.X, pady=2)
        ttk.Button(frame, text="Binarizar", command=self.aplicar_binarizacion).pack(fill=tk.X, pady=2)
        ttk.Button(frame, text="Histograma", command=self.mostrar_histograma).pack(fill=tk.X, pady=2)

        # --- NUEVAS FUNCIONES ---
        ttk.Label(frame, text="Recorte (x1,y1,x2,y2)").pack(pady=(10,0))
        self.recorte_entry = ttk.Entry(frame, width=20)
        self.recorte_entry.insert(0, "50,50,200,200")
        self.recorte_entry.pack(pady=2)
        ttk.Button(frame, text="Recortar", command=self.aplicar_recorte).pack(fill=tk.X, pady=2)

        ttk.Label(frame, text="Zoom área (x1,y1,x2,y2,escala)").pack(pady=(10,0))
        self.zoom_entry = ttk.Entry(frame, width=25)
        self.zoom_entry.insert(0, "50,50,150,150,2")
        self.zoom_entry.pack(pady=2)
        ttk.Button(frame, text="Zoom área", command=self.aplicar_zoom_area).pack(fill=tk.X, pady=2)

        ttk.Label(frame, text="Extraer capa RGB (0=R,1=G,2=B)").pack(pady=(10,0))
        self.capa_rgb_entry = ttk.Entry(frame, width=5)
        self.capa_rgb_entry.insert(0, "0")
        self.capa_rgb_entry.pack(pady=2)
        ttk.Button(frame, text="Extraer capa RGB", command=self.aplicar_extraer_capa_rgb).pack(fill=tk.X, pady=2)

        ttk.Label(frame, text="Extraer capa CMYK (0=C,1=M,2=Y,3=K)").pack(pady=(10,0))
        self.capa_cmyk_entry = ttk.Entry(frame, width=5)
        self.capa_cmyk_entry.insert(0, "3")
        self.capa_cmyk_entry.pack(pady=2)
        ttk.Button(frame, text="Extraer capa CMYK", command=self.aplicar_extraer_capa_cmyk).pack(fill=tk.X, pady=2)

        ttk.Label(frame, text="Rotación (°)").pack(pady=(10,0))
        self.rotacion_entry = ttk.Entry(frame, width=5)
        self.rotacion_entry.insert(0, "0")
        self.rotacion_entry.pack(pady=2)
        ttk.Button(frame, text="Rotar", command=self.aplicar_rotacion).pack(fill=tk.X, pady=2)

        ttk.Button(frame, text="Fusión simple", command=self.aplicar_fusion).pack(fill=tk.X, pady=5)
        ttk.Button(frame, text="Fusión ecualizada", command=self.aplicar_fusion_eq).pack(fill=tk.X, pady=5)
    # --- NUEVAS FUNCIONES ---
    def aplicar_recorte(self):
        if self.img is None:
            return
        try:
            coords = list(map(int, self.recorte_entry.get().split(',')))
            if len(coords) != 4:
                raise ValueError("Se requieren 4 valores: x1,y1,x2,y2")
            np_img = pil_to_np(self.img)
            out = main.recortar_imagen(np_img, *coords)
            self.mostrar_imagen(np_to_pil(out))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def aplicar_zoom_area(self):
        if self.img is None:
            return
        try:
            vals = list(map(int, self.zoom_entry.get().split(',')))
            if len(vals) != 5:
                raise ValueError("Se requieren 5 valores: x1,y1,x2,y2,escala")
            np_img = pil_to_np(self.img)
            out = main.zoom_area(np_img, *vals)
            self.mostrar_imagen(np_to_pil(out))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def aplicar_extraer_capa_rgb(self):
        if self.img is None:
            return
        try:
            canal = int(self.capa_rgb_entry.get())
            if canal not in [0,1,2]:
                raise ValueError("Canal debe ser 0, 1 o 2")
            np_img = pil_to_np(self.img)
            out = main.extraer_capa_rgb(np_img, canal)
            self.mostrar_imagen(np_to_pil(out))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def aplicar_extraer_capa_cmyk(self):
        if self.img is None:
            return
        try:
            canal = int(self.capa_cmyk_entry.get())
            if canal not in [0,1,2,3]:
                raise ValueError("Canal debe ser 0, 1, 2 o 3")
            np_img = pil_to_np(self.img)
            out = main.extraer_capa_cmyk(np_img, canal)
            self.mostrar_imagen(Image.fromarray(out))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _crear_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="gray")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # -----------------------------
    # Funciones de imagen
    # -----------------------------
    def abrir_imagen(self):
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not path: return
        self.img = Image.open(path).convert("RGB")
        self.mostrar_imagen(self.img)

    def abrir_imagen2(self):
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not path: return
        self.img2 = Image.open(path).convert("RGB")
        messagebox.showinfo("Imagen 2", "Segunda imagen cargada correctamente.")

    def mostrar_imagen(self, img):
        self.result = img
        img_resized = img.copy()
        img_resized.thumbnail((600, 600))
        self.tk_img = ImageTk.PhotoImage(img_resized)
        self.canvas.delete("all")
        self.canvas.create_image(300, 300, image=self.tk_img)

    def guardar_resultado(self):
        if self.result is None:
            messagebox.showwarning("Aviso", "No hay imagen para guardar.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            self.result.save(path)
            messagebox.showinfo("Guardado", f"Imagen guardada en {path}")

    # -----------------------------
    # Transformaciones
    # -----------------------------
    def aplicar_brillo(self, _=None):
        if self.img is None: return
        valor = float(self.brillo_scale.get())
        np_img = pil_to_np(self.img)
        out = main.ajustar_brillo(np_img, valor)
        self.mostrar_imagen(np_to_pil(out))

    def aplicar_brillo_canal(self):
        if self.img is None: return
        valores = [int(self.entry_r.get()), int(self.entry_g.get()), int(self.entry_b.get())]
        np_img = pil_to_np(self.img)
        out = main.ajustar_brillo_canal(np_img, valores)
        self.mostrar_imagen(np_to_pil(out))

    def aplicar_contraste_log(self):
        if self.img is None: return
        np_img = pil_to_np(self.img)
        out = main.contraste_logaritmico(np_img)
        self.mostrar_imagen(np_to_pil(out))

    def aplicar_contraste_exp(self):
        if self.img is None: return
        np_img = pil_to_np(self.img)
        out = main.contraste_exponencial(np_img, gamma=1.2)
        self.mostrar_imagen(np_to_pil(out))

    def aplicar_negativo(self):
        if self.img is None: return
        np_img = pil_to_np(self.img)
        out = main.foto_negativa(np_img)
        self.mostrar_imagen(np_to_pil(out))

    def aplicar_grises(self):
        if self.img is None: return
        np_img = pil_to_np(self.img)
        out = main.convertir_a_grises(np_img)
        self.mostrar_imagen(Image.fromarray(out))

    def aplicar_binarizacion(self):
        if self.img is None: return
        np_img = pil_to_np(self.img)
        out = main.binarizar(np_img, umbral=128)
        self.mostrar_imagen(Image.fromarray(out))

    def aplicar_rotacion(self):
        if self.img is None: return
        try:
            angulo = int(self.rotacion_entry.get())
            np_img = pil_to_np(self.img)
            out = main.rotar_imagen(np_img, angulo)
            self.mostrar_imagen(np_to_pil(out))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def aplicar_fusion(self):
        if self.img is None or self.img2 is None:
            messagebox.showwarning("Aviso", "Carga dos imágenes para fusionar.")
            return
        out = main.fusionar_imagenes(pil_to_np(self.img), pil_to_np(self.img2), alpha=0.5)
        self.mostrar_imagen(np_to_pil(out))

    def aplicar_fusion_eq(self):
        if self.img is None or self.img2 is None:
            messagebox.showwarning("Aviso", "Carga dos imágenes para fusionar.")
            return
        out = main.fusionar_imagenes_ecualizadas(pil_to_np(self.img), pil_to_np(self.img2), alpha=0.5)
        self.mostrar_imagen(np_to_pil(out))

    def mostrar_histograma(self):
        if self.result is None:
            messagebox.showwarning("Aviso", "Primero aplica una transformación o abre una imagen.")
            return
        np_img = pil_to_np(self.result)
        main.mostrar_histograma(np_img)


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()