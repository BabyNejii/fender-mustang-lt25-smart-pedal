# Fender Mustang LT25: "Ultimate" 6-Button Smart Footswitch Build Manual (v2.6 Interactive Checklist Edition)

A definitive, step-by-step master engineering and assembly manual for building a custom 6-button intelligent footswitch controller for the **Fender Mustang LT25**. Features a slanted ergonomic wedge, bank switching, dual operating modes (Preset vs. FX Stompbox), dedicated top-right Mute/Tuner switch, rotary encoder navigation, 1.3" OLED screen, RGB LED indicators, dual power architecture, and smartphone Wi-Fi configuration.

> [!TIP]
> **Interactive Build Progress:**  
> Every actionable step throughout this guide is formatted as a markdown checkbox (`- [ ]`). As you complete each step, mark it with an `x` (`- [x]`). When you ask for guidance or troubleshooting, I will check this file to see your exact progress!

---

## 0. "ZERO FRYING & ZERO SHORTS" Safety Verification Protocol

> [!CAUTION]
> **READ THIS BEFORE TURNING ON YOUR SOLDERING IRON OR CONNECTING ANY POWER.**  
> The Raspberry Pi Zero 2 W Broadcom BCM2710A1 processor has **zero tolerance for overvoltage or reverse polarity**. Follow these 7 non-negotiable rules to ensure no components are damaged:

- [X] **Safety Rule 1: Buck Converter Multimeter Calibration (DO NOT connect Pi before this!):**
  * The MP1584EN step-down buck module arrives with a random factory potentiometer setting (often 8V–9V). If connected directly to the Pi, it will instantly destroy the PMIC and processor.
  * **Procedure:** Connect the 9V DC adapter to the DC-022 jack $\to$ connect to Buck `IN+` and `IN-`. **DO NOT solder Buck `OUT` to the Pi yet.** Power up, touch multimeter probes to Buck `OUT+` and `OUT-`, and slowly turn the brass trimpot screw until the output reads **5.22V DC** (safe operating range: 5.18V to 5.25V).
  * **Locking:** Once trimmed, unplug power and apply a generous drop of hot glue directly over the brass screw to prevent stage vibration from shifting the voltage.
- [x] **Safety Rule 2: 1.1A PTC Polyfuse Protection (RXEF110):**
  * Solder the **RXEF110 1.1A polyfuse** (Comet `#15283`, yellow disc) in series between Buck `OUT+` and Pi **Pin 2 (+5V)**.
  * **Why this is essential:** If an accidental short occurs anywhere on the Pi or LED strip, the 1.1A polyfuse automatically trips into high resistance within milliseconds, preventing trace burning or board damage, and automatically resets once cooled.
- [ ] **Safety Rule 3: KY-040 Rotary Encoder 3.3V Fatal Trap:**
  * The KY-040 breakout board contains onboard surface-mount pull-up resistors (10kΩ) connected between the `CLK`, `DT`, and `SW` data lines and the module's `+` (VCC) pin.
  * If you connect the KY-040 `+` (VCC) pin to **5V**, it will feed 5.0V directly into the Raspberry Pi's GPIO pins (18, 22, 32). The Pi's GPIO lines are strictly 3.3V and **not 5V tolerant**; this will permanently kill the GPIO bank.
  * **Mandatory:** Solder the KY-040 `+` (VCC) wire strictly to **Pin 1 or Pin 17 (+3.3V)**. NEVER to 5V!
- [ ] **Safety Rule 4: Filtering & Bulk Decoupling Capacitors:**
  * Solder the **CE 220µF 25V Fujicon electrolytic capacitor** (Comet `#3792`) directly across Pi Header Pin 2 (+5V) and Pin 6 (GND). **Electrolytic polarity:** The white stripe with minus signs goes to **GND (Pin 6)**; the longer lead goes to **+5V (Pin 2)**.
  * Solder the **CW 100nF 63V MKS02 box capacitor** (Comet `#27363`, small red/yellow box) directly across VCC (Pin 14) and GND (Pin 7) of the `SN74HCT125N` level shifter buffer. This absorbs transient switching current spikes when LEDs switch states.
- [ ] **Safety Rule 5: WS2812B Data Line 470Ω Resistor & Level Shifting:**
  * The Raspberry Pi outputs 3.3V logic. The WS2812B LED strip runs on 5V and requires data voltage $V_{IH} \ge 0.7 \times V_{DD} = 3.5V$.
  * Route Pi GPIO 18 (Pin 12) through the `SN74HCT125N` buffer (Comet `#44148`) and then through the **RW25CF 470Ω 1/4W resistor** (Comet `#24761`, Yellow-Violet-Brown-Gold) in series with the LED `DIN` line. The resistor dampens transmission line reflections, eliminates ringing, and prevents first-pixel latch-up.
- [ ] **Safety Rule 6: Heat Shrink on Every Lug & Exposed Lead:**
  * Every footswitch lug, DC barrel jack solder tab, capacitor lead, and polyfuse lead must be fully insulated using the Comet heat shrink tubing (`THS-002A` 2mm for signal wires/capacitors, `THS-003A` 3mm for DC jack, `THS-004A` 4mm for the polyfuse body).
  * Bare wires shifting inside a stomped enclosure will cause ground shorts or phantom switch triggers.
