# Fender Mustang LT25 Smart Footswitch: Hardware Engineering Manual & Schematics

This document provides the complete hardware engineering reference for the **Fender Mustang LT25 6-Button Smart Footswitch Controller**. It encompasses circuit schematics, pinout assignments, power supply design, logic level shifting, mechanical ergonomics, and current budget analyses.

---

## 1. System Architecture & Block Diagram

The controller is hosted by a **Raspberry Pi Zero 2 W** single-board computer acting as an intelligent USB HID host connected to the Fender Mustang LT25 micro-USB port. It interfaces with an onboard 1.3-inch OLED display, 6 addressable WS2812B RGB status LEDs, a mechanical quadrature rotary encoder, and 6 rugged stage footswitches.

### 1.1 Mermaid System Architecture

```mermaid
flowchart TD
    subgraph PowerSubsystem["Power Supply & Protection Subsystem"]
        DC_IN["9V DC Pedalboard Supply<br/>(2.1mm x 5.5mm Center-Negative)"]
        D_SCHOTTKY["1N5822 Schottky Diode<br/>(Reverse Polarity Protection)"]
        BUCK["MP1584EN Step-Down Converter<br/>(9V DC &rarr; 5.20V DC)"]
        FUSE["RXEF110 1.1A PTC Polyfuse<br/>(Overcurrent Protection)"]
        C_BULK["220&mu;F 25V Electrolytic Cap<br/>(Transient Smoothing)"]
        
        DC_IN --> D_SCHOTTKY
        D_SCHOTTKY --> BUCK
        BUCK --> FUSE
        FUSE --> C_BULK
    end

    subgraph HostSBC["Host Single-Board Computer"]
        PI["Raspberry Pi Zero 2 W<br/>(Broadcom BCM2710A1 64-bit Quad-Core)"]
        GPIO["40-Pin GPIO Header"]
        USB_OTG["USB OTG Port (Host Mode)"]
        PI --- GPIO
        PI --- USB_OTG
    end

    subgraph LevelShifter["Logic Level Shifting Subsystem"]
        LS["SN74HCT125N / 74AHCT125<br/>High-Speed CMOS Quad Buffer"]
        C_DEC["100nF Box Bypass Cap"]
        R_SERIES["470&Omega; 1/4W Resistor<br/>(Ringing Suppression)"]
        LS --- C_DEC
        LS --> R_SERIES
    end

    subgraph UserInterface["Stage Control & Visual UI"]
        SW_LOWER["5x Lower Footswitches<br/>(Presets 1-5 / Bank & Mode Nav)"]
        SW_TUNER["1x Upper-Deck Footswitch<br/>(Switch 6: Dedicated Mute/Tuner)"]
        ENCODER["KY-040 Rotary Encoder<br/>(CLK, DT, SW - Strictly 3.3V VCC)"]
        OLED["1.3\" I2C OLED Display<br/>(SH1106 / SSD1306 128x64)"]
        LEDS["6x WS2812B RGB NeoPixels<br/>(Individually Addressable)"]
    end

    subgraph AmpInterface["Amp Isolation & Link"]
        ISOLATOR["ADuM3160 Full-Speed USB Isolator<br/>(Ground-Loop Hum Eliminator)"]
        AMP["Fender Mustang LT25<br/>(USB HID Interrupt Endpoint)"]
    end

    C_BULK -->|5.2V Rail| GPIO
    FUSE -->|5.2V VCC| LS
    FUSE -->|5.2V VDD| LEDS
    
    GPIO -->|3.3V Logic PWM0 / GPIO 18| LS
    R_SERIES -->|5.0V DIN| LEDS
    
    GPIO -->|I2C1: SDA/SCL, 3.3V| OLED
    GPIO -->|Quadrature: GPIO 24/25/12| ENCODER
    GPIO -->|Active-Low GPIO 17,27,22,23,05| SW_LOWER
    GPIO -->|Active-Low GPIO 06| SW_TUNER
    
    USB_OTG --> ISOLATOR
    ISOLATOR --> AMP
```

### 1.2 ASCII Hardware Wiring Block Diagram

