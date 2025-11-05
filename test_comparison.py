#!/usr/bin/env python3
"""
Compare Python and JavaScript lab outputs for compatibility testing
"""
import sys
sys.path.insert(0, 'src')

import pycek_public as cek
import numpy as np

print("=== Python vs JavaScript Comparison ===\n")

# Test 1: Surface Adsorption with same seed
print("Test 1: Surface Adsorption Lab")
print("-" * 50)
lab = cek.surface_adsorption(make_plots=False)
lab.set_student_ID(123456)
lab.set_parameters(temperature=298.15)
np.random.seed(123456)  # Reset after set_student_ID call
data = lab.create_data_for_lab()

print(f"Python output:")
print(f"  Data points: {len(data)}")
print(f"  First point: {data[0]}")
print(f"  Last point: {data[-1]}")
print(f"  Sample metadata: {lab.metadata.get('sample_ID')}")
print()

print("Expected JavaScript output (from test):")
print("  Data points: 100")
print("  First point: [ 500, 0.0008166575 ]")
print("  Last point: [ 10000.000000000002, 0.0170063114 ]")
print()

# Test 2: Crystal Violet
print("Test 2: Crystal Violet Lab")
print("-" * 50)
cv_lab = cek.crystal_violet(make_plots=False)
cv_lab.set_student_ID(123456)
cv_lab.set_parameters(
    volumes={"cv": 10, "oh": 10, "h2o": 10},
    temperature=298.15
)
np.random.seed(123456)
cv_data = cv_lab.create_data_for_lab()

print(f"Python output:")
print(f"  Data points: {len(cv_data)}")
print(f"  First point: {cv_data[0]}")
print(f"  Last point: {cv_data[-1]}")
print()

print("Expected JavaScript output:")
print("  Data points: 501")
print("  First point (t=0): [ 0, 1.338598 ]")
print("  Last point: [ 1000, 0.041535 ]")
print()

# Test 3: Statistics Lab
print("Test 3: Statistics Lab")
print("-" * 50)
stats_lab = cek.stats_lab(make_plots=False)
stats_lab.set_student_ID(123456)
stats_lab.set_parameters(sample='Linear fit')
np.random.seed(123456)
stats_data = stats_lab.create_data_for_lab()

print(f"Python output:")
print(f"  Data points: {len(stats_data)}")
print(f"  First point: {stats_data[0]}")
print(f"  Last point: {stats_data[-1]}")
print()

print("Expected JavaScript output:")
print("  Data points: 10")
print("  First point: [ 1.04, 12.697 ]")
print("  Last point: [ 9.585, 118.337 ]")
print()

print("=== Analysis ===")
print("Due to different RNG algorithms (NumPy vs mulberry32),")
print("exact values will differ, but:")
print("  ✓ Data shapes should match")
print("  ✓ Trends should be similar")
print("  ✓ Value ranges should be comparable")
print("  ✓ Metadata should be identical")
