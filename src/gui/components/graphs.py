# src/gui/components/graphs.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphController:
    def __init__(self, master, title):
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self._configure_axes(title)
        
    def _configure_axes(self, title):
        """Configura estilo dos gráficos"""
        self.ax.set_facecolor('#2E2E2E')
        self.fig.patch.set_facecolor('#2b2b2b')
        self.ax.tick_params(colors='white')
        self.ax.set_xlabel("Hora do Dia", color='white')
        self.ax.set_ylabel("Tempo (minutos)", color='white')
        self.ax.set_title(title, color='white', fontsize=14, fontweight='bold')
        self.ax.set_xticks(range(0, 24))
        self.ax.set_xlim(0, 23)
        self.ax.grid(True, alpha=0.3)
    
    def update_data(self, hourly_data):
        """Atualiza gráfico com novos dados"""
        hours = list(range(24))
        values = [hourly_data.get(h, 0) / 60 for h in hours]  # Converte de segundos para minutos
        
        self.ax.clear()
        self._configure_axes(self.ax.get_title())
        self.ax.plot(hours, values, marker='o', linestyle='-', color='#00C0FF')
        self.canvas.draw()
    
    def get_widget(self):
        return self.canvas.get_tk_widget()