```text
  +---------------------------------------------------------------------------------------+
  |                                POWER DISTRIBUTION BUS                                 |
  +---------------------------------------------------------------------------------------+
    [9V DC Pedal Supply] (Center-Negative 2.1mm/5.5mm)
           |
          [+] Outer Sleeve ----------------+
          [-] Center Pin ---+              |
                            |              v
                            |     [ 1N5822 Schottky Diode ] (3A 40V, Low Vf ~0.28V)
                            |              |
                            |              v
                            |       MP1584EN BUCK IN+
                            +-----> MP1584EN BUCK IN- & COMMON STAR GROUND
                                           |
                                   [ MP1584EN BUCK ]
                              (Calibrated precisely to 5.20V DC)
                                           |
                                        OUT+ (5.20V)
                                           |
                                  [ RXEF110 1.1A Polyfuse ]
                                           |
    +--------------------------------------+---------------------------------------+
    |                                      |                                       |
    v                                      v                                       v
  Pi Zero 2 W Pin 02 (+5V)          74AHCT125 Pin 14 (VCC)                  WS2812B LED 1 (+5V)
    |                                      |                                       |
   [=] 220uF Electrolytic Cap             [=] 100nF Bypass Cap                     +---> LED 2..6
    |                                      |                                       |
    v                                      v                                       v
  Pi Zero 2 W Pin 06 (GND)          74AHCT125 Pin 07 (GND)                  WS2812B Ground Bus
    |                                      |                                       |
  ==+======================================+=======================================+==
                                COMMON STAR GROUND BUS

  +---------------------------------------------------------------------------------------+
  |                             SIGNAL & LOGIC CONNECTIONS                                |
  +---------------------------------------------------------------------------------------+
  Pi Zero 2 W (3.3V)                                  Peripherals
  ------------------                                  -----------
  Pin 01 (+3.3V) -----------------------------------> OLED Pin 1 (VCC)
  Pin 17 (+3.3V) -----------------------------------> KY-040 Pin 3 (VCC) [NEVER 5V!]
  Pin 03 (GPIO 02 / I2C1_SDA) ----------------------> OLED Pin 3 (SDA)
  Pin 05 (GPIO 03 / I2C1_SCL) ----------------------> OLED Pin 4 (SCL)
  Pin 12 (GPIO 18 / PWM0) ----> 74AHCT125 (1A)
                                74AHCT125 (1Y) ----> [ 470R Resistor ] ---> WS2812B DIN (LED 1)
  Pin 18 (GPIO 24) <--------------------------------- KY-040 (CLK / Channel A)
  Pin 22 (GPIO 25) <--------------------------------- KY-040 (DT  / Channel B)
  Pin 32 (GPIO 12) <--------------------------------- KY-040 (SW  / Push Button)
  Pin 11 (GPIO 17) <--------------------------------- Switch 1 (Preset 1 / Bank Down)
  Pin 13 (GPIO 27) <--------------------------------- Switch 2 (Preset 2)
  Pin 15 (GPIO 22) <--------------------------------- Switch 3 (Preset 3 / Mode Toggle)
  Pin 16 (GPIO 23) <--------------------------------- Switch 4 (Preset 4 / Tap Tempo)
  Pin 29 (GPIO 05) <--------------------------------- Switch 5 (Preset 5 / Bank Up)
  Pin 31 (GPIO 06) <--------------------------------- Switch 6 (Upper Deck Mute/Tuner)

  Pi USB OTG Port --------> ADuM3160 USB Isolator ---> Panel USB-A ---> Fender Mustang LT25
```

---

## 2. Complete 40-Pin GPIO Mapping Specification

The Raspberry Pi Zero 2 W utilizes a 40-pin GPIO expansion header. Every pin used in this design, its internal pull resistor status, signal direction, and hardware peripheral mapping is defined below:

