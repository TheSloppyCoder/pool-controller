#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import datetime as dt
from datetime import datetime
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import json
from gpiozero import LED

version = "Version | V1.0"


RELAY_PIN = LED(26)



class Main:
    def __init__(self, master=None):
        self.root = tk.Tk() if master is None else tk.Toplevel(master)
        self.root.configure(background="#181C14", height=600, padx=20, pady=20, width=1024)
        self.root.geometry("1024x600")
        self.root.title("Pool Pump Controller")
        self.root.resizable(False, False)
        self.root.attributes('-fullscreen', 'true')

        # Create frames for each page
        self.dashboard_page = tk.Frame(self.root, background="#181C14")
        self.settings_page = tk.Frame(self.root, background="#181C14")
        self.about_page = tk.Frame(self.root, background="#181C14")

        #------------------------- Project Variables ------------------------------
        self.is_bypass_on = False
        self.is_pool_pump_on = False
        self.time_intervals = [0, 15, 30, 45]

        # Main widget
        self.mainwindow = self.root
        self.show_dashboard_page()
        self.clock()


    # -------------------------------------------------------------------------
    #                            Dashboard Page
    # -------------------------------------------------------------------------
    def show_dashboard_page(self):
        self.settings_page.pack_forget() # Hide Settings Frame, if shown
        self.about_page.pack_forget() # Hide About Frame, if shown


        self.lbl_title = ttk.Label(self.dashboard_page, name="lbl_title")
        self.lbl_title.configure(background="#181C14", font="{Arial} 30 {bold}", foreground="#ffffff",
                                 text='POOL CONTROLLER')
        self.lbl_title.place(anchor="nw", x=0, y=0)

        self.lbl_pool_pump_img = ttk.Label(self.dashboard_page, name="lbl_pool_pump_img")
        self.img_pool_pump = tk.PhotoImage(file="img/pump-img.png")
        self.lbl_pool_pump_img.configure(background="#181C14", image=self.img_pool_pump)
        self.lbl_pool_pump_img.place(anchor="nw", rely=0.1, x=30)

        self.lbl_power_icon = ttk.Label(self.dashboard_page, name="lbl_power_icon")
        self.img_power_icon = tk.PhotoImage(file="img/power-icon.png")
        self.lbl_power_icon.configure(background="#181C14", image=self.img_power_icon)
        self.lbl_power_icon.place(anchor="nw", x=930, y=0)

        self.lbl_pump_icon = ttk.Label(self.dashboard_page, name="lbl_pump_icon")
        self.img_pump_icon = tk.PhotoImage(file="img/pump-on-icon.png")
        self.lbl_pump_icon.configure(background="#181C14", image=self.img_pump_icon)
        #self.lbl_pump_icon.place(anchor="nw", x=860, y=0)

        self.lbl_bypass_icon = ttk.Label(self.dashboard_page, name="lbl_bypass_icon")
        self.img_bypass_icon = tk.PhotoImage(file="img/bypass-icon.png")
        self.lbl_bypass_icon.configure(background="#181C14", image=self.img_bypass_icon)
        #self.lbl_bypass_icon.place(anchor="nw", x=790, y=0)

        self.lbl_chlorine_icon = ttk.Label(self.dashboard_page, name="lbl_chlorine_icon")
        self.img_chlorine = tk.PhotoImage(file="img/chlorine-icon.png")
        self.lbl_chlorine_icon.configure(background="#181C14", image=self.img_chlorine)
        #self.lbl_chlorine_icon.place(anchor="nw", x=720, y=0)

        self.lbl_temp_cold_icon = ttk.Label(self.dashboard_page, name="lbl_temp_cold_icon")
        self.img_temp_cold = tk.PhotoImage(file="img/temp-cold-icon.png")
        self.lbl_temp_cold_icon.configure(background="#181C14", image=self.img_temp_cold)
        #self.lbl_temp_cold_icon.place(anchor="nw", x=650, y=0)

        self.lbl_temp_hot_icon = ttk.Label(self.dashboard_page, name="lbl_temp_hot_icon")
        self.img_temp_hot = tk.PhotoImage(file="img/temp-hot-icon.png")
        self.lbl_temp_hot_icon.configure(background="#181C14", image=self.img_temp_hot)
        #self.lbl_temp_hot_icon.place(anchor="nw", x=580, y=0)

        self.lbl_sand_icon = ttk.Label(self.dashboard_page, name="lbl_sand_icon")
        self.img_sand = tk.PhotoImage(file="img/sand-icon.png")
        self.lbl_sand_icon.configure(background="#181C14", image=self.img_sand)
        #self.lbl_sand_icon.place(anchor="nw", x=510, y=0)

        self.seperator_title = ttk.Separator(self.dashboard_page, name="seperator_title")
        self.seperator_title.configure(orient="horizontal")
        self.seperator_title.place(anchor="nw", width=980, x=0, y=60)

        self.lbl_time = ttk.Label(self.dashboard_page, name="lbl_time")
        self.lbl_time.configure(background="#181C14", font="{Arial} 40 {bold}", foreground="greenyellow",
                                text='Wait...')
        self.lbl_time.place(anchor="center", relx=0.5, y=110)

        self.lbl_pool_temp = ttk.Label(self.dashboard_page, name="lbl_pool_temp")
        self.lbl_pool_temp.configure(background="#181C14", font="{Arial} 28 {bold}", foreground="#ffffff",
                                     text='POOL TEMP         23.5 °C')
        self.lbl_pool_temp.place(anchor="nw", x=440, y=170)

        self.lbl_lapa_temp = ttk.Label(self.dashboard_page, name="lbl_lapa_temp")
        self.lbl_lapa_temp.configure(background="#181C14", font="{Arial} 28 {bold}", foreground="#ffffff",
                                     text='LAPA TEMP         23.5 °C')
        self.lbl_lapa_temp.place(anchor="nw", x=440, y=240)

        self.lbl_roof_temp = ttk.Label(self.dashboard_page, name="lbl_roof_temp")
        self.lbl_roof_temp.configure(background="#181C14", font="{Arial} 28 {bold}", foreground="#ffffff",
                                     text='ROOF TEMP         23.5 °C')
        self.lbl_roof_temp.place(anchor="nw", x=440, y=310)

        self.lbl_humidity = ttk.Label(self.dashboard_page, name="lbl_humidity")
        self.lbl_humidity.configure(background="#181C14", font="{Arial} 28 {bold}", foreground="#ffffff",
                                    text='HUMIDITY             23.5 %')
        self.lbl_humidity.place(anchor="nw", x=440, y=380)

        self.btn_bypass = ttk.Button(self.dashboard_page, name="btn_bypass", command=lambda: self.toggle_bypass())
        self.img_bypass_btn = tk.PhotoImage(file="img/bypass-btn.png")
        self.btn_bypass.configure(image=self.img_bypass_btn)
        self.btn_bypass.place(anchor="nw", x=445, y=475)

        self.btn_settings = ttk.Button(self.dashboard_page, name="btn_settings", command=lambda: self.show_settings_page())
        self.img_settings_btn = tk.PhotoImage(file="img/settings-btn.png")
        self.btn_settings.configure(image=self.img_settings_btn)
        self.btn_settings.place(anchor="nw", x=560, y=475)

        self.btn_info = ttk.Button(self.dashboard_page, name="btn_info", command=lambda: self.show_about_page())
        self.img_info_btn = tk.PhotoImage(file="img/info-btn.png")
        self.btn_info.configure(image=self.img_info_btn)
        self.btn_info.place(anchor="nw", x=675, y=475)

        self.btn_close = ttk.Button(self.dashboard_page, name="btn_close",
                                    command=lambda: self.root.destroy())
        self.img_close_btn = tk.PhotoImage(file="img/close-btn.png")
        self.btn_close.configure(image=self.img_close_btn)
        self.btn_close.place(anchor="nw", x=790, y=475)

        self.lbl_water_level = ttk.Label(self.dashboard_page, name="lbl_water_level")
        self.lbl_water_level.configure(background="#181C14", font="{Arial} 17 {bold}", foreground="#ffffff",
                                       text='Water Level')
        self.lbl_water_level.place(anchor="nw", x=775, y=90)

        self.seperator_water_level = ttk.Separator(self.dashboard_page, name="seperator_water_level")
        self.seperator_water_level.configure(orient="horizontal")
        self.seperator_water_level.place(anchor="nw", width=135, x=775, y=130)

        self.lbl_water_level_arrow = ttk.Label(self.dashboard_page, name="lbl_water_level_arrow")
        self.img_water_lvl = tk.PhotoImage(file="img/water-level-arrow-icon.png")
        self.lbl_water_level_arrow.configure(background="#181C14", image=self.img_water_lvl)
        self.lbl_water_level_arrow.place(anchor="nw", x=922, y=100)

        pb = ttk.Style()
        pb.theme_use('clam')
        pb.configure("blue.Vertical.TProgressbar", background='blue')
        self.pb_water_level = ttk.Progressbar(self.dashboard_page, name="pb_water_level")
        self.pb_water_level.configure(style="blue.Vertical.TProgressbar", orient="vertical", value=30)
        self.pb_water_level.place(anchor="nw", height=385, width=60, x=920, y=178)

        self.lbl_version = ttk.Label(self.dashboard_page, name="lbl_version")
        self.lbl_version.configure(background="#181C14", font="{Arial} 10 {bold}", foreground="#ffffff", text=version)
        self.lbl_version.place(anchor="nw", x=0, y=540)


        self.dashboard_page.pack(fill="both", expand=True) # Pack and show Dashboard Frame
        self.refresh_controller_status()


    # -------------------------------------------------------------------------
    #                            Settings Page
    # -------------------------------------------------------------------------
    def show_settings_page(self):
        self.dashboard_page.pack_forget() # Hide Dashboard Frame, if shown

        self.lbl_title = ttk.Label(self.settings_page, name="lbl_title")
        self.lbl_title.configure(background="#181C14", font="{Arial} 40 {bold}", foreground="#ffffff", text='SETTINGS')
        self.lbl_title.place(anchor="n", relx=0.5, x=0, y=0)
        self.seperator_title = ttk.Separator(self.settings_page, name="seperator_title")
        self.seperator_title.configure(orient="horizontal")
        self.seperator_title.place(anchor="nw", width=980, x=0, y=75)

        self.lbl_pool_pump_timing = ttk.Label(self.settings_page, name="lbl_pool_pump_timing")
        self.lbl_pool_pump_timing.configure(background="#181C14", font="{Arial} 28 {bold}", foreground="#ffffff",
                                            text='Pool Pump Timing')
        self.lbl_pool_pump_timing.place(anchor="nw", x=0, y=100)
        self.seperator_pool_pump_timing = ttk.Separator(self.settings_page, name="seperator_pool_pump_timing")
        self.seperator_pool_pump_timing.configure(orient="horizontal")
        self.seperator_pool_pump_timing.place(anchor="nw", width=330, x=0, y=155)
        self.lbl_pump_on = ttk.Label(self.settings_page, name="lbl_pump_on")
        self.lbl_pump_on.configure(background="#181C14", font="{Arial} 20 {bold}", foreground="#ffffff",
                                   text='Pump On (Hour)')
        self.lbl_pump_on.place(anchor="nw", x=0, y=180)
        self.lbl_pump_off = ttk.Label(self.settings_page, name="lbl_pump_off")
        self.lbl_pump_off.configure(background="#181C14", font="{Arial} 20 {bold}", foreground="#ffffff",
                                    text='Pump Off (Hour)')
        self.lbl_pump_off.place(anchor="nw", x=0, y=240)
        self.sb_pump_on = tk.Spinbox(self.settings_page, name="sb_pump_on")
        self.sb_pump_on.configure(font="{Arial} 20 {bold}", from_=1, to=24)
        self.sb_pump_on.place(anchor="nw", width=60, x=260, y=180)
        self.sb_pump_off = tk.Spinbox(self.settings_page, name="sb_pump_off")
        self.sb_pump_off.configure(font="{Arial} 20 {bold}", from_=1, to=24)
        self.sb_pump_off.place(anchor="nw", width=60, x=260, y=240)

        self.lbl_temp_trigger = ttk.Label(self.settings_page, name="lbl_temp_trigger")
        self.lbl_temp_trigger.configure(background="#181C14", font="{Arial} 28 {bold}", foreground="#ffffff",
                                        text='Roof Temp Trigger')
        self.lbl_temp_trigger.place(anchor="nw", x=0, y=350)
        self.seperator_roof_temp = ttk.Separator(self.settings_page, name="seperator_roof_temp")
        self.seperator_roof_temp.configure(orient="horizontal")
        self.seperator_roof_temp.place(anchor="nw", width=330, x=0, y=405)
        self.lbl_temp_degrees = ttk.Label(self.settings_page, name="lbl_temp_degrees")
        self.lbl_temp_degrees.configure(background="#181C14", font="{Arial} 20 {bold}", foreground="#ffffff",
                                        text='Temp °C')
        self.lbl_temp_degrees.place(anchor="nw", x=0, y=440)
        self.sb_temp_trigger = tk.Spinbox(self.settings_page, name="sb_temp_trigger")
        self.sb_temp_trigger.configure(font="{Arial} 20 {bold}", from_=1, to=60)
        self.sb_temp_trigger.place(anchor="nw", width=60, x=260, y=440)

        self.seperator_middle = ttk.Separator(self.settings_page, name="seperator_middle")
        self.seperator_middle.configure(orient="horizontal")
        self.seperator_middle.place(anchor="nw", height=420, x=360, y=110)

        self.lbl_chlorine_and_sand_dates = ttk.Label(self.settings_page, name="lbl_chlorine_and_sand_dates")
        self.lbl_chlorine_and_sand_dates.configure(background="#181C14", font="{Arial} 28 {bold}", foreground="#ffffff",
                                                   text='Pool Chlorine and Sand Dates')
        self.lbl_chlorine_and_sand_dates.place(anchor="nw", x=400, y=100)
        self.seperator_pool_temp_values = ttk.Separator(self.settings_page, name="seperator_pool_temp_values")
        self.seperator_pool_temp_values.configure(orient="horizontal")
        self.seperator_pool_temp_values.place(anchor="nw", width=535, x=400, y=155)
        self.lbl_chlorine_date = ttk.Label(self.settings_page, name="lbl_chlorine_date")
        self.lbl_chlorine_date.configure(background="#181C14", font="{Arial} 20 {bold}", foreground="#ffffff",
                                         text='Next Chlorine Add Date')
        self.lbl_chlorine_date.place(anchor="nw", x=580, y=180)
        self.lbl_sand_date = ttk.Label(self.settings_page, name="lbl_sand_date")
        self.lbl_sand_date.configure(background="#181C14", font="{Arial} 20 {bold}", foreground="#ffffff",
                                     text='Next Sand Add Date')
        self.lbl_sand_date.place(anchor="nw", x=580, y=240)
        self.dt_chlorine = DateEntry(self.settings_page, font="{Arial} 16 {}", background="cyan", foreground="black", bd=2)
        self.dt_chlorine.place(anchor="nw", x=400, y=183)
        self.dt_sand = DateEntry(self.settings_page, font="{Arial} 16 {}", background="orange", foreground="black", bd=2)
        self.dt_sand.place(anchor="nw", x=400, y=243)
        self.lbl_settings_chlorine_img = ttk.Label(self.settings_page, name="lbl_chlorine")
        self.img_chlorine_settings = tk.PhotoImage(file="img/chlorine-settings-img.png")
        self.lbl_settings_chlorine_img.configure(image=self.img_chlorine_settings, background="#181C14")
        self.lbl_settings_chlorine_img.place(anchor="nw", width=80, x=900, y=180)
        self.lbl_settings_sand_img = ttk.Label(self.settings_page, name="lbl_sand")
        self.img_sand_settings = tk.PhotoImage(file="img/sand-settings-img.png")
        self.lbl_settings_sand_img.configure(image=self.img_sand_settings, background="#181C14")
        self.lbl_settings_sand_img.place(anchor="nw", width=80, x=900, y=240)

        self.lbl_pool_temp_indicators = ttk.Label(self.settings_page, name="lbl_pool_temp_indicators")
        self.lbl_pool_temp_indicators.configure(background="#181C14", font="{Arial} 28 {bold}", foreground="#ffffff",
                                                text='Pool Temp Indicators')
        self.lbl_pool_temp_indicators.place(anchor="nw", x=400, y=350)
        self.seperator_pool_temp_indicators = ttk.Separator(self.settings_page, name="seperator_pool_temp_indicators")
        self.seperator_pool_temp_indicators.configure(orient="horizontal")
        self.seperator_pool_temp_indicators.place(anchor="nw", width=380, x=400, y=405)
        self.lbl_hot_temp_value = ttk.Label(self.settings_page, name="lbl_hot_temp_value")
        self.lbl_hot_temp_value.configure(background="#181C14", font="{Arial} 20 {bold}", foreground="#ffffff",
                                          text='Hot Temp   °C')
        self.lbl_hot_temp_value.place(anchor="nw", x=400, y=440)
        self.lbl_cold_temp_value = ttk.Label(self.settings_page, name="lbl_cold_temp_value")
        self.lbl_cold_temp_value.configure(background="#181C14", font="{Arial} 20 {bold}", foreground="#ffffff",
                                           text='Cold Temp °C')
        self.lbl_cold_temp_value.place(anchor="nw", x=400, y=490)
        self.sb_hot_temp = tk.Spinbox(self.settings_page, name="sb_hot_temp_value")
        self.sb_hot_temp.configure(font="{Arial} 20 {bold}", from_=1, to=60)
        self.sb_hot_temp.place(anchor="nw", width=60, x=650, y=440)
        self.sb_cold_temp = tk.Spinbox(self.settings_page, name="sb_cold_temp_value")
        self.sb_cold_temp.configure(font="{Arial} 20 {bold}", from_=1, to=60)
        self.sb_cold_temp.place(anchor="nw", width=60, x=650, y=490)

        self.btn_save = ttk.Button(self.settings_page, name="btn_save", command=lambda: self.save_settings())
        self.img_savebtn = tk.PhotoImage(file="img/save-btn.png")
        self.btn_save.configure(image=self.img_savebtn, text='SAVE')
        self.btn_save.place(anchor="nw", x=800, y=450)

        self.btn_close = ttk.Button(self.settings_page, name="btn_close", command=lambda: self.show_dashboard_page())
        self.img_closebtn = tk.PhotoImage(file="img/close-btn.png")
        self.btn_close.configure(image=self.img_closebtn, text='CLOSE')
        self.btn_close.place(anchor="nw", x=895, y=450)

        self.load_settings()
        self.settings_page.pack(fill="both", expand=True) # Pack and Show Settings Frame


    # -------------------------------------------------------------------------
    #                            About Page
    # -------------------------------------------------------------------------
    def show_about_page(self):
        self.dashboard_page.pack_forget() # Hide dashboard Frame

        self.frame_logo = tk.Frame(self.about_page, name="frame_logo")
        self.frame_logo.configure(background="#181C14", height=200, width=200)
        self.lbl_img_logo = ttk.Label(self.frame_logo, name="lbl_img_logo")
        self.img_logo = tk.PhotoImage(file="img/sloppy-logo.png")
        self.lbl_img_logo.configure(background="#181C14", image=self.img_logo)
        self.lbl_img_logo.pack(padx=10, side="right")
        self.lbl_sloppy = ttk.Label(self.frame_logo, name="lbl_sloppy")
        self.lbl_sloppy.configure(background="#181C14", font="{Arial} 28 {bold}", foreground="#ffffff", text='The Sloppy Coder')
        self.lbl_sloppy.pack(padx=10, side="left")
        self.frame_logo.pack(side="top")

        self.frame_version = tk.Frame(self.about_page, name="frame_version")
        self.frame_version.configure(background="#181C14", height=200, width=200)
        self.lbl_about_version = ttk.Label(self.frame_version, name="lbl_about_version")
        self.lbl_about_version.configure(background="#181C14", font="{Arial} 22 {bold}", foreground="#ffffff", text='Version | V1.0')
        self.lbl_about_version.pack(side="left")
        self.lbl_version_seperator = ttk.Label(self.frame_version, name="lbl_version_seperator")
        self.lbl_version_seperator.configure(background="#181C14", font="{Arial} 60 {}", foreground="#ffffff", text='|')
        self.lbl_version_seperator.pack(padx=50, side="left")
        self.lbl_license = ttk.Label(self.frame_version, name="lbl_license")
        self.lbl_license.configure(background="#181C14", font="{Arial} 22 {bold}", foreground="#ffffff", text='License: GNU 3.0')
        self.lbl_license.pack(side="left")
        self.frame_version.pack(side="top")

        self.btn_close = ttk.Button(self.about_page, name="btn_close", command=lambda: self.show_dashboard_page())
        self.img_closebtn = tk.PhotoImage(file="img/close-btn.png")
        self.btn_close.configure(image=self.img_closebtn)
        self.btn_close.pack(anchor="center", pady=60, side="top")

        self.lbl_img_contribution = ttk.Label(self.about_page, name="lbl_img_contribution")
        self.lbl_img_contribution.configure(background="#181C14", font="{Arial} 10 {bold}", foreground="#ffffff", text='Pump Image | https://www.flaticon.com/free-icon/motor_12907541?term=pool+pump&page=1&position=6&origin=search&related_id=12907541')
        self.lbl_img_contribution.pack(anchor="center", pady=10, side="bottom")


        self.about_page.pack(fill="both", expand=True)  # Pack and show About Page



    def run(self):
        self.mainwindow.mainloop()



    def clock(self):
        self.root.after(1000, self.clock)
        self.time_now = dt.datetime.now()
        self.lbl_time.configure(text=self.time_now.strftime("%H:%M:%S  %p"))
        self.toggle_pool_pump()
        self.check_config()
        self.check_and_display_sensor_data()
        
        
    # -------------------------------------------------------------------------
    #               Load Sensor Data and Display on Dashboard
    # -------------------------------------------------------------------------    
    def check_and_display_sensor_data(self):
        with open("sensor_data.json") as file:
            data = json.load(file)
        
        self.lbl_pool_temp.configure(text=f"POOL TEMP         {data['pool_temp']} °C")
        self.lbl_lapa_temp.configure(text=f"LAPA TEMP         {data['lapa_temp']} °C")
        self.lbl_roof_temp.configure(text=f"ROOF TEMP         {data['roof_temp']} °C")
        self.lbl_humidity.configure(text=f"HUMIDITY             {data['humidity']} %")

    # -------------------------------------------------------------------------
    #               Save Values of Settings Page to config.json
    # -------------------------------------------------------------------------
    def save_settings(self):
        new_settings = {
            "pump_on_hour": tk.getint(self.sb_pump_on.get()),
            "pump_off_hour": tk.getint(self.sb_pump_off.get()),
            "minimum_trigger_temp": tk.getint(self.sb_temp_trigger.get()),
            "chlorine_date": self.dt_chlorine.get_date().strftime("%m/%d/%y"),
            "sand_date": self.dt_sand.get_date().strftime("%m/%d/%y"),
            "hot_temp_indicator": tk.getint(self.sb_hot_temp_value.get()),
            "cold_temp_indicator": tk.getint(self.sb_cold_temp_value.get())
        }
        save_settings = json.dumps(new_settings, indent=4)
        try:
            with open("config.json", "w") as save_file:
                save_file.write(save_settings)
            messagebox.showinfo("Settings", "Your Settings has been saved")
        except:
            messagebox.showerror("Error", "There was an error saving the settings")


    # -------------------------------------------------------------------------
    #               Load Values in config.json and display in Settings Page
    # -------------------------------------------------------------------------
    def load_settings(self):
        try:
            with open("config.json") as file:
                data = json.load(file)

            self.sb_pump_on_value = tk.StringVar()
            self.sb_pump_on_value.set(data["pump_on_hour"])
            self.sb_pump_on.configure(textvariable=self.sb_pump_on_value)

            self.sb_pump_off_value = tk.StringVar()
            self.sb_pump_off_value.set(data["pump_off_hour"])
            self.sb_pump_off.configure(textvariable=self.sb_pump_off_value)

            self.sb_temp_trigger_value = tk.StringVar()
            self.sb_temp_trigger_value.set(data["minimum_trigger_temp"])
            self.sb_temp_trigger.configure(textvariable=self.sb_temp_trigger_value)

            self.dt_chlorine.set_date(data["chlorine_date"])
            self.dt_sand.set_date(data["sand_date"])

            self.sb_hot_temp_value = tk.StringVar()
            self.sb_hot_temp_value.set(data["hot_temp_indicator"])
            self.sb_hot_temp.configure(textvariable=self.sb_hot_temp_value)

            self.sb_cold_temp_value = tk.StringVar()
            self.sb_cold_temp_value.set(data["cold_temp_indicator"])
            self.sb_cold_temp.configure(textvariable=self.sb_cold_temp_value)

        except FileNotFoundError:
            messagebox.showerror("Error", "There was an error loading the settings, possible file not found")



    # -------------------------------------------------------------------------
    #          Toggle Bypass ON / OFF
    # -------------------------------------------------------------------------
    def toggle_bypass(self):
        if self.is_bypass_on == False:
            RELAY_PIN.on()
            self.is_bypass_on = True
            self.lbl_pump_icon.place(anchor="nw", x=860, y=0)
            self.img_pool_pump.configure(file="img/bypass-on-img.png")
            self.lbl_bypass_icon.place(anchor="nw", x=790, y=0)
        else:
            RELAY_PIN.off()
            self.is_bypass_on = False
            self.lbl_pump_icon.place_forget()
            self.img_pool_pump.configure(file="img/pump-img.png")
            self.lbl_bypass_icon.place_forget()



    # -------------------------------------------------------------------------
    #          Read Config Time and Temp Data and Trigger Accordingly
    # -------------------------------------------------------------------------
    def toggle_pool_pump(self):
        if self.time_now.second in self.time_intervals:
            if self.is_bypass_on:
                pass
            else:
                with open("config.json") as read_file:
                    config = json.load(read_file)
                #
                # TODO: Check aswell for the Roof Temp
                # Need Actual Temp Data
                if self.time_now.hour >= config["pump_on_hour"] and self.time_now.hour < config["pump_off_hour"]:
                    RELAY_PIN.on()
                    self.is_pool_pump_on = True
                    self.lbl_pump_icon.place(anchor="nw", x=860, y=0)
                    self.img_pool_pump.configure(file="img/pump-on-img.png")
                else:
                    RELAY_PIN.off()
                    self.lbl_pump_icon.place_forget()
                    self.img_pool_pump.configure(file="img/pump-img.png")



    # -------------------------------------------------------------------------
    #          Check Config Data and Trigger events and reminders accordingly
    # -------------------------------------------------------------------------
    def check_config(self):
        today = datetime.today().strftime("%m/%d/%y")
        try:
            with open("config.json") as file:
                data = json.load(file)
                
            with open("sensor_data.json") as sfile:
                s_data = json.load(sfile)
        except FileNotFoundError:
            messagebox.showerror("Error", "There was an error loading the settings, possible file not found")

        # Check Chlorine Date
        if today >= data["chlorine_date"]:
            self.lbl_chlorine_icon.place(anchor="nw", x=720, y=0)
        else:
            self.lbl_chlorine_icon.place_forget()

        # Check Sand Date
        if today >= data["sand_date"]:
            self.lbl_sand_icon.place(anchor="nw", x=510, y=0)
        else:
            self.lbl_sand_icon.place_forget()

        # Check Hot Temp
        if s_data["pool_temp"] >= data["hot_temp_indicator"]:
            self.lbl_temp_hot_icon.place(anchor="nw", x=580, y=0)
        else:
            self.lbl_temp_hot_icon.place_forget()
            
        # Check Cold Temp
        if s_data["pool_temp"] <= data["cold_temp_indicator"]:
            self.lbl_temp_cold_icon.place(anchor="nw", x=650, y=0)
        else:
            self.lbl_temp_cold_icon.place_forget()
            


    # -------------------------------------------------------------------------
    #          Refresh Icons and Images, after Settings Page is Closed.
    # -------------------------------------------------------------------------
    def refresh_controller_status(self):
        if self.is_pool_pump_on:
            self.lbl_pump_icon.place(anchor="nw", x=860, y=0)
            self.img_pool_pump.configure(file="img/pump-on-img.png")
        else:
            self.lbl_pump_icon.place_forget()
            self.img_pool_pump.configure(file="img/pump-img.png")




if __name__ == "__main__":
    app = Main()
    app.run()
