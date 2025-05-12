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
        master.title("PyCalculator")
        # --- MODIFICA: Dimensioni finestra per layout più orizzontale ---
        master.geometry("520x550") 
        master.resizable(False, False)

        # Variabili di stato interne
        self.expression_on_display = "0" 
        self.clear_display_on_next_digit = True
        self.angle_mode = "rad" 
        self.memory_value = 0.0 

        # --- Display ---
        self.testo_display_var = tk.StringVar()
        self.aggiorna_display() 

        style = ttk.Style()
        try:
            style.theme_use('clam') 
        except tk.TclError:
            print("Attenzione: Tema 'clam' non trovato, si utilizza il tema di default.")

        style.configure("Display.TEntry", font=('Arial', 28), foreground='black', justify='right')
        
        frame_display = ttk.Frame(master, padding=(10, 10, 10, 0))
        frame_display.pack(fill=tk.X)

        self.display = ttk.Entry(frame_display, textvariable=self.testo_display_var, 
                                 style="Display.TEntry", state='readonly')
        self.display.pack(fill=tk.X, ipady=15)

        # --- Pulsanti ---
        frame_pulsanti = ttk.Frame(master, padding=10)
        frame_pulsanti.pack(expand=True, fill=tk.BOTH)

        # --- MODIFICA: Layout pulsanti 6 colonne x 8 righe ---
        layout_pulsanti = [
            # Riga 0
            ('(', 0, 0, 1, 1, 'parentesi'), (')', 0, 1, 1, 1, 'parentesi'), 
            ('MC', 0, 2, 1, 1, 'memoria'), ('MR', 0, 3, 1, 1, 'memoria'), 
            ('MS', 0, 4, 1, 1, 'memoria'), ('M+', 0, 5, 1, 1, 'memoria'),
            # Riga 1
            ('sin', 1, 0, 1, 1, 'funzione_trig'), ('cos', 1, 1, 1, 1, 'funzione_trig'),
            ('tan', 1, 2, 1, 1, 'funzione_trig'), ('sin⁻¹', 1, 3, 1, 1, 'funzione_trig_inv'),
            ('cos⁻¹', 1, 4, 1, 1, 'funzione_trig_inv'), ('tan⁻¹', 1, 5, 1, 1, 'funzione_trig_inv'),
            # Riga 2
            ('sinh', 2, 0, 1, 1, 'funzione_iperbolica'), ('cosh', 2, 1, 1, 1, 'funzione_iperbolica'),
            ('tanh', 2, 2, 1, 1, 'funzione_iperbolica'), ('log', 2, 3, 1, 1, 'funzione_log'),
            ('ln', 2, 4, 1, 1, 'funzione_log'), ('M-', 2, 5, 1, 1, 'memoria'),
            # Riga 3
            ('x³', 3, 0, 1, 1, 'funzione_unaria'), ('x²', 3, 1, 1, 1, 'funzione_unaria'),
            ('√', 3, 2, 1, 1, 'funzione_unaria'), ('1/x', 3, 3, 1, 1, 'funzione_unaria'),
            ('xʸ', 3, 4, 1, 1, 'operatore_potenza'), ('%', 3, 5, 1, 1, 'funzione_unaria'),
            # Riga 4
            ('π', 4, 0, 1, 1, 'costante'), ('e', 4, 1, 1, 1, 'costante'),
            ('deg', 4, 2, 1, 1, 'modalita_angolo'), ('rad', 4, 3, 1, 1, 'modalita_angolo'),
            ('C', 4, 4, 1, 1, 'clear'), ('CE', 4, 5, 1, 1, 'clear_entry'),
            # Riga 5
            ('7', 5, 0, 1, 1, 'numero'), ('8', 5, 1, 1, 1, 'numero'),
            ('9', 5, 2, 1, 1, 'numero'), ('←', 5, 3, 1, 1, 'backspace'),
            ('/', 5, 4, 1, 1, 'operatore'), ('*', 5, 5, 1, 1, 'operatore'),
            # Riga 6
            ('4', 6, 0, 1, 1, 'numero'), ('5', 6, 1, 1, 1, 'numero'),
            ('6', 6, 2, 1, 1, 'numero'), ('+/-', 6, 3, 1, 1, 'negate'),
            ('-', 6, 4, 1, 1, 'operatore'), ('+', 6, 5, 1, 1, 'operatore'),
            # Riga 7
            ('1', 7, 0, 1, 1, 'numero'), ('2', 7, 1, 1, 1, 'numero'),
            ('3', 7, 2, 1, 1, 'numero'), ('0', 7, 3, 1, 1, 'numero'), # 0 come pulsante singolo
            ('.', 7, 4, 1, 1, 'numero'), ('=', 7, 5, 1, 1, 'uguale')
        ]
        # --- FINE MODIFICA LAYOUT ---
        
        common_font = ('Arial', 16); common_padding = 5 # Ridotto padding per far stare più pulsanti
        common_relief_map_hover_effect = [('pressed', tk.SUNKEN), ('active', tk.GROOVE), ('!active', tk.RAISED)]
        common_foreground_black = [('active', 'black'), ('!active', 'black')]

        # (Definizioni stili Numero, Operatore, Clear, Uguale, Funzione, Modalita, ModalitaAttiva, Memoria invariate)
        style.configure("Numero.TButton", font=common_font, padding=common_padding, background='#E0E0E0', foreground='black', relief=tk.RAISED) 
        style.map("Numero.TButton", foreground=common_foreground_black, background=[('active', '#E0E0E0'), ('!active', '#E0E0E0')], relief=common_relief_map_hover_effect)
        style.configure("Operatore.TButton", font=(common_font[0], common_font[1], 'bold'), padding=common_padding, background='#D0D0D0', foreground='black', relief=tk.RAISED)
        style.map("Operatore.TButton", foreground=common_foreground_black, background=[('active', '#D0D0D0'), ('!active', '#D0D0D0')], relief=common_relief_map_hover_effect)
        style.configure("Clear.TButton", font=(common_font[0], common_font[1], 'bold'), padding=common_padding, background='#FF6347', foreground='black', relief=tk.RAISED)
        style.map("Clear.TButton", foreground=common_foreground_black, background=[('active', '#FF6347'), ('!active', '#FF6347')], relief=common_relief_map_hover_effect)
        style.configure("Uguale.TButton", font=(common_font[0], common_font[1], 'bold'), padding=common_padding, background='#FF8C00', foreground='black', relief=tk.RAISED)
        style.map("Uguale.TButton", foreground=common_foreground_black, background=[('active', '#FF8C00'), ('!active', '#FF8C00')], relief=common_relief_map_hover_effect)
        style.configure("Funzione.TButton", font=common_font, padding=common_padding, background='#C8C8C8', foreground='black', relief=tk.RAISED) 
        style.map("Funzione.TButton", foreground=common_foreground_black, background=[('active', '#C8C8C8'), ('!active', '#C8C8C8')], relief=common_relief_map_hover_effect)
        colore_modalita_inattiva = '#B0E0E6'; colore_modalita_attiva = '#87CEEB'   
        style.configure("Modalita.TButton", font=common_font, padding=common_padding, background=colore_modalita_inattiva, foreground='black', relief=tk.RAISED)      
        style.map("Modalita.TButton", foreground=common_foreground_black, background=[('!disabled', colore_modalita_inattiva), ('active', colore_modalita_inattiva)], relief=[('pressed', tk.SUNKEN), ('active', tk.GROOVE), ('!active', tk.RAISED)])
        style.configure("ModalitaAttiva.TButton", font=common_font, padding=common_padding, background=colore_modalita_attiva, foreground='black', relief=tk.SUNKEN)     
        style.map("ModalitaAttiva.TButton", foreground=common_foreground_black, background=[('!disabled', colore_modalita_attiva), ('active', colore_modalita_attiva)], relief=[('pressed', tk.SUNKEN), ('active', tk.GROOVE), ('!active', tk.SUNKEN)])
        style.configure("Memoria.TButton", font=common_font, padding=common_padding, background='#ADD8E6', foreground='black', relief=tk.RAISED) 
        style.map("Memoria.TButton", foreground=common_foreground_black, background=[('active', '#ADD8E6'), ('!active', '#ADD8E6')], relief=common_relief_map_hover_effect)

        self.buttons = {} 
        for (testo, riga, col, cspan, rspan, tipo) in layout_pulsanti:
            stile_pulsante = "Numero.TButton" 
            if tipo == 'operatore': stile_pulsante = "Operatore.TButton"
            elif tipo == 'uguale': stile_pulsante = "Uguale.TButton"
            elif tipo == 'clear' or tipo == 'backspace' or tipo == 'clear_entry': stile_pulsante = "Clear.TButton"
            elif tipo == 'negate': stile_pulsante = "Numero.TButton"
            elif tipo in ['parentesi', 'funzione_unaria', 'costante', 'funzione_trig', 
                          'funzione_trig_inv', 'funzione_log', 'operatore_potenza', 
                          'funzione_iperbolica', 'funzione_placeholder']: 
                stile_pulsante = "Funzione.TButton"
            elif tipo == 'modalita_angolo': 
                stile_pulsante = "Modalita.TButton"
            elif tipo == 'memoria': 
                stile_pulsante = "Memoria.TButton"

            pulsante = ttk.Button(frame_pulsanti, text=testo, style=stile_pulsante,
                                  command=lambda t=testo: self.gestisci_click(t))
            pulsante.grid(row=riga, column=col, columnspan=cspan, rowspan=rspan, sticky="nsew", padx=1, pady=1)
            
            if tipo == 'modalita_angolo': 
                self.buttons[testo] = pulsante

        # --- MODIFICA: Configurazione righe/colonne per nuovo layout ---
        for i in range(8): # 8 righe di pulsanti (da 0 a 7)
            frame_pulsanti.rowconfigure(i, weight=1)
        for i in range(6): # 6 colonne di pulsanti (da 0 a 5)
            frame_pulsanti.columnconfigure(i, weight=1)
        # --- FINE MODIFICA ---
        
        self._aggiorna_stile_pulsanti_modalita_angolo()

    # ... (resto delle funzioni _aggiorna_stile_pulsanti_modalita_angolo, aggiorna_display, _format_result, _evaluate_current_expression, gestisci_click invariate) ...
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
        expr_to_eval = self.expression_on_display
        open_p = expr_to_eval.count('('); closed_p = expr_to_eval.count(')')
        if open_p > closed_p: expr_to_eval += ')' * (open_p - closed_p)
        temp_eval = expr_to_eval
        while temp_eval and (temp_eval[-1] in "+-*/(" or temp_eval.endswith('**')):
            if temp_eval.endswith('**'): temp_eval = temp_eval[:-2]
            else: temp_eval = temp_eval[:-1]
        if not temp_eval: raise ValueError("Espressione non valida per la valutazione")
        return eval(temp_eval)


    def gestisci_click(self, testo_pulsante):
        numeri = "0123456789"
        operatori_base = "+-*/"
        
        if "Errore" in self.expression_on_display and testo_pulsante not in ['C', '←']:
            self.aggiorna_display(); return
        elif "Errore" in self.expression_on_display and testo_pulsante in ['C', '←']:
             self.expression_on_display = "0"; self.clear_display_on_next_digit = True
             self.aggiorna_display(); return

        if testo_pulsante in numeri:
            if self.clear_display_on_next_digit: self.expression_on_display = testo_pulsante
            elif self.expression_on_display == "0": self.expression_on_display = testo_pulsante
            else: self.expression_on_display += testo_pulsante
            self.clear_display_on_next_digit = False
        elif testo_pulsante == '.':
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
            if self.expression_on_display == "0" or self.clear_display_on_next_digit: self.expression_on_display = '('
            elif self.expression_on_display[-1] in numeri + ')': self.expression_on_display += '*('
            else: self.expression_on_display += '('
            self.clear_display_on_next_digit = False 
        elif testo_pulsante == ')':
            open_p = self.expression_on_display.count('('); closed_p = self.expression_on_display.count(')')
            if open_p > closed_p and self.expression_on_display and self.expression_on_display[-1] not in operatori_base + '(**':
                self.expression_on_display += ')'; self.clear_display_on_next_digit = False
        elif testo_pulsante == 'xʸ':
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(**' or self.expression_on_display[-1] == '(': return
            self.expression_on_display += '**'; self.clear_display_on_next_digit = False
        elif testo_pulsante in operatori_base:
            if not self.expression_on_display and testo_pulsante != '-': return
            if self.expression_on_display == "0" and testo_pulsante == '-':
                self.expression_on_display = '-'; self.clear_display_on_next_digit = False; self.aggiorna_display(); return
            if self.expression_on_display == "-" and testo_pulsante in "+*/": return
            if len(self.expression_on_display) >= 2 and self.expression_on_display[-2:] == '**':
                if testo_pulsante == '-': self.expression_on_display += testo_pulsante
                self.aggiorna_display(); return
            ultimo_carattere = self.expression_on_display[-1] if self.expression_on_display else None
            if ultimo_carattere in operatori_base : 
                if testo_pulsante == '-' and ultimo_carattere in "*/(": self.expression_on_display += testo_pulsante
                elif ultimo_carattere == testo_pulsante and testo_pulsante in "*/": pass
                else: self.expression_on_display = self.expression_on_display[:-1] + testo_pulsante
            elif ultimo_carattere == '(' and testo_pulsante == '-': self.expression_on_display += testo_pulsante
            elif ultimo_carattere != '(': self.expression_on_display += testo_pulsante
            self.clear_display_on_next_digit = False 
        elif testo_pulsante == 'x³':
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(': self.aggiorna_display(); return
            self.expression_on_display += '**3'; self.clear_display_on_next_digit = True
        elif testo_pulsante == 'x²':
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(': self.aggiorna_display(); return
            self.expression_on_display += '**2'; self.clear_display_on_next_digit = True 
        elif testo_pulsante == '√':
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(': self.aggiorna_display(); return
            try:
                valore_da_radicare = self._evaluate_current_expression()
                if valore_da_radicare < 0: self.expression_on_display = "Errore: Radice Negativa"
                else: self.expression_on_display = self._format_result(math.sqrt(valore_da_radicare))
            except (SyntaxError, ValueError): self.expression_on_display = "Errore Sintassi"
            except Exception as e: print(f"Errore in sqrt: {e}"); self.expression_on_display = "Errore"
            self.clear_display_on_next_digit = True
        elif testo_pulsante == 'π':
            val_costante = self._format_result(math.pi)
            if self.expression_on_display == "0" or self.clear_display_on_next_digit: self.expression_on_display = val_costante
            elif self.expression_on_display[-1] in numeri + ')': self.expression_on_display += '*' + val_costante
            else: self.expression_on_display += val_costante
            self.clear_display_on_next_digit = False
        elif testo_pulsante == 'e':
            val_costante = self._format_result(math.e)
            if self.expression_on_display == "0" or self.clear_display_on_next_digit: self.expression_on_display = val_costante
            elif self.expression_on_display[-1] in numeri + ')': self.expression_on_display += '*' + val_costante
            else: self.expression_on_display += val_costante
            self.clear_display_on_next_digit = False
        elif testo_pulsante == 'deg':
            self.angle_mode = "deg"; self._aggiorna_stile_pulsanti_modalita_angolo()
        elif testo_pulsante == 'rad':
            self.angle_mode = "rad"; self._aggiorna_stile_pulsanti_modalita_angolo()
        elif testo_pulsante in ['sin', 'cos', 'tan']:
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(': self.aggiorna_display(); return
            try:
                valore_angolo = self._evaluate_current_expression()
                angolo_in_radianti = valore_angolo
                if self.angle_mode == "deg": angolo_in_radianti = math.radians(valore_angolo)
                risultato_trig = 0
                if testo_pulsante == 'sin': risultato_trig = math.sin(angolo_in_radianti)
                elif testo_pulsante == 'cos': risultato_trig = math.cos(angolo_in_radianti)
                elif testo_pulsante == 'tan':
                    cos_val = math.cos(angolo_in_radianti)
                    if abs(cos_val) < 1e-12: self.expression_on_display = "Errore: Indefinito"; self.clear_display_on_next_digit = True; self.aggiorna_display(); return
                    risultato_trig = math.tan(angolo_in_radianti)
                self.expression_on_display = self._format_result(risultato_trig)
            except (SyntaxError, ValueError): self.expression_on_display = "Errore Sintassi"
            except Exception as e: print(f"Errore in {testo_pulsante}: {e}"); self.expression_on_display = "Errore"
            self.clear_display_on_next_digit = True
        elif testo_pulsante == '%':
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(': self.aggiorna_display(); return
            try:
                valore_da_percentualizzare = self._evaluate_current_expression()
                risultato_percentuale = valore_da_percentualizzare / 100.0
                self.expression_on_display = self._format_result(risultato_percentuale)
            except (SyntaxError, ValueError): self.expression_on_display = "Errore Sintassi"
            except Exception as e: print(f"Errore in % eval: {e}"); self.expression_on_display = "Errore"
            self.clear_display_on_next_digit = True
        elif testo_pulsante in ['sin⁻¹', 'cos⁻¹', 'tan⁻¹']:
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(': self.aggiorna_display(); return
            try:
                valore_input = self._evaluate_current_expression()
                risultato_angolo_rad = 0 
                if testo_pulsante == 'sin⁻¹':
                    if -1 <= valore_input <= 1: risultato_angolo_rad = math.asin(valore_input)
                    else: self.expression_on_display = "Errore: Dominio sin⁻¹"; self.clear_display_on_next_digit = True; self.aggiorna_display(); return
                elif testo_pulsante == 'cos⁻¹':
                    if -1 <= valore_input <= 1: risultato_angolo_rad = math.acos(valore_input)
                    else: self.expression_on_display = "Errore: Dominio cos⁻¹"; self.clear_display_on_next_digit = True; self.aggiorna_display(); return
                elif testo_pulsante == 'tan⁻¹': risultato_angolo_rad = math.atan(valore_input)
                risultato_finale_angolo = risultato_angolo_rad
                if self.angle_mode == "deg": risultato_finale_angolo = math.degrees(risultato_angolo_rad)
                self.expression_on_display = self._format_result(risultato_finale_angolo)
            except (SyntaxError, ValueError): self.expression_on_display = "Errore Sintassi"
            except Exception as e: print(f"Errore in {testo_pulsante}: {e}"); self.expression_on_display = "Errore"
            self.clear_display_on_next_digit = True
        elif testo_pulsante == '1/x':
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(': self.aggiorna_display(); return
            try:
                valore_da_invertire = self._evaluate_current_expression()
                if valore_da_invertire == 0: self.expression_on_display = "Errore: Divisione per 0"
                else: self.expression_on_display = self._format_result(1 / valore_da_invertire)
            except (SyntaxError, ValueError): self.expression_on_display = "Errore Sintassi"
            except Exception as e: print(f"Errore in 1/x: {e}"); self.expression_on_display = "Errore"
            self.clear_display_on_next_digit = True
        elif testo_pulsante == 'n!':
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(': self.aggiorna_display(); return
            try:
                valore_input = self._evaluate_current_expression()
                if isinstance(valore_input, float) and not valore_input.is_integer(): self.expression_on_display = "Errore: Input non intero"
                elif valore_input < 0: self.expression_on_display = "Errore: Dominio n!"
                else:
                    risultato_fattoriale = math.factorial(int(valore_input))
                    self.expression_on_display = self._format_result(risultato_fattoriale)
            except (SyntaxError, ValueError): self.expression_on_display = "Errore: Input non intero"
            except OverflowError: self.expression_on_display = "Errore: Overflow"
            except Exception as e: print(f"Errore in n!: {e}"); self.expression_on_display = "Errore"
            self.clear_display_on_next_digit = True
        elif testo_pulsante in ['log', 'ln']:
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(': self.aggiorna_display(); return
            try:
                valore_input = self._evaluate_current_expression()
                risultato_log = 0
                if valore_input <= 0: self.expression_on_display = "Errore: Dominio log"; self.clear_display_on_next_digit = True; self.aggiorna_display(); return
                if testo_pulsante == 'log': risultato_log = math.log10(valore_input)
                elif testo_pulsante == 'ln': risultato_log = math.log(valore_input)
                self.expression_on_display = self._format_result(risultato_log)
            except (SyntaxError, ValueError): self.expression_on_display = "Errore Sintassi"
            except Exception as e: print(f"Errore in {testo_pulsante}: {e}"); self.expression_on_display = "Errore"
            self.clear_display_on_next_digit = True
        elif testo_pulsante in ['sinh', 'cosh', 'tanh']:
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(': self.aggiorna_display(); return
            try:
                valore_input = self._evaluate_current_expression()
                risultato_iperbolico = 0
                if testo_pulsante == 'sinh': risultato_iperbolico = math.sinh(valore_input)
                elif testo_pulsante == 'cosh': risultato_iperbolico = math.cosh(valore_input)
                elif testo_pulsante == 'tanh': risultato_iperbolico = math.tanh(valore_input)
                self.expression_on_display = self._format_result(risultato_iperbolico)
            except (SyntaxError, ValueError): self.expression_on_display = "Errore Sintassi"
            except OverflowError: self.expression_on_display = "Errore: Overflow"
            except Exception as e: print(f"Errore in {testo_pulsante}: {e}"); self.expression_on_display = "Errore"
            self.clear_display_on_next_digit = True
        elif testo_pulsante == 'MC': 
            self.memory_value = 0.0
        elif testo_pulsante == 'MR': 
            self.expression_on_display = self._format_result(self.memory_value)
            self.clear_display_on_next_digit = True 
        elif testo_pulsante == 'MS': 
            if not self.expression_on_display or "Errore" in self.expression_on_display: return
            try:
                valore_da_memorizzare = self._evaluate_current_expression()
                self.memory_value = valore_da_memorizzare
                self.clear_display_on_next_digit = True 
            except (SyntaxError, ValueError): self.expression_on_display = "Errore Sintassi"
            except Exception as e: print(f"Errore in MS: {e}"); self.expression_on_display = "Errore"
        elif testo_pulsante == 'M+': 
            if not self.expression_on_display or "Errore" in self.expression_on_display: return
            try:
                valore_da_aggiungere = self._evaluate_current_expression()
                self.memory_value += valore_da_aggiungere
                self.clear_display_on_next_digit = True
            except (SyntaxError, ValueError): self.expression_on_display = "Errore Sintassi"
            except Exception as e: print(f"Errore in M+: {e}"); self.expression_on_display = "Errore"
        elif testo_pulsante == 'M-': 
            if not self.expression_on_display or "Errore" in self.expression_on_display: return
            try:
                valore_da_sottrarre = self._evaluate_current_expression()
                self.memory_value -= valore_da_sottrarre
                self.clear_display_on_next_digit = True
            except (SyntaxError, ValueError): self.expression_on_display = "Errore Sintassi"
            except Exception as e: print(f"Errore in M-: {e}"); self.expression_on_display = "Errore"
        elif testo_pulsante == '=':
            try:
                risultato = self._evaluate_current_expression()
                self.expression_on_display = self._format_result(risultato)
                if self.expression_on_display == "-0": self.expression_on_display = "0"
            except ZeroDivisionError: self.expression_on_display = "Errore: Divisione per 0"
            except (SyntaxError, ValueError) : self.expression_on_display = "Errore Sintassi"
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