| Physical Pin # | BCM GPIO | Signal / Function Name | Direction | Pull Resistor State | Connected Peripheral | Default State | Description |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **01** | — | **+3.3V DC** | Power Out | — | 1.3" OLED VCC | Active High | Quiet analog-filtered 3.3V rail from Pi PMIC |
| **02** | — | **+5.0V DC** | Power In | — | Main 5V Bus / Polyfuse Out | +5.20V DC | Primary power input feeding Pi regulator & USB |
| **03** | GPIO 02 | **I2C1_SDA** | Bi-dir | Internal 1.8kΩ Pull-Up | OLED SDA (Data) | High (Idle) | I2C Bus 1 Data line (3.3V logic) |
| **04** | — | **+5.0V DC** | Power In | — | Common 5V Plane | +5.20V DC | Tied internally on Pi PCB to Pin 02 |
| **05** | GPIO 03 | **I2C1_SCL** | Output | Internal 1.8kΩ Pull-Up | OLED SCL (Clock) | High (Idle) | I2C Bus 1 Clock line (400 kHz fast mode) |
| **06** | — | **GND** | Ground | — | Star Ground Bus | 0.0V | Primary system chassis return point |
| **07** | GPIO 04 | — | Unused | — | Unconnected | High-Z | Reserved |
| **08** | GPIO 14 | UART0_TXD | Unused | — | Unconnected | High-Z | Reserved (Serial console disabled) |
| **09** | — | **GND** | Ground | — | OLED Display GND | 0.0V | Dedicated clean digital ground for OLED |
| **10** | GPIO 15 | UART0_RXD | Unused | — | Unconnected | High-Z | Reserved |
| **11** | GPIO 17 | **SW1_INPUT** | Input | Internal Pull-Up (50kΩ) | Footswitch 1 (Preset 1 / Bank -) | High (Active Low) | Stomped = Pulls to GND |
| **12** | GPIO 18 | **PWM0_WS2812** | Output | None | SN74HCT125N Pin 2 (1A) | 3.3V PWM | 800 kHz DMA/PWM stream for NeoPixels |
| **13** | GPIO 27 | **SW2_INPUT** | Input | Internal Pull-Up (50kΩ) | Footswitch 2 (Preset 2) | High (Active Low) | Stomped = Pulls to GND |
| **14** | — | **GND** | Ground | — | 74AHCT125 Pin 7 (GND) | 0.0V | Level shifter logic ground return |
| **15** | GPIO 22 | **SW3_INPUT** | Input | Internal Pull-Up (50kΩ) | Footswitch 3 (Preset 3 / Mode) | High (Active Low) | Stomped = Pulls to GND |
| **16** | GPIO 23 | **SW4_INPUT** | Input | Internal Pull-Up (50kΩ) | Footswitch 4 (Preset 4 / Tap) | High (Active Low) | Stomped = Pulls to GND |
| **17** | — | **+3.3V DC** | Power Out | — | KY-040 VCC (+) | +3.3V DC | **STRICT RULE: Powers KY-040 pull-ups safely** |
| **18** | GPIO 24 | **ENC_CLK** | Input | Internal + Module Pull-Up | KY-040 Channel A (CLK) | High (Resting) | Quadrature encoder leading edge |
| **19** | GPIO 10 | SPI0_MOSI | Unused | — | Unconnected | High-Z | Reserved |
| **20** | — | **GND** | Ground | — | KY-040 Encoder GND | 0.0V | Ground reference for rotary encoder |
| **21** | GPIO 09 | SPI0_MISO | Unused | — | Unconnected | High-Z | Reserved |
| **22** | GPIO 25 | **ENC_DT** | Input | Internal + Module Pull-Up | KY-040 Channel B (DT) | High (Resting) | Quadrature encoder lagging edge |
| **23** | GPIO 11 | SPI0_SCLK | Unused | — | Unconnected | High-Z | Reserved |
| **24** | GPIO 08 | SPI0_CE0 | Unused | — | Unconnected | High-Z | Reserved |
| **25** | — | **GND** | Ground | — | Unconnected | 0.0V | Common ground plane |
| **26** | GPIO 07 | SPI0_CE1 | Unused | — | Unconnected | High-Z | Reserved |
| **27** | GPIO 00 | ID_SD | Reserved | — | Unconnected | High-Z | Do not use (HAT EEPROM I2C) |
| **28** | GPIO 01 | ID_SC | Reserved | — | Unconnected | High-Z | Do not use (HAT EEPROM I2C) |
| **29** | GPIO 05 | **SW5_INPUT** | Input | Internal Pull-Up (50kΩ) | Footswitch 5 (Preset 5 / Bank +) | High (Active Low) | Stomped = Pulls to GND |
| **30** | — | **GND** | Ground | — | Footswitch Daisy Ground | 0.0V | Common return wire for SW 1-6 |
| **31** | GPIO 06 | **SW6_TUNER** | Input | Internal Pull-Up (50kΩ) | Footswitch 6 (Upper Deck Mute) | High (Active Low) | Stomped = Pulls to GND |
| **32** | GPIO 12 | **ENC_SW** | Input | Internal Pull-Up (50kΩ) | KY-040 Push Button (SW) | High (Active Low) | Knob press = Pulls to GND |
| **33** | GPIO 13 | PWM1 | Unused | — | Unconnected | High-Z | Reserved |
| **34** | — | **GND** | Ground | — | Unconnected | 0.0V | Common ground plane |
| **35** | GPIO 19 | — | Unused | — | Unconnected | High-Z | Reserved |
| **36** | GPIO 16 | — | Unused | — | Unconnected | High-Z | Reserved |
| **37** | GPIO 26 | — | Unused | — | Unconnected | High-Z | Reserved |
| **38** | GPIO 20 | — | Unused | — | Unconnected | High-Z | Reserved |
| **39** | — | **GND** | Ground | — | Common Return Bus | 0.0V | Common ground plane |
| **40** | GPIO 21 | — | Unused | — | Unconnected | High-Z | Reserved |

