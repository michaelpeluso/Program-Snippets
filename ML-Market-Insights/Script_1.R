install.packages(c("tidyr", "dplyr", "ggplot2", "plotly", "caret", "cluster", "rpart.plot", "randomForest"))
# Load necessary libraries
library(dplyr)
library(tidyr)
library(ggplot2)
library(plotly)
library(caret)
library(cluster)
library(rpart)
library(randomForest)

# Load the data
data <- read.csv("/Users/phill/Downloads/ai_job_market_insights.csv")

# Data Preparation
data <- data %>%
  mutate(
    AI_Adoption_Level = as.factor(AI_Adoption_Level),
    Automation_Risk = as.factor(Automation_Risk),
    Remote_Friendly = as.factor(Remote_Friendly),
    Job_Growth_Projection = as.factor(Job_Growth_Projection),
    Salary_USD = as.numeric(Salary_USD)
  ) %>%
  drop_na() # Remove rows with missing values

# Exploratory Data Analysis (EDA)

# Distribution of salaries
ggplot(data, aes(x = Salary_USD)) +
  geom_histogram(bins = 30, fill = "blue", alpha = 0.7) +
  theme_minimal() +
  ggtitle("Distribution of Salaries")

# AI Adoption Level by Industry
ggplot(data, aes(x = Industry, fill = AI_Adoption_Level)) +
  geom_bar(position = "dodge") +
  theme_minimal() +
  ggtitle("AI Adoption Levels by Industry") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Clustering
# Normalize numerical data
num_data <- data %>%
  select(Salary_USD) %>%
  scale()

# Perform K-Means Clustering
set.seed(123)
kmeans_result <- kmeans(num_data, centers = 3)
data$Cluster <- as.factor(kmeans_result$cluster)

# Visualize Clusters
ggplot(data, aes(x = Salary_USD, y = as.numeric(AI_Adoption_Level), color = Cluster)) +
  geom_point() +
  theme_minimal() +
  ggtitle("Clusters Based on Salary and AI Adoption Level")

# Classification

# Split the data into training and testing sets
set.seed(123)
train_index <- createDataPartition(data$Job_Growth_Projection, p = 0.8, list = FALSE)
train_data <- data[train_index, ]
test_data <- data[-train_index, ]

# Train a Random Forest Model
rf_model <- randomForest(Job_Growth_Projection ~ Salary_USD + AI_Adoption_Level + Automation_Risk + Remote_Friendly,
                         data = train_data, ntree = 100)

# Predict on Test Data
rf_predictions <- predict(rf_model, test_data)

# Evaluate Model Accuracy
conf_matrix <- confusionMatrix(rf_predictions, test_data$Job_Growth_Projection)
print(conf_matrix)

# Decision Tree Model
tree_model <- rpart(Job_Growth_Projection ~ Salary_USD + AI_Adoption_Level + Automation_Risk + Remote_Friendly,
                    data = train_data, method = "class")

# Plot Decision Tree
plot(tree_model)
text(tree_model, use.n = TRUE)
summary(tree_model)
