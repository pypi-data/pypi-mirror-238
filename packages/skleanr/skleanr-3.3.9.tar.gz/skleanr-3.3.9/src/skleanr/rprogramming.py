
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

1) Write a R program to create a Data Frame which contain details of 5 employees and display summary of the data using R.

library(ggplot2)
library(gridExtra)
library(dplyr)

# Create a data frame with employee details
employee_data <- data.frame(
  EmployeeID = c(1, 2, 3, 4, 5),
  FirstName = c("John", "Jane", "Robert", "Samantha", "Michael"),
  LastName = c("Doe", "Smith", "Johnson", "Williams", "Brown"),
  Age = c(30, 28, 35, 29, 32),
  Department = c("HR", "Finance", "IT", "Sales", "Marketing"),
  Salary = c(50000, 60000, 75000, 55000, 65000)
)

# Display the data frame
print(employee_data)

# Display a summary of the data
summary(employee_data)

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

2) For anydataset visialize the following types of chart : Scatterplot. Bubble Chart, Bar Chart , Dot Plots ,Histogram ,Box Plot ,Pie Chart

library(ggplot2)
library(dplyr)
library(gridExtra)

# Sample data
set.seed(123)
data <- data.frame(
  X = rnorm(100),
  Y = rnorm(100),
  Category = factor(sample(1:5, 100, replace = TRUE)),
  Size = runif(100, 1, 5),
  Value = rpois(100, lambda = 5)
)

# Scatterplot
scatterplot <- ggplot(data, aes(x = X, y = Y, color = Category)) +
  geom_point() +
  labs(title = "Scatterplot")

# Bubble Chart
bubble_chart <- ggplot(data, aes(x = X, y = Y, size = Size, color = Category)) +
  geom_point() +
  labs(title = "Bubble Chart")

# Bar Chart
bar_chart <- ggplot(data, aes(x = Category)) +
  geom_bar() +
  labs(title = "Bar Chart")

# Dot Plots
dot_plots <- ggplot(data, aes(x = Value)) +
  geom_histogram(binwidth = 0.5, fill = "blue", color = "black") +
  labs(title = "Dot Plots")

# Histogram
histogram <- ggplot(data, aes(x = X)) +
  geom_histogram(binwidth = 0.2, fill = "lightblue") +
  labs(title = "Histogram")

# Box Plot
box_plot <- ggplot(data, aes(x = Category, y = X, fill = Category)) +
  geom_boxplot() +
  labs(title = "Box Plot")

# Pie Chart
pie_chart_data <- data %>%
  group_by(Category) %>%
  summarize(Count = n())
pie_chart <- ggplot(pie_chart_data, aes(x = "", y = Count, fill = Category)) +
  geom_bar(stat = "identity") +
  coord_polar(theta = "y") +
  labs(title = "Pie Chart")

# Arrange and display the charts
grid.arrange(scatterplot, bubble_chart, bar_chart, dot_plots, histogram, box_plot, pie_chart, ncol = 2)




////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

3) Write the script in R to sort the values contained in the following vector in ascending order and descending order: (23, 45, 10, 34, 89, 20, 67, 99).
Demonstrate the output using graph.

library(ggplot2)
library(gridExtra)
library(dplyr)

# Vector of values
values <- c(23, 45, 10, 34, 89, 20, 67, 99)

# Sort the vector in ascending order
sorted_values_asc <- sort(values)

# Sort the vector in descending order
sorted_values_desc <- sort(values, decreasing = TRUE)

# Create a data frame for visualization
data_df <- data.frame(
  Values = c(sorted_values_asc, sorted_values_desc),
  Order = rep(c("Ascending", "Descending"), each = length(values))
)

# Load necessary libraries
library(ggplot2)

# Create a line plot for visualization
line_plot <- ggplot(data_df, aes(x = 1:length(Values), y = Values, group = Order, color = Order)) +
  geom_line() +
  geom_point() +
  labs(title = "Sorted Values in Ascending and Descending Order", x = "Index", y = "Value") +
  scale_color_manual(values = c("Ascending" = "blue", "Descending" = "red"))

