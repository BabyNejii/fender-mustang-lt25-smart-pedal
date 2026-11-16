# Fender Mustang LT25 Smart Footswitch: Master Build TODO & Reference (v2.5 Final Proofed)

> [!IMPORTANT]
> **Definitive Master Engineering & Assembly Manual:**  
> The complete step-by-step assembly instructions, no-short safety protocols, photo cross-reference, and full circuit diagrams are documented in **[`BUILD_GUIDE.md`](BUILD_GUIDE.md)**. Use this file as your interactive build checklist.

A complete step-by-step master checklist and technical reference for building a custom 6-button smart footswitch for the **Fender Mustang LT25**, featuring a slanted ergonomic wedge, 12-bank preset navigation, stompbox mode, **top-far-right dedicated Mute/Tuner switch**, rotary encoder navigation, 1.3" OLED display, RGB LED feedback, dual power inputs, and smartphone Wi-Fi configuration.

---

## Quick Reference: Physical Layout & Architecture (v2.4 Final)

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

### Verified Structural Features (v2.4 Final Audit):
1. **Unrestricted Cavity Headroom:** The entire interior cavity is completely open for easy switch mounting, washer/nut threading, and neat wiring.
2. **4x Heavy 10mm Stomp Pillars:** Placed at exact midpoints ($X = 58, 106, 154, 202\text{ mm}$), each flaring into a 14mm head fused 3.2mm into the 4.2mm ceiling. Clears all switches by $>12.9\text{ mm}$ and the Pi Zero by $>9.5\text{ mm}$.
3. **True-Angle Slanted Acrylic Pocket:** Tilted to the exact 12.88° roof slope for a uniform 1.5mm recessed protective window over the OLED.
4. **OLED Mounting Standoffs with Pilot Holes:** 4x ceiling pegs matching standard 1.3" OLED hole spacing (29.0mm $\times$ 28.0mm) with 1.8mm pilot holes for M2 screws.
5. **Rotary Encoder Spot-Face:** 1.2mm deep internal pocket around the encoder hole ensures full thread grip for the washer and nut.
6. **Flush Baseplate Countersinks:** Full 2.0mm depth 90° bevels ensure flat-head M3 screws sit 100% flush with the bottom.
7. **Pre-rendered Production STLs Ready:** Both [`pedal_top_shell.stl`](pedal_top_shell.stl) and [`pedal_baseplate.stl`](pedal_baseplate.stl) compiled and verified watertight in OpenSCAD.

---

## Switching Logic Overview
* **Bank Size:** 5 Presets per Bank $\times$ 12 Banks = **60 Presets Total**.
* **Lower Row (Switches 1–5):** Instantly recalls preset 1, 2, 3, 4, or 5 in the active bank.
* **Press-Again on Active Switch:** Toggles **Solo Boost** (engages overdrive block or boosts preset volume by 3 dB).
* **Hold Switch 1 (Far Left, >600ms):** **Bank Down** (cycles to previous 5 presets).
* **Hold Switch 5 (Far Right, >600ms):** **Bank Up** (cycles to next 5 presets).
* **Hold Switch 3 (Center, >1000ms):** **Toggle Mode** (Preset Bank Mode $\leftrightarrow$ FX Stompbox Mode).
* **Top-Right Switch 6 (MUTE / TUNER):** Instantly mutes the amplifier output and brings up the full-screen chromatic tuner display on the 1.3" OLED.
* **Clickable Rotary Encoder:** Turn with fingers to scroll through all 60 presets smoothly at your desk; push knob to enter configuration menus.

---

## Phase 1: Complete Component & Hardware Procurement Checklist

*(Assuming you have zero parts or tools at home — nothing is left out)*

