const crops = [
  "tea",
  "paddy",
  "wheat",
  "cardamom",
  "rose",
  "coconut",
  "tulsi",
  "banana",
  "cotton",
  "turmeric"
];

function extractCrop(text) {
  const lower = text.toLowerCase();

  for (let crop of crops) {
    if (lower.includes(crop)) {
      return crop;
    }
  }

  return null;
}

module.exports = extractCrop;