---

## 3. Power Supply Subsystem Engineering

### 3.1 Input Stage & Polarity Protection
Stage pedalboards standardly provide **9V DC Center-Negative** power (standard Boss PSA style 2.1mm $\times$ 5.5mm coaxial jack). Connecting a center-positive supply or accidental reverse cable insertion is catastrophic for unbuffered circuitry.

To prevent reverse-polarity destruction:
1. The **Outer Sleeve** (+9V DC) feeds the anode of a **1N5822 Schottky Barrier Diode** (rated 40V, 3.0A continuous forward current).
2. The 1N5822 exhibits an ultra-low forward voltage drop ($V_F \approx 0.28\text{V}$ at 500mA), dissipating negligible power ($\sim 140\text{mW}$) while blocking negative voltages up to -40V with zero reverse leakage breakdown.
3. The **Center Pin** (0V GND) ties straight to the system Star Ground.

### 3.2 MP1584EN Step-Down DC-DC Buck Converter
The MP1584EN high-frequency step-down switching regulator converts 9V DC down to a stabilized 5.20V DC rail:
* **Switching Frequency:** Up to 1.5 MHz, allowing tiny filtering inductors and keeping switching noise well outside guitar audio bandwidth (avoiding RF induction into instrument pick-ups).
* **Target Calibration Voltage:** **5.20V – 5.22V DC** at no load.
* **Why 5.20V?** The Raspberry Pi Zero 2 W onboard PMIC allows an input range of $4.75\text{V} \le V_{IN} \le 5.25\text{V}$. Under peak quad-core CPU load, trace resistance and polyfuse internal resistance ($R \approx 0.15\Omega$) cause an IR voltage drop of $\Delta V \approx 0.15\text{V}$. Trimming the buck converter to 5.20V ensures the voltage on the Pi internal rail settles cleanly at **5.00V–5.05V**, completely avoiding the infamous Raspberry Pi lightning bolt under-voltage warning.
* **Mechanical Trimpot Locking:** After multimeter calibration, a dab of high-temperature hot melt glue or lacquer is applied over the miniature brass potentiometer screw to permanently prevent vibration-induced resistance drift during heavy stage stomping.

### 3.3 Overcurrent & Thermal Protection: RXEF110 PTC Polyfuse
Directly in series with the buck converter output sits an **RXEF110 Polymeric Positive Temperature Coefficient (PPTC) resettable fuse**:
* **Hold Current ($I_H$):** 1.10 A continuous.
* **Trip Current ($I_T$):** 2.20 A instantaneous trip.
* **Maximum Voltage:** 72 V.
* **Behavior:** In the event of an accidental wire short on the 5V bus, the polyfuse trips into a high-resistance state ($>10\text{k}\Omega$) in less than 200ms, protecting the MP1584EN inductor and Pi PCB copper traces. Once the fault is removed and power cycled, the fuse cools down and self-resets.

