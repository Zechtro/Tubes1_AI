import flet as ft
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from flet import Slider, ElevatedButton, Row, Column, Image, Dropdown, dropdown, FilePicker, FilePickerResultEvent, AlertDialog, Text
import base64
import threading
import time
import json

plt.switch_backend("Agg")

matrix_3d = []
global_min = 0
global_max = 125
playback_speed = 1
is_playing = False
play_thread = None
iter = 0
total_iter = 0
progress_slider = None

def create_dummy():
    global matrix_3d
    print("create dummy")
    cube = list(range(1, 126))
    matrix_3d = [cube]

def read_json_content(file_content):
    global matrix_3d, total_iter
    try:
        matrix_3d = json.loads(file_content)
        total_iter = len(matrix_3d)
        print("read json content")
    except json.JSONDecodeError:
        print("read json error")

def show_error_dialog(page, message):
    error_dialog = AlertDialog(
        title=Text("Error"),
        content=Text(message),
        actions=[ElevatedButton(text="OK", on_click=lambda e: close_dialog(page))],
    )
    page.dialog = error_dialog
    page.dialog.open = True
    page.update()

def close_dialog(page):
    page.dialog.open = False
    page.update()

def on_file_selected(e: FilePickerResultEvent):
    if e.files:
        file = e.files[0]
        if file.path.endswith(".json"):
            with open(file.path, "r") as f:
                file_content = f.read()
                read_json_content(file_content)
                update_plot_image(e.page)
        else:
            show_error_dialog(e.page, "Error, only JSON files are accepted!")

def update_plot_image(page):
    global plot_image, total_iter, progress_slider
    plot_image.src_base64 = update_plot()
    progress_slider.max = total_iter - 1
    progress_slider.divisions = total_iter - 1
    progress_slider.value = 0
    progress_slider.label = "{value}"
    page.update()

def update_plot():
    global iter, matrix_3d, global_min, global_max
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    array_1d = np.array(matrix_3d[iter]).reshape(5, 5, 5)
    for i in range(5):
        layer = array_1d[i, :, :]
        
        row = i // 3
        col = i % 3

        sns.heatmap(layer, annot=True, fmt='d', cmap='icefire', ax=axes[row, col],
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

def on_slider_change(e):
    global iter
    iter = int(e.control.value)
    plot_image.src_base64 = update_plot()
    e.page.update()

def on_playback_speed_change(e):
    global playback_speed
    playback_speed = float(e.control.value)
    print("Playback Speed:", playback_speed)

def main(page: ft.Page):
    create_dummy()
    global progress_slider, plot_image

    play_pause_button = ElevatedButton(text="Play", on_click=on_play_pause_clicked, height=50)

    progress_slider = Slider(min=0, max=total_iter - 1, label="{value}", divisions=total_iter, on_change=on_slider_change, height=50)

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
            dropdown.Option("2"),
            dropdown.Option("4"),
            dropdown.Option("8"),
            dropdown.Option("16"),
            dropdown.Option("32"),
            dropdown.Option("64"),
            dropdown.Option("128")
        ],
        on_change=on_playback_speed_change,
        width=200, height=50
    )

    file_picker = FilePicker(on_result=on_file_selected)

    upload_button = ElevatedButton(text="Upload JSON File", on_click=lambda e: file_picker.pick_files(), height=50)

    plot_image = Image(src_base64=update_plot(), width=700, height=500)

    page.add(
        file_picker,
        Column(height=20),
        Column(
            [
                Row([upload_button, play_pause_button, playback_speed_dropdown], alignment="center"),
                progress_slider,
                plot_image
            ],
            alignment="center",
            horizontal_alignment="center"
        )
    )

ft.app(target=main)
