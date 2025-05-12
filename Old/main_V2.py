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
        master.title("Calcolatrice Scientifica") # Titolo aggiornato
        master.geometry("400x580") # Altezza aumentata per la nuova riga di pulsanti
        master.resizable(False, False)

        # Variabili di stato interne
        self.input_corrente = "0"
        self.espressione_completa = ""
        self.nuovo_input_atteso = True # True se il prossimo numero deve sovrascrivere il display

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

        # Layout aggiornato con una nuova riga per le parentesi e funzioni
        layout_pulsanti = [
            # Riga 0: Parentesi e funzioni scientifiche base
            ('(', 0, 0, 1, 1, 'parentesi'), (')', 0, 1, 1, 1, 'parentesi'), ('%', 0, 2, 1, 1, 'funzione'), ('x²', 0, 3, 1, 1, 'funzione'),
            # Riga 1 (precedente 0)
            ('C', 1, 0, 1, 1, 'clear'), ('CE', 1, 1, 1, 1, 'clear_entry'), ('←', 1, 2, 1, 1, 'backspace'), ('/', 1, 3, 1, 1, 'operatore'),
            # Riga 2 (precedente 1)
            ('7', 2, 0, 1, 1, 'numero'), ('8', 2, 1, 1, 1, 'numero'), ('9', 2, 2, 1, 1, 'numero'), ('*', 2, 3, 1, 1, 'operatore'),
            # Riga 3 (precedente 2)
            ('4', 3, 0, 1, 1, 'numero'), ('5', 3, 1, 1, 1, 'numero'), ('6', 3, 2, 1, 1, 'numero'), ('-', 3, 3, 1, 1, 'operatore'),
            # Riga 4 (precedente 3)
            ('1', 4, 0, 1, 1, 'numero'), ('2', 4, 1, 1, 1, 'numero'), ('3', 4, 2, 1, 1, 'numero'), ('+', 4, 3, 1, 1, 'operatore'),
            # Riga 5 (precedente 4)
            ('+/-', 5, 0, 1, 1, 'negate'), ('0', 5, 1, 1, 1, 'numero'), ('.', 5, 2, 1, 1, 'numero'), ('=', 5, 3, 1, 1, 'uguale'),
        ]

        common_font = ('Arial', 16)
        common_padding = 5
        common_relief_map = [('pressed', tk.SUNKEN), ('active', tk.GROOVE), ('!active', tk.RAISED)]
        common_foreground_map = [('active', 'black'), ('!active', 'black')]

        style.configure("Numero.TButton", font=common_font, padding=common_padding, background='#E0E0E0', foreground='black') 
        style.map("Numero.TButton", foreground=common_foreground_map, background=[('active', '#E0E0E0'), ('!active', '#E0E0E0')], relief=common_relief_map)
        
        style.configure("Operatore.TButton", font=(common_font[0], common_font[1], 'bold'), padding=common_padding, background='#D0D0D0', foreground='black')
        style.map("Operatore.TButton", foreground=common_foreground_map, background=[('active', '#D0D0D0'), ('!active', '#D0D0D0')], relief=common_relief_map)

        style.configure("Clear.TButton", font=(common_font[0], common_font[1], 'bold'), padding=common_padding, background='#FF6347', foreground='black')
        style.map("Clear.TButton", foreground=common_foreground_map, background=[('active', '#FF6347'), ('!active', '#FF6347')], relief=common_relief_map)
        
        style.configure("Uguale.TButton", font=(common_font[0], common_font[1], 'bold'), padding=common_padding, background='#FF8C00', foreground='black')
        style.map("Uguale.TButton", foreground=common_foreground_map, background=[('active', '#FF8C00'), ('!active', '#FF8C00')], relief=common_relief_map)

        # Nuovo stile per Parentesi e Funzioni
        style.configure("Funzione.TButton", 
                        font=common_font, 
                        padding=common_padding,
                        background='#C8C8C8', # Sfondo leggermente diverso
                        foreground='black') 
        style.map("Funzione.TButton",
                  foreground=common_foreground_map,
                  background=[('active', '#C8C8C8'), ('!active', '#C8C8C8')],
                  relief=common_relief_map)


        for (testo, riga, col, cspan, rspan, tipo) in layout_pulsanti:
            stile_pulsante = "Numero.TButton" 
            if tipo == 'operatore': 
                stile_pulsante = "Operatore.TButton"
            elif tipo == 'uguale':
                stile_pulsante = "Uguale.TButton"
            elif tipo == 'clear' or tipo == 'backspace' or tipo == 'clear_entry':
                stile_pulsante = "Clear.TButton"
            elif tipo == 'negate': 
                 stile_pulsante = "Numero.TButton"
            elif tipo == 'parentesi' or tipo == 'funzione': # Applica il nuovo stile
                 stile_pulsante = "Funzione.TButton"


            pulsante = ttk.Button(frame_pulsanti, text=testo, style=stile_pulsante,
                                  command=lambda t=testo: self.gestisci_click(t))
            pulsante.grid(row=riga, column=col, columnspan=cspan, rowspan=rspan, sticky="nsew", padx=1, pady=1)

        # Aggiorna il numero di righe configurate per l'espansione
        for i in range(6): # 6 righe di pulsanti (da 0 a 5)
            frame_pulsanti.rowconfigure(i, weight=1)
        for i in range(4): 
            frame_pulsanti.columnconfigure(i, weight=1)

    def aggiorna_display(self, valore=None):
        if valore is None:
            self.testo_display_var.set(self.input_corrente)
        else:
            self.testo_display_var.set(str(valore))

    def gestisci_click(self, testo_pulsante):
        numeri = "0123456789"
        operatori = "+-*/" 
        # Consideriamo le parentesi in modo speciale, non come operatori standard
        # per la logica di concatenazione dell'espressione.

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
        
        elif testo_pulsante == '(':
            # Se un numero era in input_corrente e non era atteso un nuovo input,
            # e l'espressione non è vuota e non termina con un operatore o '(',
            # aggiungi '*' per moltiplicazione implicita.
            if not self.nuovo_input_atteso and self.input_corrente != "0" and self.input_corrente not in operatori and "Errore" not in self.input_corrente:
                if self.espressione_completa and (self.espressione_completa[-1].isdigit() or self.espressione_completa[-1] == ')'):
                    self.espressione_completa += '*'
                self.espressione_completa += self.input_corrente
            
            self.espressione_completa += '('
            self.input_corrente = "0" 
            self.nuovo_input_atteso = True 
            self.aggiorna_display()

        elif testo_pulsante == ')':
            # Aggiungi l'input corrente all'espressione se è un numero valido
            if not self.nuovo_input_atteso and self.input_corrente not in operatori and "Errore" not in self.input_corrente:
                # Non aggiungere "0" se è il valore di default dopo un operatore o '('
                if not (self.input_corrente == "0" and self.espressione_completa and self.espressione_completa[-1] in operatori + '('):
                    self.espressione_completa += self.input_corrente
            
            # Aggiungi la parentesi chiusa solo se ce n'è una aperta da chiudere (controllo base)
            open_parentheses = self.espressione_completa.count('(')
            closed_parentheses = self.espressione_completa.count(')')
            if open_parentheses > closed_parentheses:
                self.espressione_completa += ')'
                self.input_corrente = "0" # Resetta per il prossimo input
                self.nuovo_input_atteso = True 
                self.aggiorna_display(self.espressione_completa) # Mostra l'espressione per vedere la ')'
                # Oppure, per coerenza con gli operatori, potremmo resettare il display a "0"
                # self.aggiorna_display() # Mostrerebbe "0"
            # Se non c'è una '(' aperta, non fare nulla o segnala errore (eval lo farà)

        elif testo_pulsante in operatori: 
            if self.input_corrente == "Errore" or self.input_corrente == "Errore: Divisione per 0":
                return 
            # Non permettere un operatore se l'input corrente è solo "-" e l'espressione è vuota
            if self.input_corrente == "-" and not self.espressione_completa:
                 return

            # Aggiungi l'input corrente all'espressione se è un numero valido
            # o se è l'inizio di un numero negativo (es. dopo un operatore, si preme '-' e poi un numero)
            if not self.nuovo_input_atteso or (self.input_corrente == "-" and self.espressione_completa and self.espressione_completa[-1] in operatori):
                # Non aggiungere "0" se è il valore di default dopo un operatore o '('
                # tranne se l'operatore è '-' e l'espressione è vuota (per iniziare con un negativo)
                if not (self.input_corrente == "0" and self.espressione_completa and self.espressione_completa[-1] in operatori + '(' \
                        and not (testo_pulsante == '-' and not self.espressione_completa) ): # Evita di aggiungere "0" prima di un operatore
                    self.espressione_completa += self.input_corrente


            # Gestione operatori consecutivi
            if self.espressione_completa and self.espressione_completa[-1] in operatori:
                # Se l'ultimo è un operatore e il nuovo è '-', permetti (per numeri negativi)
                if testo_pulsante == '-' and self.espressione_completa[-1] in "*/+(": # Aggiunto '(' qui
                    self.espressione_completa += testo_pulsante 
                else: # Altrimenti sostituisci l'ultimo operatore
                    self.espressione_completa = self.espressione_completa[:-1] + testo_pulsante
            elif self.espressione_completa and self.espressione_completa[-1] == '(' and testo_pulsante == '-':
                self.espressione_completa += testo_pulsante # Permetti (-
            elif self.espressione_completa or testo_pulsante == '-': # Aggiungi operatore se c'è espressione o se è '-'
                self.espressione_completa += testo_pulsante
            
            self.nuovo_input_atteso = True
            self.input_corrente = "0" # Resetta display per il prossimo numero
            self.aggiorna_display()
        
        elif testo_pulsante == '=':
            if self.input_corrente and self.input_corrente != "-" and "Errore" not in self.input_corrente:
                if not (self.espressione_completa and self.espressione_completa[-1] in operatori and self.nuovo_input_atteso):
                     self.espressione_completa += self.input_corrente
            
            # Assicurati che tutte le parentesi aperte siano chiuse prima di eval
            open_p = self.espressione_completa.count('(')
            closed_p = self.espressione_completa.count(')')
            if open_p > closed_p:
                self.espressione_completa += ')' * (open_p - closed_p)


            if self.espressione_completa:
                try:
                    espressione_da_valutare = self.espressione_completa.replace('--', '+')
                    # Rimuovi operatori finali prima di eval, es. "5*=" -> "5"
                    if espressione_da_valutare and espressione_da_valutare[-1] in operatori:
                        espressione_da_valutare = espressione_da_valutare[:-1]

                    if not espressione_da_valutare: # Se dopo la pulizia è vuota
                        self.aggiorna_display(self.input_corrente) # Mostra l'ultimo input
                        return

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
                except SyntaxError:
                     self.aggiorna_display("Errore Sintassi")
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
                if self.input_corrente == "0": 
                    self.input_corrente = "-"
                    self.nuovo_input_atteso = False 
                elif self.input_corrente.startswith('-'):
                    self.input_corrente = self.input_corrente[1:]
                else:
                    self.input_corrente = '-' + self.input_corrente
                self.aggiorna_display()
        
        # Per debug, stampa lo stato dopo ogni click
        # print(f"Btn: '{testo_pulsante}' | Input: '{self.input_corrente}' | Expr: '{self.espressione_completa}' | NuovoInput: {self.nuovo_input_atteso}")


# --- Funzione Principale ---
def main():
    root = tk.Tk()
    app = Calcolatrice(root)
    root.mainloop()

if __name__ == "__main__":
    main()