# Display the line plot
print(line_plot)



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

4)  The following table shows the number of units of different products sold on different days:
Create five sample numeric vectors from this data visualize data using R.

library(ggplot2)
library(gridExtra)
library(dplyr)

# Load necessary libraries
library(ggplot2)
library(gridExtra)
library(dplyr)

# Create a data frame for the sales data
sales_data <- data.frame(
  Week = 1:5,
  Bread = c(12, 3, 5, 11, 9),
  Milk = c(21, 27, 18, 20, 15),
  Cola = c(10, 1, 33, 6, 12),
  Chocolate = c(6, 7, 4, 13, 12),
  Detergent = c(5, 8, 12, 20, 23)
)

# Create a line plot to visualize sales over time
ggplot(sales_data, aes(x = Week)) +
  geom_line(aes(y = Bread, color = "Bread"), linewidth = 1) +
  geom_line(aes(y = Milk, color = "Milk"),linewidth = 1) +
  geom_line(aes(y = Cola, color = "Cola"), linewidth = 1) +
  geom_line(aes(y = Chocolate, color = "Chocolate"), linewidth = 1) +
  geom_line(aes(y = Detergent, color = "Detergent"), linewidth = 1) +
  labs(title = "Product Sales Over Time", x = "Week", y = "Sales") +
  scale_color_manual(values = c("Bread" = "blue", "Milk" = "green", "Cola" = "red", "Chocolate" = "purple", "Detergent" = "orange")) +
  theme_minimal()


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

5) Consider the following data frame given below:
(i) Create a subset of subject less than 4 by using subset () funcon and demonstrate the output.
(ii) Create a subject where the subject column is less than 3 and the class equals to 2 by using [] brackets and demonstrate the output using R

# Load necessary libraries
library(ggplot2)
library(gridExtra)
library(dplyr)

# Create the data frame
df <- data.frame(
  Subject = c(1, 2, 1, 2, 1, 2),
  Class = c(1, 2, 1, 2, 1, 2),
  Marks = c(56, 75, 48, 69, 84, 53)
)


# Create a subset where Subject < 3 and Class == 2
subset_df <- df[df$Subject < 3 & df$Class == 2, ]

# View the subset
print(subset_df)

# Create a scatterplot to visualize the relationship between Subject and Marks
ggplot(df, aes(x = Subject, y = Marks)) +
  geom_point() +
  labs(title = "Scatterplot of Subject vs. Marks", x = "Subject", y = "Marks")


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

6) The data analyst of Argon technology Mr. John needs to enter the salaries of 10 employees in R. The salaries of the employees are given in the following table:

i) Which R command will Mr. John use to enter these values demonstrate the output.
ii) Now Mr. John wants to add the salaries of 5 new employees in the existing table, which command he will use to join datasets with new values in R. Demonstrate the output.
(iii) Visialize the data using chart .

library(ggplot2)
library(gridExtra)
library(dplyr)

# Create a data frame for the existing salaries
employee_data <- data.frame(
  "Sr. No." = 1:10,
  "Name of employees" = c("Vivek", "Karan", "James", "Soham", "Renu", "Farah", "Hetal", "Mary", "Ganesh", "Krish"),
  Salaries = c(21000, 55000, 67000, 50000, 54000, 40000, 30000, 70000, 20000, 15000)
)

# Display the data frame
print(employee_data)

# Create a data frame for the new employees
new_employee_data <- data.frame(
  "Sr. No." = 11:15,
  "Name of employees" = c("Amit", "Sneha", "Rekha", "Rahul", "Priya"),
  Salaries = c(45000, 60000, 53000, 48000, 62000)
)

# Combine the new data with the existing data
combined_data <- rbind(employee_data, new_employee_data)

# Display the combined data
print(combined_data)


# Create a histogram to visualize the distribution of salaries
ggplot(combined_data, aes(x = Salaries)) +
  geom_histogram(binwidth = 10000, fill = "blue", color = "black") +
  labs(title = "Salary Distribution", x = "Salaries", y = "Frequency") +
  theme_minimal()



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

7) Analyse and visualize churn modelling data using R.
 
 # Load necessary libraries
