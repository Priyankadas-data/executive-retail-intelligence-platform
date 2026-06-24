SELECT Region, Category, SUM(Sales) AS Total_Sales, SUM(Profit) AS Total_Profit
FROM superstore
GROUP BY Region, Category;