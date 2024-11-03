import flet as ft
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from flet import Container, Slider, ElevatedButton, Row, Column, Image
import base64
import threading
import time

plt.switch_backend("Agg")

matrix_3d = None
global_min, global_max = None, None
current_layer = 0
playback_speed = 1
is_playing = False
play_thread = None

def create_dummy():
    list_of_cubes = []
    for i in range(10):
        cube = np.random.randint(0, 100, size=(5, 5, 5))  
        list_of_cubes.append(cube)
    return list_of_cubes

def load_cube(cube):
    global matrix_3d, global_min, global_max
    matrix_3d = cube
    global_min, global_max = matrix_3d.min(), matrix_3d.max()
    save_cube_to_file(cube)  

def save_cube_to_file(cube):
    with open("cube.txt", "w") as f:
        for i in range(cube.shape[0]):
            layer = cube[i, :, :]
            np.savetxt(f, layer, fmt='%d', delimiter=' ')
            f.write("\n")  

def update_plot():
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    for i in range(5):
        layer = matrix_3d[i, :, :]
        
        row = i // 3
        col = i % 3

        sns.heatmap(layer, annot=True, fmt='d', cmap='plasma', ax=axes[row, col], 
                    cbar=False,
                    vmin=global_min,
                    vmax=global_max, 
                    xticklabels=[],
                    yticklabels=[])

        axes[row, col].set_title(f'Matrix Level {i + 1}')

    for j in range(i + 1, 6):
        fig.delaxes(axes.flatten()[j])
        
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)

    return base64.b64encode(buf.getvalue()).decode("utf-8")

def play_loop(page):
    global current_layer, is_playing
    while is_playing:
        current_layer = (current_layer + 1) % matrix_3d.shape[0]
        progress_slider.value = current_layer
        plot_image.src_base64 = update_plot()
        page.update()
        time.sleep(1 / playback_speed) 

def on_play_pause_clicked(e):
    global is_playing, play_thread
    is_playing = not is_playing
    e.control.text = "Pause" if is_playing else "Play"
    e.control.update()
    if is_playing:
        play_thread = threading.Thread(target=play_loop, args=(e.page,))
        play_thread.start()
    else:
        if play_thread:
            is_playing = False

def on_progress_bar_changed(e):
    global current_layer
    current_layer = int(e.control.value)
    update_image(e.page)

def update_image(page):
    plot_image.src_base64 = update_plot()
    page.update()

def main(page: ft.Page):
    list_of_cubes = create_dummy()
    load_cube(list_of_cubes[0])

    play_pause_button = ElevatedButton(text="Play", on_click=on_play_pause_clicked)
    global progress_slider
    progress_slider = Slider(min=0, max=matrix_3d.shape[0] - 1, value=0, on_change=on_progress_bar_changed)
    load_button = ElevatedButton(text="Load File", on_click=lambda e: load_cube(list_of_cubes[0]))

    global plot_image
    plot_image = Image(src_base64=update_plot(), width=600, height=400)

    page.add(Column([
        Row([load_button, play_pause_button]),
        progress_slider,
        plot_image
    ]))

    def on_slider_change(e):
        progress_slider.value = current_layer
        plot_image.src_base64 = update_plot()
        page.update()
    
    progress_slider.on_change = on_slider_change

ft.app(target=main)
