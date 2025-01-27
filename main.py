import fs from 'fs/promises';
import Papa from 'papaparse';

async function cleanCSV(csvContent) {
  // Parse the CSV content
  const { data } = Papa.parse(csvContent, { header: true });

  // Clean the data
  const cleanedData = data
    .filter(row => Object.values(row).every(value => value !== '')) // Remove rows with empty values
    .map(row => {
      // Convert numeric strings to numbers
      const numericColumns = ['App Usage Time (min/day)', 'Screen On Time (hours/day)', 'Battery Drain (mAh/day)', 'Number of Apps Installed', 'Data Usage (MB/day)', 'Age', 'User Behavior Class'];
      numericColumns.forEach(col => {
        row[col] = parseFloat(row[col]);
      });

      // Normalize 'App Usage Time' to hours/day for consistency with 'Screen On Time'
      row['App Usage Time (hours/day)'] = row['App Usage Time (min/day)'] / 60;
      delete row['App Usage Time (min/day)'];

      return row;
    });

  // Remove duplicates
  const uniqueData = Array.from(new Set(cleanedData.map(JSON.stringify))).map(JSON.parse);

  // Sort by User ID
  uniqueData.sort((a, b) => a['User ID'] - b['User ID']);

  return uniqueData;
}

async function main() {
  try {
    const csvContent = await fs.readFile('user_behavior_dataset.csv', 'utf-8');
    const cleanedData = await cleanCSV(csvContent);

    console.log('Data Cleaning Results:');
    console.log(`Original row count: ${Papa.parse(csvContent, { header: true }).data.length}`);
    console.log(`Cleaned row count: ${cleanedData.length}`);
    console.log('\nFirst 5 rows of cleaned data:');
    console.log(cleanedData.slice(0, 5));

    // Basic data analysis
    const avgScreenTime = cleanedData.reduce((sum, row) => sum + row['Screen On Time (hours/day)'], 0) / cleanedData.length;
    const avgAppUsageTime = cleanedData.reduce((sum, row) => sum + row['App Usage Time (hours/day)'], 0) / cleanedData.length;
    const avgBatteryDrain = cleanedData.reduce((sum, row) => sum + row['Battery Drain (mAh/day)'], 0) / cleanedData.length;

    console.log('\nBasic Data Analysis:');
    console.log(`Average Screen On Time: ${avgScreenTime.toFixed(2)} hours/day`);
    console.log(`Average App Usage Time: ${avgAppUsageTime.toFixed(2)} hours/day`);
    console.log(`Average Battery Drain: ${avgBatteryDrain.toFixed(2)} mAh/day`);

  } catch (error) {
    console.error('Error:', error);
  }
}

main();