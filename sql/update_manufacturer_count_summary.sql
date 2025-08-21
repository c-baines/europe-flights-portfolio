-- Query to delete counts for the present year and then recount manufacturers 
-- 29/7/25

WITH deleted AS (
    DELETE FROM manufacturer_count_summary
    WHERE year = 2025 -- want to find a way to get present year rather than hard coding 
    )
    INSERT INTO manufacturer_count_summary (count, year, manufacturer)
    SELECT 
    COUNT(*) AS count,
    DATE_PART('year', dof)::int AS year,
    CASE
        WHEN model ILIKE '%BOEING%' 
        OR model ~* '^7[2-8]\d' 
        THEN 'Boeing'
        
        WHEN model ILIKE '%AIRBUS%' 
        OR model ~* '^A-?3\d' 
        OR model ~* '^A2\d' 
        OR model ~* '^A1\d' 
        OR model ILIKE '%MBB%' 
        OR model ILIKE '%EC%'
        THEN 'Airbus'
        
        WHEN model ILIKE '%EMBRAER%' 
        OR model ~* '^E\d' 
        OR model ILIKE '%EMB%' 
        OR model ILIKE '%ERJ%' 
        OR model ILIKE '%PHENOM%' 
        THEN 'Embraer'
        
        WHEN model ILIKE '%BOMBARDIER%' 
        OR model ILIKE '%CRJ%' 
        OR model ILIKE '%CHALLENGER%' 
        OR model ILIKE '%DHC%' 
        OR model ILIKE '%BD%' 
        OR model ILIKE '%GLOBAL EXPRESS%'
        THEN 'Bombardier'
        
        WHEN model ILIKE '%ATR%' 
        THEN 'ATR'
        
        WHEN model ILIKE '%CESSNA%' 
        OR model ILIKE '%CITATION%' 
        OR model ~* '^C-?\d{3}' 
        THEN 'Cessna'
        
        WHEN model ILIKE '%PIPER%' 
        OR model ILIKE 'PA-%' 
        THEN 'Piper'

        WHEN model ILIKE '%GROUND VEHICLE%'
        OR model ILIKE '%MAINTAINANCE%'
        OR model ILIKE '%AIRPORT%FIRE%'
        OR model ILIKE '%FIRE%RESCUE%'
        OR model ILIKE '%FIRE%DEP%'
        OR model ILIKE 'FIRE%ENGINE%'
        OR model ILIKE '%SNOW AND CLEANING%'
        THEN 'Ground Support Equipment (GSE)'
        
        WHEN model IS NULL
        THEN 'Not recorded'
        
        ELSE 'Other'
    END AS manufacturer
    FROM flight_list
    WHERE DATE_PART('year', dof)::int = 2025
    GROUP BY 
    DATE_PART('year', dof)::int,
    CASE
        WHEN model ILIKE '%BOEING%' 
        OR model ~* '^7[2-8]\d' 
        THEN 'Boeing'
        
        WHEN model ILIKE '%AIRBUS%' 
        OR model ~* '^A-?3\d' 
        OR model ~* '^A2\d' 
        OR model ~* '^A1\d' 
        OR model ILIKE '%MBB%' 
        OR model ILIKE '%EC%'
        THEN 'Airbus'
        
        WHEN model ILIKE '%EMBRAER%' 
        OR model ~* '^E\d' 
        OR model ILIKE '%EMB%' 
        OR model ILIKE '%ERJ%' 
        OR model ILIKE '%PHENOM%' 
        THEN 'Embraer'
        
        WHEN model ILIKE '%BOMBARDIER%' 
        OR model ILIKE '%CRJ%' 
        OR model ILIKE '%CHALLENGER%' 
        OR model ILIKE '%DHC%' 
        OR model ILIKE '%BD%' 
        OR model ILIKE '%GLOBAL EXPRESS%'
        THEN 'Bombardier'
        
        WHEN model ILIKE '%ATR%' 
        THEN 'ATR'
        
        WHEN model ILIKE '%CESSNA%' 
        OR model ILIKE '%CITATION%' 
        OR model ~* '^C-?\d{3}' 
        THEN 'Cessna'
        
        WHEN model ILIKE '%PIPER%' 
        OR model ILIKE 'PA-%' 
        THEN 'Piper'

        WHEN model ILIKE '%GROUND VEHICLE%'
        OR model ILIKE '%MAINTAINANCE%'
        OR model ILIKE '%AIRPORT%FIRE%'
        OR model ILIKE '%FIRE%RESCUE%'
        OR model ILIKE '%FIRE%DEP%'
        OR model ILIKE 'FIRE%ENGINE%'
        OR model ILIKE '%SNOW AND CLEANING%'
        THEN 'Ground Support Equipment (GSE)'
        
        WHEN model IS NULL
        THEN 'Not recorded'
        
        ELSE 'Other'
    END;