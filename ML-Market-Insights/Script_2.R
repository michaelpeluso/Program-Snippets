###############################################
## Visualizing Salary Ranges with Gradient Clusters
###############################################

# 1. Load Libraries

# Installing and loading the necessary packages
install_if_missing <- function(pkg){
  if(!require(pkg, character.only = TRUE)){
    install.packages(pkg, repos = "http://cran.us.r-project.org")
    library(pkg, character.only = TRUE)
  }
}

# List of packages we need
packages <- c("tidyverse", "ggplot2", "RColorBrewer")

# Install and load each package
for(p in packages){
  install_if_missing(p)
}

# 2. Get the Data Ready

# Loading the CSV file
job_data <- read_csv("./ai_job_market_insights.csv")

# Making sure the data types are correct
job_data <- job_data %>%
  mutate(
    Job_Title = as.factor(Job_Title),
    Required_Skills = as.character(Required_Skills)
  )

# Splitting multiple skills into separate rows
job_data_expanded <- job_data %>%
  separate_rows(Required_Skills, sep = ",\\s*") %>%
  mutate(
    Skill = trimws(Required_Skills),
    Skill = as.factor(Skill)
  ) %>%
  select(Job_Title, Skill, Salary_USD)

# 3. Preform Calculations

# Calculating average salary for each Job Title and Skill combo
comb_salary <- job_data_expanded %>%
  group_by(Job_Title, Skill) %>%
  summarize(
    Avg_Salary = mean(Salary_USD, na.rm = TRUE),
    .groups = "drop"
  )

# Creating a simple label for the salary
comb_salary <- comb_salary %>%
  mutate(
    Salary_Range_Label = paste0(
      round(Avg_Salary / 1000), "k"
    )
  )

# 4. K-means Clustering

# Setting a determined seed
set.seed(123)

# Choosing number of cluster groups
k <- 4

# Running k-means on the average salaries
clustering <- kmeans(comb_salary$Avg_Salary, centers = k, nstart = 25)

# Getting the cluster centers to order them
cluster_centers <- clustering$centers
ordered_clusters <- order(cluster_centers)

# Mapping the original cluster numbers to the ordered ones
cluster_mapping <- setNames(seq_along(ordered_clusters), ordered_clusters)

# Adding the ordered cluster info to our dataframe
comb_salary$Cluster_Ordered <- cluster_mapping[as.character(clustering$cluster)]

# 5. Visualize Plots

# determine colors for clusters
gradient_palette <- brewer.pal(n = 10, name = "YlGn")[5:9]

# Scatter Plot of Avg_Salary per Clustered Skill
scatter_plot <- ggplot(comb_salary, aes(x = Job_Title, y = Avg_Salary, color = Cluster_Ordered)) +
  geom_point(size = 4, alpha = 0.7) +
  scale_color_gradientn(colors = gradient_palette, name = "Cluster", breaks = 1:k) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
    axis.title = element_text(size = 12),
    plot.title = element_text(size = 14, face = "bold", hjust = 0.5)
  ) +
  labs(title = "Average Salary by Job Title per Clustered Skill", x = "Job Title", y = "Average Salary (USD)")
print(scatter_plot)

# Creating the heatmap
p <- ggplot(comb_salary, aes(x = Job_Title, y = Skill, fill = Cluster_Ordered)) +
  geom_tile(color = "white") + 
  geom_text(aes(label = Salary_Range_Label), color = "white", size = 3) +
  # Setting up the gradient colors
  scale_fill_gradientn(colors = gradient_palette, name = "Cluster", breaks = 1:k) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    axis.title = element_text(size = 12),
    plot.title = element_text(size = 14, face = "bold", hjust = 0.5)
  ) +
  labs(title = "Salary Ranges by Job Title and Skill (Clusters)", x = "Job Title", y = "Skill")
print(p)