library(ggplot2)
library(gridExtra)
library(dplyr)

# Load the churn modeling dataset from a CSV file
churn_data <- read.csv("/Users/surajchavan/Downloads/Churn.csv")

# View the first few rows of the dataset
head(churn_data)

# Create a bar chart to visualize the distribution of churn (Exited) by Gender
bar_chart <- ggplot(churn_data, aes(x = Gender, fill = factor(Exited))) +
  geom_bar() +
  labs(title = "Churn Distribution by Gender", x = "Gender", y = "Count") +
  scale_fill_discrete(name = "Exited")

# Create a histogram to visualize the distribution of Age by churn status
histogram <- ggplot(churn_data, aes(x = Age, fill = factor(Exited))) +
  geom_histogram(binwidth = 5, alpha = 0.7) +
  labs(title = "Age Distribution by Churn Status", x = "Age", y = "Frequency") +
  scale_fill_discrete(name = "Exited")

# Create a scatterplot to visualize the relationship between Credit Score and Balance
scatterplot <- ggplot(churn_data, aes(x = CreditScore, y = Balance, color = factor(Exited))) +
  geom_point() +
  labs(title = "Scatterplot of Credit Score vs. Balance", x = "Credit Score", y = "Balance") +
  scale_color_discrete(name = "Exited")

# Create a box plot to visualize the distribution of Estimated Salary by churn status
box_plot <- ggplot(churn_data, aes(x = factor(Exited), y = EstimatedSalary, fill = factor(Exited))) +
  geom_boxplot() +
  labs(title = "Box Plot of Estimated Salary by Churn Status", x = "Churn Status", y = "Estimated Salary") +
  scale_fill_discrete(name = "Exited")

grid.arrange(scatterplot,bar_chart, histogram, box_plot, ncol = 2)


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

8) Analyse and visualize IRIS data using R.

# Load necessary libraries
library(ggplot2)
library(gridExtra)
library(dplyr)

# Load the Iris dataset from a CSV file
iris_data <- read.csv("/Users/surajchavan/Downloads/Iris.csv")

# View the first few rows of the dataset
head(iris_data)

# Scatterplot
scatterplot <- ggplot(iris_data, aes(x = SepalLengthCm, y = SepalWidthCm, color = Species)) +
  geom_point() +
  labs(title = "Scatterplot of Sepal Length vs. Sepal Width", x = "Sepal Length (cm)", y = "Sepal Width (cm)")

# Bubble Chart
bubble_chart <- ggplot(iris_data, aes(x = SepalLengthCm, y = SepalWidthCm, size = PetalLengthCm, color = Species)) +
  geom_point() +
  labs(title = "Bubble Chart of Sepal Length vs. Sepal Width", x = "Sepal Length (cm)", y = "Sepal Width (cm)")



# Dot Plots (Not typically used for this type of data)

# Histogram
histogram <- ggplot(iris_data, aes(x = SepalLengthCm, fill = Species)) +
  geom_histogram(binwidth = 0.2, alpha = 0.7) +
  labs(title = "Histogram of Sepal Length", x = "Sepal Length (cm)", y = "Frequency")

# Box Plot
box_plot <- ggplot(iris_data, aes(x = Species, y = SepalLengthCm, fill = Species)) +
  geom_boxplot() +
  labs(title = "Box Plot of Sepal Length by Species", x = "Species", y = "Sepal Length (cm)")

grid.arrange(scatterplot, bubble_chart, histogram, box_plot, ncol = 2)

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

9) Analyse and visualize supermarket data using R.

# Load necessary libraries
library(ggplot2)
library(gridExtra)
library(dplyr)

# Load the supermarket sales dataset from a CSV file
supermarket_data <- read.csv("/Users/surajchavan/Downloads/Supermarket2.csv")

# View the first few rows of the dataset
head(supermarket_data)

# Summary statistics for numeric columns
summary(supermarket_data[, c("Unit_price", "Quantity", "Tax", "Total", "cogs", "gross_margin_percentage", "gross_income", "Rating")])

