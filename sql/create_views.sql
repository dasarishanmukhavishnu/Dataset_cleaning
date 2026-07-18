/*Show each department with the total number of employees, average salary, minimum salary, and maximum salary.*/

CREATE OR REPLACE  VIEW vw_department_summary AS 
SELECT 
    Department,
    COUNT(Employee_ID) AS Total_Employees,
    ROUND(AVG(Salary),2) AS Average_Salary,
    MIN(Salary) AS Min_Salary,
    MAX(Salary) AS Max_Salary
FROM Employees
Group BY Department;

/*Show each region with the total number of employees, average salary, minimum salary, and maximum salary.*/

CREATE OR REPLACE  VIEW vw_region_summary AS 
SELECT 
    Region,
    COUNT(Employee_ID) AS Total_Employees,
    ROUND(AVG(Salary),2) AS Average_Salary,
    MIN(Salary) AS Min_Salary,
    MAX(Salary) AS Max_Salary
FROM Employees
Group BY Region;

/*Show each performance score with the number of employees and average salary.*/

CREATE OR REPLACE VIEW vw_performance_score AS
SELECT 
    Performance_Score,
    COUNT(Employee_ID) AS Total_Employees,
    ROUND(AVG(Salary),2) AS Average_Salary
FROM Employees
GROUP BY Performance_Score;

/*Compare remote and office employees by showing total employees and average salary for each work mode.*/

CREATE OR REPLACE VIEW vw_remote_summary AS
SELECT 
    Remote_Work,
    COUNT(Employee_ID) AS Total_Employees,
    ROUND(AVG(Salary),2) AS Average_Salary
FROM Employees
GROUP BY Remote_Work;

/*Show each employee status with the total number of employees and average salary.*/


CREATE OR REPLACE VIEW vw_status_summary AS
SELECT 
    Status,
    COUNT(Employee_ID) AS Total_Employees,
    ROUND(AVG(Salary),2) AS Average_Salary
FROM Employees
GROUP BY Status;

/*For each department in every region, show the employee count and average salary.*/

CREATE OR REPLACE VIEW vw_dept_region_summary AS
SELECT 
    Department,
    Region,
    COUNT(Employee_ID) AS Total_Employees,
    ROUND(AVG(Salary),2) AS Average_Salary
FROM Employees
GROUP BY Department,Region;

/*Group employees into age ranges (Under 25, 25-34, 35-44, 45+) and show employee count, average salary, minimum salary, and maximum salary for each group.*/

CREATE OR REPLACE VIEW vw_age_group_summary AS
SELECT 
    CASE 
        WHEN Age < 25 THEN 'Under 25'
        WHEN Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN AGE BETWEEN 35 AND 44 THEN '35-44'
        ELSE '45+'
    END AS Age_Group,
    COUNT(Employee_ID) AS Total_Employees,
    ROUND(AVG(Salary),2) AS Average_Salary,
    MIN(Salary) AS Min_Salary,
    MAX(Salary) AS Max_Salary
FROM Employees
GROUP BY Age_Group;

/*Show the number and percentage of valid and invalid phone numbers.*/

CREATE OR REPLACE VIEW vw_phno_valid_summary AS
SELECT
    phno_is_valid,
    COUNT(Employee_ID) AS Total_Employees,
    ROUND(COUNT(Employee_ID) * 100 / (SELECT COUNT(*) FROM Employees),2) AS Percentage 
FROM Employees
GROUP BY phno_is_valid;

/*Create a one-row summary containing:

Total Employees
Average Salary
Highest Salary
Lowest Salary
Total Departments
Total Regions
Total Remote Employees
Total Invalid Phone Numbers */

CREATE OR REPLACE VIEW vw_hr_dashboard AS
SELECT
    COUNT(Employee_ID) AS Total_Employees,
    ROUND(AVG(Salary),2) AS Average_Salary,
    MAX(Salary) AS Highest_Salary,
    MIN(Salary) AS Lowest_Salary,
    COUNT(DISTINCT Department) AS Total_Departments,
    COUNT(DISTINCT Region) AS Total_Regions,
    SUM(Remote_Work) AS Total_Remote_Workers,
    COUNT(*) - SUM(phno_is_valid) AS Total_Invalid_PHNO
FROM Employees;
