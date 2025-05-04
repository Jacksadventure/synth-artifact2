// ./models/photoModel.js

// Represents the semantic structure of a photo's data
export class Photo {
  constructor(data) {
    this.uuid = data.uuid;
    this.filename = data.filename;
    this.albumUUIDs = data.albums;
    this.metadata = data.exif_info;
    this.aestheticScore = data.score.overall;
    this.semanticLabels = data.labels;
    this.location = data.location;
    this.dateTaken = data.date;
    // ... additional properties as needed
  }

  // Semantically meaningful method to determine if photo meets criteria
  matchesCriteria(criteria) {
    // Implement logic based on criteria object
    // For example, check if aestheticScore exceeds a threshold
    return this.aestheticScore >= criteria.minScore;
  }
}
