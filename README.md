# Intapp Time Parser

A browser-based toolkit for parsing and visualizing legal time entry data. This project contains two standalone HTML applications that work together to transform raw time tracking exports into actionable insights.

## Overview

This toolkit provides two complementary tools:

1. **Intapp Timesheet Processor** (`index.html`) - Parses Intapp time export HTML files and generates clean, organized summaries
2. **Trello Hours Dashboard** (`chart.html`) - Visualizes daily hours logged through interactive bar charts with reference lines

Both applications run entirely in the browser with no server-side dependencies (except for the optional n8n webhook integration in chart.html).

---

## File Documentation

### `index.html` - Intapp Timesheet Processor

The main entry point and primary data processing tool. This file provides a complete client-side parser for Intapp time export files, transforming complex HTML exports into clean, navigable tables.

**Core Functionality:**
- **File Input**: Accepts `.html` files exported from Intapp time tracking systems
- **HTML Parsing**: Uses the DOMParser API to extract time entry data from nested tables
- **Data Extraction**: Pulls out Date, Client Name, Matter Name, Hours Billed, and Narrative
- **Matter Number Cleaning**: Automatically strips leading zeros from matter numbers (e.g., `56522-00004` becomes `56522-4`)
- **Dual View Modes**: Supports grouping by Date or by Client Name
- **Collapsible Sections**: Click to expand/collapse grouped data sections
- **Print-Optimized**: Special CSS for clean printing with expanded sections and preserved colors

**Data Structure Extracted:**
```javascript
{
    date: "MM/DD/YYYY",           // Date of time entry
    clientName: "Client Name",    // Client from Intapp
    matterName: "Matter (Num)",   // Matter name with cleaned number
    hours: "0.00",                // Hours billed as string
    narrative: "Work description" // Time entry narrative
}
```

**Key Features:**
- **Toggle View Modes**: Switch between "Group by Date" (chronological) and "Group by Client" (alphabetical by client, then matter)
- **Collapsible Headers**: Click black (Level 1) or gray (Level 2) headers to show/hide sections
- **Alternating Row Colors**: White and light gray alternating rows for readability
- **Daily Totals**: When grouped by date, shows total hours per day
- **Total Rows**: Highlighted with borders for clear summation

**Technical Implementation:**
- Pure JavaScript with no external dependencies
- Uses `DOMParser` to parse uploaded HTML files
- Event delegation for collapsible sections
- CSS media queries for print optimization
- Toggle button state management with active/inactive styling

---

### `chart.html` - Trello Hours Dashboard

A visualization tool that fetches processed time data from an n8n webhook and renders it as an interactive bar chart using Chart.js.

**Core Functionality:**
- **Webhook Integration**: Fetches data from `https://automate.felixjen.com/webhook/trello-chart`
- **Toggleable Date Range**: Option to truncate data to last 21 days
- **Interactive Charting**: Uses Chart.js with annotation plugin
- **Reference Lines**: Displays threshold lines at 7 hours (orange, dashed) and 9 hours (red, solid)

**UI Components:**
- **Toggle Switch**: Slide toggle for "Truncate to Last 21 Days" with Trello green accent
- **Run Workflow Button**: Triggers data fetch from n8n webhook
- **Loading States**: Button text changes during fetch operations
- **Error Handling**: Alert on failed webhook connections

**Chart Configuration:**
- **Type**: Vertical bar chart
- **Colors**: Trello blue (`#0079bf`) for bars
- **Reference Lines**: 
  - Red solid line at 9 hours (overtime threshold)
  - Orange dashed line at 7 hours (minimum threshold)
- **Tooltips**: Custom formatting showing "X Hours"
- **Responsive**: Maintains aspect ratio across screen sizes

**Data Format Expected:**
```javascript
{
    dates: ["2024-01-01", "2024-01-02", ...],  // Array of date strings
    hours: [8.5, 7.0, 9.5, ...]                  // Array of hour values
}
```

**Technical Implementation:**
- Chart.js v4.x with Annotation Plugin
- Async/await for fetch operations
- Dynamic chart destruction/recreation on data updates
- Trello-inspired styling (blues, greens, clean typography)

---

## Usage Guide

### Processing Intapp Exports (index.html)

1. **Export from Intapp**: Generate your time export as HTML from the Intapp system
2. **Open index.html**: Load the file in any modern browser (Chrome, Firefox, Edge, Safari)
3. **Select File**: Click the file input and choose your exported `.html` file
4. **View Data**: The table will automatically generate with entries grouped by date
5. **Toggle Views**: Click "Group by Client Name" to reorganize alphabetically by client
6. **Navigate Data**: Click black header rows to collapse/expand date or client sections
7. **Print**: Use Ctrl+P (or Cmd+P) to print - the output is optimized for printing

### Viewing Hours Chart (chart.html)

1. **Setup n8n Workflow**: Ensure your n8n instance has a workflow at `/webhook/trello-chart` that returns the expected JSON format
2. **Open chart.html**: Load in any modern browser
3. **Select Date Range**: Toggle "Truncate to Last 21 Days" if desired
4. **Fetch Data**: Click "Run Workflow" to retrieve and display the chart
5. **Analyze**: View bars against the 7-hour and 9-hour reference lines

---

## Technical Architecture

### Data Flow
```
Intapp Export (HTML)
        ↓
   index.html (Parser)
        ↓
  Processed/Viewed Data
        ↓
   (Optional: Sent to n8n)
        ↓
   chart.html (Visualization)
```

### Browser APIs Used
- **FileReader API** - For reading uploaded HTML files
- **DOMParser API** - For parsing Intapp HTML structure
- **Fetch API** - For retrieving chart data from webhooks
- **Canvas API** - Via Chart.js for rendering charts
- **CSS Grid/Flexbox** - For responsive layouts

### External Dependencies (chart.html only)
- `https://cdn.jsdelivr.net/npm/chart.js` - Chart rendering library
- `https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation` - Reference line plugin

---

## Styling Notes

Both files use clean, professional styling inspired by Trello and modern SaaS applications:

- **Color Palette**: 
  - Trello Blue: `#0079bf`
  - Trello Green: `#5aac44`
  - Accents: Orange (`#ff9f43`), Red (`#ff6b6b`)
  - Neutrals: Grays from `#172b4d` to `#f4f5f7`

- **Typography**: System fonts (Segoe UI, Roboto, Helvetica) for crisp rendering
- **Shadows**: Subtle box shadows for depth (`0 4px 12px rgba(0,0,0,0.1)`)
- **Border Radius**: 4-8px for modern, friendly appearance

---

## Browser Compatibility

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

Both files use modern ES6+ JavaScript features (async/await, arrow functions, const/let) and modern CSS (flexbox, CSS variables via preprocessor patterns).

---

## File Structure

```
intapp-time-parser/
├── index.html      # Intapp Timesheet Processor - Main parser tool
├── chart.html      # Trello Hours Dashboard - Visualization tool
└── README.md       # This documentation file
```

---

## License

This project is standalone HTML/JavaScript with no build process required. Simply open either HTML file in a browser to use.
