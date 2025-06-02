import gui
import queries

image_refs = []

def select_image(user_image_label, result_frame):

    file_path = gui.select_image(user_image_label)
    query_results = queries.query_with_image(file_path)

    gui.show_results_in_gui(query_results, result_frame)

def search_by_text(query_text, result_frame):

    results = queries.query_with_text(query_text)

    gui.show_results_in_gui(results, result_frame)

def create_window():

    gui.create_main_menu()