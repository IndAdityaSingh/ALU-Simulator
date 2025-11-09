# 🧮 Number System & ALU Simulator (Interactive GUI)

An interactive Python-based **Number System Converter** and **ALU (Arithmetic Logic Unit) Simulator** built using **Tkinter**.  
This tool helps visualize base conversions and simulate digital arithmetic and logical operations in a fun, educational way.

---

## 🌟 Features

### 🔢 **Number System Converter**
- Convert numbers between **Binary, Octal, Decimal, and Hexadecimal** systems.
- Handles both positive and negative numbers.
- Provides **instant, accurate conversions** with progress animation.
- Includes **input validation** and **error alerts** for invalid entries.

### ⚙️ **ALU (Arithmetic Logic Unit) Simulator**
- Performs basic arithmetic and logic operations:
  - **ADD**, **SUB**, **AND**, **OR**, **XOR**, **NOT(A)**
- Supports **Binary**, **Octal**, and **Decimal** inputs.
- Displays real-time operation results in a neat, readable format.

### 💡 **Additional Features**
- **Modern Tkinter UI** with tabs, progress bars, and tooltips.
- **Sound feedback** for success and error events.
- **Threaded execution** for smooth performance without UI freezing.
- **Error handling** with message boxes.
- **Educational design** — perfect for students learning digital logic and number systems.

---

## 🧰 Tech Stack

| Component | Description |
|------------|-------------|
| **Language** | Python 3.x |
| **GUI Framework** | Tkinter (`ttk` themed widgets) |
| **Modules Used** | `tkinter`, `threading`, `time`, `platform`, `winsound` *(optional)* |
| **Compatibility** | Windows, macOS, Linux |

---

## 🚀 How It Works

### **Input**
- Enter numeric values for **Operand A** and **Operand B**.
- Choose the **base** (Binary, Octal, or Decimal).
- Select the **operation** or **conversion type**.

### **Processing**
- The program validates and converts input into internal decimal form.
- Performs the selected ALU operation or base conversion.
- Uses background threads for **smooth, animated progress**.

### **Output**
- Displays the **final result** instantly.
- Provides **real-time feedback** with animations, sounds, and status messages.
- Alerts user in case of **invalid inputs** or **base mismatches**.

---

## 🖼️ Screenshots

| Converter Tab | ALU Simulator |
|----------------|----------------|
| ![Converter Screenshot](assets/converter_tab.png) | ![ALU Screenshot](assets/alu_tab.png) |

*(Add screenshots in an `assets/` folder in your repo.)*

---

## 📂 Project Structure

