import os
import tkinter as tk
import tkinter.font
import tkinter.filedialog

class Window:
    def __init__(self, media_converter, speech_to_text, text_exporter, output_directory):
        self.media_converter = media_converter
        self.speech_to_text = speech_to_text
        self.text_exporter = text_exporter

        # Main window
        self.window = tk.Tk()
        self.window.option_add('*Font', 'Helvetica 14')
        self.window.update_idletasks()
        size = tuple(int(_) for _ in self.window.geometry().split('+')[0].split('x'))
        x = self.window.winfo_screenwidth()/2 - size[0]/2
        y = self.window.winfo_screenheight()/2 - size[1]/2
        self.window.geometry("+%d+%d" % (x, y))

        # Status label
        self.status_label = tk.Label(text="[waiting for selection]")

        # File input
        input_frame = tk.Frame()
        input_label = tk.Label(master=input_frame, text="Select input file: ", width=20)
        self.input_file = tk.Entry(master=input_frame, width=40, background="white")
        input_button = tk.Button(master=input_frame, text="Browse")
        input_button.bind("<Button-1>", lambda event: Window.clear_and_insert(self.input_file, tkinter.filedialog.askopenfilename()))
        input_label.pack(side=tk.LEFT)
        self.input_file.pack(side=tk.LEFT)
        input_button.pack(side=tk.LEFT)

        # File output
        output_frame = tk.Frame()
        output_label = tk.Label(master=output_frame, text="Select output directory: ", width=20)
        self.output_directory = tk.Entry(master=output_frame, width=40, background="white")
        self.output_directory.insert(0, output_directory)
        output_button = tk.Button(master=output_frame, text="Browse")
        output_button.bind("<Button-1>", lambda event: Window.clear_and_insert(self.output_directory, tkinter.filedialog.askdirectory()))
        output_label.pack(side=tk.LEFT)
        self.output_directory.pack(side=tk.LEFT)
        output_button.pack(side=tk.LEFT)

        # Confirm button
        confirm_frame = tk.Frame()
        confirm_button = tk.Button(master=confirm_frame, text="Convert", width=65)
        confirm_button.pack()

        # Binders
        confirm_button.bind("<Button-1>", lambda event: self.convert())

        # Final packing
        self.status_label.pack()
        input_frame.pack()
        output_frame.pack()
        confirm_frame.pack()

    def show(self):
        self.window.mainloop()

    def clear_and_insert(widget, text):
        widget.delete(0, tk.END)
        widget.insert(0, text)

    def display(self, color, message):
        self.status_label["foreground"] = color
        self.status_label["text"] = "[" + message.lower() + "]"
        self.window.update_idletasks()

    def display_info(self, message):
        self.display("black", message)

    def display_success(self, message):
        self.display("green", message)

    def display_error(self, message):
        self.display("red", message)

    def convert(self):
        source = self.input_file.get()
        destination_directory = self.output_directory.get()
        tmp_path = destination_directory + '/_transcribe_tmp.flac'
        destination = destination_directory + '/' + (source.split('/')[-1].rsplit('.', 1)[0]).lower().replace(' ', '-') + '.docx'

        try:
            self.display_info('converting file')
            self.media_converter.convert(source, tmp_path)
            self.display_info('transcribing file')
            content = self.speech_to_text.convert(tmp_path)
            self.display_info('saving file')
            self.text_exporter.export(content, destination)
            os.remove(tmp_path)
        except Exception as e:
            self.display_error(str(e))
        else:
            self.display_success("Done")
