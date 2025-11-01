/**
 * Google Apps Script for Snake Game Quiz Results
 * 
 * This script receives quiz results from the Snake game and appends them to a Google Sheet.
 * Deploy this as a web app to receive POST requests from the game.
 * 
 * Setup Instructions:
 * 1. Create a new Google Sheet
 * 2. Open Extensions → Apps Script
 * 3. Copy this code into the script editor
 * 4. Change YOUR_SECRET_TOKEN_HERE to a secure random string
 * 5. Save and deploy as Web App:
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 6. Copy the web app URL and add it to snake_game.py
 */

// Configuration
const SECRET_TOKEN = "YOUR_SECRET_TOKEN_HERE"; // Change this to a secure token
const SHEET_NAME = "Quiz Results"; // Name of the sheet to write to

/**
 * Handle HTTP GET requests (for testing)
 */
function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({
      status: "ok",
      message: "Snake Game Quiz Results API is running. Send POST requests to log quiz results."
    }))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Handle HTTP POST requests (quiz results)
 */
function doPost(e) {
  try {
    // Parse the request
    const data = JSON.parse(e.postData.contents);
    
    // Validate token (optional security measure)
    if (data.token && data.token !== SECRET_TOKEN) {
      return createResponse(403, "Invalid token");
    }
    
    // Get or create the sheet
    const sheet = getOrCreateSheet(SHEET_NAME);
    
    // Extract data
    const timestamp = data.timestamp ? new Date(data.timestamp * 1000) : new Date();
    const questionId = data.question_id || "N/A";
    const question = data.question || "N/A";
    const correct = data.correct ? "Yes" : "No";
    const coinsEarned = data.coins_earned || 0;
    
    // Append row to sheet
    sheet.appendRow([
      timestamp,
      questionId,
      question,
      correct,
      coinsEarned
    ]);
    
    return createResponse(200, "Quiz result logged successfully");
    
  } catch (error) {
    Logger.log("Error: " + error.toString());
    return createResponse(500, "Error processing request: " + error.toString());
  }
}

/**
 * Get existing sheet or create new one with headers
 */
function getOrCreateSheet(sheetName) {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = spreadsheet.getSheetByName(sheetName);
  
  if (!sheet) {
    // Create new sheet
    sheet = spreadsheet.insertSheet(sheetName);
    
    // Add headers
    sheet.appendRow([
      "Timestamp",
      "Question ID",
      "Question",
      "Correct",
      "Coins Earned"
    ]);
    
    // Format header row
    const headerRange = sheet.getRange(1, 1, 1, 5);
    headerRange.setFontWeight("bold");
    headerRange.setBackground("#4285f4");
    headerRange.setFontColor("#ffffff");
    
    // Set column widths
    sheet.setColumnWidth(1, 150); // Timestamp
    sheet.setColumnWidth(2, 100); // Question ID
    sheet.setColumnWidth(3, 400); // Question
    sheet.setColumnWidth(4, 80);  // Correct
    sheet.setColumnWidth(5, 120); // Coins Earned
  }
  
  return sheet;
}

/**
 * Create JSON response
 */
function createResponse(status, message) {
  const response = {
    status: status === 200 ? "ok" : "error",
    message: message
  };
  
  return ContentService
    .createTextOutput(JSON.stringify(response))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Test function to verify setup (run this manually in the script editor)
 */
function testSetup() {
  const sheet = getOrCreateSheet(SHEET_NAME);
  
  // Add test data
  sheet.appendRow([
    new Date(),
    "TEST",
    "This is a test question",
    "Yes",
    10
  ]);
  
  Logger.log("Test setup complete! Check the '" + SHEET_NAME + "' sheet.");
}

/**
 * Clear all data except headers (useful for testing)
 */
function clearData() {
  const sheet = getOrCreateSheet(SHEET_NAME);
  const lastRow = sheet.getLastRow();
  
  if (lastRow > 1) {
    sheet.deleteRows(2, lastRow - 1);
    Logger.log("Cleared " + (lastRow - 1) + " rows of data.");
  } else {
    Logger.log("No data to clear.");
  }
}
