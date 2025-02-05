# src/gui/components/sidebar.py
import customtkinter as ctk
from datetime import datetime

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, log_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.log_callback = log_callback
        self._create_widgets()
        self._configure_layout()
        
    def _create_widgets(self):
        # Botões de controle
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_phone_day = ctk.CTkButton(
            self.btn_frame, 
            text="Celular (Hoje)",
            command=lambda: self.log_callback('phone', 'day'),
            fg_color="#3B8ED0"
        )
        self.btn_phone_all = ctk.CTkButton(
            self.btn_frame,
            text="Celular (Histórico)",
            command=lambda: self.log_callback('phone', 'all'),
            fg_color="#1F6AA5"
        )
        self.btn_human_day = ctk.CTkButton(
            self.btn_frame,
            text="Ausências (Hoje)",
            command=lambda: self.log_callback('human', 'day'), 
            fg_color="#2AAA8A"
        )
        self.btn_human_all = ctk.CTkButton(
            self.btn_frame,
            text="Ausências (Histórico)",
            command=lambda: self.log_callback('human', 'all'),
            fg_color="#218B6D"
        )

    def _configure_layout(self):
        self.grid_columnconfigure(0, weight=1)
        padding = {"padx":5, "pady":5}
        
        self.btn_frame.grid(row=0, column=0, sticky="nsew")
        self.btn_phone_day.grid(row=0, column=0, **padding)
        self.btn_phone_all.grid(row=1, column=0, **padding)
        self.btn_human_day.grid(row=2, column=0, **padding) 
        self.btn_human_all.grid(row=3, column=0, **padding)