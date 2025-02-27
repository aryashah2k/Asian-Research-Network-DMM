// Arya st125462

// Find Top 5 Most Cited Publications

use("StochasticallyYours");
db.citation_network.aggregate([
  {
    $group: { 
      _id: "$citedPublicationId", 
      totalCitations: { $sum: 1 } 
    } 
  }, 
  { 
    $sort: { 
      totalCitations: -1
    }
  },
  {
    $limit: 5 
  }
]);


// Find Researchers Who Have Co-Authored More Than 3 Publications

use("StochasticallyYours");
db.researcher.aggregate([
  {
    $unwind: "$publications"
  },
  {
    $lookup: {
      from: "publication", 
      localField: "publications", 
      foreignField: "title", 
      as: "publicationDetails"
    }
  },
  {
    $unwind: "$publicationDetails"
  },
  {
    $group: {
      _id: "$_id",
      firstName: { $first: "$firstName" },
      middleName: { $first: "$middleName" },
      lastName: { $first: "$lastName" },
      email: { $first: "$email" },
      totalPublications: { $sum: 1 }
    }
  },
  {
    $match: {
      totalPublications: { $gte: 3 }
    }
  }
]);


// Find Institutions With the Most Research Collaborations


use("StochasticallyYours");
db.collaboration_network.aggregate([
  { 
    $sort: { 
      partnerCount: -1
    }
  }, 
  { 
    $limit: 5 
  }
]);


// Find the Citation Impact of Publications Whose Methodology was Impactful

use('Stochastically Yours');
db.getCollection('citation_network').aggregate([
  // Match documents where the citationType is 'Methodology'
  { 
    $match: { 
      citationType: 'Methodology' 
    } 
  },
  // Group by citedPublicationId and calculate the total citation impact
  {
    $group: { 
      _id: '$citedPublicationId',
      totalCitationImpact: { $sum: '$citationImpact' } 
    } 
  }
]);


// Find the Average Citation Impact of Publications Per Field

use('StochasticallyYours');
db.getCollection('publication').aggregate([
  // Group by field and calculate the average research impact
  {
    $group: { 
      _id: '$field', 
      averageCitationImpact: { 
        $avg: { $size: '$citations' } 
      } 
    } 
  },
  // Sort by average citation impact in descending order 
  { 
    $sort: { 
      averageCitationImpact: -1 
    } 
  }
]);

// Kaung st124974

// List All Institutions That Have Collaborated on More Than 10 Joint Publications
db.collaboration_network.find(
  { 'jointPublications': { $gt: 10 } },
  { 'institutionId': 1, '_id': 0 }
)

// Retrieve All Publications That Have at Least certain count of Citations and Belong to the ‘AI Ethics’ Field
db.citation_network.aggregate([
  {
    $lookup: {
      from: "publication",
      localField: "citedPublicationId",
      foreignField: "publicationId",
      as: "PublicationDetails"
    }
  },
  { $unwind: "$PublicationDetails" },
  { $match: { "PublicationDetails.field": "AI Ethics" } },
  {
    $group: {
      _id: "$citedPublicationId",
      citationCount: { $sum: 1 }
    }
  },
  { $match: { citationCount: { $gte: 3 } } }
]);

// Find the Research Topics That Have Gained Popularity (TrendIndex > 80)
db.research_topic.find(
  { 'trendIndex': { $gt: 80 } },
  { 'name': 1, '_id': 0 }
)

// Find The Average Citation Impact for Each Research Institution
db.citation_network.aggregate([
  {
    $lookup: {
      from: "publication",
      localField: "citedPublicationId",
      foreignField: "publicationId",
      as: "PublicationDetails"
    }
  },
  { $unwind: "$PublicationDetails" },
  {
    $group: {
      _id: "$PublicationDetails.institutionId",
      avgImpact: { $avg: "$citationImpact" }
    }
  }
]);

// Identify grants titles and amounts greater than 100k that intituions have received 
db.institution.aggregate([
  {
    $lookup: {
      from: "grants",
      localField: "institutionId",
      foreignField: "institutionId",
      as: "InstitutionGrants"
    }
  },
  {
    $unwind: {
      path: "$InstitutionGrants",
      preserveNullAndEmptyArrays: true
    }
  },
  {
    $project: {
      _id: 0,
      institutionId: "$institutionId",
      institutionName: "$name",
      grantTitle: {
        $ifNull: ["$InstitutionGrants.title", "No Grants"]
      },
      amount: {
        $ifNull: ["$InstitutionGrants.amount", 0]
      }
    }
  },
  {
    $match: {
      amount: { $gt: 1000000 }
    }
  },
  {
    $sort: { amount: -1 }
  }
]); 


// Suryansh st12499
// List Conferences That Have Published the Most Research Papers
use('StochasticallyYours');

