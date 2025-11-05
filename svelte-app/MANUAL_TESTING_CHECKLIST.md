# PYCEK Svelte Migration - Manual Testing Checklist

## Setup

```bash
cd svelte-app
npm install  # If not already done
npm run dev
```

Then open **http://localhost:5173** in your browser.

---

## 🏠 Home Page Testing

### Visual Check
- [ ] Page loads without errors
- [ ] Title shows "Chemical Energetics and Kinetics Virtual Notebook"
- [ ] Two grids of cards are visible
- [ ] All text is readable (no CSS issues)

### Navigation Cards (Top Grid)
- [ ] Calendar card exists
- [ ] Lab Manual (PDF) card exists
- [ ] Lab Report Template (DOCX) card exists
- [ ] Notes of Statistics (PDF) card exists
- [ ] Python Primer (PDF) card exists

### Lab Cards (Bottom Grid)
- [ ] Statistics Lab card exists
- [ ] Bomb Calorimetry Lab card exists
- [ ] Crystal Violet Lab card exists
- [ ] Chemical Equilibrium Lab card exists
- [ ] Surface Adsorption Lab card exists

### Hover Effects
- [ ] Cards lift up slightly on hover
- [ ] Links change color on hover

### Navigation
- [ ] Click "Statistics Lab" - goes to `/stats`
- [ ] Click browser back button - returns to home
- [ ] Click "Surface Adsorption Lab" - goes to `/surface`
- [ ] Click browser back button - returns to home

---

## 🧪 Surface Adsorption Lab (`/surface`)

### Page Load
- [ ] Page title: "Surface Adsorption Lab"
- [ ] Objectives section visible
- [ ] Instructions section visible
- [ ] Input form visible in gray box

### Form Elements
- [ ] "Student ID" text input exists
- [ ] "Output file" text input exists (default: "Automatic")
- [ ] "Temperature (°C)" number input exists (default: 25)
- [ ] "Run Experiment" button exists
- [ ] "Reset Counter" button exists

### Test 1: Invalid Student ID
**Steps:**
1. [ ] Leave Student ID blank
2. [ ] Click "Run Experiment"

**Expected:**
- [ ] Red error message appears: "Invalid Student ID: must be a number"
- [ ] No data generated
- [ ] No plot shown

### Test 2: Valid Experiment
**Steps:**
1. [ ] Enter Student ID: `123456`
2. [ ] Set Temperature: `25`
3. [ ] Leave Output file: `Automatic`
4. [ ] Click "Run Experiment"

**Expected:**
- [ ] Gray results panel appears below form
- [ ] Metadata shown (student_ID, temperature, etc.)
- [ ] Plot appears with:
  - [ ] X-axis: "Dye added (mg)"
  - [ ] Y-axis: "Dye in solution (mol/L)"
  - [ ] ~100 blue data points
  - [ ] "TEMPLATE" watermark visible (gray, rotated)
- [ ] Green "Download [filename]" button appears
- [ ] Filename looks like: `data_[timestamp]_[random]_1.csv`

### Test 3: CSV Download
**Steps:**
1. [ ] Click the green download button

**Expected:**
- [ ] CSV file downloads
- [ ] Open file in text editor or Excel
- [ ] Check file contains:
  - [ ] Header line: `Dye added (mg),Dye in solution (mol/L)`
  - [ ] ~100 data rows
  - [ ] Comment lines at bottom starting with `#`
  - [ ] Metadata includes: `# Student ID = 123456`
  - [ ] Metadata includes: `# Temperature (C) = 25`

### Test 4: Different Temperature
**Steps:**
1. [ ] Set Temperature: `50`
2. [ ] Click "Run Experiment"

**Expected:**
- [ ] New plot appears with different data
- [ ] Metadata shows `Temperature (C) = 50`
- [ ] Data values should differ from first run

### Test 5: Custom Filename
**Steps:**
1. [ ] Change Output file to: `my_test.csv`
2. [ ] Click "Run Experiment"

**Expected:**
- [ ] Download button says "Download my_test.csv"
- [ ] Downloaded file is named `my_test.csv`

### Test 6: Reset Counter
**Steps:**
1. [ ] Click "Reset Counter"

