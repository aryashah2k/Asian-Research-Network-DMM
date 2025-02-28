------------- x -------------
-- Arya's queries
------------- x -------------
-- 1. Rank researchers based on their total citations within their respective institutions.
SELECT 
    R.ResearcherID,
    R.FirstName,
    R.LastName,
    R.TotalCitations,
    I.Name AS InstitutionName,
    RANK() OVER (PARTITION BY I.InstitutionID ORDER BY R.TotalCitations DESC) AS ResearcherRank
FROM Researcher R
INNER JOIN Institution I ON R.CurrentPositionId = I.InstitutionID;


-- 2. Calculate the total grant amount, average amount, and the number of grants for each funding agency.
SELECT 
    F.AgencyID,
    F.Name AS FundingAgency,
    COUNT(G.GrantID) AS TotalGrants,
    SUM(G.Amount) AS TotalAmountFunded,
    AVG(G.Amount) AS AverageGrantAmount
FROM FundingAgency F
LEFT OUTER JOIN Grants G ON F.AgencyID = G.FundingAgencyId
GROUP BY F.AgencyID, F.Name
HAVING TotalGrants > 5
ORDER BY TotalAmountFunded DESC;


-- 3. List publications with zero citations and the total count of such publications. 
WITH NoCitationPublications AS (
    SELECT PublicationID, Title, CitationCount
    FROM Publication
    WHERE CitationCount = 0
)
SELECT 
    PublicationID,
    Title,
    (SELECT COUNT(*) FROM NoCitationPublications) AS TotalNoCitationCount
FROM NoCitationPublications;


-- 4. Compute the average trend index and rank research topics by their popularity score
SELECT 
    TopicID,
    Name AS ResearchTopic,
    PopularityScore,
    AVG(TrendIndex) OVER (PARTITION BY TopicID) AS AvgTrendIndex,
    RANK() OVER (ORDER BY PopularityScore DESC) AS PopularityRank
FROM ResearchTopic
WHERE PopularityScore > 0;


-- 5. List the top institutions with the highest number of collaborations and calculate the average success rate
SELECT 
    CN.InstitutionID,
    I.Name AS InstitutionName,
    CN.PartnerCount,
    CN.SuccessRate,
    AVG(CN.SuccessRate) OVER () AS AvgSuccessRate
FROM CollaborationNetwork CN
JOIN Institution I ON CN.InstitutionID = I.InstitutionID
WHERE CN.PartnerCount > 0
ORDER BY CN.PartnerCount DESC;
-- this query helps print the institute name along with the ID making it easier to identify the institute.


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

------------- x -------------
-- Swaraj's queries
------------- x -------------

-- 1. FIND THE MOST CITED PUBLICATION FOR EACH YEAR.
SELECT 
    YEAR(PublicationDate) AS Year,
    Title,
    MAX(CitationCount) AS MaxCitations
FROM Publication
GROUP BY YEAR(PublicationDate), Title
ORDER BY Year DESC, MaxCitations DESC;


-- 2. Calculate the success rate of grants for each funding agency based on approved grants.
SELECT 
    F.Name AS FundingAgency,
    COUNT(CASE WHEN G.GrantStatus = 'Approved' THEN 1 END) AS ApprovedGrants,
    COUNT(G.GrantID) AS TotalGrants,
    (COUNT(CASE WHEN G.GrantStatus = 'Approved' THEN 1 END) * 100.0 / COUNT(G.GrantID)) AS SuccessRate
FROM FundingAgency F
LEFT OUTER JOIN Grants G ON F.AgencyID = G.FundingAgencyId
GROUP BY F.AgencyID, F.Name
HAVING COUNT(G.GrantID) > 0
ORDER BY SuccessRate DESC;


-- 3. RETRIEVE PUBLICATIONS WITH DETAILS OF DATASETS THEY HAVE USED, 
SELECT 
    P.PublicationID,
    P.Title,
    COUNT(DU.DatasetID) AS DatasetsUsed
FROM Publication P
LEFT OUTER JOIN DatasetGroup DU ON P.PublicationID = DU.PublicationID
GROUP BY P.PublicationID, P.Title
HAVING COUNT(DU.DatasetID) > 0
ORDER BY DatasetsUsed DESC, P.PublicationDate DESC;


-- 4. IDENTIFY THE TOP 5 PUBLICATIONS BASED ON THEIR CITATION IMPACT FROM THE CITATION NETWORK.
SELECT 
    P.PublicationID,
    P.Title,
    CN.CitationImpact
FROM Publication P
INNER JOIN CitationNetwork CN ON P.PublicationID = CN.CitedPublicationID
ORDER BY CN.CitationImpact DESC
LIMIT 5;


-- 5. CALCULATE THE AVERAGE CITATION IMPACT FOR EACH RESEARCH TOPIC
SELECT RT.TopicID, RT.Name, AVG(CN.CitationImpact) AS AvgCitationImpact
FROM ResearchTopic RT
INNER JOIN CitationNetwork CN ON CN.CitedPublicationID = RT.TopicID
GROUP BY RT.TopicID, RT.Name;



-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

------------- x -------------
-- Suryansh's queries
------------- x -------------

