# src/gui/main_window.py
import customtkinter as ctk
from .components.graphs import GraphController
from .components.sidebar import Sidebar
from data_processing.log_parser import LogAnalyzer
import cv2


class MainWindow(ctk.CTk):
    def __init__(self, start_callback, stop_callback, detector, is_detection_running):
        super().__init__()
        self.title("Analisador de Atividades")
        self.geometry("1200x800")
        self.is_detection_running = is_detection_running
        self.stop_callback = stop_callback  # Store the stop callback for use on close

        # Configuração do layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Frame para agrupar os botões
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=0, column=0, pady=15)

        # Botões de início e parada
        self.btn_start = ctk.CTkButton(self.button_frame, text="Iniciar", fg_color="green", command=start_callback, width=100, height=30)
        self.btn_stop = ctk.CTkButton(self.button_frame, text="Finalizar", fg_color="red", command=stop_callback, width=100, height=30)

        self.btn_start.grid(row=0, column=0, padx=(0, 5))
        self.btn_stop.grid(row=0, column=1, padx=(5, 0))

        # Sidebar
        self.sidebar = Sidebar(self, self.update_graphs)
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Gráficos
        self.graph = GraphController(self, "Atividade Diária")  # Adicione o título aqui
        self.graph.get_widget().grid(row=1, column=1, columnspan=3, sticky="nsew", padx=10, pady=(15, 10))

        # Inicializa analisador de logs
        self.phone_log_analyzer = LogAnalyzer(["./logs/cellphone"])
        self.human_log_analyzer = LogAnalyzer(["./logs/human"])

        # Armazena referência ao detector
        self.detector = detector

        # Bind the close event to the stop callback
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_graphs(self, data_type, period):
        # Determina o caminho dos logs e o título do gráfico com base no tipo de dados
        if data_type == 'phone':
            log_analyzer = self.phone_log_analyzer
            title = "Uso do Celular"
        elif data_type == 'human':
            log_analyzer = self.human_log_analyzer
            title = "Ausência Humana"

        # Obtém os dados de acordo com o período
        if period == 'day':
            data = log_analyzer.get_daily_data()
        elif period == 'week':
            data = log_analyzer.get_weekly_data()
        elif period == 'month':
            data = log_analyzer.get_monthly_data()
        else:
            data = log_analyzer.get_global_data()

        # Atualiza o gráfico com os novos dados
        self.graph.update_data(data)
        self.graph._configure_axes(title)

    def on_closing(self):
        self.stop_callback()
        self.quit()