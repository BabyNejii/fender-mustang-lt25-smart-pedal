# Alternative Hardware Procurement & Market Investigation
**Project:** Fender Mustang LT25 Smart Footswitch Controller (Raspberry Pi Zero 2 W)  
**Target Region:** Sofia / Bulgaria & European Union  
**Date:** October 2026  
**Investigator:** Hardware Procurement & Supply Chain Agent  

---

## Executive Summary: Is AliExpress the Only Option?

**Short Answer:**  
**No, AliExpress is not the only option, but it remains the most cost-effective and consolidated single-cart solution.** 

The table below summarizes the four evaluated procurement pathways for sourcing the complete bill of materials (including the 6–7x momentary soft-touch footswitches, KY-040 encoder, 1.3" OLED, MP1584EN buck, WS2812B strip, ADUM3160 isolator, USB-C breakout, long USB cable, 9V pedal power supply, passives, and fasteners):

| Metric | Pathway A: 100% Bulgarian Local | Pathway B: Temu + Comet Sofia | Pathway C: Botland EU (Poland) + Comet | Pathway D: AliExpress Choice + Comet (Baseline) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Build Cost** | **~165 – 195 BGN** | **~96.76 BGN** (€49.47) | **~150 – 175 BGN** | **~78.86 BGN** (€40.32) |
| **Number of Checkouts** | 5 – 6 separate stores | **2 checkouts** | 4 – 5 stores | **2 checkouts** |
| **Delivery Time** | 1 – 2 days (Courier/Pickup) | **6 – 10 business days** | 2 – 5 days (GLS) + 7–10d | **7 – 10 business days** |
| **Shipping Fees** | ~25 – 35 BGN across couriers | **0.00 BGN** (Free delivery) | ~14.67 BGN (GLS) + locals | **0.00 BGN** (Free Choice delivery) |
| **Fatal Blocker / Gaps** | **FAILED on Footswitches** (No local stock of PBS-24 momentary switches) | None (All parts available in one cart) | Lacks footswitches & ADUM3160 isolator | None (All parts available in Choice) |
| **Customs / Tax Risk** | 0 (Local Bulgarian VAT) | 0 (DDP IOSS pre-cleared, delivered by Speedy/DPD) | 0 (EU Internal Market, VAT invoice) | 0 (DDP IOSS pre-cleared, delivered by Speedy/Post) |

---

## Detailed Evaluation of Procurement Pathways

### Pathway A: 100% Local Bulgarian Sourcing (In-Country)
*Targeting: Comet Electronics, Ardboard, Robotev, Microrobotics, Hit-Electronics, MusicWorld, ITT, 3DPrintX.*

Can everything be bought strictly inside Bulgaria for immediate 1–2 day build turnaround?

#### What IS Available in Bulgaria:
1. **Comet Electronics (Sofia Druzhba-2 Warehouse):**
   - **ADUM3160 USB Isolator Module:** **YES!** Order Code `5165736` (*LC-USB-3160* by Shenzhen LC Technology). Stock: **91 pcs** in Sofia warehouse! Unit price: $14.35 USD (~30.96 BGN incl. VAT).
   - **1.28" / 1.3" I2C OLED Display:** **YES!** Part Code `WEA012864LWPP3N00000` (Winstar 1.28" 128x64 White, SH1106 controller, I2C). Stock: **167 pcs** in Sofia warehouse. Unit price: $7.82 USD (~16.90 BGN incl. VAT).
   - **Discrete Passives & Wire:** **YES!** 74HCT125N level shifter, 1N5822 diodes, 1.1A polyfuse, 100nF WIMA, 220µF cap, 470R resistor, DC-022 jack, 24 AWG flexible Staubli wire, zip ties, heat shrink tubing (~11.48 BGN).
2. **Ardboard.com (Bulgaria):**
   - **MP1584EN Buck Converter Module:** **YES!** Product Code `1044`. Stock: 34 pcs. Price: 5.90 BGN (€3.02).
   - **KY-040 Rotary Encoder Module:** **YES!** Stock available. Price: ~3.50 BGN.
3. **Hit-Electronics.com (Bulgaria):**
   - **1m WS2812B 60 LED/m 5V Strip:** **YES!** Price: ~12.50 BGN.
4. **MusicWorld.bg / Muziker.bg (Sofia):**
   - **9V DC 1A Guitar Pedal Power Supply:** **YES!** Center-negative 2.1mm plug (e.g. Behringer PSU-SB). Price: ~22.00 – 25.00 BGN.
5. **3DPrintX / 3D Support (Bulgaria):**
   - **M3 Heat-Set Threaded Brass Inserts:** **YES!** Ruthex M3x5.7mm brass inserts (50–100 pack). Price: ~16.50 – 19.00 BGN.
6. **ITT Bulgaria / Praktiker (Sofia):**
   - M2/M2.5/M3 machine screws, clear acrylic, 3M tape, silicone feet (~16.00 BGN).

#### ❌ The Fatal Blocker: SPST Momentary Soft-Touch Footswitches
- **No electronic component distributor or music store in Bulgaria stocks individual raw momentary stomp switches (PBS-24-102 soft-touch momentary, 12mm thread).**
  - *Elimex* only stocks latching switches (`PBS-24-102 #` Code 17114), which physically lock ON/OFF and cannot be used for momentary microcontroller event handling.
  - *MusicWorld.bg* and *Muziker.bg* only sell finished external pedal enclosures (such as Boss FS-5U at 75 BGN each — purchasing 7 units would cost over 500 BGN).
  - *Comet Electronics* only offers industrial APEM / RS-PRO panel switches rated IP67 at €15 – €30+ per switch (~250 BGN for 7 switches).
- **Logistics Overhead:** Even if footswitches were replaced with non-pedal tactile buttons, ordering across 5 separate stores incurs 25–35 BGN in courier delivery fees unless you drive between physical warehouses across Sofia.

**Pathway A Verdict:** **Infeasible for pedal footswitches** and costs more than double (~175 BGN vs 79 BGN).

---

### Pathway B: "Temu Unified Basket" + Comet Sofia Local
*Targeting: Temu (Consolidated EU Logistics) + Comet Electronics (Sofia Passives)*

Temu operates a high-volume marketplace model that directly mirrors AliExpress Choice logistics in Bulgaria, partnering with local couriers (**Speedy** and **DPD**) with full European Union IOSS tax pre-clearance.

#### Sourcing Breakdown:
1. **Store 1: Comet Electronics (Sofia - In-Person or Speedy):**
   - All 10 discrete components, logic shifter (`SN74HCT125N`), diodes, polyfuse, caps, DC-022 power jack, and stranded wire.
   - **Subtotal:** **11.48 BGN (~€5.87)**.
2. **Store 2: Temu (Single Combined Basket):**
   - **6x/8x SPST Momentary Soft-Touch Footswitches** (12mm thread, clickless, PBS-24 style): ~€11.50 (~22.49 BGN)
   - **KY-040 Rotary Encoder Module with Knob:** ~€1.30 (~2.54 BGN)
   - **1.3" I2C OLED Display Module (128x64 SH1106 / SSD1306):** ~€3.20 (~6.26 BGN)
   - **2x MP1584EN 3A DC-DC Step-Down Buck Modules:** ~€1.80 (~3.52 BGN)
   - **1m WS2812B Addressable RGB Strip (60 LED/m, IP30):** ~€3.40 (~6.65 BGN)
   - **ADUM3160 USB Digital Isolator Board:** ~€6.80 (~13.30 BGN)
   - **USB-C Female Breakout Board (with 5.1k CC resistors):** ~€1.10 (~2.15 BGN)
   - **Rugged 2m–3m USB-A to Micro-USB Cable & OTG Adapter:** ~€2.60 (~5.09 BGN)
   - **9V DC 1A Guitar Pedal Power Supply (Center-Negative, 2.1mm):** ~€5.50 (~10.76 BGN)
   - **M3 Brass Heat-Set Threaded Inserts (50–100 pack):** ~€1.90 (~3.72 BGN)
   - **Fastener & Consumables Kit (M2/M2.5/M3 screws, silicone feet, acrylic, 3M tape):** ~€4.50 (~8.80 BGN)
   - **Subtotal:** **~€43.60 (~85.28 BGN)**.

#### Temu Logistics & Performance:
- **Unified Package:** Everything from Temu is bundled into a single parcel.
- **Shipping Cost:** **FREE** (orders over ~25–30 BGN qualify for free standard shipping to Bulgaria).
- **Delivery Time:** **6 to 10 business days** (8–12 calendar days).
- **Courier in Bulgaria:** Handed directly to **Speedy** or **Box Now lockers** with full SMS notification.
- **Customs & Fees:** 0 BGN. VAT is collected at checkout under EU IOSS.
- **Combined Project Cost:** **~96.76 BGN (~€49.47)** across **2 checkouts**.

---

### Pathway C: "Botland EU / Poland" (botland.store) + Comet Sofia
*Targeting: Botland.store (Golina, Poland EU Warehouse) + Local Additions*

Botland is one of Europe's premier maker/robotics distributors, shipping across the EU via GLS with fast transit and official EU VAT commercial invoicing.

#### What Botland Can Supply:
- KY-040 rotary encoder module (~€1.60)
- 1.3" I2C OLED display (SH1106) (~€5.20)
- Step-down buck converters (Pololu or mini buck) (~€3.80)
- WS2812B addressable LED strip 1m (~€4.50)
- USB-C breakout board (~€1.80)
- M3 brass heat-set inserts (~€4.20)
- Hookup accessories, screws, silicone feet (~€3.50)
- *Botland Basket Subtotal:* **€24.60 (~48.11 BGN)**.
- *GLS Zone 2 Shipping to Bulgaria:* **€7.50 (~14.67 BGN)**.
- *Botland Total Delivered:* **€32.10 (~62.78 BGN)** (Transit: 2–5 business days).

#### ❌ Critical Inventory Gaps on Botland:
1. **NO Guitar Stomp Footswitches:** Botland does not carry PBS-24 series guitar pedal footswitches.
2. **NO ADUM3160 USB Isolator Module:** Botland does not stock USB 2.0 digital isolation breakout boards.
3. **NO Center-Negative Guitar Pedal Power Supply:** Botland power supplies are center-positive electronic supplies.

#### Filling the Gaps:
To complete the build under Pathway C, you must split orders further:
- ADUM3160 from Comet Sofia (PID 5165736): **30.96 BGN**
- 9V Pedal PSU from MusicWorld Sofia: **22.00 BGN**
- Comet Sofia passives & wire: **11.48 BGN**
- 7x Footswitches from AliExpress or Musikding.de (Germany): **~20.00 – 52.00 BGN**
- **Combined Cost:** **~147.22 – 179.22 BGN** across **4 to 5 checkouts**.

**Pathway C Verdict:** Offers fast 2–5 day shipping for generic maker sensors, but because it lacks the footswitches and isolator, you end up waiting for overseas footswitches anyway while paying double the price.

---

### Pathway D: "AliExpress Choice" + Comet Sofia (Baseline Benchmark)
*Targeting: AliExpress Choice (Consolidated Logistics) + Comet Electronics (Sofia Local)*

This represents the optimized 2-store strategy previously outlined in the procurement guide.

#### Sourcing Breakdown:
1. **Store 1: Comet Electronics (Sofia Druzhba-2):**
   - SN74HCT125N level shifter, 1N5822 diodes, 1.1A polyfuse, 100nF, 220µF, 470R, DC-022 jack, flexible 24 AWG wire, zip ties, heat shrink.
   - **Cost:** **11.48 BGN (~€5.87)**.
2. **Store 2: AliExpress Choice (Unified Order):**
   - 7x SPST Momentary Soft-Touch Footswitches (12mm thread): €8.50 (~16.60 BGN)
   - 1x KY-040 Rotary Encoder Module + Knob: €1.10 (~2.15 BGN)
   - 1x 1.3" I2C OLED Display (SH1106): €2.50 (~4.89 BGN)
   - 1x MP1584EN 3A Buck Converter: €0.85 (~1.66 BGN)
   - 1m WS2812B 60 LED/m Strip: €2.80 (~5.48 BGN)
   - 1x ADUM3160 USB Digital Isolator: €5.50 (~10.76 BGN)
   - 1x USB-C Female Breakout Board: €0.90 (~1.76 BGN)
   - 1x 2m–3m Rugged Micro-USB Cable & OTG: €2.20 (~4.30 BGN)
   - 1x 9V DC 1A Guitar Pedal Power Supply (Center-Negative): €4.50 (~8.80 BGN)
   - 1x M3 Heat-Set Threaded Inserts (50–100pk): €1.50 (~2.93 BGN)
   - Fastener Assortment (M2/M2.5/M3 screws, acrylic, feet, 3M tape): €4.10 (~8.02 BGN)
   - **Subtotal:** **€34.45 (~67.38 BGN)**.

#### AliExpress Choice Logistics:
- **Unified Package:** All items flagged with the **Choice** badge are aggregated in AliExpress fulfillment hubs and shipped in **one single parcel**.
- **Shipping Cost:** **FREE** (orders over €10.00 qualify for free consolidated shipping).
- **Delivery Time:** **7 to 10 business days**.
- **Courier in Bulgaria:** Speedy or Bulgarian Posts directly to door or locker.
- **Customs & Tax:** DDP under EU IOSS (VAT pre-collected at checkout, zero customs intervention).
- **Combined Project Cost:** **~78.86 BGN (~€40.32)** across **strictly 2 checkouts**.

---

## Direct Side-by-Side Comparison Matrix

| Factor | Pathway A: 100% Bulgarian Local | Pathway B: Temu + Comet Sofia | Pathway C: Botland EU + Comet | Pathway D: AliExpress Choice + Comet |
| :--- | :--- | :--- | :--- | :--- |
| **Total Price (BGN)** | ~165 – 195 BGN | **96.76 BGN** | ~150 – 175 BGN | **78.86 BGN** |
| **Total Price (EUR)** | ~€84 – €100 | **€49.47** | ~€77 – €90 | **€40.32** |
| **Number of Carts** | 5 – 6 stores | **2 carts** | 4 – 5 stores | **2 carts** |
| **Delivery Time** | 1 – 2 days *(Incomplete)* | **6 – 10 business days** | 2 – 5 days (GLS) + 7–10d | **7 – 10 business days** |
| **Shipping Costs** | 25 – 35 BGN across couriers | **0.00 BGN** (Free) | 14.67 BGN (GLS) + locals | **0.00 BGN** (Free) |
| **Stomp Footswitches** | ❌ **NOT AVAILABLE** |  Available (~22 BGN / 8pk) | ❌ **NOT AVAILABLE** |  Available (~16.60 BGN / 7pk) |
| **ADUM3160 Isolator** |  Comet PID 5165736 (31 лв.) |  Available (~13.30 BGN) | ❌ **NOT AVAILABLE** |  Available (~10.76 BGN) |
| **1.3" I2C OLED** |  Comet WEA012864 (17 лв.) |  Available (~6.26 BGN) |  Available (~10.15 BGN) |  Available (~4.89 BGN) |
| **9V Pedal PSU** |  MusicWorld (22 лв.) |  Available (~10.76 BGN) | ❌ Center-pos only |  Available (~8.80 BGN) |
| **Customs Hassle** | None | None (IOSS DDP via Speedy) | None (EU Internal Market) | None (IOSS DDP via Speedy) |

---

## Strategic Recommendation & Action Plan

1. **If your priority is Lowest Cost + Minimum Checkouts (Recommended):**
   - **Choose Pathway D (AliExpress Choice + Comet Electronics Sofia).**
   - Cost: **~78.86 BGN (€40.32)** total.
   - You only manage **2 checkouts**. All passives/wire are ready for immediate pickup at Comet Sofia; all maker modules, switches, and mechanicals arrive together in 7–10 days with zero customs fees.

2. **If you want an Alternative to AliExpress with Unified Cart & Free Shipping:**
   - **Choose Pathway B (Temu + Comet Electronics Sofia).**
   - Cost: **~96.76 BGN (€49.47)** total (~18 BGN more than AliExpress).
   - Temu successfully aggregates all non-Comet parts into one single order, ships free to Bulgaria via Speedy/DPD, and delivers in 6–10 business days.

3. **Why 100% Local Bulgarian Sourcing (Pathway A) Fails:**
   - While Comet Electronics surprisingly stocks both the ADUM3160 isolator (PID `5165736`, 91 in stock) and a high-grade 1.28" SH1106 OLED (PID `WEA012864LWPP3N00000`, 167 in stock), **no Bulgarian store stocks individual momentary soft-touch stomp switches (PBS-24-102 momentary)**. 
   - Furthermore, purchasing the isolator, OLED, PSU, and inserts locally inflates the price from ~79 BGN to over 165 BGN.

4. **Why Botland (Pathway C) is Not Feasible:**
   - Botland is an excellent robotics supplier, but it lacks guitar-specific parts (stomp switches and center-negative supplies) as well as the ADUM3160 USB isolator. You would pay €7.50 for GLS shipping and still have to place 3 other orders elsewhere.
