// Arya st125462

// UPDATE: 

// Increase Citation Impact by 10% for Publications in a Specific Field

use("StochasticallyYours");
db.citation_network.updateMany(
  {
    "citationType": "Analysis" 
  },
  { 
    $mul: {
      "citationImpact": 1.1 
    } 
  }
);


// Change the Citation Type from ‘Technical Report’ to ‘Conference Paper’

use("StochasticallyYours");
db.citation_network.updateOne(
  { 
    "citationType": "Technical Report" 
  },
  { 
    $set: {
      "citationType": "Conference Paper" 
    } 
  }
);

// DELETE:

// Delete Reviews Where the Decision Was ‘Reject’ and Score Was Below 2

use("StochasticallyYours");
db.review.deleteMany({
  rating: { $lt: 3 },
  decision: "reject"
});

// Kaung st124974

// UPDATE

// Mark Old Publications (Before 2000) as ‘Archived’
db.publication.updateMany(
  {
    $expr: {
      $lt: [
        {
          $dateFromString: {
            dateString: "$publicationDate"
          }
        },
        ISODate("2000-01-01")
      ]
    }
  },
  { $set: { "status": "ARCHIVED" } }
);


// Promote Institutions in Top 10 Global Ranking
db.institution.updateMany(
  { 'ranking': { $lte: 10 } },
  {
    $inc: {
      'researchBudget': 1000000
    }
  }
)

// DELETE

// Remove Research Statements That Are Too Short (Less Than 10 Words)
db.research_statement.deleteMany({
    $expr: {
      $lt: [
        { $size: { $split: ['$statement', ''] } }
      ]
    }
  })

// Suryansh st124997

// UPDATE

// Adjust the Citation Score in Research Impact Based on New Metrics
use("StochasticallyYours");

db.research_impact.updateMany(
  { "field": "Environmental Science" },
  { $mul: { "citationScore": 1.05 } }
);

// Change the Citation Type for All Self-Citations
use("StochasticallyYours");

db.citation_network.updateMany(
  {
    $expr: { $eq: [ "$citingPublicationID", "$citedPublicationID" ] }
  },
  { $set: { "citationType": "Self-Citation" } }
);

// DELETE

// Delete All Publications That Are Marked as Retracted
use("StochasticallyYours");

db.publication.deleteMany(
  { "status": "RETRACTED" }
);

// Swaraj st125052

// UPDATE

// Move Open Access Journals to a Special Category
use("StochasticallyYours");

db.journal.updateMany(
  { "openAccessStatus": "Open Access" },
  { $set: { "scope": "Public Research Repository" } }
);

// Flag Publications with High Citation Count
use("StochasticallyYours");

db.publication.updateMany(
  { "citationCount": { $gte: 100 } },
  { $set: { "highImpact": true } }
);


// DELETE
// Remove DatasetS If the Dataset Size Is 0 Bytes
use("StochasticallyYours");

db.dataset.deleteMany(
  { size: 0 }
);