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
        master.title("Calcolatrice Scientifica")
        master.geometry("400x630") 
        master.resizable(False, False)

        # Variabili di stato interne
        self.expression_on_display = "0" 
        self.clear_display_on_next_digit = True
        self.angle_mode = "rad" # Modalità angolare: "rad" o "deg". Default a radianti.

        # --- Display ---
        self.testo_display_var = tk.StringVar()
        self.aggiorna_display() 

        style = ttk.Style()
        style.configure("Display.TEntry", font=('Arial', 28), foreground='black', justify='right')
        
        frame_display = ttk.Frame(master, padding=(10, 10, 10, 0))
        frame_display.pack(fill=tk.X)

        self.display = ttk.Entry(frame_display, textvariable=self.testo_display_var, 
                                 style="Display.TEntry", state='readonly')
        self.display.pack(fill=tk.X, ipady=15)

        # --- Pulsanti ---
        frame_pulsanti = ttk.Frame(master, padding=10)
        frame_pulsanti.pack(expand=True, fill=tk.BOTH)

        # Layout aggiornato con tipi per deg/rad e sin
        layout_pulsanti = [
            # Riga 0: Costanti, modalità angolare, funzioni trig base
            ('π', 0, 0, 1, 1, 'costante'), ('e', 0, 1, 1, 1, 'costante'), 
            ('deg', 0, 2, 1, 1, 'modalita_angolo'), ('rad', 0, 3, 1, 1, 'modalita_angolo'),
            # Riga 1: Parentesi, radice, quadrato, e aggiungiamo sin
            ('(', 1, 0, 1, 1, 'parentesi'), (')', 1, 1, 1, 1, 'parentesi'), 
            ('√', 1, 2, 1, 1, 'funzione_unaria'), ('x²', 1, 3, 1, 1, 'funzione_unaria'),
            # Riga 2: Clear, backspace, operatori
            ('C', 2, 0, 1, 1, 'clear'), ('CE', 2, 1, 1, 1, 'clear_entry'), ('←', 2, 2, 1, 1, 'backspace'), ('/', 2, 3, 1, 1, 'operatore'),
            # Riga 3: Numeri e operatori
            ('7', 3, 0, 1, 1, 'numero'), ('8', 3, 1, 1, 1, 'numero'), ('9', 3, 2, 1, 1, 'numero'), ('*', 3, 3, 1, 1, 'operatore'),
            # Riga 4: Numeri e operatori
            ('4', 4, 0, 1, 1, 'numero'), ('5', 4, 1, 1, 1, 'numero'), ('6', 4, 2, 1, 1, 'numero'), ('-', 4, 3, 1, 1, 'operatore'),
            # Riga 5: Numeri e operatori
            ('sin', 5, 0, 1, 1, 'funzione_trig'), # Aggiunto sin
            ('1', 5, 1, 1, 1, 'numero'), ('2', 5, 2, 1, 1, 'numero'), ('3', 5, 3, 1, 1, 'numero'), # Spostato +
            # Riga 6: +/- , 0, . , =, +
            ('+/-', 6, 0, 1, 1, 'negate'), ('0', 6, 1, 1, 1, 'numero'), ('.', 6, 2, 1, 1, 'numero'), ('+', 6, 3, 1, 1, 'operatore'), # Spostato + qui
            ('=', 0, 0, 0, 0, 'uguale') # L'uguale lo mettiamo in una riga a parte per un layout migliore
        ]
        
        # Riorganizziamo l'ultima riga per mettere = con columnspan
        # e spostiamo il + nella riga 6
        # Layout aggiornato per una migliore disposizione, specialmente per =
        del layout_pulsanti[-1] # Rimuovi il vecchio placeholder per =
        layout_pulsanti.append( ('=', 7, 0, 4, 1, 'uguale') ) # Riga 7, = occupa 4 colonne


        common_font = ('Arial', 16); common_padding = 5
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

        style.configure("Funzione.TButton", font=common_font, padding=common_padding, background='#C8C8C8', foreground='black') 
        style.map("Funzione.TButton", foreground=common_foreground_map, background=[('active', '#C8C8C8'), ('!active', '#C8C8C8')], relief=common_relief_map)
        
        # Stile per i pulsanti di modalità angolare (per evidenziare quello attivo)
        style.configure("Modalita.TButton", font=common_font, padding=common_padding, background='#B0E0E6', foreground='black') # Azzurrino
        style.map("Modalita.TButton",
                  foreground=common_foreground_map,
                  background=[('active', '#B0E0E6'), ('!active', '#B0E0E6')], # Sfondo non cambia su hover
                  relief=common_relief_map)
        
        style.configure("ModalitaAttiva.TButton", font=common_font, padding=common_padding, background='#87CEEB', foreground='black', relief=tk.SUNKEN) # Azzurro più scuro, incavato
        style.map("ModalitaAttiva.TButton",
                  foreground=common_foreground_map,
                  background=[('active', '#87CEEB'), ('!active', '#87CEEB')],
                  relief=[('!active', tk.SUNKEN)])


        self.buttons = {} # Dizionario per tenere traccia dei pulsanti deg/rad
        for (testo, riga, col, cspan, rspan, tipo) in layout_pulsanti:
            stile_pulsante = "Numero.TButton" 
            if tipo == 'operatore': stile_pulsante = "Operatore.TButton"
            elif tipo == 'uguale': stile_pulsante = "Uguale.TButton"
            elif tipo == 'clear' or tipo == 'backspace' or tipo == 'clear_entry': stile_pulsante = "Clear.TButton"
            elif tipo == 'negate': stile_pulsante = "Numero.TButton"
            elif tipo in ['parentesi', 'funzione_unaria', 'costante', 'funzione_trig']: 
                stile_pulsante = "Funzione.TButton"
            elif tipo == 'modalita_angolo': # Usa lo stile Modalita.TButton
                stile_pulsante = "Modalita.TButton"


            pulsante = ttk.Button(frame_pulsanti, text=testo, style=stile_pulsante,
                                  command=lambda t=testo: self.gestisci_click(t))
            pulsante.grid(row=riga, column=col, columnspan=cspan, rowspan=rspan, sticky="nsew", padx=1, pady=1)
            
            if tipo == 'modalita_angolo': # Salva i riferimenti ai pulsanti deg/rad
                self.buttons[testo] = pulsante


        # Aggiorna il numero di righe configurate per l'espansione
        for i in range(8): # 8 righe di pulsanti (da 0 a 7)
            frame_pulsanti.rowconfigure(i, weight=1)
        for i in range(4): 
            frame_pulsanti.columnconfigure(i, weight=1)
        
        self._aggiorna_stile_pulsanti_modalita_angolo() # Imposta lo stile iniziale

    def _aggiorna_stile_pulsanti_modalita_angolo(self):
        """Aggiorna lo stile dei pulsanti deg/rad per evidenziare quello attivo."""
        if 'deg' in self.buttons and 'rad' in self.buttons:
            if self.angle_mode == "deg":
                self.buttons['deg'].configure(style="ModalitaAttiva.TButton")
                self.buttons['rad'].configure(style="Modalita.TButton")
            else: # rad
                self.buttons['rad'].configure(style="ModalitaAttiva.TButton")
                self.buttons['deg'].configure(style="Modalita.TButton")


    def aggiorna_display(self):
        self.testo_display_var.set(self.expression_on_display)

    def _format_result(self, result_val):
        if isinstance(result_val, float):
            if result_val.is_integer(): return str(int(result_val))
            else:
                formatted = f"{result_val:.10g}" 
                if '.' in formatted: formatted = formatted.rstrip('0').rstrip('.')
                return formatted
        return str(result_val)


    def gestisci_click(self, testo_pulsante):
        numeri = "0123456789"
        operatori_base = "+-*/"
        
        if "Errore" in self.expression_on_display:
            if testo_pulsante == 'C' or testo_pulsante == '←':
                self.expression_on_display = "0"
                self.clear_display_on_next_digit = True
            self.aggiorna_display()
            return

        if testo_pulsante in numeri:
            # (Logica numeri invariata)
            if self.clear_display_on_next_digit: self.expression_on_display = testo_pulsante
            elif self.expression_on_display == "0": self.expression_on_display = testo_pulsante
            else: self.expression_on_display += testo_pulsante
            self.clear_display_on_next_digit = False

        elif testo_pulsante == '.':
            # (Logica punto decimale invariata)
            segmento_corrente = ""; temp_expr = self.expression_on_display
            if self.clear_display_on_next_digit: temp_expr = "0" 
            for char_idx in range(len(temp_expr) - 1, -1, -1):
                char = temp_expr[char_idx]
                if char in operatori_base + "()": break
                segmento_corrente = char + segmento_corrente
            if '.' not in segmento_corrente:
                if self.clear_display_on_next_digit: self.expression_on_display = "0."
                elif not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(': self.expression_on_display += "0."
                else: self.expression_on_display += '.'
            self.clear_display_on_next_digit = False
        
        elif testo_pulsante == '(':
            # (Logica parentesi aperta invariata)
            if self.expression_on_display == "0" or self.clear_display_on_next_digit: self.expression_on_display = '('
            elif self.expression_on_display[-1] in numeri + ')': self.expression_on_display += '*('
            else: self.expression_on_display += '('
            self.clear_display_on_next_digit = False 

        elif testo_pulsante == ')':
            # (Logica parentesi chiusa invariata)
            open_p = self.expression_on_display.count('('); closed_p = self.expression_on_display.count(')')
            if open_p > closed_p and self.expression_on_display and self.expression_on_display[-1] not in operatori_base + '(':
                self.expression_on_display += ')'; self.clear_display_on_next_digit = False
        
        elif testo_pulsante in operatori_base:
            # (Logica operatori base invariata)
            if not self.expression_on_display and testo_pulsante != '-': return
            if self.expression_on_display == "0" and testo_pulsante == '-':
                self.expression_on_display = '-'; self.clear_display_on_next_digit = False
                self.aggiorna_display(); return
            if self.expression_on_display == "-" and testo_pulsante in "+*/": return
            ultimo_carattere = self.expression_on_display[-1] if self.expression_on_display else None
            if ultimo_carattere in operatori_base:
                if testo_pulsante == '-' and ultimo_carattere in "*/(": self.expression_on_display += testo_pulsante
                elif ultimo_carattere == testo_pulsante and testo_pulsante in "*/": pass
                else: self.expression_on_display = self.expression_on_display[:-1] + testo_pulsante
            elif ultimo_carattere == '(' and testo_pulsante == '-': self.expression_on_display += testo_pulsante
            elif ultimo_carattere != '(': self.expression_on_display += testo_pulsante
            self.clear_display_on_next_digit = False 
        
        elif testo_pulsante == 'x²':
            # (Logica x² invariata)
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(': self.aggiorna_display(); return
            self.expression_on_display += '**2'; self.clear_display_on_next_digit = True 
        
        elif testo_pulsante == '√':
            # (Logica radice quadrata invariata)
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(': self.aggiorna_display(); return
            try:
                expr_to_sqrt = self.expression_on_display; open_p = expr_to_sqrt.count('('); closed_p = expr_to_sqrt.count(')')
                if open_p > closed_p: expr_to_sqrt += ')' * (open_p - closed_p)
                valore_da_radicare = eval(expr_to_sqrt)
                if valore_da_radicare < 0: self.expression_on_display = "Errore: Radice Negativa"
                else: self.expression_on_display = self._format_result(math.sqrt(valore_da_radicare))
            except SyntaxError: self.expression_on_display = "Errore Sintassi"
            except Exception as e: print(f"Errore in sqrt eval: {e}, Espressione: {self.expression_on_display}"); self.expression_on_display = "Errore"
            self.clear_display_on_next_digit = True
        
        elif testo_pulsante == 'π':
            # (Logica Pi invariata)
            val_costante = self._format_result(math.pi)
            if self.expression_on_display == "0" or self.clear_display_on_next_digit: self.expression_on_display = val_costante
            elif self.expression_on_display[-1] in numeri + ')': self.expression_on_display += '*' + val_costante
            else: self.expression_on_display += val_costante
            self.clear_display_on_next_digit = False

        elif testo_pulsante == 'e':
            # (Logica e invariata)
            val_costante = self._format_result(math.e)
            if self.expression_on_display == "0" or self.clear_display_on_next_digit: self.expression_on_display = val_costante
            elif self.expression_on_display[-1] in numeri + ')': self.expression_on_display += '*' + val_costante
            else: self.expression_on_display += val_costante
            self.clear_display_on_next_digit = False
        
        # --- NUOVA LOGICA PER DEG/RAD e SIN ---
        elif testo_pulsante == 'deg':
            self.angle_mode = "deg"
            self._aggiorna_stile_pulsanti_modalita_angolo()
        
        elif testo_pulsante == 'rad':
            self.angle_mode = "rad"
            self._aggiorna_stile_pulsanti_modalita_angolo()

        elif testo_pulsante == 'sin':
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(':
                self.aggiorna_display(); return
            try:
                expr_to_eval = self.expression_on_display
                open_p = expr_to_eval.count('('); closed_p = expr_to_eval.count(')')
                if open_p > closed_p: expr_to_eval += ')' * (open_p - closed_p)
                
                valore_angolo = eval(expr_to_eval)
                
                angolo_in_radianti = valore_angolo
                if self.angle_mode == "deg":
                    angolo_in_radianti = math.radians(valore_angolo)
                
                risultato_sin = math.sin(angolo_in_radianti)
                self.expression_on_display = self._format_result(risultato_sin)

            except SyntaxError: self.expression_on_display = "Errore Sintassi"
            except Exception as e:
                print(f"Errore in sin eval: {e}, Espressione: {self.expression_on_display}"); self.expression_on_display = "Errore"
            self.clear_display_on_next_digit = True
        # --- FINE LOGICA DEG/RAD e SIN ---

        elif testo_pulsante == '=':
            # (Logica = invariata)
            expr_to_eval = self.expression_on_display; open_p = expr_to_eval.count('('); closed_p = expr_to_eval.count(')')
            if open_p > closed_p: expr_to_eval += ')' * (open_p - closed_p)
            while expr_to_eval and expr_to_eval[-1] in operatori_base + '(': expr_to_eval = expr_to_eval[:-1]
            if expr_to_eval:
                try:
                    expr_to_eval = expr_to_eval.replace('--', '+')
                    risultato = eval(expr_to_eval)
                    self.expression_on_display = self._format_result(risultato)
                    if self.expression_on_display == "-0": self.expression_on_display = "0"
                except ZeroDivisionError: self.expression_on_display = "Errore: Divisione per 0"
                except SyntaxError: self.expression_on_display = "Errore Sintassi"
                except Exception as e: print(f"Errore eval: {e}, Espressione: {expr_to_eval}"); self.expression_on_display = "Errore"
            else:
                if self.expression_on_display and self.expression_on_display[-1] not in operatori_base + '(': pass 
                else: self.expression_on_display = "0"
            self.clear_display_on_next_digit = True

        elif testo_pulsante == 'C':
            self.expression_on_display = "0"; self.clear_display_on_next_digit = True
        
        elif testo_pulsante == 'CE': 
            self.expression_on_display = "0"; self.clear_display_on_next_digit = True

        elif testo_pulsante == '←': 
            if len(self.expression_on_display) > 1: self.expression_on_display = self.expression_on_display[:-1]
            elif self.expression_on_display != "0": self.expression_on_display = "0"
            if self.expression_on_display == "0": self.clear_display_on_next_digit = True
            else: self.clear_display_on_next_digit = False
        
        elif testo_pulsante == '+/-':
            # (Logica +/- invariata)
            if self.clear_display_on_next_digit and self.expression_on_display not in ["0", "Errore", "Errore Sintassi", "Errore: Divisione per 0"]:
                try:
                    val = float(self.expression_on_display); val = -val
                    self.expression_on_display = self._format_result(val); self.clear_display_on_next_digit = True 
                except ValueError: pass 
            else:
                start_index = 0
                for i in range(len(self.expression_on_display) - 1, -1, -1):
                    if self.expression_on_display[i] in operatori_base + '(': start_index = i + 1; break
                segment_to_negate = self.expression_on_display[start_index:]; prefix = self.expression_on_display[:start_index]
                if segment_to_negate and segment_to_negate != "0":
                    if segment_to_negate.startswith('-'): self.expression_on_display = prefix + segment_to_negate[1:]
                    else:
                        if not prefix or prefix[-1] in operatori_base + '(': self.expression_on_display = prefix + '-' + segment_to_negate
                elif segment_to_negate == "0": self.expression_on_display = prefix + "-"
            self.clear_display_on_next_digit = False 
            if self.expression_on_display == "": self.expression_on_display = "0" 

        self.aggiorna_display()

# --- Funzione Principale ---
def main():
    root = tk.Tk()
    app = Calcolatrice(root)
    root.mainloop()

if __name__ == "__main__":
    main()