### 3.4 Decoupling and Bulk Capacitance Network
Switching WS2812B RGB LEDs generate aggressive transient current steps (di/dt) of up to 300mA in nanoseconds when PWM transitions occur:
1. **Bulk Reservoir Capacitor:** A **220µF 25V 105°C low-ESR electrolytic capacitor** is soldered directly across Pi Header Pin 2 (+5V) and Pin 6 (GND). This smooths voltage ripple and provides instantaneous charge during simultaneous LED state transitions.
2. **High-Frequency Decoupling Capacitor:** A **100nF (0.1µF) WIMA MKS02 box capacitor** is soldered across the level shifter IC pins (Pin 14 VCC to Pin 7 GND) with leads cut shorter than 4mm to eliminate high-frequency parasitic inductance.

### 3.5 System Current Budget Analysis

| Subsystem / Component | Typical Current (mA) | Peak Transient Current (mA) | Voltage Rail | Power Dissipation (W) |
| :--- | :---: | :---: | :---: | :---: |
| **Raspberry Pi Zero 2 W** (Quad A53 @ 1GHz, Idle/OS) | 120 mA | 180 mA | 5.0V | 0.60 W |
| **Pi Zero 2 W CPU Surge** (Active UI Render / HID TX) | 220 mA | 380 mA | 5.0V | 1.10 W |
| **1.3" I2C OLED Display** (128x64 SH1106, 50% pixels on) | 22 mA | 30 mA | 3.3V (Pi Reg) | 0.08 W |
| **KY-040 Rotary Encoder** (Pull-ups enabled) | 1 mA | 2 mA | 3.3V (Pi Reg) | < 0.01 W |
| **SN74HCT125N Level Shifter** (Quiescent + switching) | 2 mA | 5 mA | 5.0V | 0.01 W |
| **WS2812B RGB LEDs** (5 Dim Standby @ 8mA + 1 Active Emerald @ 25mA) | 65 mA | 95 mA | 5.0V | 0.35 W |
| **WS2812B Peak Surge** (All 6 LEDs White @ full 100% test) | 120 mA | 360 mA | 5.0V | 1.80 W |
| **ADuM3160 USB Isolator & Amp HID Bus** | 35 mA | 60 mA | 5.0V | 0.18 W |
| **TOTAL SYSTEM (Standard Stage Performance)** | **~465 mA** | **~752 mA** | **5.0V Bus** | **~2.33 W** |
| **TOTAL SYSTEM (Worst-Case Stress Test Peak)** | **~560 mA** | **~932 mA** | **5.0V Bus** | **~3.45 W** |

**Headroom Verification:**
* The MP1584EN buck converter is rated for **3.0A continuous** output. At our worst-case peak of ~0.93A, the buck converter operates at **<31% of its rated capacity**, running completely cool inside the sealed enclosure without requiring active heatsinking.
* The RXEF110 polyfuse ($I_H = 1.10\text{A}$) provides continuous headroom above the 0.75A operational envelope, avoiding nuisance tripping during LED flashes while guaranteeing instant short-circuit tripping.
* Standard 9V 1A pedalboard power bricks deliver $9\text{V} \times 1\text{A} = 9.0\text{W}$. With $\approx 88\%$ buck efficiency, 9V input current is under **300mA**, leaving $>700\text{mA}$ available for other daisy-chained guitar pedals!

---

## 4. Logic-Level Shifting Circuit (3.3V $\rightarrow$ 5.0V)

### 4.1 The Physics of the WS2812B Input Threshold
The WS2812B addressable LED uses a high-speed single-wire pulse-width modulation protocol (800 kHz, 1.25µs bit period).
According to the Worldsemi WS2812B datasheet:
$$\text{Input High Voltage } (V_{IH,\text{min}}) = 0.7 \times V_{DD}$$
When running $V_{DD}$ at **5.0V**:
$$V_{IH,\text{min}} = 0.7 \times 5.0\text{V} = \mathbf{3.50\text{V}}$$

The Raspberry Pi GPIO outputs CMOS logic at **3.30V maximum**.
Because $3.30\text{V} < 3.50\text{V}$, driving the WS2812B directly from GPIO 18 operates inside the undefined logic transition region. While a breadboard setup may accidentally work at room temperature, minor supply fluctuations or temperature changes cause the first LED to latch up, skip frames, or flicker violently.

