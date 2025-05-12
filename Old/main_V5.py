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
        master.geometry("400x580") 
        master.resizable(False, False)

        # Variabili di stato interne
        self.expression_on_display = "0" 
        self.clear_display_on_next_digit = True 

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

        layout_pulsanti = [
            ('(', 0, 0, 1, 1, 'parentesi'), (')', 0, 1, 1, 1, 'parentesi'), 
            ('√', 0, 2, 1, 1, 'funzione_unaria'), # Sostituito % con √
            ('x²', 0, 3, 1, 1, 'funzione_unaria'), 
            ('C', 1, 0, 1, 1, 'clear'), ('CE', 1, 1, 1, 1, 'clear_entry'), ('←', 1, 2, 1, 1, 'backspace'), ('/', 1, 3, 1, 1, 'operatore'),
            ('7', 2, 0, 1, 1, 'numero'), ('8', 2, 1, 1, 1, 'numero'), ('9', 2, 2, 1, 1, 'numero'), ('*', 2, 3, 1, 1, 'operatore'),
            ('4', 3, 0, 1, 1, 'numero'), ('5', 3, 1, 1, 1, 'numero'), ('6', 3, 2, 1, 1, 'numero'), ('-', 3, 3, 1, 1, 'operatore'),
            ('1', 4, 0, 1, 1, 'numero'), ('2', 4, 1, 1, 1, 'numero'), ('3', 4, 2, 1, 1, 'numero'), ('+', 4, 3, 1, 1, 'operatore'),
            ('+/-', 5, 0, 1, 1, 'negate'), ('0', 5, 1, 1, 1, 'numero'), ('.', 5, 2, 1, 1, 'numero'), ('=', 5, 3, 1, 1, 'uguale'),
        ]

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

        for (testo, riga, col, cspan, rspan, tipo) in layout_pulsanti:
            stile_pulsante = "Numero.TButton" 
            if tipo == 'operatore': stile_pulsante = "Operatore.TButton"
            elif tipo == 'uguale': stile_pulsante = "Uguale.TButton"
            elif tipo == 'clear' or tipo == 'backspace' or tipo == 'clear_entry': stile_pulsante = "Clear.TButton"
            elif tipo == 'negate': stile_pulsante = "Numero.TButton"
            elif tipo in ['parentesi', 'funzione_unaria']: # 'funzione_placeholder' rimosso se non più usato
                stile_pulsante = "Funzione.TButton"

            pulsante = ttk.Button(frame_pulsanti, text=testo, style=stile_pulsante,
                                  command=lambda t=testo: self.gestisci_click(t))
            pulsante.grid(row=riga, column=col, columnspan=cspan, rowspan=rspan, sticky="nsew", padx=1, pady=1)

        for i in range(6): frame_pulsanti.rowconfigure(i, weight=1)
        for i in range(4): frame_pulsanti.columnconfigure(i, weight=1)

    def aggiorna_display(self):
        self.testo_display_var.set(self.expression_on_display)

    def _format_result(self, result_val):
        """Formatta il risultato per la visualizzazione."""
        if isinstance(result_val, float):
            if result_val.is_integer():
                return str(int(result_val))
            else:
                # Usa 'g' per una formattazione più intelligente (scientifico se necessario)
                # e rstrip per rimuovere zeri e punti decimali non necessari.
                formatted = f"{result_val:.10g}" 
                if '.' in formatted:
                    formatted = formatted.rstrip('0').rstrip('.')
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
            if self.clear_display_on_next_digit:
                self.expression_on_display = testo_pulsante
            elif self.expression_on_display == "0":
                self.expression_on_display = testo_pulsante
            else:
                self.expression_on_display += testo_pulsante
            self.clear_display_on_next_digit = False

        elif testo_pulsante == '.':
            segmento_corrente = ""
            temp_expr = self.expression_on_display
            if self.clear_display_on_next_digit: 
                temp_expr = "0" 
            for char_idx in range(len(temp_expr) - 1, -1, -1):
                char = temp_expr[char_idx]
                if char in operatori_base + "()": break
                segmento_corrente = char + segmento_corrente
            if '.' not in segmento_corrente:
                if self.clear_display_on_next_digit: self.expression_on_display = "0."
                elif not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(':
                     self.expression_on_display += "0."
                else: self.expression_on_display += '.'
            self.clear_display_on_next_digit = False
        
        elif testo_pulsante == '(':
            if self.expression_on_display == "0" or self.clear_display_on_next_digit:
                self.expression_on_display = '('
            elif self.expression_on_display[-1] in numeri + ')':
                self.expression_on_display += '*('
            else: 
                self.expression_on_display += '('
            self.clear_display_on_next_digit = False 

        elif testo_pulsante == ')':
            open_p = self.expression_on_display.count('(')
            closed_p = self.expression_on_display.count(')')
            if open_p > closed_p and self.expression_on_display and \
               self.expression_on_display[-1] not in operatori_base + '(':
                self.expression_on_display += ')'
                self.clear_display_on_next_digit = False
        
        elif testo_pulsante in operatori_base:
            if not self.expression_on_display and testo_pulsante != '-': return
            if self.expression_on_display == "0" and testo_pulsante == '-':
                self.expression_on_display = '-'; self.clear_display_on_next_digit = False
                self.aggiorna_display(); return
            if self.expression_on_display == "-" and testo_pulsante in "+*/": return

            ultimo_carattere = self.expression_on_display[-1] if self.expression_on_display else None
            if ultimo_carattere in operatori_base:
                if testo_pulsante == '-' and ultimo_carattere in "*/(":
                    self.expression_on_display += testo_pulsante
                elif ultimo_carattere == testo_pulsante and testo_pulsante in "*/": pass
                else: self.expression_on_display = self.expression_on_display[:-1] + testo_pulsante
            elif ultimo_carattere == '(' and testo_pulsante == '-':
                self.expression_on_display += testo_pulsante
            elif ultimo_carattere != '(': 
                self.expression_on_display += testo_pulsante
            self.clear_display_on_next_digit = False 
        
        elif testo_pulsante == 'x²':
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(':
                self.aggiorna_display(); return
            self.expression_on_display += '**2'
            self.clear_display_on_next_digit = True 
        
        # --- NUOVA LOGICA PER √ (Radice Quadrata) ---
        elif testo_pulsante == '√':
            if not self.expression_on_display or self.expression_on_display[-1] in operatori_base + '(':
                # Non si può fare la radice di un operatore o di una parentesi aperta
                self.aggiorna_display()
                return
            
            try:
                # Valuta l'espressione corrente per ottenere il numero su cui applicare sqrt
                # È importante chiudere le parentesi se necessario
                expr_to_sqrt = self.expression_on_display
                open_p = expr_to_sqrt.count('(')
                closed_p = expr_to_sqrt.count(')')
                if open_p > closed_p:
                    expr_to_sqrt += ')' * (open_p - closed_p)
                
                # Rimuovi operatori finali prima di eval se l'espressione è solo un numero
                # Questa parte è delicata. Se l'espressione è "5+", sqrt non dovrebbe fare nulla.
                # Se è "5", sqrt(5) è ok. Se è "(2+3)", sqrt(5) è ok.
                
                valore_da_radicare = eval(expr_to_sqrt)
                if valore_da_radicare < 0:
                    self.expression_on_display = "Errore: Radice Negativa"
                else:
                    risultato_sqrt = math.sqrt(valore_da_radicare)
                    self.expression_on_display = self._format_result(risultato_sqrt)

            except SyntaxError:
                self.expression_on_display = "Errore Sintassi"
            except Exception as e:
                print(f"Errore in sqrt eval: {e}, Espressione: {self.expression_on_display}")
                self.expression_on_display = "Errore"
            
            self.clear_display_on_next_digit = True
        # --- FINE LOGICA √ ---

        elif testo_pulsante == '=':
            expr_to_eval = self.expression_on_display
            open_p = expr_to_eval.count('('); closed_p = expr_to_eval.count(')')
            if open_p > closed_p: expr_to_eval += ')' * (open_p - closed_p)
            while expr_to_eval and expr_to_eval[-1] in operatori_base + '(':
                expr_to_eval = expr_to_eval[:-1]
            if expr_to_eval:
                try:
                    expr_to_eval = expr_to_eval.replace('--', '+')
                    risultato = eval(expr_to_eval)
                    self.expression_on_display = self._format_result(risultato)
                    if self.expression_on_display == "-0": self.expression_on_display = "0"
                except ZeroDivisionError: self.expression_on_display = "Errore: Divisione per 0"
                except SyntaxError: self.expression_on_display = "Errore Sintassi"
                except Exception as e:
                    print(f"Errore eval: {e}, Espressione: {expr_to_eval}"); self.expression_on_display = "Errore"
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
            # (Logica +/- invariata, ma potrebbe necessitare di revisione per coerenza con sqrt)
            if self.clear_display_on_next_digit and self.expression_on_display not in ["0", "Errore", "Errore Sintassi", "Errore: Divisione per 0"]:
                try:
                    val = float(self.expression_on_display); val = -val
                    self.expression_on_display = self._format_result(val)
                    self.clear_display_on_next_digit = True 
                except ValueError: pass 
            else:
                start_index = 0
                for i in range(len(self.expression_on_display) - 1, -1, -1):
                    if self.expression_on_display[i] in operatori_base + '(':
                        start_index = i + 1; break
                segment_to_negate = self.expression_on_display[start_index:]
                prefix = self.expression_on_display[:start_index]
                if segment_to_negate and segment_to_negate != "0":
                    if segment_to_negate.startswith('-'):
                        self.expression_on_display = prefix + segment_to_negate[1:]
                    else:
                        if not prefix or prefix[-1] in operatori_base + '(':
                            self.expression_on_display = prefix + '-' + segment_to_negate
                elif segment_to_negate == "0": 
                     self.expression_on_display = prefix + "-"
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