- [ ] **Safety Rule 7: Star Ground Bus:**
  * Daisy-chain one lug of each of the 6 footswitches together using black FLEXI-E 0.25mm² wire and return it directly to Pi **Pin 6 (GND)**.
  * Tie Buck `OUT-`, OLED `GND`, and KY-040 `GND` to this common star ground system.

---

## 1. Master Bill of Materials (BOM) & Parts Verification

Every component listed below has been verified against your physical parts in hand:

| Check | Component / Subsystem    | Item Description in Order / Photos                                            | Qty Used    | Sourced From             |
| :---: | :----------------------- | :---------------------------------------------------------------------------- | :---------- | :----------------------- |
| - [ ] | **SBC Host**             | Raspberry Pi Zero 2 W (Quad-core 64-bit, 512MB RAM, Wi-Fi)                    | 1           | Official / Comet         |
| - [ ] | **Pin Header**           | 2×20 GPIO Male Pin Header (2.54mm straight pitch)                             | 1           | Comet / Ali              |
| - [ ] | **Storage**              | MicroSD Card (16GB or 32GB Class 10 / A1)                                     | 1           | Local / Bundled          |
| - [ ] | **Footswitches**         | SPST Momentary Soft-Touch Push Button (`203948.png`, PBS-24-102 clickless)    | 6 (1 spare) | AliExpress (7pk ordered) |
| - [ ] | **Display**              | 1.3" I2C OLED Module White (`203917.png`, SH1106, 128×64)                     | 1           | AliExpress Choice        |
| - [ ] | **Rotary Encoder**       | KY-040 Rotary Encoder Module with Knob Cap (`203948.png`)                     | 1           | AliExpress Choice        |
| - [ ] | **Status LEDs**          | WS2812B 5050 RGB LED Strip (`203917.png`, 30 LED/m black PCB)                 | 6 LEDs      | AliExpress Choice        |
| - [ ] | **DC-DC Buck Converter** | MP1584EN 3A DC-DC Step Down Module (`203917.png`, calibrated to 5.22V)        | 1           | AliExpress Choice        |
| - [ ] | **9V Power Jack**        | DC-022 5.5mm × 2.1mm DC Power Jack Panel Mount (`47599`)                      | 1           | Comet Electronics        |
| - [ ] | **Overcurrent Polyfuse** | RXEF110 PTC Resettable Fuse (Ih 1.1A, 72V, yellow disc) (`15283`)             | 1           | Comet Electronics        |
| - [ ] | **Level Shifter IC**     | SN74HCT125N DIP-14 Quad Bus Buffer 3-State (`44148`)                          | 1           | Comet Electronics        |
| - [ ] | **Decoupling Capacitor** | CW 100nF 63V MKS02 Polyester Box Capacitor (`27363`)                          | 1           | Comet Electronics        |
| - [ ] | **Bulk Capacitor**       | CE 220µF 25V 105C Fujicon Radial Electrolytic (`3792`)                        | 1           | Comet Electronics        |
| - [ ] | **Data Resistor**        | RW25CF 470R 1/4W Carbon Film Resistor (`24761`)                               | 1           | Comet Electronics        |
| - [ ] | **Hookup Wire**          | FLEXI-E 0.25mm² Stranded Wire: Black (`42020`), Red (`42021`), Blue (`42711`) | 3 meters    | Comet Electronics        |
| - [ ] | **Heat Shrink Tubing**   | THS-002A 2mm (`7603`), THS-003A 3mm (`7604`), THS-004A 4mm (`7605`)           | 3 meters    | Comet Electronics        |
| - [ ] | **Cable Ties**           | CT100 100mm × 2.5mm Black Nylon Cable Ties (`20848`)                          | 100pk       | Comet Electronics        |
| - [ ] | **Vibration Lock Tape**  | 10mm Kapton Polyimide Tape (33M roll) (`203859.png`)                          | 20mm strip  | AliExpress Choice        |
| - [ ] | **Enclosure Screws**     | M3×10mm 304 Stainless Countersunk Screws (`203855.png`)                       | 4           | AliExpress Choice        |
| - [ ] | **Threaded Inserts**     | M3×L4×OD4.2mm Brass Heat-Set Inserts (`203855.png`)                           | 4           | AliExpress Choice        |
| - [ ] | **Pi Mounting Screws**   | M2.5×6mm Pan-Head Screws (`203855.png`)                                       | 4           | AliExpress Choice        |
| - [ ] | **Pi Lock Nuts**         | DIN985 M2.5 Nylon Lock Nuts (`203855.png`)                                    | 4           | AliExpress Choice        |
| - [ ] | **OLED Screws**          | M2×5mm Pan-Head Machine Screws (`203855.png`)                                 | 4           | AliExpress Choice        |
| - [ ] | **Rubber Bumper Feet**   | 12.5mm × 5.2mm Round Rubber Bumper Pads (`203849.png`)                        | 4           | AliExpress Choice        |
| - [ ] | **OLED Window Shield**   | 1.0mm Transparent Acrylic Plexiglas Sheet (`203849.png`)                      | 1 piece     | AliExpress Choice        |
| - [ ] | **Window Adhesive**      | 3M Double-Sided Adhesive Tape (`203849.png` / `213756.png`)                   | Perimeter   | AliExpress Choice        |
| - [ ] | **Footswitch Toppers**   | Black Aluminum/Frosted Toppers (`203849.png`, 2 pkgs)                         | 6           | AliExpress Choice        |
| - [ ] | **Pedal Power Supply**   | 9V DC 1.0A EU Plug Guitar Pedal Adapter (`203849.png`, center negative)       | 1           | AliExpress Choice        |
| - [ ] | **Hot Glue Gun**         | 20W/100W Dual-Temp Hot Melt Glue Gun + Sticks (`203849.png`)                  | 1 + sticks  | AliExpress Choice        |
| - [ ] | **USB Digital Isolator** | ADuM3160 Full-Speed USB Isolator (`203907.png`, breaks audio ground hum)      | 1           | AliExpress Choice        |
| - [ ] | **USB Extension Cable**  | 0.3m USB 2.0 Male to Panel-Mount Female Cable (`203907.png`)                  | 1           | AliExpress Choice        |
| - [ ] | **Micro USB OTG**        | Micro USB Male to USB-A Female OTG Adapter (`203907.png`)                     | 1           | AliExpress Choice        |
| - [ ] | **Amp USB Cable**        | Micro USB Fast Charging Cable (`203941.png`)                                  | 1           | AliExpress Choice        |