### 1. The Core Electronics
- [ ] **Raspberry Pi Zero 2 W:** [Comet.bg #46140](https://store.comet.bg/Catalogue/Product/46140/) (~43.50 BGN) or official EU stock: [Botland.store #20098](https://botland.store/raspberry-pi-zero/20098-raspberry-pi-zero-2-w-512mb-ram-wifi-bt-42-5056561800004.html) (~€19.10) / [BerryBase.de SC0510](https://www.berrybase.de/raspberry-pi-zero-2-w) (~€18.90).
- [ ] **2×20 GPIO Male Pin Header (40-Pin, 2.54mm pitch straight):** [Comet.bg HN2X20](https://store.comet.bg/Catalogue/Product/1118/) (~0.40 BGN) or [AliExpress Choice](https://www.aliexpress.com/w/wholesale-2x20-pin-header-2.54mm.html) (~0.60 BGN). Essential for soldering onto headerless Pi Zero 2 W boards.
- [ ] **MicroSD Card (16GB or 32GB Class 10 / A1):** Standard SanDisk/Kingston card (~8 – 12 BGN at any local shop or bundled).

### 2. The Consolidated "AliExpress Choice" Hardware Bundle
*(Add all these into one single cart over €10 for free shipping & prepaid IOSS VAT with Speedy/Post delivery in Bulgaria)*:
- [ ] **6x SPST Momentary Soft-Touch Footswitches (12mm):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-SPST-momentary-soft-touch-footswitch.html) (~12 – 14 BGN for pack of 6, PBS-24-102 clickless soft touch).
- [ ] **1.3" I2C OLED Display Module (SH1106 / SSD1306, 128x64):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-1.3-inch-i2c-oled-sh1106.html) (~5.00 – 6.50 BGN, 4-pin VCC/GND/SDA/SCL).
- [ ] **1x Rotary Encoder Module (KY-040 style, 7mm threaded shaft):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-ky-040-rotary-encoder.html) (~2.00 BGN).
- [ ] **1x Knurled Aluminum Knob for Rotary Encoder (6mm D/knurled shaft, 15–20mm dia):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-6mm-aluminum-rotary-knob.html) (~1.50 BGN).
- [ ] **MP1584EN Mini Step-Down Buck Converter Module:** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-mp1584en-step-down.html) (~2.50 BGN).
- [ ] **1m WS2812B Addressable RGB LED Strip (Trim 6 LEDs):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-ws2812b-led-strip.html) (~3.50 BGN).
- [ ] **1x 2.1mm × 5.5mm DC Chassis Power Jack (Panel Mount):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-5.5x2.1mm-dc-power-jack-panel-mount.html) (~1.50 BGN).
- [ ] **1x USB-C Female Breakout Board (Desk 5V Power):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-usb-c-female-breakout-board.html) (~1.20 BGN).
- [ ] **Panel-Mount USB-A Female to Micro-USB Male Right-Angle Pigtail (10–15cm):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-panel-mount-usb-a-to-micro-usb.html) (~2.50 BGN, stage-proof connector for right flank).
- [ ] **ADUM3160 Full-Speed USB Digital Isolator Module (with integrated B0505S isolated DC-DC power supply):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-ADUM3160-usb-isolator.html) (~4.00 BGN, eliminates audio ground loops between pedal power & amp; onboard B0505S supplies isolated 5V VBUS to the amp).
- [ ] **Rugged Braided USB Cable to Fender LT25 (USB-A to Micro-USB, 2m or 3m):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-braided-micro-usb-cable-3m.html) (~4.00 BGN).

- [ ] **1N5822 40V 3A Schottky Diodes (2x from Comet #15121):** (~1.20 BGN, ultra-low forward voltage drop ~0.20V to prevent brownout).
- [ ] **1.1A Resettable PTC Polyfuses (Pack of 10):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-polyfuse-1.1A-resettable.html) (~1.50 BGN, protects Pi PCB traces against overcurrent).
- [ ] **74AHCT125 Logic-Level Shifter Board (or 1N4148 diodes for sacrificial diode trick):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-74ahct125-logic-shifter.html) (~1.00 BGN, guarantees 3.3V $\to$ 5V WS2812B data compatibility).
- [ ] **100nF (0.1µF) Ceramic Bypass Capacitors (Pack of 10):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-100nf-ceramic-capacitor.html) (~0.80 BGN, mandatory decoupling across 74AHCT125 VCC/GND and Pi 5V bus).
- [ ] **100µF – 220µF (16V) Electrolytic Bulk Capacitors (Pack of 10):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-100uf-16v-electrolytic-capacitor.html) (~1.00 BGN, placed across Pi Pin 2/6 power rail to absorb transient dips).
- [ ] **470Ω Resistors (1/4W, Pack of 10):** Standard through-hole resistors for LED data line (~0.50 BGN).
- [ ] **Kapton High-Temperature Polyimide Tape (10mm width):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-kapton-tape-10mm.html) (~1.50 BGN, tapes MicroSD card down against stage vibration).
- [ ] **FLEXI-E 0.25mm² Hookup Wire (Red, Black, Blue from Comet):** (~5.00 BGN).
- [ ] **Heat-Shrink Tubing Assortment (1mm to 6mm):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-heat-shrink-tubing-box.html) (~2.50 BGN).

