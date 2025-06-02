from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar, Canvas, Frame
import traceback
import logic

def show_results_in_gui(query_results, result_frame):
    for widget in result_frame.winfo_children():
        widget.destroy()

    logic.image_refs.clear()
    result_count = len(query_results['ids'][0])

    grid_frame = tk.Frame(result_frame)
    grid_frame.grid(row=0, column=1)

    result_frame.grid_columnconfigure(0, weight=1)
    result_frame.grid_columnconfigure(1, weight=0)
    result_frame.grid_columnconfigure(2, weight=1)

    for j in range(result_count):
        data = query_results['data'][0][j]
        distance = query_results['distances'][0][j]
        metadata = query_results['metadatas'][0][j]

        image = Image.fromarray(data).resize((250, 250))
        tk_img = ImageTk.PhotoImage(image)
        logic.image_refs.append(tk_img)

        frame = tk.Frame(grid_frame, padx=10, pady=15)
        row = j // 3
        col = j % 3

        frame.grid(row=row, column=col, padx=10, pady=10)

        tk.Label(frame, image=tk_img).pack()
        text = f"{metadata['class_name']} ({distance:.2f})"
        tk.Label(frame, text=text, font=("Helvetica", 12)).pack(pady=5)

def select_image(user_image_label):
    file_path = filedialog.askopenfilename(
        title="Оберіть зображення",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if file_path:
        try:
            image = Image.open(file_path).convert("RGB").resize((250, 250))
            tk_img = ImageTk.PhotoImage(image)
            user_image_label.config(image=tk_img)
            user_image_label.image = tk_img

            return file_path
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to process image:\n{e}")

def create_main_menu():
    root = tk.Tk()
    root.title("Головне меню")
    root.geometry("400x250")

    label = tk.Label(root, text="Метод пошуку релевантних зображень", font=("Helvetica", 16, "bold"))
    label.pack(pady=20)

    search_button = tk.Button(root, text="Пошук за зображенням", font=("Helvetica", 12),
                              command=lambda: open_search_window(root))
    search_button.pack(pady=10)

    text_search_button = tk.Button(root, text="Пошук за текстом", font=("Helvetica", 12),
                                   command=lambda: open_text_search_window(root))
    text_search_button.pack(pady=10)

    exit_button = tk.Button(root, text="Вихід", font=("Helvetica", 12), command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

def open_search_window(main_root):
    main_root.withdraw()

    search_window = tk.Toplevel(main_root)
    search_window.title("Пошук релевантних зображень")
    search_window.geometry("1000x700")

    def on_back():
        search_window.destroy()
        main_root.deiconify()

    search_window.protocol("WM_DELETE_WINDOW", on_back)

    search_window.grid_rowconfigure(2, weight=1)
    search_window.grid_columnconfigure(0, weight=1)

    title_label = tk.Label(search_window, text="Пошук подібних зображень", font=("Helvetica", 18, "bold"))
    title_label.grid(row=0, column=0, pady=10)

    user_frame = tk.Frame(search_window)
    user_frame.grid(row=1, column=0)

    tk.Label(user_frame, text="Ваше зображення:", font=("Helvetica", 14)).pack()
    user_image_label = tk.Label(user_frame)
    user_image_label.pack(pady=5)

    choose_button = tk.Button(search_window, text="Обрати зображення", font=("Helvetica", 12),
                              command=lambda: logic.select_image(user_image_label, result_frame))
    choose_button.grid(row=2, column=0, pady=10)

    result_container = tk.Frame(search_window)
    result_container.grid(row=3, column=0, sticky="nsew")

    result_container.grid_rowconfigure(0, weight=1)
    result_container.grid_columnconfigure(0, weight=1)

    canvas = Canvas(result_container)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar = Scrollbar(result_container, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    scrollable_frame = Frame(canvas)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="n", tags="frame")
    canvas.configure(yscrollcommand=scrollbar.set)

    def resize_canvas(event):
        canvas.itemconfig(canvas_frame, width=event.width)

    canvas.bind("<Configure>", resize_canvas)

    result_frame = scrollable_frame

    back_button = tk.Button(search_window, text="В меню", font=("Helvetica", 12), command=on_back)
    back_button.grid(row=4, column=0, pady=10)

def open_text_search_window(main_root):
    main_root.withdraw()

    text_window = tk.Toplevel(main_root)
    text_window.title("Пошук релевантних зображень")
    text_window.geometry("1000x700")

    def on_back():
        text_window.destroy()
        main_root.deiconify()

    text_window.protocol("WM_DELETE_WINDOW", on_back)

    tk.Label(text_window, text="Введіть свій запит:", font=("Helvetica", 14)).pack(pady=10)
    query_entry = tk.Entry(text_window, font=("Helvetica", 12), width=50)
    query_entry.pack(pady=5)

    result_container = tk.Frame(text_window)
    result_container.pack(fill="both", expand=True)

    canvas = Canvas(result_container)
    scrollbar = Scrollbar(result_container, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def resize_canvas(event):
        canvas.itemconfig(canvas_frame, width=event.width)

    canvas.bind("<Configure>", resize_canvas)

    result_frame = scrollable_frame    

    search_button = tk.Button(text_window, text="Знайти", font=("Helvetica", 12), command=lambda: logic.search_by_text(query_entry.get().strip() , result_frame))
    search_button.pack(pady=10)

    back_button = tk.Button(text_window, text="В меню", font=("Helvetica", 12), command=on_back)
    back_button.pack(pady=5)