db.getCollection('publication').aggregate([
  -- Match documents where the venue type is 'Conference'
  { 
    $match: { 'venue.type': 'Conference' } 
  },
  // Group by venueId and count the number of publications for each conference
  {
    $group: {
      _id: '$venue.venueId',
      publicationCount: { $sum: 1 }
    }
  },
  // Sort by publication count in descending order
  { 
    $sort: { publicationCount: -1 } 
  },
  // Optionally, limit the number of results if needed
  { 
    $limit: 10 
  }
]);

// Find the Success Rate of Institution Collaborations
use('StochasticallyYours');

db.getCollection('collaboration_network').aggregate([
  {
    $project: {
      institutionId: 1,
      successRate: {
        $cond: {
          if: { $gt: [ "$partnerCount", 0 ] },
          then: { $divide: [ "$jointPublications", "$partnerCount" ] },
          else: 0
        }
      }
    }
  }
]);

// Identify Top Funded Research Groups
use('StochasticallyYours');

db.getCollection('research_group').aggregate([
  -- Project the necessary fields and calculate the number of grants
  {
    $project: {
      name: 1,
      grantsCount: { $size: "$grants" }
    }
  },
  // Sort the groups by the number of grants in descending order
  {
    $sort: { grantsCount: -1 }
  },
  // Limit the results to the top funded groups
  {
    $limit: 10
  }
]);

// Find Publications That Have Been Cited in More Than 3 times in a Different Fields
use('StochasticallyYours');

db.getCollection('publication').aggregate([
  // Unwind the citations array to get individual citation entries
  { $unwind: '$citations' },

  // Group by publication ID and field, and count citations
  { 
    $group: { 
      _id: { publicationId: '$_id', field: '$field' }, 
      citationCount: { $sum: 1 } 
    } 
  },

  // Match groups with more than 3 citations
  { $match: { citationCount: { $gt: 3 } } },

  // Lookup to get the full publication details
  { 
    $lookup: {
      from: 'publication',
      localField: '_id.publicationId',
      foreignField: '_id',
      as: 'publicationDetails'
    } 
  },

  // Unwind the publication details array
  { $unwind: '$publicationDetails' },

  // Project the required fields
  { 
    $project: {
      _id: 0,
      publicationId: '$_id.publicationId',
      title: '$publicationDetails.title',
      field: '$_id.field',
      citationCount: 1
    } 
  }
]);

// Find the Average Research Budget of Institutions That Have More Than 10 Departments
use("StochasticallyYours");
db.getCollection('institution').aggregate([
    // Match institutions with more than 10 departments
    { $match: { departmentCount: { $gt: 10 } } },
    
    // Group to calculate the average research budget
    {
        $group: {
            _id: "$name",
            averageResearchBudget: { $avg: "$researchBudget" }
        }
    }
]);

// Swaraj 125052

// Retrieve Publications Published in 2025
use('StochasticallyYours');

db.publication.find(
  { 
    "publicationDate": { 
      $gte: "2023-01-01", 
      $lt: "2024-01-01" 
    } 
  }
);

// Find Research Fields With Most Publications
use('StochasticallyYours');

db.publication.aggregate([
  { 
    $group: { 
      _id: "$field", 
      totalPublications: { $sum: 1 } 
    } 
  },
  { 
    $sort: { totalPublications: -1 } 
  }
]);

// Find Institutions That Offer the Most Research Grants
use('StochasticallyYours');

db.getCollection('grants').aggregate([
  // Group by agencyId and count the number of grants for each institution
  { 
    $group: { 
      _id: '$agencyId', 
      totalGrants: { $sum: 1 } 
    } 
  },
  // Sort by the number of grants in descending order
  { 
    $sort: { totalGrants: -1 } 
  },
  // Limit to the top institutions
  { 
    $limit: 10 
  }
]);

// List All Countries That Have More Than 10 Research Institutions    
use('StochasticallyYours');

// List All Countries That Have More Than 10 Research Institutions
db.country.aggregate([
  {
    $lookup: {
      from: "institution",
      localField: "name",
      foreignField: "countryId",
      as: "Institutions"
    }
  },
  {
    $group: {
      _id: "$name",
      institutionCount: { $sum: { $size: "$Institutions" } }
    }
  },
  {
    $match: { "institutionCount": { $gt: 10 } }
  }
]);

// Find the Most Common Grant Types Issued by Funding AgenciesBased on Certain Keywords mentioned in the Grant Description
use('StochasticallyYours');

db.getCollection('grants').aggregate([
  // Match documents where the description mentions a particular field
  { 
    $match: { description: /renewable energy/i } 
  },
  // Group by agencyId and count the number of grants for each agency
  { 
    $group: { _id: '$agencyId', count: { $sum: 1 } } 
  },
  // Sort by count in descending order to find the most common grant types
  { 
    $sort: { count: -1 } 
  }
]);