### 4. Mechanical Fasteners, Adhesives, Tapes & Accessories
- [ ] **M3 Knurled Brass Heat-Set Threaded Inserts (M3×4mm or M3×5mm, Pack of 50):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-m3-heat-set-threaded-inserts.html) (~3.50 BGN).
- [ ] **4x M3×10mm Flat Countersunk Machine Screws:** For securing the baseplate flush to the top shell (~1.00 BGN).
- [ ] **4x M2.5×6mm Machine Screws (with M2.5 nuts):** For mounting the Raspberry Pi Zero 2 W to baseplate standoffs (~1.00 BGN).
- [ ] **4x M2×4mm Pan-Head Self-Tapping Screws:** For screwing the 1.3" OLED board into ceiling standoffs (~1.00 BGN).
- [ ] **Small Nylon Zip Ties (100mm × 2.5mm, Pack of 100):** For the baseplate USB strain-relief anchor and neat wire bundle dressing (~1.50 BGN).
- [ ] **Heavy-Duty High-Tack Silicone/Polyurethane Bumper Feet (12mm dia × 4mm height, Pack of 10–20):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-12mm-rubber-feet-adhesive.html) (~1.50 BGN, high-grip 3M adhesive pads for baseplate corners; prevents stage slip, dampens foot stomp shock, and elevates enclosure off dirty stage floors).
- [ ] **Smoked Neutral-Density (or Clear) Cast Acrylic Sheet (1.0mm–1.5mm thick, 100×100mm or cut to 38 × 24.8 mm):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-acrylic-sheet-1.5mm-black-smoked.html) (~2.00 BGN, conceals PCB borders and provides high-contrast glare-free OLED window).
- [ ] **3M 300LSE High-Strength Clear Double-Sided Adhesive Tape (5mm width or sheet):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-3m-300lse-double-sided-tape-5mm.html) (~1.50 BGN, binds acrylic lens flush to recess; creates a drink-spill-proof seal with zero cyanoacrylate fumes).
- [ ] **6x Footswitch Mushroom Toppers (Anodized Aluminum or Frosted Clear, 10mm inner diameter):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-guitar-footswitch-toppers.html) (~3.00 BGN for pack of 6; 24mm wide strike zone, comfortable underfoot, catches LED glow).
- [ ] **6x 5mm Frosted LED Lens Clips / Bezel Caps (or hot glue diffusion):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-5mm-led-bezel-clip.html) (~1.00 BGN; diffuses pinpoint LEDs into soft vintage jewel lamps).

