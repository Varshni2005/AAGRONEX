const express = require("express");
const router = express.Router();
const CropIssue = require("../models/CropIssue");
const extractCrop = require("../utils/extractCrop");

router.post("/search", async (req, res) => {
    try {
        const { query } = req.body;

        if (!query) {
            return res.status(400).json({
                success: false,
                message: "Query required"
            });
        }

        // STEP 1: detect crop
        const detectedCrop = extractCrop(query);

        // STEP 2: lowercase query
        let symptomText = query.toLowerCase();

        // STEP 3: remove crop word from query
        if (detectedCrop) {
            symptomText = symptomText.replace(detectedCrop, "");
        }

        // STEP 4: remove extra common words
        symptomText = symptomText
            .replace(/\bin\b|\bwith\b|\bon\b|\bof\b|\bfor\b/g, "")
            .trim();

        // STEP 5: split keywords
        const keywords = symptomText
            .split(" ")
            .filter(word => word.length > 2);

        // STEP 6: build AND regex search
        const symptomConditions = keywords.map(word => ({
            symptom: { $regex: word, $options: "i" }
        }));

        const filter = {
            $and: symptomConditions
        };

        // STEP 7: crop filter first priority
        if (detectedCrop) {
            filter.crop = { $regex: `^${detectedCrop}$`, $options: "i" };
        }

        const results = await CropIssue.find(filter).limit(1);

        if (!results.length) {
            return res.json({
                success: false,
                message: "No matching issue found"
            });
        }

        res.json({
            success: true,
            detectedCrop,
            data: results
        });

    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
});

module.exports = router;