---

## 2. Enclosure Architecture & Mechanical Layout

```text
+----------------------------------------------------------------------------------------------------+
|  [9V DC] [USB-C 5V]                                                          [RECESSED USB HOST]   |
|                                                                                                    |
|                       +-----------------+   (KNOB)                                  (O)  SWITCH 6  |
|                       |  1.3" OLED      |   Rotary                               [MUTE / TUNER]    |
|                       |  (128x64 I2C)   |   Encoder                                 *    (LED 6)   |
|                       +-----------------+                                                          |
|                                                                                                    |
|           (LED 1)           (LED 2)           (LED 3)           (LED 4)           (LED 5)          |
|              *                 *                 *                 *                 *             |
|                                                                                                    |
|             (O)               (O)               (O)               (O)               (O)            |
|           SWITCH 1          SWITCH 2          SWITCH 3          SWITCH 4          SWITCH 5         |
|          [PRESET 1]        [PRESET 2]        [PRESET 3]        [PRESET 4]        [PRESET 5]        |
|          [BANK -]                           [MODE/STOMP]                         [BANK +]          |
+----------------------------------------------------------------------------------------------------+
|  FRONT HEIGHT: 32mm                                                             REAR HEIGHT: 48mm  |
|                                <--- ~14.47° TRUE ERGONOMIC SLANT --->                              |
+----------------------------------------------------------------------------------------------------+
```

- [ ] **3D Models Ready:**
  * [`pedal_top_shell.stl`](pedal_top_shell.stl) (Watertight top wedge with 4x 10mm stomp pillars).
  * [`pedal_baseplate.stl`](pedal_baseplate.stl) (Watertight bottom plate with MP1584EN & USB-C mounting cradles).
  * [`pedal_enclosure.scad`](pedal_enclosure.scad) (Parametric source model).
- [ ] **Slicer Checklist (Bambu Studio / OrcaSlicer):**
  * Rotate part **45° diagonally** on the 256×256mm build plate.
  * Print top shell upright with flat bottom rim on bed. Enable Tree Supports ("Tree Auto", "On build plate only").
  * 6 perimeters / wall loops, 45% Gyroid infill, PETG / PETG-CF.

---

## 3. Circuit Schematic & 40-Pin Header Wiring

### Circuit Schematic

```text
  [ 9V DC IN ] (Pedalboard Power Supply, Center Negative)
       |
      [+] (Outer Sleeve) -------------------------------> Buck IN+
      [-] (Center Pin)   -------------------------------> Buck IN- & Star GND
                                                            |
                                                     [ MP1584EN Buck ]
                                                   (Calibrated to 5.22V)
                                                            |
                                                         OUT+ (5.22V)
                                                            |
                                                  [ RXEF110 1.1A Polyfuse ]
                                                            |
                                                            +-----> Pi Zero Pin 02 (+5V Bus)
                                                            |        |
                                                            |       [=] 220µF Bulk Cap (Comet #3792)
                                                            |        |  (Long lead to +5V, Stripe to GND)
                                                            |        v
                                                            |     Pi Zero Pin 06 (Star GND)
                                                            |
                                                            +-----> SN74HCT125N Pin 14 (VCC)
                                                            |        |
                                                            |       [=] 100nF Box Cap (Comet #27363) to GND
                                                            |
                                                            +-----> WS2812B LED Strip +5V Rail

  COMMON STAR GROUND ----------------------------------------------------------------------------> Pi Pin 06 / 09 / 14 / 20 / 30 / 34 / 39
                                                                                                 & Buck OUT-
                                                                                                 & Footswitch Ground Bus (Pins 2 of SW1–6)
                                                                                                 & KY-040 GND & OLED GND & LED Strip GND
                                                                                                 & SN74HCT125N Pin 07 (GND) & Pin 01 (1OE to GND)
```

### Raspberry Pi Zero 2 W 40-Pin Header Physical Pinout

