# برنامه محاسبه حجم و نامعادله

import tkinter as tk
from tkinter import ttk, messagebox
import math

# ---------- ساخت برنامه ----------
app = tk.Tk()
app.title("Volume Calculator")
app.geometry("550x450")
app.resizable(False, False)
app.configure(bg="#fdfdfd")

current_lang = tk.StringVar(value="FA")

# ---------- استایل ----------
style = ttk.Style(app)
style.theme_use("clam")

style.configure("TFrame", background="#fdfdfd")
style.configure("TLabel", background="#fdfdfd", foreground="#222222", font=("Helvetica", 11))
style.configure("Title.TLabel", font=("Helvetica", 13, "bold"))
style.configure("TButton", font=("Helvetica", 11), padding=5)

# ---------- جابجایی صفحه ----------
def open_calc_page():
    start_frame.pack_forget()
    notebook.select(vol_tab)
    notebook.pack(expand=True, fill="both", padx=15, pady=15)

def open_settings_page():
    start_frame.pack_forget()
    notebook.select(settings_tab)
    notebook.pack(expand=True, fill="both", padx=15, pady=15)

def open_help_page():
    start_frame.pack_forget()
    notebook.select(help_tab)
    notebook.pack(expand=True, fill="both", padx=15, pady=15)

def go_home():
    notebook.pack_forget()
    start_frame.pack(expand=True, fill="both")

# ---------- تغییر زبان ----------
def change_language():
    lang = current_lang.get()

    if lang == "FA":
        notebook.tab(0, text="حجم")
        notebook.tab(1, text="نامعادله")
        notebook.tab(2, text="تنظیمات")
        notebook.tab(3, text="راهنما")
    else:
        notebook.tab(0, text="Volume")
        notebook.tab(1, text="Inequality")
        notebook.tab(2, text="Settings")
        notebook.tab(3, text="Help")

# ---------- صفحه شروع ----------
start_frame = tk.Frame(app, bg="#fdfdfd")
start_frame.pack(expand=True, fill="both")

tk.Label(start_frame,text="Volume Lab Pro",
         font=("Helvetica", 20, "bold"),
         bg="#fdfdfd",fg="#222222").pack(pady=30)

tk.Button(start_frame,text="محاسبات / Calculations",width=25,
          bg="#4caf50",fg="white",command=open_calc_page).pack(pady=10)

tk.Button(start_frame,text="تنظیمات / Settings",width=25,
          bg="#2196f3",fg="white",command=open_settings_page).pack(pady=10)

tk.Button(start_frame,text="راهنما / Help",width=25,
          bg="#ff9800",fg="white",command=open_help_page).pack(pady=10)

tk.Button(start_frame,text="خروج / Exit",width=25,
          bg="#f44336",fg="white",command=app.destroy).pack(pady=10)

# ---------- تب‌ها ----------
notebook = ttk.Notebook(app)

# ===== تب حجم =====
vol_tab = ttk.Frame(notebook)
notebook.add(vol_tab, text="حجم")

ttk.Label(vol_tab, text="محاسبه حجم", style="Title.TLabel").pack(pady=10)

shape_vol = tk.StringVar(value="کره")

ttk.Combobox(
    vol_tab,
    textvariable=shape_vol,
    values=[
        "کره", "نیم کره", "مکعب", "استوانه",
        "مخروط", "مخروط ناقص", "هرم",
        "منشور مستطیلی", "کره توخالی"
    ],
    state="readonly",
    width=18
).pack(pady=5)

frames = {}
entries = {}

def make_input_frame(name, labels):
    frame = ttk.Frame(vol_tab)
    entries[name] = []

    for label in labels:
        ttk.Label(frame, text=label).pack(side="left", padx=5)
        e = ttk.Entry(frame, width=10)
        e.pack(side="left")
        entries[name].append(e)

    frames[name] = frame

make_input_frame("کره", ["شعاع r:"])
make_input_frame("نیم کره", ["شعاع r:"])
make_input_frame("مکعب", ["ضلع a:"])
make_input_frame("استوانه", ["r:", "h:"])
make_input_frame("مخروط", ["r:", "h:"])
make_input_frame("مخروط ناقص", ["R:", "r:", "h:"])
make_input_frame("هرم", ["طول:", "عرض:", "ارتفاع:"])
make_input_frame("منشور مستطیلی", ["طول:", "عرض:", "ارتفاع:"])
make_input_frame("کره توخالی", ["R:", "r:"])

def refresh_volume_inputs(*args):
    for f in frames.values():
        f.pack_forget()
    frames[shape_vol.get()].pack(pady=5)

shape_vol.trace_add("write", refresh_volume_inputs)
refresh_volume_inputs()

vol_result = ttk.Label(vol_tab, text="", font=("Helvetica", 12, "bold"))
vol_result.pack(pady=10)

