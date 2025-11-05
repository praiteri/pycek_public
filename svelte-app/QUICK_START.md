# Quick Start Guide - PYCEK Svelte

## Install & Run (First Time)

```bash
cd svelte-app
npm install
npm run dev
```

Open: **http://localhost:5173**

## Quick Test (30 seconds)

1. Go to Surface Adsorption Lab
2. Enter Student ID: `123456`
3. Set Temperature: `25`
4. Click "Run Experiment"
5. ✅ Plot should appear
6. ✅ Click download, CSV should save

**If that works, you're probably good!**

## Full Testing

See `MANUAL_TESTING_CHECKLIST.md` for comprehensive testing.

## Build for Production

```bash
npm run build
```

Output goes to `build/` directory.

Deploy `build/` folder to any static host (GitHub Pages, Netlify, etc.)

## Troubleshooting

**Server won't start?**
- Make sure port 5173 is free
- Delete `node_modules` and run `npm install` again

**Plot doesn't appear?**
- Check browser console (F12) for errors
- Make sure you entered a numeric Student ID

**Download doesn't work?**
- Check browser's download settings
- Try a different browser

## Files Overview

```
src/
├── lib/
│   ├── labs/           → Lab logic (data generation)
│   ├── utils/          → Helpers (RNG, CSV, etc.)
│   └── components/     → Plot component
└── routes/             → Pages for each lab

static/docs/            → PDF files for download
```

## Need Help?

1. Check `TEST_REPORT.md` - Known issues
2. Check `MANUAL_TESTING_CHECKLIST.md` - Testing guide
3. Check browser console for errors
4. Read `README.md` for full documentation
