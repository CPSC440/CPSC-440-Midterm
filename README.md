## 🚀 Project Readme: CPSC 440 Midterm ALU/Extensions

This repository contains the implementation of a simulated 32-bit Arithmetic Logic Unit (ALU) and its specialized extensions.

The core logic is implemented entirely using bit-wise operations on Python lists of integers (`[0, 1]`) to simulate hardware registers and gate logic.

---

## 💻 Core Components and Implementation Details

### 1. Core ALU (`core/alu.py`)

The primary file implements fundamental arithmetic logic.

* **`add(A_bits, B_bits, initial_carry)`:** Implements 32-bit addition using a **ripple-carry adder**.
    * Crucially, this function supports the `initial_carry` parameter, allowing it to perform **subtraction** ($A - B = A + \sim B + 1$).
    * It correctly calculates and returns the **ALU Flags** ($N$, $Z$, $C$, $V$).
    * **Length Correction:** For floating-point and two's complement encoding, the function prepends a carry-out bit to the result list when necessary.
* **`sub(A_bits, B_bits)`:** Implements subtraction using the two's complement method: $A - B = A + (-B)$.
* **Two's Complement Codec:** Includes functions for **`encode_twos_complement`** (integer to bits) and **`decode_twos_complement`** (bits to integer), correctly handling the 32-bit range and overflow detection.

---

### 2. Floating-Point Extension (`core/f_extension.py`)

This module implements IEEE-754 Single Precision (32-bit) Floating-Point Addition.

* **Constants:** Uses $8$ bits for the exponent, $23$ bits for the fraction, and a bias of $127$.
* **`fadd_f32(a_bits, b_bits)`:** Performs the full addition algorithm:
    1.  **Unpack:** Extracts sign, exponent, and fraction.
    2.  **Align:** Equalizes exponents by shifting the smaller significand right.
    3.  **Add/Subtract:** Performs 24-bit significand addition/subtraction using the core ALU.
    4.  **Normalize:** Detects carry-out (e.g., $1.0 + 1.0 = 10.0$) and shifts the significand right while **incrementing the exponent**.
    5.  **Repack:** Combines the final sign, exponent, and fraction into a 32-bit result.

---

### 3. Multiplication and Division Extensions (`core/m_extension.py`)

This module handles 32-bit signed integer multiplication and division.

* **`mul(rs1_bits, rs2_bits)`:** Performs simple multiplication of two 32-bit two's complement numbers and returns the **lower 32 bits** of the product, consistent with the RISC-V `MUL` instruction.
* **`div(rs1_bits, rs2_bits)`:** Implements **signed 32-bit division** using a modified **Restoring Division Algorithm**:
    1.  Handles signs separately by operating on the **absolute values** of the dividend and divisor.
    2.  Utilizes a 32-iteration loop to simulate the combined A (Remainder) and Q (Quotient) register shifts.
    3.  **Fixed-Width Logic:** Contains critical logic to ensure the A and M registers remain exactly **32 bits wide** during subtraction/restoration, preventing length mismatch errors caused by the ALU's carry-out mechanism.
    4.  Performs final sign correction on both the quotient and the remainder.

---

## ✅ Testing

Unit tests for all components are provided in the `tests/` directory:

* `test_alu.py`: Verifies `add`, `sub`, and two's complement encoding/decoding.
* `test_f_extension.py`: Verifies floating-point addition correctness (e.g., $1.0 + 1.0 = 2.0$).
* `test_m_extension.py`: Verifies signed integer multiplication and division correctness, including handling negative numbers and division by zero.

## AI Usage

Inline Agentic AI was used throughout the writing of the core code. Prompt AI was used to create the test cases, main.py, this README, and for debugging.

## Test

Use the code by running the following commands:
```bash
python main.py
python -m tests.test_alu
python -m tests.test_f_extension
python -m tests.test_m_extension
```