-- 1. List institutions with their research groups, including total members and projects for each group.
SELECT 
    I.InstitutionID,
    I.Name AS InstitutionName,
    RG.GroupID,
    RG.Name AS ResearchGroupName,
    RG.MemberCount,
    RG.ProjectCount
FROM Institution I
INNER JOIN ResearchGroup RG ON I.InstitutionID = RG.Leader
WHERE RG.MemberCount > 5 AND RG.ProjectCount > 2
ORDER BY RG.MemberCount DESC;


-- 2. SHOW PUBLICATIONS WITH THE HIGHEST CITATION IMPACT IN THE NETWORK.
SELECT C.CitedPublicationID, P.Title, C.CitationImpact
FROM CitationNetwork C
INNER JOIN Publication P ON C.CitedPublicationID = P.PublicationID
ORDER BY C.CitationImpact DESC
LIMIT 10;


-- 3. Retrieve conferences with the highest number of submissions and the best acceptance rates below 30%.
SELECT 
    C.ConferenceID,
    C.Name,
    C.SubmissionDeadline,
    C.AcceptanceRate
FROM Conference C
WHERE C.AcceptanceRate < 0.3
ORDER BY C.SubmissionDeadline ASC, C.AcceptanceRate ASC
LIMIT 5;


-- 4. Identify researchers who have authored publications in more than two different languages.
SELECT 
    R.ResearcherID,
    R.FirstName,
    R.LastName,
    COUNT(DISTINCT P.Language) AS LanguageCount
FROM Researcher R
INNER JOIN PublicationNetwork PR ON R.ResearcherID = PR.ResearcherID
INNER JOIN Publication P ON PR.PublicationID = P.PublicationID
GROUP BY R.ResearcherID, R.FirstName, R.LastName
HAVING LanguageCount > 2
ORDER BY LanguageCount DESC;


-- 5. List research groups with the highest number of projects and their respective leaders.
SELECT 
    RG.GroupID,
    RG.Name AS ResearchGroupName,
    R.FirstName AS LeaderFirstName,
    R.LastName AS LeaderLastName,
    RG.ProjectCount AS ProjectCount
FROM ResearchGroup RG
INNER JOIN Researcher R ON RG.Leader = R.ResearcherID
WHERE RG.ProjectCount > 0
ORDER BY RG.ProjectCount DESC
LIMIT 10;

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

------------- x -------------
-- Kaung's queries
------------- x -------------

-- Find top 10 researchers with highest citation count in a specific field
SELECT
	R.ResearcherID,
    R.FirstName,
    R.LastName,
    R.TotalCitations,
    P.Field
FROM Researcher R
INNER JOIN PublicationNetwork PN on R.ResearcherID = PN.ResearcherID
INNER JOIN Publication P on P.PublicationID = PN.PublicationID
WHERE P.Field = 'Artificial Intelligence'
ORDER BY R.TotalCitations DESC
LIMIT 10;


-- Retrieve top 10 publications with the highest impact in a given year
SELECT 
	P.PublicationID,
    P.Title,
    P.PublicationDate,
    RI.CitationScore,
    RI.FieldWeightImpact,
    RI.IndustryImpact
FROM Publication P
INNER JOIN ResearchImpact RI ON P.PublicationID = RI.PublicationID
WHERE YEAR (P.PublicationDate) = 2023
ORDER BY RI.FieldWeightImpact DESC
LIMIT 10;


-- Find top 10 research groups with most successful grants
select 
    rg.GroupID,
    rg.Name as GroupName,
    count(g.GrantID) as SuccessfulGrantCount
from ResearchGroup rg
join Grants g on concat('GRANT_',rg.GrantID) = g.GrantID
where g.GrantStatus = 'APPROVED'
GROUP by rg.GroupID
order by SuccessfulGrantCount desc
limit 10;


-- Find the top 10 Institutions with highest successrate and their national country
select 
	i.`Name` as InstitutionName,
    c.CountryName,
    cn.SuccessRate
from CollaborationNetwork cn
join Institution i on cn.InstitutionID = i.InstitutionID
join Country c on i.CountryID = c.CountryID
order by cn.SuccessRate desc 
limit 10;


-- Find top 10 high impact publications with Journals in English Language and status accepted  for each field
select 
	p.Field, 
    p.PublicationID, 
    p.Title, 
    j.Name as JournalName, 
    j.ImpactFactor,
    p.Status
from Publication p
join Journal j on p.JournalID = j.JournalID
where j.ImpactFactor >= (SELECT AVG(ImpactFactor) FROM Journal)
and p.Language = 'English'
and p.Status = 'ACCEPTED'
order by p.Field, j.ImpactFactor desc
limit 10;

-- Find the top 10 Institutions with higest successrate and their national country

select distinct 
    r.ResearcherID,
    r.FirstName,
    r.LastName,
    j.JournalID,
    j.`Name` as JournalName,
    p.PublicationID,
    p.Title
from Researcher r
join PublicationNetwork pn on r.ResearcherID = pn.ResearcherID
join Publication p on p.PublicationID = pn.PublicationID
join Journal j on j.JournalID = p.JournalID
where j.ImpactFactor >= (SELECT AVG(ImpactFactor) FROM Journal)
order by r.ResearcherID;