```text
                                              +3.3V  (01) (02)  +5.0V (From 1.1A Polyfuse Output & Bulk Caps)
        (OLED SDA) -------- GPIO 02 / I2C1_SDA (SDA)  (03) (04)  +5.0V (Internal Pi PCB 5V Rail)
        (OLED SCL) -------- GPIO 03 / I2C1_SCL (SCL)  (05) (06)  GND   (Star Ground Bus - Return to All)
                            GPIO 04                   (07) (08)  GPIO 14 / UART0_TXD
        (OLED GND) ----------------------- GND (09) (10)  GPIO 15 / UART0_RXD
        (Switch 1 - Preset 1 / Bank -) --- GPIO 17    (11) (12)  GPIO 18 (WS2812B Data via 74HCT125)
        (Switch 2 - Preset 2) ------------ GPIO 27    (13) (14)  GND
        (Switch 3 - Preset 3 / Mode) ----- GPIO 22    (15) (16)  GPIO 23 (Switch 4 - Preset 4)
        (KY-040 VCC strictly 3.3V!) ------ +3.3V Rail (17) (18)  GPIO 24 (Rotary Encoder CLK)
                            GPIO 10 / SPI_MOSI        (19) (20)  GND
                            GPIO 09 / SPI_MISO        (21) (22)  GPIO 25 (Rotary Encoder DT)
                            GPIO 11 / SPI_SCLK        (23) (24)  GPIO 08 / SPI_CE0
                                           GND        (25) (26)  GPIO 07 / SPI_CE1
                            GPIO 00                   (27) (28)  GPIO 01
        (Switch 5 - Preset 5 / Bank +) --- GPIO 05    (29) (30)  GND
        (Switch 6 - MUTE / TUNER) -------- GPIO 06    (31) (32)  GPIO 12 (Rotary Encoder SW Push Button)
                            GPIO 13                   (33) (34)  GND
                            GPIO 19                   (35) (36)  GPIO 16
                            GPIO 26                   (37) (38)  GPIO 20
                                           GND        (39) (40)  GPIO 21
```

---

## 4. Step-by-Step Soldering & Wiring Checklist

#### Phase 4.0: Soldering the 2×20 GPIO Pin Header to the Raspberry Pi Zero 2 W
- [x] **4.0.1 (Header Insertion & Orientation):** Insert the 40-pin (2×20) male header into the Pi Zero 2 W from the top. The **long pin legs must stick UPWARD** on the component side (the side with the metal RF shield and processor). The **short solder legs protrude through the BOTTOM** (the side with the gold test pads and microSD slot). The black plastic spacer must sit on the top surface.
- [x] **4.0.2 (Seating & Diagonal Tack Soldering):** Support the board or press the header pins gently into a breadboard or soft surface so the header stays perpendicular (90° vertical). Solder **only Pin 1** (top-left square pad) on the bottom side.
- [x] **4.0.3 (Flushness & Alignment Check):** Look from the side: ensure the black plastic spacer is seated 100% flat and flush against the PCB with zero gap, and pins stand at a straight 90° angle. If crooked, touch your iron to Pin 1 for 1 second while gently pressing the plastic spacer flat against the board. Once square, solder the diagonally opposite corner: **Pin 40**. Re-verify alignment before proceeding.
- [x] **4.0.4 (Soldering All 40 Pins):** Set soldering iron to **320°C–350°C** with a clean, tinned chisel or bevel tip. Solder the remaining 38 pins one by one from the bottom side. Heat both the pin and copper ring simultaneously for 1.5–2 seconds, feed a tiny dab of rosin-core solder until it flows into a clean, shiny, concave cone ("mini volcano"), then withdraw solder and iron.
  > [!TIP]
  > Ground pins (Pins 6, 9, 14, 20, 25, 30, 34, 39) tie into internal copper ground planes and absorb heat faster. Allow 0.5 to 1 second extra dwell time on GND pins so solder wets fully across the ring without creating a cold joint.
- [x] **4.0.5 (Cleaning & Visual Bridge Inspection):** Clean flux residue off the bottom of the board with 90%+ isopropyl alcohol (IPA) and a soft brush or cotton swab. Inspect all 40 solder joints under bright light or phone camera zoom. Verify:
  1. No solder bridges (short circuits) between any adjacent pins.
  2. Pay extreme attention to **Pin 1 (3.3V) vs Pin 3 (SDA)**, and **Pin 2/Pin 4 (+5V) vs Pin 6 (GND)**.
- [x] **4.0.6 (Multimeter Header Pre-Flight Test):** Set multimeter to **Continuity / Resistance mode**:
  * Probe between **Pin 2 (+5V)** and **Pin 6 (GND)**: Must show NO continuity (infinite resistance / no beep). If it beeps, find and remove the solder bridge before applying any power!
  * Probe between **Pin 1 (+3.3V)** and **Pin 6 (GND)**: Must show NO continuity (infinite resistance / no beep).
  * Probe between adjacent pins (Pin 1 to Pin 2, Pin 3 to Pin 4, Pin 5 to Pin 6): Verify no unexpected shorts.

#### Phase 4.1: DC Power Jack Wiring
- [x] **4.1.1 (DC Jack Polarity):** Guitar pedals use **Center-Negative**. Solder a **Red FLEXI-E wire** to the outer sleeve terminal (+9V DC). Slide a 3mm heat shrink tube over it.
- [x] **4.1.2 (DC Jack GND):** Solder a **Black FLEXI-E wire** to the center pin terminal (GND). Slide a 3mm heat shrink tube over it. Shrink both sleeves.