# Summary statistics for categorical columns
summary(supermarket_data[, c("Branch", "City", "Customer_type", "Gender", "Product_line", "Payment")])

# Count of missing values
colSums(is.na(supermarket_data))

# Count of unique values for categorical columns
sapply(supermarket_data[, c("Branch", "City", "Customer_type", "Gender", "Product_line", "Payment")], function(x) length(unique(x)))

# Frequency table for Product_line
table(supermarket_data$Product_line)


# Create a scatterplot to visualize the relationship between Unit_price and Quantity
scatterplot <- ggplot(supermarket_data, aes(x = Unit_price, y = Quantity, color = Customer_type)) +
  geom_point() +
  labs(title = "Scatterplot of Unit Price vs. Quantity", x = "Unit Price", y = "Quantity")

# Create a box plot to visualize the distribution of Total by City
box_plot <- ggplot(supermarket_data, aes(x = City, y = Total, fill = City)) +
  geom_boxplot() +
  labs(title = "Box Plot of Total Sales by City", x = "City", y = "Total Sales")

# Create a bar chart to visualize the distribution of Customer_type
bar_chart <- ggplot(supermarket_data, aes(x = Customer_type, fill = Customer_type)) +
  geom_bar() +
  labs(title = "Customer Type Distribution", x = "Customer Type", y = "Count")

# Additional analyses and visualizations can be performed based on specific research questions and objectives.
# Additional visualizations and analyses can be performed based on your specific research questions and objectives.
grid.arrange(scatterplot,bar_chart,  box_plot, ncol = 2)


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

10) Analyse and visualize Loan data using R.

# Load necessary libraries
library(ggplot2)
library(gridExtra)
library(dplyr)

# Load the loan dataset from a CSV file
loan_data <- read.csv("/Users/surajchavan/Downloads/Loan.csv")

# View the first few rows of the dataset
head(loan_data)


# Summary statistics for numeric columns
summary(loan_data[, c("ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term")])

# Summary statistics for categorical columns
summary(loan_data[, c("Gender", "Married", "Dependents", "Education", "Self_Employed", "Credit_History", "Property_Area", "Loan_Status")])

# Count of missing values
colSums(is.na(loan_data))

# Count of unique values for categorical columns
sapply(loan_data[, c("Gender", "Married", "Dependents", "Education", "Self_Employed", "Credit_History", "Property_Area", "Loan_Status")], function(x) length(unique(x)))

# Frequency table for Loan_Status
table(loan_data$Loan_Status)

# Correlation matrix for numeric variables
cor(loan_data[, c("ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term")])

# Crosstabulation of Loan_Status and other categorical variables
table(loan_data$Loan_Status, loan_data$Gender)
table(loan_data$Loan_Status, loan_data$Married)


# Create a scatterplot to visualize the relationship between ApplicantIncome and LoanAmount
scatterplot <- ggplot(loan_data, aes(x = ApplicantIncome, y = LoanAmount, color = Loan_Status)) +
  geom_point() +
  labs(title = "Scatterplot of Applicant Income vs. Loan Amount", x = "Applicant Income", y = "Loan Amount")

# Create a box plot to visualize the distribution of LoanAmount by Loan_Status
box_plot <- ggplot(loan_data, aes(x = Loan_Status, y = LoanAmount, fill = Loan_Status)) +
  geom_boxplot() +
  labs(title = "Box Plot of Loan Amount by Loan Status", x = "Loan Status", y = "Loan Amount")

# Create a bar chart to visualize the distribution of Loan_Status by Gender
bar_chart <- ggplot(loan_data, aes(x = Gender, fill = Loan_Status)) +
  geom_bar() +
  labs(title = "Loan Status Distribution by Gender", x = "Gender", y = "Count")

# Create a histogram to visualize the distribution of ApplicantIncome
histogram <- ggplot(loan_data, aes(x = ApplicantIncome, fill = Loan_Status)) +
  geom_histogram(binwidth = 1000, alpha = 0.7) +
  labs(title = "Histogram of Applicant Income", x = "Applicant Income", y = "Frequency")

grid.arrange(scatterplot,bar_chart, histogram, box_plot, ncol = 2)


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




