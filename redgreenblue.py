import customtkinter
import tkinter
import RPi.GPIO as GPIO


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        try:

            self.title("Colour Select")
            self.minsize(1024, 600)
            self.attributes('-fullscreen', True)

            self.radio_var = tkinter.IntVar(0)
            self.configure(fg_color="white")

            self.frame_red = customtkinter.CTkFrame(master=self, fg_color="#EA2626")
            # Each radio button controls the value of the variable self.radio_var, either 7, 11 or 13.
            self.radiobutton_red = customtkinter.CTkRadioButton(master=self.frame_red, text="",
                                                                command=self.radiobutton_event, variable=self.radio_var,
                                                                value=7,
                                                                fg_color="white", border_color="black", hover=False,
                                                                radiobutton_width=160, radiobutton_height=260,
                                                                border_width_unchecked=60, border_width_checked=60)

            self.frame_green = customtkinter.CTkFrame(master=self, fg_color="#42B549")
            self.radiobutton_green = customtkinter.CTkRadioButton(master=self.frame_green, text="",
                                                                  command=self.radiobutton_event,
                                                                  variable=self.radio_var,
                                                                  fg_color="white", border_color="black",
                                                                  value=11,
                                                                  hover=False,
                                                                  radiobutton_width=160, radiobutton_height=260,
                                                                  border_width_unchecked=60, border_width_checked=60)

            self.frame_blue = customtkinter.CTkFrame(master=self, fg_color="#3094C3")
            self.radiobutton_blue = customtkinter.CTkRadioButton(master=self.frame_blue, text="",
                                                                 command=self.radiobutton_event,
                                                                 variable=self.radio_var,
                                                                 fg_color="white", border_color="black",
                                                                 value=13,
                                                                 hover=False,
                                                                 radiobutton_width=160, radiobutton_height=260,
                                                                 border_width_unchecked=60, border_width_checked=60)

            self.frame_quit = customtkinter.CTkFrame(master=self, fg_color="yellow")
            self.button_quit = customtkinter.CTkButton(self.frame_quit, fg_color="black", text="X",
                                                       command=self.on_closing, width=1004, height=80, hover=False,
                                                       font=customtkinter.CTkFont(family="Courier New", weight='bold',
                                                                                  size=40))

            # Place the three frames within the master frame, including one bottom 'exit' frame
            self.frame_red.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            self.frame_green.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
            self.frame_blue.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
            self.frame_quit.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure((0, 1, 2), weight=1)

            # Place and Align the radiobuttons inside their own frames

            self.radiobutton_red.grid(row=0, column=0, padx=(85, 0), pady=10, sticky="nsew")
            self.radiobutton_green.grid(row=0, column=0, padx=(85, 0), pady=10, sticky="nsew")
            self.radiobutton_blue.grid(row=0, column=0, padx=(85, 0), pady=10, sticky="nsew")
            self.frame_red.grid_rowconfigure(0, weight=1)
            self.frame_red.grid_columnconfigure(0, weight=1)

            self.frame_green.grid_rowconfigure(0, weight=1)
            self.frame_green.grid_columnconfigure(0, weight=1)

            self.frame_blue.grid_rowconfigure(0, weight=1)
            self.frame_blue.grid_columnconfigure(0, weight=1)

            # add the quit button
            self.button_quit.pack()

        except KeyboardInterrupt:
            self.on_closing()

    def radiobutton_event(self):

        #  set all as low
        for pin in (7, 11, 13):
            GPIO.output(pin, GPIO.LOW)

        # Set our selected one to be high
        GPIO.output(self.radio_var.get(), GPIO.HIGH)

    # Run in all instances of the program closing, to release the GUI elements and the GPIO pins
    def on_closing(self):
        GPIO.cleanup()
        self.destroy()

    # Used to help the application detect KeyboardInterrupts when GUI has focus
    def check(self):
        self.after(50, self.check)


if __name__ == "__main__":

    # config the pins

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)

    # set all low for the start
    for pin in (7, 11, 13):
        GPIO.output(pin, GPIO.LOW)

    app = App()
    app.after(50, app.check)
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.bind("<Control-c>", app.on_closing)
    try:
        app.mainloop()
    except KeyboardInterrupt:
        GPIO.cleanup()
