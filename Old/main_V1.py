import tkinter as tk
from tkinter import ttk
import math

# --- Classe Calcolatrice ---
class Calcolatrice:
    def __init__(self, master):
        """
        Inizializza la calcolatrice.
        master: la finestra principale di Tkinter.
        """
        self.master = master
        master.title("Calcolatrice")
        master.geometry("400x500")
        master.resizable(False, False)

        # Variabili di stato interne
        self.input_corrente = "0"
        self.espressione_completa = ""
        self.nuovo_input_atteso = True

        # --- Display ---
        self.testo_display_var = tk.StringVar()
        self.aggiorna_display() 

        style = ttk.Style()
        # Stile per il display
        style.configure("Display.TEntry", font=('Arial', 28), foreground='black', justify='right')
        
        frame_display = ttk.Frame(master, padding=(10, 10, 10, 0))
        frame_display.pack(fill=tk.X)

        self.display = ttk.Entry(frame_display, textvariable=self.testo_display_var, 
                                 style="Display.TEntry", state='readonly')
        self.display.pack(fill=tk.X, ipady=15)

        # --- Pulsanti ---
        frame_pulsanti = ttk.Frame(master, padding=10)
        frame_pulsanti.pack(expand=True, fill=tk.BOTH)

        layout_pulsanti = [
            ('C', 0, 0, 1, 1, 'clear'), ('CE', 0, 1, 1, 1, 'clear_entry'), ('←', 0, 2, 1, 1, 'backspace'), ('/', 0, 3, 1, 1, 'operatore'),
            ('7', 1, 0, 1, 1, 'numero'), ('8', 1, 1, 1, 1, 'numero'), ('9', 1, 2, 1, 1, 'numero'), ('*', 1, 3, 1, 1, 'operatore'),
            ('4', 2, 0, 1, 1, 'numero'), ('5', 2, 1, 1, 1, 'numero'), ('6', 2, 2, 1, 1, 'numero'), ('-', 2, 3, 1, 1, 'operatore'),
            ('1', 3, 0, 1, 1, 'numero'), ('2', 3, 1, 1, 1, 'numero'), ('3', 3, 2, 1, 1, 'numero'), ('+', 3, 3, 1, 1, 'operatore'), # '+' userà 'Operatore.TButton'
            ('+/-', 4, 0, 1, 1, 'negate'), ('0', 4, 1, 1, 1, 'numero'), ('.', 4, 2, 1, 1, 'numero'), ('=', 4, 3, 1, 1, 'uguale'),
        ]

        # --- MODIFICA STILI UNIVERSALE ---
        common_font = ('Arial', 16)
        common_padding = 5
        common_relief_map = [('pressed', tk.SUNKEN), ('active', tk.GROOVE), ('!active', tk.RAISED)]
        common_foreground_map = [('active', 'black'), ('!active', 'black')]

        # Stile per i pulsanti numerici, '.', '+/-'
        style.configure("Numero.TButton", 
                        font=common_font, 
                        padding=common_padding,
                        background='#E0E0E0', # Sfondo per numeri
                        foreground='black') 
        style.map("Numero.TButton",
                  foreground=common_foreground_map,
                  background=[('active', '#E0E0E0'), ('!active', '#E0E0E0')], # Sfondo non cambia
                  relief=common_relief_map)
        
        # Stile per gli operatori (+, -, *, /)
        style.configure("Operatore.TButton", 
                        font=(common_font[0], common_font[1], 'bold'), # Operatori in grassetto
                        padding=common_padding,
                        background='#D0D0D0', # Sfondo per operatori
                        foreground='black')
        style.map("Operatore.TButton",
                  foreground=common_foreground_map,
                  background=[('active', '#D0D0D0'), ('!active', '#D0D0D0')], # Sfondo non cambia
                  relief=common_relief_map)

        # Stile per i pulsanti C, CE, ←
        style.configure("Clear.TButton", 
                        font=(common_font[0], common_font[1], 'bold'), 
                        padding=common_padding,
                        background='#FF6347',  # Sfondo per clear
                        foreground='black')
        style.map("Clear.TButton",
                  foreground=common_foreground_map,
                  background=[('active', '#FF6347'), ('!active', '#FF6347')], # Sfondo non cambia
                  relief=common_relief_map)
        
        # Stile per il pulsante '='
        style.configure("Uguale.TButton", 
                        font=(common_font[0], common_font[1], 'bold'), 
                        padding=common_padding,
                        background='#FF8C00', # Sfondo per uguale
                        foreground='black') # Testo nero anche per uguale
        style.map("Uguale.TButton",
                  foreground=common_foreground_map,
                  background=[('active', '#FF8C00'), ('!active', '#FF8C00')], # Sfondo non cambia
                  relief=common_relief_map)
        # --- FINE MODIFICA STILI UNIVERSALE ---

        for (testo, riga, col, cspan, rspan, tipo) in layout_pulsanti:
            stile_pulsante = "Numero.TButton" # Default per 'numero', '.', '+/-'
            if tipo == 'operatore': # Tutti gli operatori +,-,*,/ useranno questo
                stile_pulsante = "Operatore.TButton"
            elif tipo == 'uguale':
                stile_pulsante = "Uguale.TButton"
            elif tipo == 'clear' or tipo == 'backspace' or tipo == 'clear_entry':
                stile_pulsante = "Clear.TButton"
            elif tipo == 'negate': # Anche +/- userà lo stile Numero.TButton
                 stile_pulsante = "Numero.TButton"


            pulsante = ttk.Button(frame_pulsanti, text=testo, style=stile_pulsante,
                                  command=lambda t=testo: self.gestisci_click(t))
            pulsante.grid(row=riga, column=col, columnspan=cspan, rowspan=rspan, sticky="nsew", padx=1, pady=1)

        for i in range(5): frame_pulsanti.rowconfigure(i, weight=1)
        for i in range(4): frame_pulsanti.columnconfigure(i, weight=1)

    def aggiorna_display(self, valore=None):
        if valore is None:
            self.testo_display_var.set(self.input_corrente)
        else:
            self.testo_display_var.set(str(valore))

    def gestisci_click(self, testo_pulsante):
        numeri = "0123456789"
        operatori = "+-*/" 

        if testo_pulsante in numeri:
            if self.nuovo_input_atteso:
                self.input_corrente = testo_pulsante
                self.nuovo_input_atteso = False
            elif self.input_corrente == "0":
                self.input_corrente = testo_pulsante
            else:
                self.input_corrente += testo_pulsante
            self.aggiorna_display()

        elif testo_pulsante == '.':
            if '.' not in self.input_corrente:
                if self.nuovo_input_atteso: 
                    self.input_corrente = "0."
                    self.nuovo_input_atteso = False
                else:
                    self.input_corrente += '.'
                self.aggiorna_display()
        
        elif testo_pulsante in operatori: 
            if self.input_corrente == "Errore" or self.input_corrente == "Errore: Divisione per 0":
                return 
            if self.input_corrente == "-" and not self.espressione_completa:
                 return
            if (not self.espressione_completa and self.input_corrente != "0") or \
               (not self.espressione_completa and self.input_corrente == "0" and testo_pulsante == "-") or \
               self.espressione_completa:
                if not (not self.espressione_completa and self.input_corrente == "0" and testo_pulsante != "-"):
                     self.espressione_completa += self.input_corrente

            if self.espressione_completa and self.espressione_completa[-1] in operatori:
                if testo_pulsante == '-' and self.espressione_completa[-1] in "*/+":
                    self.espressione_completa += testo_pulsante 
                    self.input_corrente = "-" 
                    self.nuovo_input_atteso = False 
                    self.aggiorna_display()
                    return
                else: 
                    self.espressione_completa = self.espressione_completa[:-1] + testo_pulsante
            else:
                self.espressione_completa += testo_pulsante
            self.nuovo_input_atteso = True
        
        elif testo_pulsante == '=':
            if self.input_corrente and self.input_corrente != "-" and self.input_corrente != "Errore" and self.input_corrente != "Errore: Divisione per 0":
                if not (self.espressione_completa and self.espressione_completa[-1] in operatori and self.nuovo_input_atteso):
                     self.espressione_completa += self.input_corrente
            if self.espressione_completa:
                try:
                    espressione_da_valutare = self.espressione_completa.replace('--', '+')
                    risultato = eval(espressione_da_valutare)
                    if isinstance(risultato, float) and risultato.is_integer():
                        self.input_corrente = str(int(risultato))
                    else:
                        self.input_corrente = f"{risultato:.10g}".rstrip('0').rstrip('.') if isinstance(risultato, float) else str(risultato)
                    self.aggiorna_display(self.input_corrente)
                    self.espressione_completa = "" 
                    self.nuovo_input_atteso = True 
                except ZeroDivisionError:
                    self.aggiorna_display("Errore: Divisione per 0")
                    self.input_corrente = "0"; self.espressione_completa = ""; self.nuovo_input_atteso = True
                except Exception as e:
                    print(f"Errore eval: {e}, Espressione: {self.espressione_completa}")
                    self.aggiorna_display("Errore")
                    self.input_corrente = "0"; self.espressione_completa = ""; self.nuovo_input_atteso = True

        elif testo_pulsante == 'C':
            self.input_corrente = "0"; self.espressione_completa = ""; self.nuovo_input_atteso = True
            self.aggiorna_display()

        elif testo_pulsante == 'CE': 
            self.input_corrente = "0"; self.nuovo_input_atteso = True
            self.aggiorna_display()

        elif testo_pulsante == '←': 
            if not self.nuovo_input_atteso and self.input_corrente != "0" and "Errore" not in self.input_corrente :
                self.input_corrente = self.input_corrente[:-1]
                if not self.input_corrente or self.input_corrente == "-": 
                    self.input_corrente = "0"; self.nuovo_input_atteso = True
                self.aggiorna_display()
            elif "Errore" in self.input_corrente: 
                self.input_corrente = "0"; self.espressione_completa = ""; self.nuovo_input_atteso = True
                self.aggiorna_display()

        elif testo_pulsante == '+/-': 
            if self.input_corrente and "Errore" not in self.input_corrente:
                if self.input_corrente == "0": # Se è 0, diventa - e aspetta un numero
                    self.input_corrente = "-"
                    self.nuovo_input_atteso = False # Permetti di digitare dopo il meno
                elif self.input_corrente.startswith('-'):
                    self.input_corrente = self.input_corrente[1:]
                else:
                    self.input_corrente = '-' + self.input_corrente
                self.aggiorna_display()

# --- Funzione Principale ---
def main():
    root = tk.Tk()
    app = Calcolatrice(root)
    root.mainloop()

if __name__ == "__main__":
    main()
