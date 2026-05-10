SELECT COUNT(*) FROM cleaned_complaints_dataset;
SELECT 
    sentiment,
    COUNT(*) AS total_reviews
FROM cleaned_complaints_dataset
GROUP BY sentiment
ORDER BY total_reviews DESC;

SELECT 
    app_name,
    ROUND(AVG(rating), 2) AS average_rating
FROM cleaned_complaints_dataset
GROUP BY app_name
ORDER BY average_rating DESC;


SELECT 
    app_name,
    review,
    rating,
    escalation_risk
FROM cleaned_complaints_dataset
WHERE escalation_risk = 'High';

SELECT 
    category,
    COUNT(*) AS total_reviews
FROM cleaned_complaints_dataset
GROUP BY category
ORDER BY total_reviews DESC;

SELECT 
    review_date,
    COUNT(*) AS total_reviews
FROM cleaned_complaints_dataset
GROUP BY review_date
ORDER BY total_reviews DESC
LIMIT 10;

SELECT 
    app_name,
    review,
    likes
FROM cleaned_complaints_dataset
ORDER BY likes DESC
LIMIT 10;

SELECT 
    app_name,
    review,
    rating,
    sentiment
FROM cleaned_complaints_dataset
WHERE sentiment = 'Negative'
AND rating <= 2;
