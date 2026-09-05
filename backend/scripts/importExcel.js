const mongoose = require("mongoose");
const XLSX = require("xlsx");
const dotenv = require("dotenv");
const path = require("path");
const CropIssue = require("../models/CropIssue");

dotenv.config({ path: path.join(__dirname, "../.env") });

async function importExcel() {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log("MongoDB connected");

    const workbook = XLSX.readFile(path.join(__dirname, "../../dataset/agronex_dataset.xlsx"));

    await CropIssue.deleteMany();

    let totalInserted = 0;

    for (const sheetName of workbook.SheetNames) {
      const sheet = workbook.Sheets[sheetName];
      const rows = XLSX.utils.sheet_to_json(sheet);

      const formattedRows = rows.map((row) => ({
        crop: row.crop || sheetName,
        issue: row.issue,
        symptom: row.symptom,
        solution: row.solution,
      }));

      const inserted = await CropIssue.insertMany(formattedRows);
      totalInserted += inserted.length;
            console.log(`${sheetName}: ${inserted.length} rows inserted`);
    }

    console.log(`Total inserted: ${totalInserted}`);
    process.exit();
  } catch (error) {
    console.error("Import error:", error.message);
    process.exit(1);
  }
}

importExcel();