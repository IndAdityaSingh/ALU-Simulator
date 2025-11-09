import tkinter as tk
from tkinter import ttk, messagebox

# Mapping human label -> base
BASES = {
    "Binary": 2,
    "Octal": 8,
    "Decimal": 10,
    "Hexadecimal": 16
}

ALU_BASES = {k: v for k, v in BASES.items() if k in ("Binary", "Octal", "Decimal")}

ALU_OPERATIONS = ["ADD", "SUB", "AND", "OR", "XOR", "NOT(A)"]


def parse_number(txt: str, base: int):
    """Parse user input string according to base. Allow optional leading +/-."""
    s = txt.strip()
    if s == "":
        raise ValueError("Empty input")
    # handle negative
    neg = s.startswith('-')
    if neg:
        s_val = s[1:]
    else:
        s_val = s
    try:
        value = int(s_val, base)
    except ValueError:
        # Let user know what characters are allowed
        raise ValueError(f"Value '{txt}' is not a valid base-{base} number.")
    return -value if neg else value


def to_binary_str(value: int, width: int = None):
    """Return binary string without '0b'. For negative numbers, show '-' + bits of abs(value)."""
    if value < 0:
        return "-" + to_binary_str(-value, width)
    b = bin(value)[2:]
    if width:
        b = b.zfill(width)
    return b


def to_octal_str(value: int):
    if value < 0:
        return "-" + oct(-value)[2:]
    return oct(value)[2:]


def format_result_integer(value: int, width: int = None):
    return {
        "binary": to_binary_str(value, width),
        "octal": to_octal_str(value),
        "decimal": str(value)
    }