### 4.2 High-Speed CMOS Solution: SN74HCT125N
To guarantee rock-solid noise margins, the design incorporates an **SN74HCT125N** (or 74AHCT125) Quad Bus Buffer with 3-state outputs:
* **HCT Input Characteristics:** The "T" designator denotes TTL compatibility. Its input thresholds are:
  $$V_{IH,\text{min}} = \mathbf{2.00\text{V}}, \quad V_{IL,\text{max}} = 0.80\text{V}$$
* When driven by the Pi's 3.3V logic ($V_{OH} \approx 3.2\text{V}$), the SN74HCT125N interprets the input with a **1.2V clean noise margin**.
* **Output Characteristics:** Running at $V_{CC} = 5.0\text{V}$, its output drives rail-to-rail CMOS levels ($V_{OH} \approx 4.8\text{V}$), completely satisfying the WS2812B $V_{IH}$ requirement.

```text
                  +5V Bus (From Polyfuse)
                     |
                     +-----------------------+
                     |                       |
                     |  SN74HCT125N          |
                     |  +-----------------+  |
                     +--| 14 (VCC)        |  |
                        |                 | [=] 100nF Box Capacitor
                        |        1A (2) <--+-- Pi GPIO 18 (PWM0, 3.3V)
      Pi GND -----------| 01 (1OE)        |  |
                        |        1Y (3) --+-- [ 470 Ohm Resistor ] ---> WS2812B DIN (5.0V)
      Star GND ---------| 07 (GND)        |  |
                        +-----------------+  |
                                             +--- Star GND
```

### 4.3 Transmission Line Ringing Suppression: 470Ω Resistor
A **470Ω 1/4W carbon film resistor** is placed in series between the buffer output (Pin 3, 1Y) and the LED `DIN` terminal.
* High-speed CMOS outputs have extremely fast rise/fall slew rates ($t_r < 3\text{ns}$).
* Without series damping, the parasitic inductance of the hookup wire and input capacitance of the LED create underdamped LC resonance ("ringing"), causing voltage spikes exceeding 6.5V.
* The 470Ω series damping resistor matches the line impedance, slows edge overshoot, suppresses ringing, and prevents first-pixel electrostatic discharge (ESD) latch-up.

---

## 5. Mechanical Enclosure & Ergonomics

### 5.1 Stepped Rake Ergonomics
Stage guitar footswitches suffer from a classic flaw: in a flat 6-button enclosure, stomping a front button risks stepping on the display or inadvertently kicking the tuner switch.

