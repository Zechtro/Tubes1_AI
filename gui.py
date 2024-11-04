import flet as ft
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from flet import Container, Slider, ElevatedButton, Row, Column, Image, Dropdown, dropdown
import base64
import threading
import time

plt.switch_backend("Agg")

matrix_3d = []
global_min, global_max = None, None
current_layer = 0
playback_speed = 1
is_playing = False
play_thread = None
iter = 0

def create_dummy():
    list_of_cubes = []
    for i in range(10):
        cube = np.random.randint(0, 100, size=(5, 5, 5))  
        matrix_3d.append(cube)

def load_cube(cube):
    global matrix_3d, global_min, global_max
    matrix_3d = cube
    global_min, global_max = matrix_3d.min(), matrix_3d.max()
    save_cube_to_file(cube) 

def save_cube_to_file(cube):
    with open("current_cube.txt", "w") as f:
        for i in range(cube.shape[0]):
            layer = cube[i, :, :]
            np.savetxt(f, layer, fmt='%d', delimiter=' ')
            f.write("\n")

def update_plot():
    global iter, matrix_3d, global_min, global_max
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    cube = matrix_3d[iter]
    for i in range(5):
        layer = cube[i, :, :]
        
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
    global iter, is_playing
    while is_playing:
        iter = (iter + 1) % len(matrix_3d)
        progress_slider.value = iter
        plot_image.src_base64 = update_plot()
        page.update()
        print(1 / playback_speed)
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

def update_image(page):
    create_dummy()
    plot_image.src_base64 = update_plot()
    page.update()

def on_slider_change(e):
    global iter 
    iter = int(e.control.value)
    print("iter: ", iter)
    progress_slider.value = iter
    plot_image.src_base64 = update_plot()
    e.page.update()

def on_playback_speed_change(e):
    global playback_speed
    playback_speed = float(e.control.value)
    print("Playback Speed:", playback_speed)

def main(page: ft.Page):
    create_dummy() # Ini ntar diganti sama list of cube yg asli

    play_pause_button = ElevatedButton(text="Play", on_click=on_play_pause_clicked)
    global progress_slider

    progress_slider = Slider(min=0, max=len(matrix_3d) - 1, divisions=len(matrix_3d) - 1, on_change=on_slider_change)

    playback_speed_dropdown = Dropdown(
        label="Playback Speed",
        value="1",
        options=[
            dropdown.Option("0.25"),
            dropdown.Option("0.5"),
            dropdown.Option("0.75"),
            dropdown.Option("1"),
            dropdown.Option("1.25"),
            dropdown.Option("1.5"),
            dropdown.Option("2")
        ],
        on_change=on_playback_speed_change
    )

    load_button = ElevatedButton(text="Load File", on_click=lambda e: load_cube(matrix_3d[0]))

    global plot_image
    plot_image = Image(src_base64=update_plot(), width=600, height=400)

    page.add(Column([
        Row([load_button, play_pause_button]),
        progress_slider,
        playback_speed_dropdown,
        plot_image
    ]))

ft.app(target=main)
