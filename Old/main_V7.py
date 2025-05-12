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
        master.geometry("400x680") # Altezza aumentata per la nuova riga
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

        # Layout aggiornato: Nuova riga 0 per sin, cos, tan, %
        # Le righe successive sono scalate
        layout_pulsanti = [
            # Riga 0: Funzioni trigonometriche e placeholder %
            ('sin', 0, 0, 1, 1, 'funzione_trig'), 
            ('cos', 0, 1, 1, 1, 'funzione_trig'), 
            ('tan', 0, 2, 1, 1, 'funzione_trig'), 
            ('%', 0, 3, 1, 1, 'funzione_placeholder'), # Placeholder per percentuale
            # Riga 1 (precedente 0): Costanti e modalità angolare
            ('π', 1, 0, 1, 1, 'costante'), ('e', 1, 1, 1, 1, 'costante'), 
            ('deg', 1, 2, 1, 1, 'modalita_angolo'), ('rad', 1, 3, 1, 1, 'modalita_angolo'),
            # Riga 2 (precedente 1): Parentesi, radice, quadrato
            ('(', 2, 0, 1, 1, 'parentesi'), (')', 2, 1, 1, 1, 'parentesi'), 
            ('√', 2, 2, 1, 1, 'funzione_unaria'), ('x²', 2, 3, 1, 1, 'funzione_unaria'),
            # Riga 3 (precedente 2): Clear, backspace, operatori
            ('C', 3, 0, 1, 1, 'clear'), ('CE', 3, 1, 1, 1, 'clear_entry'), ('←', 3, 2, 1, 1, 'backspace'), ('/', 3, 3, 1, 1, 'operatore'),
            # Riga 4 (precedente 3): Numeri e operatori
            ('7', 4, 0, 1, 1, 'numero'), ('8', 4, 1, 1, 1, 'numero'), ('9', 4, 2, 1, 1, 'numero'), ('*', 4, 3, 1, 1, 'operatore'),
            # Riga 5 (precedente 4): Numeri e operatori
            ('4', 5, 0, 1, 1, 'numero'), ('5', 5, 1, 1, 1, 'numero'), ('6', 5, 2, 1, 1, 'numero'), ('-', 5, 3, 1, 1, 'operatore'),
            # Riga 6 (precedente 5): Numeri e operatori
            # ('sin', 5, 0, 1, 1, 'funzione_trig'), # 'sin' spostato alla riga 0
            ('1', 6, 0, 1, 1, 'numero'), ('2', 6, 1, 1, 1, 'numero'), ('3', 6, 2, 1, 1, 'numero'), ('+', 6, 3, 1, 1, 'operatore'), # '+' spostato da riga 6 a qui
            # Riga 7 (precedente 6): +/- , 0, . , +
            ('+/-', 7, 0, 1, 1, 'negate'), ('0', 7, 1, 1, 1, 'numero'), ('.', 7, 2, 1, 1, 'numero'), 
            # Il pulsante '=' ora va in una riga a sé stante (riga 8)
            # ('=', 0, 0, 0, 0, 'uguale') # Rimosso il vecchio placeholder per =
        ]
        
        # Aggiungi il pulsante '=' separatamente per farlo estendere su tutta la larghezza
        layout_pulsanti.append( ('=', 8, 0, 4, 1, 'uguale') ) # Riga 8, = occupa 4 colonne


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
        
        style.configure("Modalita.TButton", font=common_font, padding=common_padding, background='#B0E0E6', foreground='black')
        style.map("Modalita.TButton", foreground=common_foreground_map, background=[('active', '#B0E0E6'), ('!active', '#B0E0E6')],relief=common_relief_map)
        
        style.configure("ModalitaAttiva.TButton", font=common_font, padding=common_padding, background='#87CEEB', foreground='black', relief=tk.SUNKEN)
        style.map("ModalitaAttiva.TButton", foreground=common_foreground_map, background=[('active', '#87CEEB'), ('!active', '#87CEEB')], relief=[('!active', tk.SUNKEN)])

        self.buttons = {} 
        for (testo, riga, col, cspan, rspan, tipo) in layout_pulsanti:
            stile_pulsante = "Numero.TButton" 
            if tipo == 'operatore': stile_pulsante = "Operatore.TButton"
            elif tipo == 'uguale': stile_pulsante = "Uguale.TButton"
            elif tipo == 'clear' or tipo == 'backspace' or tipo == 'clear_entry': stile_pulsante = "Clear.TButton"
            elif tipo == 'negate': stile_pulsante = "Numero.TButton"
            elif tipo in ['parentesi', 'funzione_unaria', 'costante', 'funzione_trig', 'funzione_placeholder']: 
                stile_pulsante = "Funzione.TButton"
            elif tipo == 'modalita_angolo': 
                stile_pulsante = "Modalita.TButton"

            pulsante = ttk.Button(frame_pulsanti, text=testo, style=stile_pulsante,
                                  command=lambda t=testo: self.gestisci_click(t))
            pulsante.grid(row=riga, column=col, columnspan=cspan, rowspan=rspan, sticky="nsew", padx=1, pady=1)
            
            if tipo == 'modalita_angolo': 
                self.buttons[testo] = pulsante

        # Aggiorna il numero di righe configurate per l'espansione
        for i in range(9): # 9 righe di pulsanti (da 0 a 8)
            frame_pulsanti.rowconfigure(i, weight=1)
        for i in range(4): 
            frame_pulsanti.columnconfigure(i, weight=1)
        
        self._aggiorna_stile_pulsanti_modalita_angolo()

    def _aggiorna_stile_pulsanti_modalita_angolo(self):
        if 'deg' in self.buttons and 'rad' in self.buttons:
            if self.angle_mode == "deg":
                self.buttons['deg'].configure(style="ModalitaAttiva.TButton")
                self.buttons['rad'].configure(style="Modalita.TButton")
            else: 
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

    def _evaluate_current_expression(self):
        """Valuta l'espressione corrente sul display, bilanciando le parentesi."""
        expr_to_eval = self.expression_on_display
        open_p = expr_to_eval.count('(')
        closed_p = expr_to_eval.count(')')
        if open_p > closed_p:
            expr_to_eval += ')' * (open_p - closed_p)
        
        # Rimuovi operatori finali prima di eval se l'espressione è solo un numero
        # o se l'utente preme una funzione unaria dopo un operatore senza inserire un numero
        temp_eval = expr_to_eval
        while temp_eval and temp_eval[-1] in "+-*/(": # Aggiunto '(' per evitare eval("(")
            temp_eval = temp_eval[:-1]
        
        if not temp_eval: # Se dopo la pulizia è vuota (es. display era solo "(", "+", etc.)
            raise ValueError("Espressione non valida per la valutazione")
            
        return eval(temp_eval)


    def gestisci_click(self, testo_pulsante):
        numeri = "0123456789"
        operatori_base = "+-*/"
        
        if "Errore" in self.expression_on_display:
            if testo_pulsante == 'C' or testo_pulsante == '←':
                self.expression_on_display = "0"; self.clear_display_on_next_digit = True
            self.aggiorna_display(); return

        if testo_pulsante in numeri:
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
                self.expression_on_display = '-'; self.clear_display_on_next_digit = False; self.aggiorna_display(); return
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
            # (Logica radice quadrata invariata, ma usa _evaluate_current_expression)
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(': self.aggiorna_display(); return
            try:
                valore_da_radicare = self._evaluate_current_expression()
                if valore_da_radicare < 0: self.expression_on_display = "Errore: Radice Negativa"
                else: self.expression_on_display = self._format_result(math.sqrt(valore_da_radicare))
            except (SyntaxError, ValueError): self.expression_on_display = "Errore Sintassi"
            except Exception as e: print(f"Errore in sqrt: {e}"); self.expression_on_display = "Errore"
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
        elif testo_pulsante == 'deg':
            self.angle_mode = "deg"; self._aggiorna_stile_pulsanti_modalita_angolo()
        elif testo_pulsante == 'rad':
            self.angle_mode = "rad"; self._aggiorna_stile_pulsanti_modalita_angolo()

        # --- LOGICA PER SIN, COS, TAN ---
        elif testo_pulsante in ['sin', 'cos', 'tan']:
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(':
                self.aggiorna_display(); return
            try:
                valore_angolo = self._evaluate_current_expression()
                angolo_in_radianti = valore_angolo
                if self.angle_mode == "deg":
                    angolo_in_radianti = math.radians(valore_angolo)
                
                risultato_trig = 0
                if testo_pulsante == 'sin':
                    risultato_trig = math.sin(angolo_in_radianti)
                elif testo_pulsante == 'cos':
                    risultato_trig = math.cos(angolo_in_radianti)
                elif testo_pulsante == 'tan':
                    # Gestione tan(90), tan(270), ecc.
                    cos_val = math.cos(angolo_in_radianti)
                    if abs(cos_val) < 1e-12: # Se cos è molto vicino a zero
                        self.expression_on_display = "Errore: Indefinito"
                        self.clear_display_on_next_digit = True
                        self.aggiorna_display()
                        return
                    risultato_trig = math.tan(angolo_in_radianti)
                
                self.expression_on_display = self._format_result(risultato_trig)
            except (SyntaxError, ValueError): self.expression_on_display = "Errore Sintassi"
            except Exception as e:
                print(f"Errore in {testo_pulsante}: {e}"); self.expression_on_display = "Errore"
            self.clear_display_on_next_digit = True
        # --- FINE LOGICA SIN, COS, TAN ---

        elif testo_pulsante == '=':
            # (Logica = invariata, ma usa _evaluate_current_expression)
            try:
                risultato = self._evaluate_current_expression()
                self.expression_on_display = self._format_result(risultato)
                if self.expression_on_display == "-0": self.expression_on_display = "0"
            except ZeroDivisionError: self.expression_on_display = "Errore: Divisione per 0"
            except (SyntaxError, ValueError) : self.expression_on_display = "Errore Sintassi" # ValueError per eval di stringa vuota
            except Exception as e: print(f"Errore eval '=': {e}"); self.expression_on_display = "Errore"
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