**Expected:**
- [ ] Results panel disappears
- [ ] Plot disappears
- [ ] Form stays filled (doesn't clear)

---

## 💜 Crystal Violet Lab (`/cv`)

### Page Load
- [ ] Page title: "Crystal Violet Lab"
- [ ] Objectives and instructions visible

### Form Elements
- [ ] Student ID input
- [ ] Output file input
- [ ] Volume of CV solution (mL) - number input
- [ ] Volume of OH solution (mL) - number input
- [ ] Volume of DI water (mL) - number input
- [ ] Temperature (°C) - number input (default: 25)
- [ ] Run Experiment button
- [ ] Reset Counter button

### Test 1: Run Experiment
**Steps:**
1. [ ] Enter Student ID: `123456`
2. [ ] Set CV volume: `10`
3. [ ] Set OH volume: `10`
4. [ ] Set H2O volume: `10`
5. [ ] Set Temperature: `25`
6. [ ] Click "Run Experiment"

**Expected:**
- [ ] Plot appears with:
  - [ ] X-axis: "Time (s)"
  - [ ] Y-axis: "Absorbance"
  - [ ] ~501 data points
  - [ ] Clear exponential decay curve (high at start, low at end)
  - [ ] "TEMPLATE" watermark
- [ ] Download button appears

### Test 2: CSV Download
**Steps:**
1. [ ] Click download button

**Expected:**
- [ ] CSV file contains:
  - [ ] Header: `Time (s),Absorbance`
  - [ ] 501 data rows
  - [ ] First absorbance value > last value (decay)
  - [ ] Metadata includes volumes and temperature

### Test 3: Different Volumes
**Steps:**
1. [ ] Set CV: `5`, OH: `15`, H2O: `10`
2. [ ] Click "Run Experiment"

**Expected:**
- [ ] Different decay curve
- [ ] Different absorbance values
- [ ] Metadata reflects new volumes

---

## 🔥 Bomb Calorimetry Lab (`/bc`)

### Form Elements
- [ ] Student ID input
- [ ] Output file input
- [ ] Sample dropdown with options:
  - [ ] --Select--
  - [ ] benzoic
  - [ ] sucrose
  - [ ] naphthalene
- [ ] Run Experiment button
- [ ] Reset Counter button

### Test 1: No Sample Selected
**Steps:**
1. [ ] Enter Student ID: `123456`
2. [ ] Leave sample as `--Select--`
3. [ ] Click "Run Experiment"

**Expected:**
- [ ] Red error: "No sample selected!"
- [ ] No data generated

### Test 2: Benzoic Acid
**Steps:**
1. [ ] Select sample: `benzoic`
2. [ ] Click "Run Experiment"

**Expected:**
- [ ] Plot appears:
  - [ ] X-axis: "Time (s)"
  - [ ] Y-axis: "Temperature (K)"
  - [ ] ~100 points
  - [ ] Temperature jump visible (increases partway through)
  - [ ] Initial temp ~298 K
  - [ ] Final temp > initial temp
- [ ] Metadata includes: `Sample = benzoic`

### Test 3: Different Samples
**Steps:**
1. [ ] Select `sucrose`, run experiment
2. [ ] Select `naphthalene`, run experiment

**Expected:**
- [ ] Each shows different temperature profiles
- [ ] All show temperature increases
- [ ] Metadata shows correct sample name

---

## 📊 Statistics Lab (`/stats`)

### Form Elements
- [ ] Student ID input
- [ ] Output file input
- [ ] Task dropdown with options:
  - [ ] --Select--
  - [ ] Averages
  - [ ] Propagation of uncertainty
  - [ ] Comparison of averages
  - [ ] Linear fit
  - [ ] Non linear fit
  - [ ] Detection of outliers
- [ ] Run Experiment button
- [ ] Reset Counter button

### Test 1: No Task Selected
**Steps:**
1. [ ] Enter Student ID: `123456`
2. [ ] Leave task as `--Select--`
3. [ ] Click "Run Experiment"

**Expected:**
- [ ] Red error: "No sample selected!"

### Test 2: Averages Task
**Steps:**
1. [ ] Select task: `Averages`
2. [ ] Click "Run Experiment"

**Expected:**
- [ ] Plot with X,Y data
- [ ] 10 data points
- [ ] Download works

### Test 3: Linear Fit Task
**Steps:**
1. [ ] Select task: `Linear fit`
2. [ ] Click "Run Experiment"

**Expected:**
- [ ] Plot shows linear trend with scatter
- [ ] Points roughly follow a line
- [ ] CSV contains X,Y columns

### Test 4: All Tasks
**Steps:**
1. [ ] Test each task option one by one

**Expected:**
- [ ] Each generates different data
- [ ] All show 10 data points
- [ ] All download CSVs successfully

---

## 🧬 Equilibrium Lab (`/eq`)

### Expected Behavior
- [ ] Page shows placeholder message
- [ ] States "under construction"
- [ ] Has back link to home page
- [ ] No actual functionality (this is OK - it's a placeholder)

---

## 📅 Calendar Page (`/calendar`)

### Expected Behavior
- [ ] Page shows placeholder message
- [ ] States calendar will be displayed
- [ ] Has back link to home page
- [ ] No actual functionality (this is OK - it's a placeholder)

---

## 🌐 Cross-Browser Testing

Repeat the above tests in:
- [ ] **Chrome** (or Chromium)
- [ ] **Firefox**
- [ ] **Safari** (if on Mac)
- [ ] **Edge** (if on Windows)

---

## 📱 Mobile/Responsive Testing

Open on phone or use browser dev tools:
1. [ ] Open Chrome DevTools (F12)
2. [ ] Click device toolbar icon (phone icon)
3. [ ] Test at various screen sizes:
   - [ ] iPhone SE (375px)
   - [ ] iPad (768px)
   - [ ] Desktop (1920px)

**Check:**
- [ ] Cards stack vertically on mobile
- [ ] Forms are usable (inputs not too small)
- [ ] Buttons are tappable
- [ ] Plots resize appropriately
- [ ] No horizontal scrolling issues

---

## 🔍 Browser Console Check

**For each lab test:**
1. [ ] Open browser console (F12 → Console tab)
2. [ ] Run experiments
3. [ ] **No red errors should appear**
4. [ ] Warnings are OK, but errors are problems

**Common errors to watch for:**
- [ ] "Cannot read property of undefined"
- [ ] "Chart is not defined"
- [ ] "Failed to fetch"
- [ ] Any CORS errors

---

## ✅ Final Verification

### All Labs Should:
- [ ] Accept student ID input
- [ ] Validate student ID (reject non-numbers)
- [ ] Generate data when "Run Experiment" clicked
- [ ] Show plot with correct axes labels
- [ ] Display TEMPLATE watermark on plots
- [ ] Show metadata in results panel
- [ ] Download CSV files
- [ ] CSV files contain correct headers and data
- [ ] Reset button clears results

### Known Issues to Document:
Write down any bugs found:

```
Bug 1:
  Lab: _____________
  Issue: _____________
  Steps to reproduce: _____________

Bug 2:
  Lab: _____________
  Issue: _____________
  Steps to reproduce: _____________
```

---

## 📋 Testing Summary

After completing all tests, fill out:

**Tests Passed:** _____ / _____

**Critical Issues (blocking):**
-

**Minor Issues (non-blocking):**
-

**Browser Compatibility:**
- Chrome: ✅ / ❌
- Firefox: ✅ / ❌
- Safari: ✅ / ❌
- Mobile: ✅ / ❌

**Recommendation:**
- [ ] **Ready for production** (all critical tests pass)
- [ ] **Needs fixes** (critical issues found)
- [ ] **Not tested fully** (incomplete checklist)

---

## 🚀 Quick Smoke Test (5 minutes)

If you're short on time, at minimum test:

1. [ ] Home page loads
2. [ ] Surface Adsorption: Enter ID `123456`, temp `25`, run → plot appears → download CSV
3. [ ] Crystal Violet: Enter ID `123456`, volumes `10,10,10`, run → plot appears
4. [ ] Bomb Calorimetry: Enter ID `123456`, sample `benzoic`, run → plot appears
5. [ ] Statistics: Enter ID `123456`, task `Linear fit`, run → plot appears
6. [ ] Check browser console - no red errors

If all 6 pass: **Probably works!** ✅
If any fail: **Needs debugging** ❌

---

**Good luck testing!** 🧪

*Report bugs back to the development team with screenshots and console errors.*
