// Test script to verify lab functionality
import { SurfaceAdsorption } from './src/lib/labs/SurfaceAdsorption.js';
import { CrystalViolet } from './src/lib/labs/CrystalViolet.js';
import { BombCalorimetry } from './src/lib/labs/BombCalorimetry.js';
import { StatisticsLab } from './src/lib/labs/StatisticsLab.js';
import { SeededRandom } from './src/lib/utils/random.js';

console.log('=== PYCEK JavaScript Lab Tests ===\n');

// Test 1: Seeded Random Number Generation
console.log('Test 1: Seeded RNG');
const rng1 = new SeededRandom(12345);
const rng2 = new SeededRandom(12345);
const nums1 = [rng1.random(), rng1.random(), rng1.random()];
const nums2 = [rng2.random(), rng2.random(), rng2.random()];
console.log('RNG with seed 12345 (first run):', nums1);
console.log('RNG with seed 12345 (second run):', nums2);
console.log('Match:', JSON.stringify(nums1) === JSON.stringify(nums2) ? '✅ PASS' : '❌ FAIL');
console.log();

// Test 2: Normal Distribution
console.log('Test 2: Normal Distribution');
const rng3 = new SeededRandom(54321);
const normalVals = rng3.normal(0, 1, 1000);
const mean = normalVals.reduce((a, b) => a + b, 0) / normalVals.length;
const variance = normalVals.reduce((a, b) => a + (b - mean) ** 2, 0) / normalVals.length;
console.log('1000 samples from N(0,1):');
console.log('  Mean:', mean.toFixed(4), '(expected ~0)');
console.log('  Std Dev:', Math.sqrt(variance).toFixed(4), '(expected ~1)');
console.log('  Match:', Math.abs(mean) < 0.1 && Math.abs(Math.sqrt(variance) - 1) < 0.1 ? '✅ PASS' : '❌ FAIL');
console.log();

// Test 3: Surface Adsorption Lab
console.log('Test 3: Surface Adsorption Lab');
try {
	const surfLab = new SurfaceAdsorption();
	surfLab.setStudentID(123456);
	surfLab.setParameters({ temperature: 298.15 });
	const data = surfLab.createDataForLab();
	console.log('  Created data points:', data.length);
	console.log('  First point:', data[0]);
	console.log('  Last point:', data[data.length - 1]);
	console.log('  CSV length:', surfLab.writeDataToString().length, 'bytes');
	console.log('  Status:', data.length > 0 ? '✅ PASS' : '❌ FAIL');
} catch (e) {
	console.log('  Status: ❌ FAIL -', e.message);
}
console.log();

// Test 4: Crystal Violet Lab
console.log('Test 4: Crystal Violet Lab');
try {
	const cvLab = new CrystalViolet();
	cvLab.setStudentID(123456);
	cvLab.setParameters({
		volumes: { cv: 10, oh: 10, h2o: 10 },
		temperature: 298.15
	});
	const data = cvLab.createDataForLab();
	console.log('  Created data points:', data.length);
	console.log('  First point (t=0):', data[0]);
	console.log('  Midpoint:', data[Math.floor(data.length / 2)]);
	console.log('  Last point:', data[data.length - 1]);
	console.log('  Decay check (first > last):', data[0][1] > data[data.length - 1][1] ? '✅ PASS' : '❌ FAIL');
} catch (e) {
	console.log('  Status: ❌ FAIL -', e.message);
}
console.log();

// Test 5: Bomb Calorimetry Lab
console.log('Test 5: Bomb Calorimetry Lab');
try {
	const bcLab = new BombCalorimetry();
	bcLab.setStudentID(123456);
	bcLab.setParameters({ sample: 'benzoic' });
	const data = bcLab.createDataForLab();
	console.log('  Created data points:', data.length);
	console.log('  Sample:', bcLab.sample);
	console.log('  Initial temp:', data[0][1], 'K');
	console.log('  Final temp:', data[data.length - 1][1], 'K');
	console.log('  Temp increase check:', data[data.length - 1][1] > data[0][1] ? '✅ PASS' : '❌ FAIL');
} catch (e) {
	console.log('  Status: ❌ FAIL -', e.message);
}
console.log();

// Test 6: Statistics Lab
console.log('Test 6: Statistics Lab');
try {
	const statsLab = new StatisticsLab();
	statsLab.setStudentID(123456);
	statsLab.setParameters({ sample: 'Linear fit' });
	const data = statsLab.createDataForLab();
	console.log('  Created data points:', data.length);
	console.log('  First point:', data[0]);
	console.log('  Last point:', data[data.length - 1]);
	console.log('  Status:', data.length === 10 ? '✅ PASS' : '❌ FAIL');
} catch (e) {
	console.log('  Status: ❌ FAIL -', e.message);
}
console.log();

console.log('=== Test Summary ===');
console.log('Run this script with: node svelte-app/test-labs.js');
