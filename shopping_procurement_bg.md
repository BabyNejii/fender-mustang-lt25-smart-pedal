# Hardware Procurement Plan & Sourcing Guide: Fender Mustang LT25 Smart Footswitch
**Platform:** Raspberry Pi Zero 2 W  
**Location:** Sofia / Bulgaria  
**Currency:** BGN (Bulgarian Lev) / EUR (€)  
**Strategy:** Minimal Shop Splitting (2 Stores Maximum)  
- **Store 1 (Sofia Local Stock):** [Comet Electronics](https://store.comet.bg) — All discrete passives, semiconductors, level shifters, DC jacks, flexible hookup wire, and cable management.  
- **Store 2 (Combined Global Choice):** [AliExpress Choice / Direct](https://www.aliexpress.com) — Specialized maker modules (ADUM3160 isolator, 1.3" OLED, WS2812B strip, MP1584EN, USB-C breakout), 3D print heat inserts, fastener kit, and guitar pedal power supply. *(With local Bulgarian alternatives noted where available).*

---

## 1. Verified Procurement Matrix

| # | Item Description | Recommended Store | Catalog / Product ID | Unit Price | Qty | Total Price | Direct Verified Link |
|---|------------------|-------------------|----------------------|------------|-----|-------------|----------------------|
| **1** | 1.3" I2C OLED Display (128x64, SH1106, 4-pin I2C) | AliExpress Choice | `1005009102928073` | €2.50 | 1 | €2.50 (~4.89 лв.) | [AliExpress Link](https://www.aliexpress.com/item/1005009102928073.html) |
| **2** | MP1584EN DC-DC Step-Down Buck Converter (3A, adj.) | AliExpress Choice *(or Ardboard.com)* | `32828603866` *(Ardboard: 1044)* | €0.85 *(Ardboard: €3.02)* | 1 | €0.85 (~1.66 лв.) | [AliExpress Link](https://www.aliexpress.com/item/32828603866.html) / [Ardboard](https://www.ardboard.com/mp1584-step-down) |
| **3** | 1m WS2812B Addressable RGB LED Strip (IP30, 60 LED/m) | AliExpress Choice | `1005004752499978` | €2.80 | 1 | €2.80 (~5.48 лв.) | [AliExpress Link](https://www.aliexpress.com/item/1005004752499978.html) |
| **4** | SN74HCT125N Quad Level Shifter IC (DIP-14 through-hole) | Comet Electronics | `44148` (TI SN74HCT125N) | €0.28 (0.55 лв.) | 1 | €0.34 (~0.66 лв. с ДДС) | [Comet.bg Link](https://store.comet.bg/Catalogue/Product/44148/) |
| **5** | 3A Schottky Barrier Diodes 40V (1N5822 DO-27 through-hole) | Comet Electronics | `15121` (SM Tech 1N5822) | $0.0608 (~0.11 лв.) | 2 | ~0.26 лв. с ДДС | [Comet.bg Link](https://store.comet.bg/Catalogue/Product/15121/) |
| **6** | 1.1A PTC Resettable Polyfuse (RXEF110 DIP leaded, 72V) | Comet Electronics | `15283` (Littelfuse RXEF110) | €0.19 (0.37 лв.) | 1 | €0.23 (~0.45 лв. с ДДС) | [Comet.bg Link](https://store.comet.bg/Catalogue/Product/15283/) |
| **7** | 100nF (0.1µF) WIMA MKS02 Polyester Capacitor (RM 2.5mm) | Comet Electronics | `27363` (MKS0C031000C00KSSD) | €0.39 (0.76 лв.) | 1 | €0.47 (~0.92 лв. с ДДС) | [Comet.bg Link](https://store.comet.bg/Catalogue/Product/27363/) |
| **8** | 220µF 25V 105°C Electrolytic Capacitor (Fujicon RK, RM 2.5mm) | Comet Electronics | `3792` (RK1E221M-RBE11) | $0.0492 (~0.09 лв.) | 1 | ~0.11 лв. с ДДС | [Comet.bg Link](https://store.comet.bg/Catalogue/Product/3792/) |
| **9** | 470 Ohm 1/4W Carbon Film Resistor (Uni-Ohm CFR0W4) | Comet Electronics | `24761` (CFR0W4J0471A50) | $0.1904 (~0.35 лв.) | 1 *(or 10pk)* | ~0.42 лв. с ДДС | [Comet.bg Link](https://store.comet.bg/Catalogue/Product/24761/) |
| **10** | 5.5mm x 2.1mm DC Power Jack Panel Mount (DC-022 w/ nut) | Comet Electronics | `47599` (DC000028) | $0.1428 (~0.26 лв.) | 1 | ~0.31 лв. с ДДС | [Comet.bg Link](https://store.comet.bg/Catalogue/Product/47599/) |
| **11** | USB-C 16-Pin Female Breakout Board (with 5.1k CC resistors) | AliExpress Choice | `1005012511554191` | €0.90 | 1 | €0.90 (~1.76 лв.) | [AliExpress Link](https://www.aliexpress.com/item/1005012511554191.html) |
| **12** | ADUM3160 Full-Speed 12Mbps USB Isolator (with B0505S) | AliExpress Choice | `1005007002260915` | €5.50 | 1 | €5.50 (~10.76 лв.) | [AliExpress Link](https://www.aliexpress.com/item/1005007002260915.html) |
| **13** | Flexible Stranded Hookup Wire 24 AWG (Staubli Flexi-E 0.25mm²) | Comet Electronics | `42020` (Blk), `42021` (Red), `42711` (Blu) | €0.73/m | 3m (1m ea) | €2.63 (~5.14 лв. с ДДС) | [Comet Black](https://store.comet.bg/Catalogue/Product/42020/) / [Red](https://store.comet.bg/Catalogue/Product/42021/) / [Blue](https://store.comet.bg/Catalogue/Product/42711/) |
| **14** | M3 Heat-Set Brass Threaded Inserts (M3x4mmx4.2mm OD, 50-100pk) | AliExpress Choice | `1005007557287955` | €1.50 | 1 pk | €1.50 (~2.93 лв.) | [AliExpress Link](https://www.aliexpress.com/item/1005007557287955.html) |
| **15** | Screw Assortment (M2x4/5, M2.5x6 Pan, M3x10 Countersunk) | AliExpress Choice *(or ITT.bg)* | `1005006827233117` | €2.90 | 1 box | €2.90 (~5.67 лв.) | [AliExpress Link](https://www.aliexpress.com/item/1005006827233117.html) |
| **16.1** | Cable Ties 100mm x 2.5mm (100 pcs pack) | Comet Electronics | `20848` (YK-0108.CV-100) | $0.612 / 100pk | 1 pk | ~1.32 лв. с ДДС | [Comet.bg Link](https://store.comet.bg/Catalogue/Product/20848/) |
| **16.2** | Heat Shrink Tubing Assortment (2mm, 3mm, 4mm - 1m each) | Comet Electronics | `7603` (2mm), `7604` (3mm), `7605` (4mm) | ~$0.25/m | 3m total | ~1.85 лв. с ДДС | [Comet 2mm](https://store.comet.bg/Catalogue/Product/7603/) / [3mm](https://store.comet.bg/Catalogue/Product/7604/) / [4mm](https://store.comet.bg/Catalogue/Product/7605/) |
| **16.3** | 12mm Adhesive Silicone Bumper Feet (Pack of 32-64 pcs) | AliExpress Choice | `10000422088422` | €1.20 | 1 sheet | €1.20 (~2.35 лв.) | [AliExpress Link](https://www.aliexpress.com/item/10000422088422.html) |
| **16.4** | Clear Acrylic Sheet (1.0mm - 1.5mm thickness, 100x150mm) | AliExpress Choice | `4001300262164` | €1.60 | 1 sheet | €1.60 (~3.13 лв.) | [AliExpress Link](https://www.aliexpress.com/item/4001300262164.html) |
| **16.5** | 3M 300LSE High-Tack Clear Double-Sided Adhesive (Sheet/Roll) | AliExpress Choice | `32902626479` | €1.30 | 1 roll/sheet | €1.30 (~2.54 лв.) | [AliExpress Link](https://www.aliexpress.com/item/32902626479.html) |
| **16.6** | 9V DC 1A Guitar Pedal Power Supply (Center-Negative, 2.1mm) | AliExpress Choice *(or MusicWorld.bg)* | `1005006019824034` | €4.50 | 1 | €4.50 (~8.80 лв.) | [AliExpress Link](https://www.aliexpress.com/item/1005006019824034.html) |

---

## 2. Store Breakdown & Basket Grouping

### Store 1: Comet Electronics (Sofia, Bulgaria)
**Pickup / Delivery:** In-store pickup at Sofia (Druzhba-2 warehouse) is free, or fast next-day courier delivery via Speedy throughout Bulgaria (~5.00 – 6.00 лв.).  
**Items Included:** 10 discrete components & consumables.

1. **SN74HCT125N Quad Level Shifter (DIP-14)**  
   - *Catalog Code:* `44148` | *Manufacturer:* Texas Instruments  
   - *Stock:* 384 pcs in Sofia warehouse  
   - *Price:* 0.28 € (0.34 € с ДДС / ~0.66 лв.)  
   - *Note:* TTL-compatible input levels ($V_{IH} = 2.0\text{V}$) make it the gold standard for reliably shifting 3.3V GPIO from the Raspberry Pi Zero 2 W to 5.0V for the WS2812B data line.
2. **2x 1N5822 3A 40V Schottky Diodes (DO-27 leaded)**  
   - *Catalog Code:* `15121` | *Manufacturer:* SM Technology  
   - *Stock:* 9,755 pcs in Sofia warehouse  
   - *Price:* $0.0608 each (~0.26 лв. total с ДДС for 2 pcs)
3. **1.1A PTC Resettable Polyfuse (RXEF110 DIP)**  
   - *Catalog Code:* `15283` | *Manufacturer:* Littelfuse Inc  
   - *Stock:* 546 pcs in Sofia warehouse  
   - *Price:* 0.19 € (0.23 € с ДДС / ~0.45 лв.)
4. **100nF 63V WIMA MKS02 Polyester Capacitor (RM 2.5mm leaded)**  
   - *Catalog Code:* `27363` | *Manufacturer:* WIMA  
   - *Stock:* 9,011 pcs in Sofia warehouse  
   - *Price:* 0.39 € (0.47 € с ДДС / ~0.92 лв.)
5. **220µF 25V 105°C Radial Electrolytic Capacitor (RM 2.5mm)**  
   - *Catalog Code:* `3792` | *Manufacturer:* Fujicon RK Series  
   - *Stock:* 4,043 pcs in Sofia warehouse  
   - *Price:* $0.0492 (~0.11 лв. с ДДС)
6. **470 Ohm 1/4W Resistor (Axial Through-Hole)**  
   - *Catalog Code:* `24761` | *Manufacturer:* Uni-Ohm  
   - *Stock:* 21,408 pcs in Sofia warehouse  
   - *Price:* $0.1904 (~0.42 лв. с ДДС for single unit, or 0.84 лв. for 10-pack)
7. **DC-022 5.5mm x 2.1mm Panel Mount Power Jack (with hex nut & washer)**  
   - *Catalog Code:* `47599` | *Model:* DC000028  
   - *Stock:* 729 pcs in Sofia warehouse  
   - *Price:* $0.1428 (~0.31 лв. с ДДС)
8. **3m Flexible Stranded 24 AWG Hookup Wire (Staubli Flexi-E 0.25mm²)**  
   - *Black:* PID `42020` (1m)  
   - *Red:* PID `42021` (1m)  
   - *Blue:* PID `42711` (1m)  
   - *Stock:* >160 meters each in Sofia warehouse  
   - *Price:* €2.18 total (€0.73/m) (~5.14 лв. с ДДС)
9. **100mm x 2.5mm Zip Ties (100 pcs pack)**  
   - *Catalog Code:* `20848` | *Model:* YK-0108.CV-100  
   - *Stock:* 1,600 pcs in Sofia warehouse  
   - *Price:* $0.612 / 100pk (~1.32 лв. с ДДС)
10. **Heat Shrink Tubing (Uni-Home 2mm, 3mm, 4mm, 1m each)**  
    - *2mm:* PID `7603` (1m, $0.19)  
    - *3mm:* PID `7604` (1m, $0.26)  
    - *4mm:* PID `7605` (1m, $0.32)  
    - *Stock:* Thousands of meters in Sofia warehouse  
    - *Price:* ~$0.77 total (~1.85 лв. с ДДС)
11. **2x20 GPIO Male Pin Header (40-Pin, 2.54mm pitch straight)**  
    - *Catalog Code:* `1118` | *Model:* HN2X20 (CviLux)  
    - *Stock:* In stock in Sofia warehouse  
    - *Price:* ~$0.20 (~0.40 лв. с ДДС)  
    - *Note:* Required for soldering onto headerless Raspberry Pi Zero 2 W boards.

**Store 1 Basket Subtotal:** **~11.88 BGN (~6.07 EUR)**

---

### Store 2: AliExpress Choice (Single Consolidated Package)
**Shipping & Terms:** Items marked **Choice** are shipped together in one single package by AliExpress Logistics with DDP (VAT is pre-collected at checkout under the EU IOSS scheme, meaning **0 customs handling fees and 0 Bulgarian Post delays**). Delivery takes 7–10 business days directly to your address or local Speedy locker. Free shipping applies to orders over €10.00.

1. **ADUM3160 Full-Speed 12Mbps USB Isolator Board with B0505S**  
   - *Item ID:* `1005007002260915`  
   - *Price:* ~€5.50 (~10.76 лв.)  
   - *Why essential:* Isolates the Raspberry Pi Zero 2 W USB controller from the Fender Mustang LT25 ground/chassis, eliminating USB ground-loop noise and protecting the amp's DSP.
2. **1.3" I2C OLED Display 128x64 (SH1106, 4-Pin: VCC/GND/SCL/SDA)**  
   - *Item ID:* `1005009102928073`  
   - *Price:* ~€2.50 (~4.89 лв.)
3. **MP1584EN 3A DC-DC Step-Down Buck Converter Module**  
   - *Item ID:* `32828603866`  
   - *Price:* ~€0.85 (~1.66 лв.)  
   - *(Local Alternative: [Ardboard.com (Code 1044)](https://www.ardboard.com/mp1584-step-down) has 34 pcs in stock in Bulgaria for €3.02).*
4. **1m WS2812B Addressable RGB LED Strip (IP30 Bare PCB, 60 LEDs/m)**  
   - *Item ID:* `1005004752499978`  
   - *Price:* ~€2.80 (~5.48 лв.)
5. **USB-C 16-Pin Female Breakout Board with 5.1k CC Resistors**  
   - *Item ID:* `1005012511554191`  
   - *Price:* ~€0.90 (~1.76 лв.)
6. **M3 Brass Heat-Set Threaded Inserts (M3x4mmx4.2mm OD, 50-100pk)**  
   - *Item ID:* `1005007557287955`  
   - *Price:* ~€1.50 (~2.93 лв.)
7. **M2 / M2.5 / M3 Machine Screw Assortment Kit (Pan Head + Countersunk)**  
   - *Item ID:* `1005006827233117`  
   - *Price:* ~€2.90 (~5.67 лв.)  
   - *(Includes 4x M3x10 countersunk DIN 965, 4x M2.5x6 pan head, 4x M2x4/M2x5 pan head).*
8. **12mm Silicone Anti-Slip Adhesive Bumper Feet (32-64 pcs)**  
   - *Item ID:* `10000422088422`  
   - *Price:* ~€1.20 (~2.35 лв.)
9. **Clear Cast Acrylic Sheet (1.0mm or 1.5mm thickness, 100x150mm)**  
   - *Item ID:* `4001300262164`  
   - *Price:* ~€1.60 (~3.13 лв.)
10. **3M 300LSE High-Strength Clear Double-Sided Adhesive (Sheet/Roll)**  
    - *Item ID:* `32902626479`  
    - *Price:* ~€1.30 (~2.54 лв.)
11. **9V DC 1A Guitar Pedal Power Supply (Center-Negative, 5.5x2.1mm plug)**  
    - *Item ID:* `1005006019824034`  
    - *Price:* ~€4.50 (~8.80 лв.)  
    - *(Local Alternative: MusicWorld.bg in Sofia stocks standard 9V center-negative pedal adapters such as Behringer PSU-SB for ~18-24 BGN).*

**Store 2 Basket Subtotal:** **~€25.55 (~49.97 BGN)** (Qualifies for Free Combined Shipping).

---

## 3. Financial Summary & Cost Comparison

| Order / Basket | Estimated Cost (BGN) | Estimated Cost (EUR) | Shipping Method & Speed |
|----------------|----------------------|----------------------|-------------------------|
| **Store 1: Comet Electronics** | **11.48 лв.** | **€5.87** | Free store pickup (Sofia) or ~5.50 лв. Speedy (Next Day) |
| **Store 2: AliExpress Choice** | **49.97 лв.** | **€25.55** | **FREE** AliExpress Combined Choice (7–10 days, DDP/No tax) |
| **Total Estimated Project Cost** | **~61.45 лв.** | **~€31.42** | **Entire build sourced across only 2 checkout carts** |

---

## 4. Practical Assembly & Procurement Tips

1. **Logic Level Shifting:**  
   Always use the `SN74HCT125N` (DIP-14) buffer between Raspberry Pi GPIO 18 (PWM) and the WS2812B Data In pin. Standard HC logic (`74HC125`) requires $V_{IH} \ge 3.5\text{V}$ when powered from 5V and will cause flickering. The `HCT` series has $V_{IH} = 2.0\text{V}$, providing reliable, rock-solid switching from the Pi's 3.3V logic.
2. **Power Supply Polarity:**  
   Guitar pedals use **Center-Negative** ($\Theta\text{--C--}\oplus$). When soldering the Comet `DC-022` jack (PID `47599`), the center pin must connect to GND and the outer sleeve terminal must connect to the input diode protection before feeding the MP1584EN.
3. **USB Ground Isolation:**  
   The `ADUM3160` module must be placed between the Raspberry Pi Zero 2 W micro-USB OTG port and the Fender Mustang LT25 micro-USB port. Ensure the speed switch on the module is set to **Full Speed (12 Mbps)**, which is the native USB MIDI/CDC audio rate for Fender Mustang amplifiers.
