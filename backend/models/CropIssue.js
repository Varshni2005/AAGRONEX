const mongoose = require("mongoose");

const cropIssueSchema = new mongoose.Schema(
  {
    crop: {
      type: String,
      required: true,
      trim: true,
      index: true,
    },
    issue: {
      type: String,
      required: true,
      trim: true,
    },
    symptom: {
      type: String,
      required: true,
      trim: true,
      index: true,
    },
    solution: {
      type: String,
      required: true,
      trim: true,
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model("CropIssue", cropIssueSchema);