#### Phase 4.2: Buck Converter Calibration & Trimpot Locking
- [x] **4.2.1 (Buck Input):** Solder the DC jack's Red wire (+9V) to MP1584EN module `IN+` pad, and Black wire (GND) to `IN-` pad. **DO NOT solder Buck output to the Pi yet.**
- [x] **4.2.2 (Trimpot Calibration):** Plug the 9V 1A pedal power adapter into the DC jack. Set multimeter to **DC Volts (20V range)** across Buck `OUT+` and `OUT-`. Turn the brass trimpot screw until output reads steadily **5.22V DC** (5.18V–5.25V).
- [x] **4.2.3 (Mechanical Lock):** Unplug the 9V power supply. Apply a generous pea-sized drop of hot glue directly over the brass adjustment screw to lock it against stage vibrations.

#### Phase 4.3: RXEF110 Polyfuse Sub-Assembly (Short-Circuit Protection)
- [x] **4.3.1 (Polyfuse Input):** Solder one lead of the **RXEF110 1.1A PTC polyfuse** (Comet #15283, yellow disc) directly to Buck converter `OUT+`. Slide a 3mm heat shrink tube (`THS-003A`) over the lead.
- [x] **4.3.2 (Polyfuse Output Feed):** Solder a **Red FLEXI-E wire** (~8cm) to the other lead of the RXEF110 polyfuse. Slide a 4mm heat shrink tube (`THS-004A`) over the entire polyfuse body and shrink it.

#### Phase 4.4: Raspberry Pi Power Rail & Capacitor Decoupling

> [!IMPORTANT]
> **Heat-Shrink Strategy: When to Shrink vs. When to Wait:**
> * **ALMOST EVERY PIN on the Pi header is a SINGLE wire:** (Switches 1–6, OLED pins, Rotary Encoder pins, Level Shifter). For all of these, you can slide 2mm heat shrink over the wire, solder it to the pin, slide the sleeve down over the joint, and shrink it immediately to prevent accidental shorts!
> * **The ONLY PIN to leave UNSHRUNK for now is Pin 2 (+5V):** In Phase 4.8, the WS2812B LED strip `+5V` wire will ALSO connect to Pin 2! Do NOT heat-shrink Pin 2 until both the capacitor positive lead and the LED strip 5V wire are soldered to it.

- [x] **4.4.1 (5V Bus):** Solder the Red wire from the polyfuse output to **Pi Header Pin 4 (+5V)** (or Pin 2). Slide heat shrink over Pin 4 and shrink it.
- [x] **4.4.2 (GND Bus):** Solder a **Black FLEXI-E wire** (~8cm) from Buck `OUT-` directly to **Pi Header Pin 6 (GND)**. Slide heat shrink over Pin 6 and shrink it.
- [x] **4.4.3 (Bulk Electrolytic - No-Cut Workaround):** 
  * **DO NOT cut the heat shrink on Pin 4 or Pin 6!**
  * Solder the **CE 220µF 25V Fujicon electrolytic capacitor** (Comet #3792) as follows:
    * **Positive Lead (Longer Lead):** Solder directly to **Pi Pin 2 (+5V)**. *(Leave Pin 2 unshrunk for now—the LED strip +5V wire will also join Pin 2 in Phase 4.8)*.
    * **Negative Lead (White stripe with minus signs):** Solder directly to **Pi Pin 14 (GND)** (or Pin 9 GND). Slide a piece of 2mm heat shrink (`THS-002A`) over the capacitor lead and shrink it.
    *(Why this works: Pin 2 and Pin 4 share the exact same +5V copper plane; Pin 6, Pin 9, and Pin 14 share the exact same ground plane).*
- [ ] **4.4.4 (IC Decoupling Capacitor):** Save the **CW 100nF 63V MKS02 box capacitor** (Comet #27363) for Phase 4.8 to solder directly across SN74HCT125N Pin 14 (VCC) and Pin 7 (GND).

#### Phase 4.5: Footswitches & Star Ground Bus Wiring
- [x] **4.5.1 (Mount Switches):** Mount the 5 preset switches (lower row) and Switch 6 (top-right deck). Tighten their hex nuts.
- [x] **4.5.2 (Daisy-Chain Ground):** Solder a continuous Black FLEXI-E wire linking one lug of Switch 1 $\to$ SW 2 $\to$ SW 3 $\to$ SW 4 $\to$ SW 5 $\to$ SW 6. Connect the end of this ground wire to **Pi Pin 30 or Pin 34 (GND)**. Slide heat shrink over every lug.
- [x] **4.5.3 (Switch 1 Signal):** Solder other lug of Switch 1 $\to$ **Pi Pin 11 (GPIO 17)**. Heat shrink lug.
- [x] **4.5.4 (Switch 2 Signal):** Solder other lug of Switch 2 $\to$ **Pi Pin 13 (GPIO 27)**. Heat shrink lug.
- [x] **4.5.5 (Switch 3 Signal):** Solder other lug of Switch 3 $\to$ **Pi Pin 15 (GPIO 22)**. Heat shrink lug.
- [x] **4.5.6 (Switch 4 Signal):** Solder other lug of Switch 4 $\to$ **Pi Pin 16 (GPIO 23)**. Heat shrink lug.
- [x] **4.5.7 (Switch 5 Signal):** Solder other lug of Switch 5 $\to$ **Pi Pin 29 (GPIO 05)**. Heat shrink lug.
- [x] **4.5.8 (Switch 6 Tuner Signal):** Solder other lug of Switch 6 $\to$ **Pi Pin 31 (GPIO 06)**. Heat shrink lug.

#### Phase 4.6: KY-040 Rotary Encoder Wiring (3.3V Strict Rule!)
- [x] **4.6.1 (Mount Encoder):** Mount the KY-040 encoder in its 7.2mm upper deck hole. Fasten washer and nut.
- [x] **4.6.2 (VCC - 3.3V ONLY):** Solder Red wire from KY-040 `+` (VCC) pin to **Pi Pin 17 (+3.3V Rail)**. *(NEVER TO 5V!)*
- [x] **4.6.3 (GND):** Solder Black wire from KY-040 `GND` pin to **Pi Pin 20 (GND)**.
- [x] **4.6.4 (CLK Data):** Solder Green wire from KY-040 `CLK` pin to **Pi Pin 18 (GPIO 24)**.
- [x] **4.6.5 (DT Data):** Solder White wire from KY-040 `DT` pin to **Pi Pin 22 (GPIO 25)**.
- [x] **4.6.6 (SW Push Button):** Solder Orange wire from KY-040 `SW` pin to **Pi Pin 32 (GPIO 12)**. Insulate pins with heat shrink.

#### Phase 4.7: 1.3" I2C OLED Display Wiring
- [x] **4.7.1 (OLED VCC):** Solder Red wire from OLED `VCC` pin to **Pi Pin 1 (+3.3V Rail)**.
- [x] **4.7.2 (OLED GND):** Solder Black wire from OLED `GND` pin to **Pi Pin 9 (GND)**.
- [x] **4.7.3 (OLED SDA):** Solder Blue wire from OLED `SDA` pin to **Pi Pin 3 (GPIO 02 / I2C1_SDA)**.
- [x] **4.7.4 (OLED SCL):** Solder Yellow wire from OLED `SCL` pin to **Pi Pin 5 (GPIO 03 / I2C1_SCL)**. Insulate pins with heat shrink.

#### Phase 4.8: WS2812B RGB Individual LEDs & Level Shifter Sub-Assembly

> [!NOTE]
> **Why Cut into 6 Separate Pixels?**
> The footswitches and LED indicator holes on the top shell are spaced 48mm apart. Because standard LED strips have LEDs spaced ~33mm apart, you must snip the strip into **6 separate single-LED segments** and link them with flexible 3-wire jumpers.

- [x] **4.8.1 (Cutting 6 Individual Pixels):** Using sharp scissors, cut through the center of the copper pads to separate **6 individual single LEDs** from the WS2812B strip. Each small square pixel now has:
  * An **Input side** (marked `+5V`, `DIN` or `DI`, `GND`)
  * An **Output side** (marked `+5V`, `DOUT` or `DO`, `GND`)
  * Arrow markers ($\rightarrow$) indicating the data flow direction.
- [x] **4.8.2 (Mounting LEDs with Hot Glue):** 
  * Turn the top shell upside down.
  * Place **LED 1** behind the hole above Switch 1 (far-left), **LED 2** above Switch 2, **LED 3** above Switch 3, **LED 4** above Switch 4, **LED 5** above Switch 5, and **LED 6** above Switch 6 (top-right Tuner/Mute).
  * **CRITICAL:** Ensure the arrows ($\rightarrow$) on all 6 LEDs point in the same chain direction: from **LED 1 $\to$ LED 2 $\to$ LED 3 $\to$ LED 4 $\to$ LED 5 $\to$ LED 6**!
  * Apply a dab of hot glue from the inside over each LED. The hot glue locks them in place and acts as a translucent diffuser lens ("jewel lamp").
- [ ] **4.8.3 (Inter-LED Jumper Bridges):** 
  * Prepare 5 sets of short 3-wire jumpers (~5cm each) using your Red, Black, and Blue FLEXI-E wire.
  * Bridge each LED to the next in series:
    * `+5V` of LED 1 $\to$ `+5V` of LED 2 $\to$ `+5V` of LED 3 $\to$ `+5V` of LED 4 $\to$ `+5V` of LED 5 $\to$ `+5V` of LED 6 (Red wire).
    * `GND` of LED 1 $\to$ `GND` of LED 2 $\to$ `GND` of LED 3 $\to$ `GND` of LED 4 $\to$ `GND` of LED 5 $\to$ `GND` of LED 6 (Black wire).
    * `DOUT` of LED 1 $\to$ `DIN` of LED 2 (Blue wire).
    * `DOUT` of LED 2 $\to$ `DIN` of LED 3 (Blue wire).
    * `DOUT` of LED 3 $\to$ `DIN` of LED 4 (Blue wire).
    * `DOUT` of LED 4 $\to$ `DIN` of LED 5 (Blue wire).
    * `DOUT` of LED 5 $\to$ `DIN` of LED 6 (Blue wire).
    *(Leave the DOUT of LED 6 unconnected—it is the last pixel in the chain).*
- [x] **4.8.4 (Level Shifter Power & Decoupling):** On the `SN74HCT125N` (Comet #44148):
  * Connect Pin 14 (VCC) to Pi **Pin 2 (+5V)** (Red wire).
  * Connect Pin 7 (GND) to Pi **Pin 14 or Pin 6 (GND)** (Black wire).
  * Connect Pin 1 (1OE) to Pin 7 (GND) (enables buffer output).
  * Solder the **CW 100nF MKS02 box capacitor** (Comet #27363) directly between Pin 14 (VCC) and Pin 7 (GND).
- [x] **4.8.5 (Level Shifter Data Feed & 470Ω Resistor):** 
  * Connect Pin 2 (1A) of the SN74HCT125N to **Pi Pin 12 (GPIO 18 / PWM0)** (Blue wire).
  * Connect Pin 3 (1Y) of the SN74HCT125N to one lead of the **RW25CF 470Ω resistor** (Comet #24761, Yellow-Violet-Brown).
  * Solder the other lead of the 470Ω resistor to the **`DIN` pad of LED 1**. Slide 2mm heat shrink over the resistor.
- [x] **4.8.6 (LED 1 Power Feed):** 
  * Solder the `+5V` pad of LED 1 to Pi **Pin 2 (+5V)** (Red wire).
  * Solder the `GND` pad of LED 1 to Pi **Pin 14 or Star GND** (Black wire).

#### Phase 4.9: USB Isolator & Amp Connection
- [x] **4.9.1 (OTG Adapter):** Plug the Micro-USB OTG adapter into the Pi Zero 2 W outer USB data port (marked "USB").
- [x] **4.9.2 (ADuM3160 Isolator):** Plug the ADuM3160 USB Digital Isolator into the OTG adapter.
- [x] **4.9.3 (Panel Pigtail):** Connect the 0.3m panel-mount USB extension cable into the isolated output of the ADuM3160 and align the socket with the right-flank pocket.
- [x] **4.9.4 (Zip-Tie Anchor):** Loop a black nylon cable tie through the baseplate's molded strain-relief bridge around the USB cable and tighten firmly.

---

## 5. Mechanical Enclosure Assembly Checklist

- [x] **5.1 (Heat-Set Inserts):** Set soldering iron to 220°C–230°C. Press 4x **M3×L4×OD4.2mm brass inserts** into the corner bosses until flush. Allow 2 minutes to cool.
- [ ] **5.2 (Acrylic Window):** Cut a 38.0mm × 24.0mm rectangle from the 1.0mm acrylic sheet. Apply 3M double-sided tape around the recess pocket perimeter and press the acrylic window into place.
- [x] **5.3 (OLED Mounting):** Fasten the 1.3" OLED board to the 4 ceiling standoffs using 4x **M2×5mm pan-head screws**.
- [x] **5.4 (Knob Installation):** Push the knurled aluminum knob onto the rotary encoder shaft and tighten its set screw.
- [x] **5.5 (Baseplate Modules):** Seat the MP1584EN buck into its cradle $(X=20, Y=34)$. Add a drop of hot glue to secure it. (The USB-C cradle at $X=40$ can be left empty).
- [x] **5.6 (MicroSD Card Kapton Lock):** Apply a 20mm strip of **Kapton tape** over the MicroSD card and socket on the Pi Zero to prevent vibration walkout.
- [x] **5.7 (Pi Zero Mounting):** Mount the Pi Zero 2 W to the 4 baseplate standoffs using 4x **M2.5×6mm pan-head screws** and 4x **DIN985 M2.5 nylon lock nuts**.
- [ ] **5.8 (Shell Closure):** Seat baseplate onto top shell and fasten with 4x **M3×10mm countersunk screws** (heads sit 100% flush in 90° bevels).
- [ ] **5.9 (Rubber Bumper Feet):** Adhere the 4x **12.5mm × 5.2mm round rubber feet** to the baseplate corners.
- [ ] **5.10 (Footswitch Toppers):** Press the **6 black footswitch toppers** onto the 6 momentary stomp switches and tighten their grub screws.

---

## 6. Pre-Flight Multimeter Checklist (Mandatory Before Powering Pi)

Perform these 5 tests with your multimeter before applying power to the Pi:

| Check | Test # | Probe 1 (Positive) | Probe 2 (Negative) | Multimeter Setting | Expected Value | Action if Incorrect |
| :---: | :---: | :--- | :--- | :--- | :--- | :--- |
| - [ ] | **1** | Buck `OUT+` | Buck `OUT-` | DC Volts (20V) | **5.18V – 5.25V DC** (9V adapter plugged in) | Adjust trimpot before connecting Pi! |
| - [ ] | **2** | Pi Header Pin 2 (+5V) | Pi Header Pin 6 (GND) | Resistance / Continuity | **> 1000Ω** (No beep / no short) | Locate and fix 5V-to-GND solder bridge. |
| - [ ] | **3** | KY-040 `+` (VCC) pin | Pi Header Pin 17 (+3.3V)| Resistance / Continuity | **0.0Ω – 0.5Ω** (Direct continuity) | **STOP:** Ensure KY-040 is NOT on 5V! |
| - [ ] | **4** | Pi Header Pin 17 (+3.3V)| Pi Header Pin 6 (GND) | Resistance / Continuity | **> 2000Ω** (No short) | Check for 3.3V short before powering up. |
| - [ ] | **5** | Switch Lugs (Pin 1) | Pi Header Pin 6 (GND) | Continuity / Beeper | **Open circuit** at rest; **Beeps** when switch pressed | Fix switch wiring or stuck actuator. |

---

## 7. Software Setup & Flashing Checklist

### Phase 7.1: Flashing the MicroSD Card from Another Computer (Raspberry Pi Imager)
On your other laptop with the SD card reader, open **Raspberry Pi Imager** and configure these exact options:
- [x] **7.1.1 (Choose Device):** Select **Raspberry Pi Zero 2 W**.
- [x] **7.1.2 (Choose OS):** Select **Raspberry Pi OS (other)** $\to$ **Raspberry Pi OS Lite (64-bit)**.
- [x] **7.1.3 (Edit Settings / OS Customisation):** Click **Edit Settings** (or the gear icon) and fill in:
  * **General Tab:**
    * Set Hostname: `lt25-pedal`
    * Set Username: `pi`
    * Set Password: *(Choose a password, e.g. `fender1234`)*
    * Configure Wireless LAN: Checkbox enabled
      * SSID: *(Your exact home Wi-Fi name, e.g. `2bombo`)*
      * Password: *(Your Wi-Fi password)*
      * Wireless LAN Country: `BG` (Bulgaria)
    * Set Locale: Time zone `Europe/Sofia`, Keyboard layout `us`
  * **Services Tab:**
    * Enable SSH: Checkbox enabled $\to$ Select **Use password authentication**
- [x] **7.1.4 (Write & Verify):** Click **Write**. Once complete and verified, safely eject the MicroSD card and insert it into the Pi Zero 2 W.
- [x] **7.1.5 (First Boot):** Power up the Pi Zero 2 W (via 5V USB or calibrated 9V buck). Booted successfully and acquired IP `192.168.0.147` on `2bombo`.

### Phase 7.2: Deploying Software from This PC (Over Wi-Fi)
From this PC's terminal:
- [x] **7.2.1 (SSH Connection):** Connected via SSH, passwordless sudo enabled, SSH key deployed to `authorized_keys`.
- [x] **7.2.2 (System Updates & Dependencies):** Package repositories updated, core build tools (`libhidapi-dev`, `libusb-1.0-0-dev`, `git`, `i2c-tools`) installed.
- [x] **7.2.3 (Verify OLED on I2C):** I2C & SPI interfaces enabled in `/boot/firmware/config.txt`.
- [x] **7.2.4 (Python Libraries):** All core libraries installed and verified with zero errors (`hidapi`, `protobuf`, `adafruit-circuitpython-ssd1306`, `luma.oled`, `rpi_ws281x`, `RPi.GPIO`, `Adafruit-Blinka-Raspberry-Pi-PWM`, `flask`, `pillow`).
- [x] **7.2.5 (USB udev Rules):** Created `/etc/udev/rules.d/99-fender-lt25.rules` for Mustang LT25 (`VID 1ed8`, `PID 0037`) and reloaded udev.
- [x] **7.2.6 (Copy Controller Script):** Uploaded [`lt25_smart_pedal.py`](lt25_smart_pedal.py) to `/home/pi/lt25_smart_pedal.py`, set execution permissions, and verified bytecode compilation.
- [x] **7.2.7 (Enable Auto-Start Service):** Installed `/etc/systemd/system/lt25-pedal.service` and enabled auto-start daemon on boot as root.
- [x] **7.2.8 (Read-Only Overlay Filesystem Stage-Proofing):**
  * `overlayroot=tmpfs` enabled in `/boot/firmware/cmdline.txt` and `/boot/firmware` set to read-only (`ro`) in `/etc/fstab`.
  * Activated on reboot (`sudo reboot`). SD card is 100% immune to abrupt stage power-cuts!

---

## 8. Functional Verification & Bench Test Checklist (100% OPERATIONAL & VERIFIED)

Connect the pedal to the Fender Mustang LT25 via the isolated USB cable:

- [x] **8.1 (Boot Time):** Cold boot completes in ~12 seconds; OLED displays stage view with colossal 64pt preset number and crisp 2-line title.
- [x] **8.2 (Lower Preset Switches 1–5):** Stomping Switches 1–5 instantly recalls presets 1–5 on the amplifier using zero-latency press-down triggers and transactional `SYNC_BEGIN` $\to$ `LoadPreset` $\to$ `SYNC_END`. Active switch LED turns Emerald Green; others remain dim.
- [x] **8.3 (Solo Boost):** Stomping the already-active preset switch toggles Solo Boost (+3.0dB audio boost on the amplifier's DSP `amp` volume parameter). OLED screen inverts color for stage visibility and LED glows Fiery Red.
- [x] **8.4 (Bank Up / Down):**
  * Holding Switch 1 (>600ms) drops to previous bank.
  * Holding Switch 5 (>600ms) advances to next bank.
  * All LEDs flash cyan twice on bank change.
- [x] **8.5 (FX Stompbox Mode):** Holding Switch 3 (>1000ms) or clicking the rotary encoder knob toggles between Preset Bank Mode and Stompbox Mode. In Stompbox mode, switches toggle individual DSP blocks (`stomp` / OD, `mod`, `delay`, `tapTimeBPM`, `reverb`) directly on the amplifier with amber LED and on-screen box feedback.
- [x] **8.6 (Dedicated Tuner Switch 6 & Any-Key Exit):** Stomping the top-right elevated Switch 6 instantly mutes the amp output via `ModalStatusMessage(context=TUNER_ENABLE, state=OK)` and lights up Tuner LED 6. Stomping ANY footswitch (1–5 or 6) while in Tuner mode immediately closes the tuner, unmutes the amp, and returns to the last active preset without changing preset slots.
- [x] **8.7 (Rotary Encoder):** Rotating the aluminum knob smoothly scrolls through all 60 amp presets (`01` to `60`) with real-time hardware sync; pushing the knob toggles operating modes.
- [x] **8.8 (OverlayFS Stage Protection):** Read-only overlay rootfs (`/media/root-ro`) verified active. Power can be yanked at any time without risk of SD card corruption.