# ---------- محاسبه حجم اصلاح شده ----------
def calculate_volume():
    try:
        s = shape_vol.get()
        values = [float(e.get()) for e in entries[s]]

        if any(v <= 0 for v in values):
            raise ValueError

        if s == "کره":
            res = 4/3 * math.pi * values[0]**3

        elif s == "نیم کره":
            res = 2/3 * math.pi * values[0]**3

        elif s == "مکعب":
            res = values[0]**3

        elif s == "استوانه":
            res = math.pi * values[0]**2 * values[1]

        elif s == "مخروط":
            res = math.pi * values[0]**2 * values[1] / 3

        elif s == "مخروط ناقص":
            R, r, h = values
            if R <= r:
                raise ValueError
            res = math.pi * h * (R**2 + R*r + r**2) / 3

        elif s == "هرم":
            res = values[0] * values[1] * values[2] / 3

        elif s == "منشور مستطیلی":
            res = values[0] * values[1] * values[2]

        elif s == "کره توخالی":
            R, r = values
            if R <= r:
                raise ValueError
            res = 4/3 * math.pi * (R**3 - r**3)

        vol_result.config(text=f"حجم ≈ {round(res,2)}")

    except:
        messagebox.showerror("خطا", "مقادیر معتبر وارد کن")

ttk.Button(vol_tab, text="محاسبه", command=calculate_volume).pack(pady=5)
ttk.Button(vol_tab, text="بازگشت به منوی اصلی", command=go_home).pack(pady=5)

# ===== تب نامعادله =====
ineq_tab = ttk.Frame(notebook)
notebook.add(ineq_tab, text="نامعادله")

ttk.Label(ineq_tab, text="ax² + bx + c", style="Title.TLabel").pack(pady=10)

ia = ttk.Entry(ineq_tab)
ib = ttk.Entry(ineq_tab)
ic = ttk.Entry(ineq_tab)

ia.pack(pady=4)
ib.pack(pady=4)
ic.pack(pady=4)

ineq_type = tk.StringVar(value="≥")

ttk.Combobox(
    ineq_tab,
    textvariable=ineq_type,
    values=["≥", "≤", ">", "<"],
    state="readonly",
    width=5
).pack(pady=5)

ineq_result = ttk.Label(ineq_tab, text="", font=("Helvetica", 12, "bold"))
ineq_result.pack(pady=10)

# ---------- حل کامل نامعادله ----------
def solve_inequality():
    try:
        a = float(ia.get())
        b = float(ib.get())
        c = float(ic.get())
        sign = ineq_type.get()

        # حالت خطی
        if a == 0:
            if b == 0:
                messagebox.showerror("خطا", "نامعادله معتبر نیست")
                return

            root = -c / b
            root = round(root,2)

            if (b > 0 and sign in [">", "≥"]) or (b < 0 and sign in ["<", "≤"]):
                ans = f"x {sign} {root}"
            else:
                opposite = {"≥":"≤","≤":"≥",">":"<","<":">"}[sign]
                ans = f"x {opposite} {root}"

            ineq_result.config(text=ans)
            return

        d = b*b - 4*a*c

        if d < 0:
            if (a > 0 and sign in [">", "≥"]) or (a < 0 and sign in ["<", "≤"]):
                ans = "همه اعداد جوابند"
            else:
                ans = "هیچ جوابی ندارد"

        else:
            x1 = (-b - math.sqrt(d)) / (2*a)
            x2 = (-b + math.sqrt(d)) / (2*a)

            lo = round(min(x1,x2),2)
            hi = round(max(x1,x2),2)

            if sign in ["≥", ">"]:
                if a > 0:
                    ans = f"x ≤ {lo} یا x ≥ {hi}"
                else:
                    ans = f"{lo} ≤ x ≤ {hi}"
            else:
                if a > 0:
                    ans = f"{lo} ≤ x ≤ {hi}"
                else:
                    ans = f"x ≤ {lo} یا x ≥ {hi}"

        ineq_result.config(text=ans)

    except:
        messagebox.showerror("خطا", "ورودی نامعتبره")

ttk.Button(ineq_tab, text="حل نامعادله", command=solve_inequality).pack(pady=5)
ttk.Button(ineq_tab, text="بازگشت به منوی اصلی", command=go_home).pack(pady=5)

# ===== تنظیمات =====
settings_tab = ttk.Frame(notebook)
notebook.add(settings_tab, text="تنظیمات")

ttk.Label(settings_tab, text="زبان / Language").pack(pady=5)

ttk.Radiobutton(settings_tab, text="فارسی",
                variable=current_lang,
                value="FA",
                command=change_language).pack()

ttk.Radiobutton(settings_tab, text="English",
                variable=current_lang,
                value="EN",
                command=change_language).pack()

# ===== راهنما =====
help_tab = ttk.Frame(notebook)
notebook.add(help_tab, text="راهنما")

help_text = """
تب حجم:
شکل مورد نظر رو انتخاب کن و ابعادش رو وارد کن.

تب نامعادله:
ضرایب a و b و c رو وارد کن.

تب تنظیمات:
زبان برنامه رو تغییر بده.
"""

ttk.Label(help_tab, text=help_text, justify="left").pack(pady=10)

app.mainloop()