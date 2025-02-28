------------- x -------------
-- Arya's queries
------------- x -------------

-- 1. Update the Field Weight Citation Impact based on the weighted average of the citation scores of all publications linked to the researcher. (DONE)
UPDATE ResearchImpact RI
INNER JOIN (
  SELECT DG.PublicationID, IFNULL(AVG(P.CitationCount * 0.75), 0) AS AvgImpact
  FROM DatasetGroup DG
  INNER JOIN Publication P ON DG.PublicationID = P.PublicationID
  GROUP BY DG.PublicationID
) AS ImpactCalc ON RI.PublicationID = ImpactCalc.PublicationID
SET RI.FieldWeightImpact = ImpactCalc.AvgImpact;


-- 2. Increase the ranking of institutions with a high collaboration success rate and significant joint Publications. (DONE)
UPDATE Institution I
SET Ranking = GREATEST(1, Ranking - 2)
WHERE InstitutionID IN (
  SELECT CN.InstitutionID
  FROM CollaborationNetwork CN
  WHERE CN.SuccessRate > 0.8 AND CN.JointPublications > 50
);


-- 3. Update the Publication table to ARCHIVE  publications older than 5 years and consider only those that have low citation impact maybe less than 10 citations (DONE)

UPDATE Publication P
JOIN (
    SELECT 
        P.PublicationID,
        COUNT(DISTINCT C.ConferenceID) AS ConferenceCount
    FROM Publication P
    LEFT JOIN Conference C ON P.ConferenceID = C.ConferenceID
    GROUP BY P.PublicationID
    HAVING ConferenceCount > 0
) AS Stats ON P.PublicationID = Stats.PublicationID
SET P.Status = 'ARCHIVED'
WHERE P.PublicationDate < DATE_SUB('2025-02-04', INTERVAL 5 YEAR)
AND P.CitationCount < 10;


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

------------- x -------------
-- Swaraj's queries
------------- x -------------

-- 1. Update the citation impact in the network based on new citations (DONE)
UPDATE CitationNetwork
SET CitationImpact = CitationImpact + (
  SELECT IFNULL(AVG(CitationCount), 0)
  FROM Publication
  WHERE PublicationID = CitedPublicationID
)
WHERE CitingPublicationID IN (
  SELECT PublicationID FROM Publication WHERE PublicationDate >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
);


-- 2. Update the member count of a research group based on the actual number of researchers linked to it.
UPDATE ResearchGroup RG
INNER JOIN (
  SELECT GroupID, COUNT(1) AS LeaderCount
  FROM ResearchGroup
  INNER JOIN Researcher ON ResearchGroup.Leader = Researcher.ResearcherID
  GROUP BY GroupID
) AS LeaderCounts ON RG.GroupID = LeaderCounts.GroupID
SET RG.MemberCount = LeaderCounts.LeaderCount;


-- 3. Update the journal acceptance rate based on review outcomes.
UPDATE Journal J
INNER JOIN (
  SELECT 
    J.JournalID,
    (COUNT(CASE WHEN R.Decision = 'Accepted' THEN 1 END) * 100.0 / NULLIF(COUNT(1), 0)) AS AcceptRate
  FROM Journal J
  LEFT JOIN Publication P ON J.JournalID = P.JournalID
  LEFT JOIN Review R ON P.PublicationID = R.PublicationID
  GROUP BY J.JournalID
) AS Stats ON J.JournalID = Stats.JournalID
SET J.AcceptanceRate = Stats.AcceptRate;



-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

------------- x -------------
-- Suryansh's queries
------------- x -------------

-- 1. If a dataset is used in a new publication, update its version to the latest.
UPDATE Dataset D
INNER JOIN DatasetGroup DG ON D.DatasetID = DG.DatasetID
INNER JOIN Publication P ON DG.PublicationID = P.PublicationID
SET D.Version = CONCAT(
    SUBSTRING_INDEX(D.Version, '.', 1),
    '.',
    CAST(SUBSTRING_INDEX(D.Version, '.', -1) AS UNSIGNED) + 1
)
WHERE P.PublicationDate = DATE_SUB(CURDATE(), INTERVAL 30 DAY);

-- 2. Rank institutions higher if their researchers have achieved new impactful publications.
UPDATE Institution
SET Ranking = GREATEST(1, Ranking - 1)
WHERE InstitutionID IN (
  SELECT InstitutionID
  FROM Researcher R
  JOIN Publication P ON P.PublicationID = R.ResearcherID
  WHERE P.CitationCount > 100
);


-- 3. Update the total citations for a researcher across all their publications.
UPDATE Researcher
SET TotalCitations = (
  SELECT COALESCE(SUM(CitationCount), 0)
  FROM Publication
  WHERE PublicationID IN (
    SELECT PublicationID FROM DatasetUsage WHERE DatasetUsage.PublicationID = Researcher.ResearcherID
  )
)
WHERE EXISTS (
  SELECT 1
  FROM Publication
  WHERE PublicationID IN (
    SELECT PublicationID FROM DatasetUsage WHERE DatasetUsage.PublicationID = Researcher.ResearcherID
  )
);

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- TODO :: Add your update queries below this line after verifying that they are producing the desired results.
------------- x -------------
-- Kaung's queries
------------- x -------------

-- update Researcher r total citations based on publications
update Researcher r
set r.TotalCitations = (
  select SUM(p.CitationCount)
  from PublicationNetwork pn
  join Publication p on pn.PublicationID = p.PublicationID
  where pn.ResearcherID = r.ResearcherID
);

-- UPDATE DEPARTMENT BUDGET BASED ON RESEARCH GROUP GRANT ALLOCATIONS
UPDATE Department d
LEFT JOIN (
  SELECT r.DepartmentID, SUM(g.Amount) as TotalGrant
  FROM ResearchGroup rg
  JOIN Researcher r ON rg.Leader = r.ResearcherID
  JOIN Grants g ON rg.GrantID = g.GrantID
  GROUP BY r.DepartmentID
) t ON d.DepartmentID = t.DepartmentID
SET d.Budget = d.Budget + t.TotalGrant;

-- Update Research Group's Member Count
UPDATE 
  ResearchGroup rg
SET 
  rg.MemberCount = (
    SELECT 
      COUNT(*) 
    FROM 
      ResearchGroupMembers rgm
    WHERE 
      rgm.ResearchGroupID = rg.GroupID
  );
