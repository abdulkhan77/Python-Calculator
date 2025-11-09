# gui_calculator_colorful.py
import tkinter as tk

# --- Color Palette ---
COLORS = {
    "window_bg": "#2a2d36",
    "display_bg": "#3a3f4b",
    "display_fg": "#ffffff",
    "button_bg": "#3a3f4b",
    "button_fg": "#ffffff",
    "operator_bg": "#ff9f0a",
    "operator_fg": "#ffffff",
    "special_bg": "#60636b",
    "special_fg": "#ffffff",
}

# --- Event Handler Functions ---

def on_key_press(event):
    """Handles keyboard presses and inserts them into the readonly display."""
    key = event.char
    if key in '0123456789./*+-':
        display_field.config(state='normal')
        display_field.insert(tk.END, key)
        display_field.config(state='readonly')

def calculate_result(event=None):
    """Calculates the expression and shows the result."""
    display_field.config(state='normal')
    try:
        expression = display_field.get()
        result = eval(expression)
        clear_display(is_internal_call=True)
        display_field.insert(0, str(result))
    except (SyntaxError, ZeroDivisionError, NameError):
        clear_display(is_internal_call=True)
        display_field.insert(0, "Error")
    finally:
        display_field.config(state='readonly')

def clear_display(event=None, is_internal_call=False):
    """Clears the entire display field."""
    if not is_internal_call: display_field.config(state='normal')
    display_field.delete(0, tk.END)
    if not is_internal_call: display_field.config(state='readonly')

def backspace(event=None):
    """Deletes the last character from the display field."""
    display_field.config(state='normal')
    current_text = display_field.get()
    if current_text:
        new_text = current_text[:-1]
        clear_display(is_internal_call=True)
        display_field.insert(0, new_text)
    display_field.config(state='readonly')

def on_button_click(char):
    """Appends the clicked character to the display."""
    display_field.config(state='normal')
    if char == '×':
        display_field.insert(tk.END, '*')
    elif char == '÷':
        display_field.insert(tk.END, '/')
    else:
        display_field.insert(tk.END, char)
    display_field.config(state='readonly')

# --- Main Window Setup ---
app = tk.Tk()
app.title("Colorful Calculator")
app.geometry("400x500")
app.resizable(True, True)
app.configure(bg=COLORS["window_bg"])

# --- Keyboard Bindings ---
app.bind("<Key>", on_key_press)
app.bind("<Return>", calculate_result)
app.bind("<BackSpace>", backspace)
app.bind("<Escape>", clear_display)

# --- Display Screen ---
display_field = tk.Entry(
    app,
    font=('Arial', 24),
    borderwidth=0,
    relief="flat",
    justify='right',
    state='readonly',
    bg=COLORS["display_bg"],
    fg=COLORS["display_fg"],
    readonlybackground=COLORS["display_bg"] # Color for readonly state
)
display_field.pack(padx=20, pady=(20, 10), ipady=10, fill='x')

# --- Button Frame ---
button_frame = tk.Frame(app, bg=COLORS["window_bg"])
button_frame.pack(padx=10, pady=10)

# --- Button Definitions ---
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('÷', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('×', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 3),
]

# --- Create and Place Buttons ---
for (text, row, col) in buttons:
    bg_color = COLORS["operator_bg"] if text in '÷×-+' else COLORS["button_bg"]
    fg_color = COLORS["operator_fg"] if text in '÷×-+' else COLORS["button_fg"]
    
    btn = tk.Button(
        button_frame,
        text=text,
        font=('Arial', 18),
        height=2,
        width=5,
        command=lambda t=text: on_button_click(t),
        bg=bg_color,
        fg=fg_color,
        borderwidth=0,
        relief="flat"
    )
    btn.grid(row=row, column=col, padx=5, pady=5)

# Create the 'Clear' (C) button separately
clear_btn = tk.Button(
    button_frame, text='C', font=('Arial', 18), height=2, width=5,
    command=clear_display, bg=COLORS["special_bg"], fg=COLORS["special_fg"],
    borderwidth=0, relief="flat"
)
clear_btn.grid(row=4, column=2, padx=5, pady=5)

# Create the 'Equals' (=) button
equals_btn = tk.Button(
    button_frame, text='=', font=('Arial', 18), height=2, width=5,
    command=calculate_result, bg=COLORS["operator_bg"], fg=COLORS["operator_fg"],
    borderwidth=0, relief="flat"
)
equals_btn.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky='we')

# --- Run the Application ---
app.mainloop()