class NumALUSimulator(tk.Tk):
    # CORRECTED: The dunder method for initialization is __init__
    def __init__(self):
        super().__init__()
        self.title("Number System & ALU Simulator")
        self.geometry("700x420")
        self.resizable(False, False)
        self._setup_style()
        self._create_widgets()

    def _setup_style(self):
        style = ttk.Style(self)
        # Use a simple theme present on most platforms
        try:
            style.theme_use('clam')
        except Exception:
            pass

    def _create_widgets(self):
        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Converter tab
        conv_frame = ttk.Frame(nb)
        nb.add(conv_frame, text="Converter")

        self._build_converter_tab(conv_frame)

        # ALU tab
        alu_frame = ttk.Frame(nb)
        nb.add(alu_frame, text="ALU Simulator")

        self._build_alu_tab(alu_frame)

    def _build_converter_tab(self, parent):
        pad = {'padx': 6, 'pady': 6}
        # Input
        left = ttk.Frame(parent)
        left.pack(side=tk.TOP, fill=tk.X, padx=8, pady=8)

        ttk.Label(left, text="Input:").grid(row=0, column=0, sticky=tk.W, **pad)
        self.conv_input = ttk.Entry(left, width=30)
        self.conv_input.grid(row=0, column=1, columnspan=2, **pad)

        ttk.Label(left, text="From Base:").grid(row=1, column=0, sticky=tk.W, **pad)
        self.conv_from = ttk.Combobox(left, values=list(BASES.keys()), state="readonly", width=12)
        self.conv_from.current(2)  # Decimal default
        self.conv_from.grid(row=1, column=1, sticky=tk.W, **pad)

        ttk.Label(left, text="To Base:").grid(row=1, column=2, sticky=tk.W, **pad)
        self.conv_to = ttk.Combobox(left, values=list(BASES.keys()), state="readonly", width=12)
        self.conv_to.current(0)  # Binary default
        self.conv_to.grid(row=1, column=3, sticky=tk.W, **pad)

        convert_btn = ttk.Button(left, text="Convert", command=self._on_convert)
        convert_btn.grid(row=0, column=3, sticky=tk.E, **pad)

        # Outputs
        out_frame = ttk.LabelFrame(parent, text="Result")
        out_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        ttk.Label(out_frame, text="Converted Value:").grid(row=0, column=0, sticky=tk.W, **pad)
        self.conv_output = ttk.Entry(out_frame, width=50)
        self.conv_output.grid(row=0, column=1, sticky=tk.W, **pad)

        # Also display all representations quickly:
        ttk.Separator(out_frame, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=2, sticky="ew", pady=4)
        ttk.Label(out_frame, text="Binary:").grid(row=2, column=0, sticky=tk.W, **pad)
        self.all_bin = ttk.Label(out_frame, text="-")
        self.all_bin.grid(row=2, column=1, sticky=tk.W, **pad)

        ttk.Label(out_frame, text="Octal:").grid(row=3, column=0, sticky=tk.W, **pad)
        self.all_oct = ttk.Label(out_frame, text="-")
        self.all_oct.grid(row=3, column=1, sticky=tk.W, **pad)

        ttk.Label(out_frame, text="Decimal:").grid(row=4, column=0, sticky=tk.W, **pad)
        self.all_dec = ttk.Label(out_frame, text="-")
        self.all_dec.grid(row=4, column=1, sticky=tk.W, **pad)

        ttk.Label(out_frame, text="Hexadecimal:").grid(row=5, column=0, sticky=tk.W, **pad)
        self.all_hex = ttk.Label(out_frame, text="-")
        self.all_hex.grid(row=5, column=1, sticky=tk.W, **pad)

    def _build_alu_tab(self, parent):
        pad = {'padx': 6, 'pady': 6}
        top = ttk.Frame(parent)
        top.pack(fill=tk.X, padx=8, pady=8)

        # Operand A
        ttk.Label(top, text="Operand A:").grid(row=0, column=0, sticky=tk.W, **pad)
        self.alu_a_entry = ttk.Entry(top, width=24)
        self.alu_a_entry.grid(row=0, column=1, **pad)
        ttk.Label(top, text="Base:").grid(row=0, column=2, sticky=tk.W, **pad)
        self.alu_a_base = ttk.Combobox(top, values=list(ALU_BASES.keys()), state="readonly", width=10)
        self.alu_a_base.current(0)  # Binary default
        self.alu_a_base.grid(row=0, column=3, **pad)

        # Operand B
        ttk.Label(top, text="Operand B:").grid(row=1, column=0, sticky=tk.W, **pad)
        self.alu_b_entry = ttk.Entry(top, width=24)
        self.alu_b_entry.grid(row=1, column=1, **pad)
        ttk.Label(top, text="Base:").grid(row=1, column=2, sticky=tk.W, **pad)
        self.alu_b_base = ttk.Combobox(top, values=list(ALU_BASES.keys()), state="readonly", width=10)
        self.alu_b_base.current(0)
        self.alu_b_base.grid(row=1, column=3, **pad)

        # Operation
        ttk.Label(top, text="Operation:").grid(row=2, column=0, sticky=tk.W, **pad)
        self.alu_op = ttk.Combobox(top, values=ALU_OPERATIONS, state="readonly", width=12)
        self.alu_op.current(0)
        self.alu_op.grid(row=2, column=1, sticky=tk.W, **pad)

        run_btn = ttk.Button(top, text="Run ALU", command=self._on_run_alu)
        run_btn.grid(row=2, column=3, sticky=tk.E, **pad)

        # Output area
        out_frame = ttk.LabelFrame(parent, text="ALU Output")
        out_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        ttk.Label(out_frame, text="Binary:").grid(row=0, column=0, sticky=tk.W, **pad)
        self.alu_bin = ttk.Label(out_frame, text="-", font=("Consolas", 10))
        self.alu_bin.grid(row=0, column=1, sticky=tk.W, **pad)

        ttk.Label(out_frame, text="Octal:").grid(row=1, column=0, sticky=tk.W, **pad)
        self.alu_oct = ttk.Label(out_frame, text="-")
        self.alu_oct.grid(row=1, column=1, sticky=tk.W, **pad)

        ttk.Label(out_frame, text="Decimal:").grid(row=2, column=0, sticky=tk.W, **pad)
        self.alu_dec = ttk.Label(out_frame, text="-")
        self.alu_dec.grid(row=2, column=1, sticky=tk.W, **pad)

        # Note/help
        note = ("Notes:\n"
                  "- For bitwise ops (AND/OR/XOR) the operands are treated as non-negative integers.\n"
                  "- NOT(A) is computed on A using the minimal bit-width required to represent A (i.e., flips A's bits).\n"
                  "- For arithmetic, negative results are shown with '-' sign.")
        ttk.Label(parent, text=note, justify=tk.LEFT).pack(fill=tk.X, padx=8, pady=(0, 8))

    def _on_convert(self):
        s = self.conv_input.get()
        from_base_label = self.conv_from.get()
        to_base_label = self.conv_to.get()

        if from_base_label not in BASES or to_base_label not in BASES:
            messagebox.showerror("Base error", "Please select valid bases.")
            return
        try:
            value = parse_number(s, BASES[from_base_label])
        except ValueError as e:
            messagebox.showerror("Parse error", str(e))
            return

        # Convert to desired base
        tb = BASES[to_base_label]
        if tb == 2:
            out = to_binary_str(value)
        elif tb == 8:
            out = to_octal_str(value)
        elif tb == 10:
            out = str(value)
        elif tb == 16:
            if value < 0:
                out = "-" + hex(-value)[2:].upper()
            else:
                out = hex(value)[2:].upper()
        else:
            out = str(value)

        self.conv_output.delete(0, tk.END)
        self.conv_output.insert(0, out)

        # Also fill 'all' representations
        width = max(1, value.bit_length()) if value >= 0 else max(1, (-value).bit_length())
        self.all_bin.config(text=to_binary_str(value, width))
        self.all_oct.config(text=to_octal_str(value))
        self.all_dec.config(text=str(value))
        if value < 0:
            self.all_hex.config(text="-" + hex(-value)[2:].upper())
        else:
            self.all_hex.config(text=hex(value)[2:].upper())

    def _on_run_alu(self):
        a_txt = self.alu_a_entry.get()
        b_txt = self.alu_b_entry.get()
        a_base_label = self.alu_a_base.get()
        b_base_label = self.alu_b_base.get()
        op = self.alu_op.get()

        # Validate bases
        if a_base_label not in ALU_BASES or (b_base_label not in ALU_BASES and op != "NOT(A)"):
            messagebox.showerror("Base error", "Please select valid bases for ALU inputs.")
            return

        try:
            a_val = parse_number(a_txt, ALU_BASES[a_base_label])
        except ValueError as e:
            messagebox.showerror("Parse error (A)", str(e))
            return

        if op != "NOT(A)":
            try:
                b_val = parse_number(b_txt, ALU_BASES[b_base_label])
            except ValueError as e:
                messagebox.showerror("Parse error (B)", str(e))
                return
        else:
            b_val = 0  # ignored

        # Perform operation
        try:
            result, display_width = self._alu_compute(a_val, b_val, op)
        except Exception as e:
            messagebox.showerror("ALU error", str(e))
            return

        res_formats = format_result_integer(result, width=display_width)

        self.alu_bin.config(text=res_formats["binary"])
        self.alu_oct.config(text=res_formats["octal"])
        self.alu_dec.config(text=res_formats["decimal"])

    def _alu_compute(self, a: int, b: int, op: str):
        """Return (result_int, display_width_for_binary)."""
        if op == "ADD":
            res = a + b
            # width enough to show result in binary
            width = max(1, res.bit_length() if res >= 0 else (-res).bit_length())
            return res, width
        if op == "SUB":
            res = a - b
            width = max(1, res.bit_length() if res >= 0 else (-res).bit_length())
            return res, width
        if op in ("AND", "OR", "XOR"):
            # treat as non-negative bit patterns for bitwise ops:
            A = a if a >= 0 else -a
            B = b if b >= 0 else -b
            max_width = max(1, A.bit_length(), B.bit_length())
            if op == "AND":
                r = A & B
            elif op == "OR":
                r = A | B
            else:
                r = A ^ B
            return r, max_width
        if op == "NOT(A)":
            A = a if a >= 0 else -a
            width = max(1, A.bit_length())
            mask = (1 << width) - 1
            r = (~A) & mask
            return r, width
        raise ValueError("Unknown operation")

# 🌟 THE CORRECTION: Changed from `"_main_"` to `"__main__"` 
# and also fixed the constructor name inside the class.
if __name__ == "__main__":
    # Also correcting the constructor call name if it was a typo in your provided class
    app = NumALUSimulator() 
    app.mainloop()