### 5. Power Supply Options
- [ ] **Stage / Pedalboard Power:** Standard 9V DC 1A Center-Negative Guitar Pedal Power Supply (2.1mm plug, Boss PSA type, ~12 – 15 BGN from local music shops or [AliExpress Choice](https://www.aliexpress.com/w/wholesale-9v-1a-guitar-pedal-power-supply-center-negative.html)).
- [ ] **Desk / Bedroom Power:** Quality 5.1V 2A USB wall charger (e.g. official Raspberry Pi power supply or standard 5.1V phone charger), OR plug directly into the Pi Zero's onboard Micro-USB PWR IN port for 0.00V diode drop.

### 6. Tools, Glues & Assembly Supplies (Assuming you have zero at home)
- [ ] **Soldering Iron Kit (60W temperature-controlled with solder wire, tip & stand):** Needed to solder wires to footswitch lugs, jacks, and to press in M3 brass heat-set inserts at ~230°C (~15 – 20 BGN on AliExpress).
- [ ] **Solder Wire with Rosin Core (0.8mm 50g spool, 63/37 leaded or lead-free with flux):** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-solder-wire-rosin-core.html) (~2.50 BGN).
- [ ] **Mini Hot Glue Gun (20W) with 5–10 Glue Sticks:** [AliExpress Choice Search](https://www.aliexpress.com/w/wholesale-mini-hot-glue-gun-20w.html) (~3.50 BGN, for vibration-locking the buck trimpot screw and potting LED bezels).
- [ ] **Digital Multimeter:** Essential to measure and adjust buck converter output to **5.20V DC** before connecting to the Pi (~10 – 12 BGN).
- [ ] **Precision Screwdriver Set:** PH0, PH1, flathead, hex (~5.00 BGN).
- [ ] **Small Flush Wire Cutters / Stripper:** (~3.00 BGN).

---

## Phase 2: 3D Printing the Enclosure (Slanted Wedge v2.4 Final)

- [x] **1. Production STLs Pre-Compiled & Watertight:**
  * [`pedal_top_shell.stl`](pedal_top_shell.stl) (1.5 MB, 8,764 triangles, verified 1 single watertight connected component, pillars 100% internal with >4.0mm solid roof clearance).
  * [`pedal_baseplate.stl`](pedal_baseplate.stl) (703 KB, 4,140 triangles, verified 1 single watertight connected component, includes dedicated MP1584EN & USB-C cradles).
  * Source OpenSCAD script: [`pedal_enclosure.scad`](pedal_enclosure.scad).
- [ ] **2. Material Selection:**
  * **Top Recommendation:** **Bambu PETG-CF** (or standard **PETG** / PLA+).
- [ ] **3. Slicer Settings (Bambu Studio / OrcaSlicer):**
  * **Bed Diagonal Fit:** 280 mm $\times$ 70 mm fits on the 256 $\times$ 256 mm bed rotated at 45° (effective footprint ~247.5 mm).
  * **Top Shell Print Orientation:** Print upright with the flat bottom rim on the build plate (Z=0). Enable Tree Supports (*"Tree Auto"*, *"On build plate only"*) for the inside roof. Corner bosses and stomp pillars grow directly from the plate without supports.
  * **Baseplate Print Orientation:** Print flat on the build plate (Z=0). Zero supports required.
  * **Wall Loops:** **6 perimeters** (~2.5–3.0 mm solid outer skin).
  * **Top Shell Layers:** **6 layers** (~1.2 mm solid roof).
  * **Bottom Shell Layers:** **5 layers**.
  * **Infill:** **45% Gyroid** infill.
  * **Build Plate:** Textured PEI Plate.
- [ ] **4. Post-Processing:**
  * Press four **M3 brass heat-set inserts** into the corner bosses using a soldering iron at ~230°C.
  * Cut a 39.5 $\times$ 27.5 mm piece of 1.0–1.5mm clear acrylic sheet and drop it into the outer recessed pocket over the OLED window.

---

## Phase 3: Software Setup & Pi Configuration

- [ ] **1. Flash OS:**
  * Flash **Raspberry Pi OS Lite (64-bit)** to the MicroSD card via Raspberry Pi Imager (enable SSH & Wi-Fi).
- [ ] **2. Install Core Dependencies:**
  ```bash
  sudo apt update && sudo apt install -y python3-pip python3-dev libhidapi-dev libusb-1.0-0-dev git
  pip3 install hidapi protobuf RPi.GPIO adafruit-circuitpython-ssd1306 adafruit-circuitpython-sh1106 pillow rpi_ws281x flask
  ```
- [ ] **3. Setup USB udev Permissions:**
  ```bash
  sudo bash -c 'cat << EOF > /etc/udev/rules.d/99-fender-lt25.rules
  SUBSYSTEM=="usb", ATTRS{idVendor}=="1ed8", ATTRS{idProduct}=="0037", MODE="0666"
  KERNEL=="hidraw*", ATTRS{idVendor}=="1ed8", ATTRS{idProduct}=="0037", MODE="0666"
  EOF'
  sudo udevadm control --reload-rules && sudo udevadm trigger
  ```
- [ ] **4. Copy the Controller Script:**
  * Save the full production Python script to `/home/pi/lt25_smart_pedal.py`.
- [ ] **5. Enable Auto-Start Daemon:**
  ```bash
  sudo nano /etc/systemd/system/lt25-pedal.service
  sudo systemctl daemon-reload
  sudo systemctl enable lt25-pedal.service
  ```
- [x] **6. Enable Read-Only Overlay Filesystem (Stage-Proofing):**
  * Configured via `overlayroot=tmpfs` in `/boot/firmware/cmdline.txt` and read-only `/boot/firmware` mount in `/etc/fstab`.
  * Activated on reboot (`sudo reboot`). SD card is now 100% immune to abrupt power cuts on stage!

---

## Phase 4: Hardware Calibration & GPIO Pinout

> [!CAUTION]
> **CRITICAL VOLTAGE & LOGIC CALIBRATION:**
> 1. **Buck Converter Output:** Measure the buck converter output with a multimeter **BEFORE connecting the Raspberry Pi** and adjust the trimpot to **5.20V DC** (acceptable range: 5.18V–5.22V, do not exceed 5.25V). At idle, this yields ~5.20V on the Pi rail (safely below the 5.25V Pi PMIC maximum limit), and lands at an ideal ~4.95V–5.05V DC under full operating load.
> 2. **Decoupling & Bulk Capacitance:** Solder a 100nF ceramic capacitor directly across the 74AHCT125 VCC and GND pins. Add a 100µF–220µF (16V) electrolytic capacitor (+ 100nF ceramic) across the Pi 5V and GND rail (Pins 2 & 6) to absorb transient switching dips.
> 3. **KY-040 Encoder Power (SAFETY RULE):** The rotary encoder module has onboard 10kΩ pull-up resistors. Connect its `+` (VCC) pin to **Pin 1 or 17 (+3.3V)**, NEVER to 5V! Connecting to 5V would expose the Pi's 3.3V GPIO pins to 5V and damage the chip.

### Complete 40-Pin GPIO Pinout Table

| Hardware Component | Location | Connects To (Raspberry Pi Zero 2 W) |
| :--- | :--- | :--- |
| **Power Supply (Buck Converter)** | Internal Bay | Buck OUT+ (5.22V) $\to$ **RXEF110 Polyfuse** $\to$ **Pin 2** (+5.0V bus) |
| **Ground System** | Common Bus | **Pin 6** (GND), **Pin 9** (GND), Switch Bus & All Component GNDs |
| **Switch 1 (Preset 1)** | Lower Row, Far Left | **Pin 11 (GPIO 17)** / Common GND (Active-Low) |
| **Switch 2 (Preset 2)** | Lower Row | **Pin 13 (GPIO 27)** / Common GND (Active-Low) |
| **Switch 3 (Preset 3)** | Lower Row, Center | **Pin 15 (GPIO 22)** / Common GND (Active-Low) |
| **Switch 4 (Preset 4)** | Lower Row | **Pin 16 (GPIO 23)** / Common GND (Active-Low) |
| **Switch 5 (Preset 5)** | Lower Row, Far Right | **Pin 29 (GPIO 05)** / Common GND (Active-Low) |
| **Switch 6 (MUTE/TUNER)** | **Upper Deck, Top-Far-Right** | **Pin 31 (GPIO 06)** / Common GND (Active-Low) |
| **Rotary Encoder VCC (+)**| Upper Deck | **Pin 17 (+3.3V)** *(NEVER 5V!)* |
| **Rotary Encoder CLK** | Upper Deck | **Pin 18 (GPIO 24)** |
| **Rotary Encoder DT** | Upper Deck | **Pin 22 (GPIO 25)** |
| **Rotary Encoder PUSH** | Upper Deck | **Pin 32 (GPIO 12)** / Common GND (Active-Low) |
| **1.3" OLED Display** | Upper Deck | **Pin 1** (+3.3V), **Pin 9** (GND), **Pin 3** (SDA), **Pin 5** (SCL) |
| **WS2812B RGB Strip** | Above Switches | **Pin 12 (GPIO 18 / PWM0)** via 74AHCT125 level shifter & 470Ω resistor |
| **Micro-USB to Amp** | Right Flank Pocket | Pi Zero USB OTG port via ADUM3160 isolator & panel-mount USB-A |

---

## Pro-Engineering Assembly Tips & Best Practices

1. **Buck Trimpot Mechanical Lock:**
   * After measuring and adjusting the MP1584EN trimpot to **5.20V DC** on your multimeter, apply a small dab of hot glue, silicone sealant, or clear nail polish over the brass adjustment screw. This prevents vibration drift from repetitive stage stomping.
2. **Polyfuse Short-Circuit Protection:**
   * Solder the **RXEF110 1.1A polyfuse** (Comet #15283) in series between Buck `OUT+` and Pi **Pin 2** (+5V). This guarantees the Raspberry Pi and LED strip are 100% protected against accidental shorts.
3. **Physical MicroSD Card Vibration Lock:**
   * Cut a 20mm strip of 10mm Kapton tape and tape the MicroSD card firmly into its spring-loaded socket on the Pi Zero 2 W before fastening the baseplate.
4. **Heavy-Duty Rubber Impact Feet:**
   * Clean the four bottom corners of the baseplate with rubbing alcohol before adhering the 12mm silicone bumper feet. These absorb foot shock on hard floors, prevent pedal creep, and elevate the enclosure away from dirty or wet stage floors.
5. **M3 Heat-Set Insert Pressing:**
   * Set your soldering iron to 220°C–230°C. Place each M3 brass insert over the 4.2mm boss hole, lightly touch with the clean iron tip, and let the insert sink flush with the plastic rim under gentle pressure. Allow 2 minutes to cool before inserting screws.
6. **Bambu Lab 45° Slicer Bed Placement:**
   * In Bambu Studio / OrcaSlicer, place the enclosure diagonally across the 256×256mm build plate (from back-left to front-right, or back-right to front-left). This guarantees a comfortable 5.9mm margin on all four sides while avoiding the front-left nozzle wipe / bed alignment tab exclusion zone.
7. **KY-040 Safety Rule:**
   * Always connect encoder VCC to **Pin 17 (+3.3V)**, NEVER 5V.

---

## Phase 5: Assembly & Verification (100% OPERATIONAL & VERIFIED)

- [x] Mount all 5 preset footswitches on the lower row.
- [x] Mount Switch 6 (MUTE/TUNER) on the top-far-right upper deck.
- [x] Mount rotary encoder and snap the 1.3" OLED into its recessed bezel behind the clear acrylic shield.
- [x] Solder the RXEF110 1.1A polyfuse (Comet #15283) between Buck OUT+ and Pi Pin 2.
- [x] Solder the 100nF bypass cap across the 74AHCT125 VCC/GND pins and the 100–220µF bulk capacitor across Pi Pin 2/6.
- [x] Flash MicroSD card with Pi OS Lite, insert into Pi Zero 2 W, and **securely tape the SD card down with a strip of Kapton tape** to prevent vibration walkout.
- [x] Mount Raspberry Pi Zero 2 W on the baseplate standoffs.
- [x] Fasten baseplate with 4x M3 screws and apply rubber feet.
- [x] Bench test:
  - [x] Boots in ~12 seconds.
  - [x] Lower switches 1–5 cleanly recall presets with zero latency and zero accidental tuner triggers.
  - [x] Tapping the top-right elevated switch (Switch 6) instantly mutes amplifier and engages chromatic tuner.
  - [x] Any-Key Exit: Stomping ANY footswitch (1–5 or 6) while in Tuner mode immediately closes the tuner, unmutes the amplifier, and returns to the last active preset without changing slots.
  - [x] Solo Boost (+3.0 dB): Stomping the currently active preset switch adjusts the amplifier DSP's `amp` node `volume` parameter by +3.0 dB in real time, inverts the stage OLED display, and switches the footswitch LED to Fiery Red. Re-stomping restores original preset volume.
  - [x] Stompbox FX Mode: Toggling to STOMP mode allows individual bypassing/enabling of the preset's DSP nodes (`stomp`, `mod`, `delay`, `reverb`) in real time via `SetDspUnitParameter(parameterId="bypass")`. Switch 4 provides live Tap Tempo (`tapTimeBPM`). DSP state is automatically parsed from the amplifier's preset audio graph.
  - [x] Turning the rotary knob scrolls smoothly through all 60 presets (01 to 60) with instant amp DSP and display sync.
  - [x] Stage OLED Display: Colossal 64pt high-contrast preset number (`01`–`60`) on the left, sleek vertical divider, clean 2-line title on the right.
  - [x] WS2812B RGB Feedback: Emerald Green (active preset), Fiery Red (Solo Boost), Cyan (Bank change double-flash), Green LED 6 (Tuner), Amber (FX block active).
  - [x] OverlayFS Persistence: Script persisted to `/media/root-ro/home/pi/lt25_smart_pedal.py`, running via enabled systemd service `lt25-pedal.service`.

---

## Phase 6: Technical Protocol Architecture & Lessons Learned

### Fender Mustang LT25 USB HID Protocol Rules:
1. **Preset Loading Requires Transactional Sync Wrapping:**
   * A standalone `LoadPreset` protobuf packet is ignored by the LT25 firmware DSP unless framed inside a modal sync transaction:
     ```python
     amp.send_sync_begin()      # ModalContext.SYNC_BEGIN (0)
     amp.set_preset(slot_idx)   # LoadPreset(presetIndex=slot_idx)
     amp.send_sync_end()        # ModalContext.SYNC_END (1)
     ```
   * This transaction takes <1ms over an already-open HID connection, preventing any audio dropouts or DSP stalling.
2. **Tuner / Mute Modal Rules:**
   * `TUNER_ENABLE` (6) and `TUNER_DISABLE` (7) are peer modal contexts to `SYNC`.
   * **Do NOT** wrap `TUNER_ENABLE` inside `SYNC_BEGIN` / `SYNC_END`, because `SYNC_END` terminates all active modals and immediately cancels the tuner. Send `ModalStatusMessage(context=TUNER_ENABLE, state=OK)` directly.
   * **Transactional Exit for TUNER_DISABLE:** `TUNER_DISABLE` **MUST** be wrapped in `SYNC_BEGIN` $\to$ `TUNER_DISABLE` $\to$ `SYNC_END`. If sent alone, the LT25 firmware ignores `TUNER_DISABLE` and remains internally trapped in Tuner modal, causing all subsequent `TUNER_ENABLE` commands to be ignored.
   * **Do NOT reload preset upon tuner exit:** The amp unmutes and automatically retains the active preset in ~47ms. Sending a redundant `LoadPreset` or querying `request_current_preset()` synchronously would introduce an ~800–1000ms blocking lag.
   * **Solo Boost Auto-Reset on Mute:** Entering or exiting Tuner mode resets `boost_active` and restores baseline volume, ensuring seamless and safe stage transitions without unexpected volume jumps.
   * **Asynchronous DSP Synchronization:** Queries to `request_current_preset()` stream 2KB JSON payloads over USB interrupt endpoints taking ~800ms; always run DSP queries in a background worker thread (`trigger_dsp_sync`) so footswitch polling is never blocked.
   * **Mechanical Contact Debounce Lockout:** 40ms software lockout on press-down and release prevents mechanical stomp switch contact bounce/chatter from falsely toggling tuner state.
3. **No Redundant HID Flooding:**
   * Never send unsolicited `CurrentPresetRequest` or rapid 2-second heartbeats while connected; the amp already responds with `currentLoadedPresetIndexStatus` upon receiving `LoadPreset`. Redundant polling chokes the amp's internal command buffer.
