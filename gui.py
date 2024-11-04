import flet as ft
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from flet import Container, Slider, ElevatedButton, Row, Column, Image, Dropdown, dropdown, alignment
import base64
import threading
import time
import json

plt.switch_backend("Agg")

matrix_3d = []
global_min, global_max = None, None
playback_speed = 1
is_playing = False
play_thread = None
iter = 0
total_iter = 0

def create_dummy():
    global matrix_3d
    cube = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125]
    matrix_3d = []
    matrix_3d.append(cube)

def save_cube_to_file():
    global matrix_3d
    with open("state.txt", "w") as f:
        for iteration, cube in enumerate(matrix_3d):
            f.write(f"Iteration {iteration + 1} \n\n")
            for i in range(cube.shape[0]):
                layer = cube[i, :, :]
                f.write(f"Layer {i + 1}\n")
                np.savetxt(f, layer, fmt='%d', delimiter=' ')
                f.write("\n")

def read_json_to_array():
    global matrix_3d, total_iter
    with open("state.json", "r") as file:
        matrix_3d = json.load(file)
    total_iter = len(matrix_3d)


def update_plot():
    global iter, matrix_3d, global_min, global_max
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    array_1d = np.array(matrix_3d[iter]).reshape(5, 5, 5)

    for i in range(5):
        layer = array_1d[i, :, :]
        
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
    progress_slider.value = iter
    plot_image.src_base64 = update_plot()
    e.page.update()

def on_playback_speed_change(e):
    global playback_speed
    playback_speed = float(e.control.value)
    print("Playback Speed:", playback_speed)

def main(page: ft.Page):
    read_json_to_array()

    play_pause_button = ElevatedButton(text="Play", on_click=on_play_pause_clicked, height=40)
    global progress_slider

    progress_slider = Slider(min=0, max=len(matrix_3d) - 1, divisions=len(matrix_3d) - 1, on_change=on_slider_change, height=40)

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
        on_change=on_playback_speed_change,
        width=200, height=40
    )

    load_button = ElevatedButton(text="Load File", on_click=lambda e: save_cube_to_file)

    global plot_image
    plot_image = Image(src_base64=update_plot(), width=700, height=500)

    page.add(
        Column(height=20),
        Column(
            [
                Row([load_button, play_pause_button, playback_speed_dropdown], alignment="center"),
                progress_slider,
                plot_image
            ],
            alignment="center",
            horizontal_alignment="center"
        )
    )


ft.app(target=main)