The custom 3D enclosure ([`pedal_enclosure.scad`](../pedal_enclosure.scad)) implements a **two-tier ergonomic wedge**:
* **Base Dimensions:** 280 mm width $\times$ 70 mm depth.
* **Front Height:** 32 mm.
* **Rear Height:** 48 mm.
* **True Slant Angle:** **12.88° (nominal ~14.5°)**.
* **Elevated Upper Deck:** The OLED display, Rotary Encoder, and **Switch 6 (Mute/Tuner)** reside on the elevated upper deck, shifted 35mm rearward and 16mm higher than the lower stomp switches. This physical elevation delta makes it virtually impossible for a musician's shoe heel or toe to strike the display or trigger the tuner by accident.

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
|                                    <--- 12.88° ERGONOMIC SLANT --->                                |
+----------------------------------------------------------------------------------------------------+
```

### 5.2 Heavy-Duty Structural Stomp Pillars
To withstand aggressive stage stomping (exceeding 80 kg dynamic foot strike):
* **4x 10mm Heavy Solid Stomp Pillars** are molded into the top shell at $X = 58, 106, 154, 202\text{ mm}$, flaring into 14mm conical heads that fuse directly into the 4.2mm thick ceiling.
* These transfer mechanical foot-strike force directly into the baseplate and stage floor, completely isolating the Pi Zero 2 W and OLED PCB from mechanical flexion.
* **Recessed Glare Shield:** The 1.3" OLED sits behind a 1.2mm recessed pocket housing a 38 $\times$ 24.8 mm smoked/clear cast acrylic lens sealed with 3M 300LSE adhesive tape to protect the glass display from direct shoe strikes and liquid drink spills.

### 5.3 3D Printing & Structural Settings
* **Material:** **Bambu PETG-CF** (Carbon Fiber Reinforced PETG) or standard **PETG** / PLA+.
* **Wall Loops:** 6 solid perimeters (~2.8mm solid outer skin).
* **Top/Bottom Layers:** 6 top layers, 5 bottom layers.
* **Infill:** **45% Gyroid infill** for omnidirectional shock absorption.
* **Bed Placement:** Fits standard 256 $\times$ 256 mm build plates rotated **45° diagonally**.
* **Fasteners:** 4x M3 $\times$ 4.2mm brass heat-set threaded inserts pressed into corner bosses at 230°C, secured with M3 $\times$ 10mm flat countersunk stainless machine screws.

---

## 6. Footswitch & Rotary Encoder Wiring

### 6.1 Mechanical Soft-Touch Footswitches
The pedal employs 6x **SPST Momentary Normally Open Soft-Touch Clickless switches** (PBS-24-102):
* **Zero Acoustic Click:** Unlike hard-latching 3PDT switches that emit a loud metallic snap during acoustic/studio performances, soft-touch momentary switches operate silently.
* **Active-Low Configuration:** One lug of each switch connects to its dedicated Raspberry Pi GPIO pin; the opposing lugs are daisy-chained into a **Star Ground Bus** returning to Pi Pin 30.
* **Internal Pull-Ups:** Internal Broadcom 50kΩ pull-up resistors maintain logic HIGH at rest. When stomped, the pin is pulled directly to GND (logic LOW).

### 6.2 KY-040 Rotary Encoder (Strict 3.3V Rule!)
The KY-040 mechanical encoder features 2-bit Gray quadrature outputs (CLK, DT) with 20 detents per revolution and an integrated momentary push switch (SW):

> [!CAUTION]
> **FATAL 3.3V TRAP WARNING:**  
> Standard KY-040 breakout boards have two onboard SMD 10kΩ pull-up resistors tied between `CLK` / `DT` and the module's `+` (VCC) pin.  
> If you connect the encoder `+` pin to **5.0V**, the module will pull the Pi's GPIO 24 and GPIO 25 lines to **5.0V**! Because Broadcom BCM2710A1 GPIO lines are strictly 3.3V and have **zero 5V tolerance**, this will immediately destroy the GPIO silicon bank.  
> **Mandatory Rule:** Connect KY-040 `+` (VCC) **exclusively to Pin 01 or Pin 17 (+3.3V)**.

### 6.3 Quadrature Timing Diagram
```text
  CLOCKWISE ROTATION:
  CLK (GPIO 24):  ---+       +-------+       +---
                     |       |       |       |
                     +-------+       +-------+
  DT  (GPIO 25):  -------+       +-------+       +---
                         |       |       |       |
                         +-------+       +-------+
  (At CLK falling edge, DT is HIGH -> Direction = +1)

  COUNTER-CLOCKWISE ROTATION:
  CLK (GPIO 24):  ---+       +-------+       +---
                     |       |       |       |
                     +-------+       +-------+
  DT  (GPIO 25):  ---+       +-------+       +---
                     |       |       |       |
                 ----+       +-------+       +---
  (At CLK falling edge, DT is LOW -> Direction = -1)
```

---

## 7. USB Digital Isolation & Ground Loop Suppression

When connecting a guitar amplifier USB port to an AC-powered or pedalboard-powered micro-controller, a massive **ground loop** is formed:
$$\text{Wall Supply GND} \longrightarrow \text{Pedalboard GND} \longrightarrow \text{Pi USB Shield} \longrightarrow \text{Amp Digital GND} \longrightarrow \text{Amp Audio Output GND}$$

This antenna loop captures 50Hz/60Hz electromagnetic mains hum and high-frequency digital hash from the Pi's quad-core CPU switching.

To achieve studio-grade signal-to-noise ratio:
1. An **ADuM3160 Full-Speed USB Digital Isolator** is inserted inline between the Raspberry Pi USB OTG host port and the Mustang LT25.
2. The ADuM3160 provides **2500V RMS galvanic isolation** using Analog Devices *iCoupler* planar magnetic pulse transformers.
3. An integrated isolated **B0505S DC-DC converter** supplies isolated +5V VBUS power to the amplifier's USB receiver without sharing an electrical ground with the pedal's buck converter.
4. **Result:** Total elimination of audio ground hum, computer digital whine, and USB bus ground currents.
