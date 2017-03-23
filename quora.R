setwd("F:\\Study\\OneDrive - The University of Texas at Dallas\\02 Study\\06 Quora\\")
library(randomForest)
library(rpart)
library(ggplot2)
train_data <- read.csv(".\\train_modified.csv",header = TRUE)
test_data  <- read.csv(".\\test_modified.csv",header = TRUE)

#Change column names in train data
names(train_data) <- as.matrix(train_data[1, ])
train_data <- train_data[-1, ]
train_data[] 

colnames(train_data)[1] <- "id"
colnames(train_data)[4] <- "similarity"

head(train_data,5)
colnames(train_data)
nrow(train_data)

test <- train_data[,c(4,5)]
head(test,5)

train_classification <- rpart(is_duplicate~similarity,data = test, method = "class")
train_classification

test_check <- test_data[,c(4,5)]
head(test_check,5)
new = data.frame(test_check$similarity)
colnames(new)[1] <- "similarity"
head(new,5)
test_classification <- predict(train_classification,newdata = new)
test_classification

unique(test_classification)


attach(test)
plot(similarity, is_duplicate, main="Scatterplot Example", 
     xlab="Similarity ", ylab="Duplicate ", pch=19)




#Change column names in test data
names(test_data) <- as.matrix(test_data[1, ])
test_data <- test_data[-1, ]
test_data[] 

colnames(test_data)[1] <- "id"
colnames(test_data)[4] <- "similarity"
colnames(test_data)[5] <- "is_duplicate"
head(test_data,5)

colnames(test_data)
train_data$is_duplicate <- train_data$is_duplicate[,drop = T]
#Random Forest
train_random_forest  <- randomForest(is_duplicate ~ similarity,data = train_data ,ntree = 250)
conf <- train_random_forest$confusion
conf

similarity <- test_data$similarity
test_random_forest  <- predict(train_random_forest,similarity)
class(test_random_forest)
unique(test_random_forest)

test <- test_random_forest
test <- as.data.frame(test)
head(test)
colnames(test)[1] <- "is_duplicate"
test$test_id <- seq.int(nrow(test))
test <- test[,c("test_id","is_duplicate")]
test$test_id  <- test$test_id - 1
test$test_id  <- as.integer(test$test_id)
head(test,5)

write.csv(test,".\\test_random_forest.csv",row.names=FALSE)
nrow(test)

head(test_random_forest,5)

#Classification
train_classification <- rpart(train_data[,5]~train_data[,4],method = "class")
test_classification  <- predict(train_classification,newdata = test_data[,4])

#Logistic Regression
train_logistic <- glm(is_duplicate ~ similarity,family=binomial(link='logit'),data=train_data)
summary(train_logistic)
test_logistic  <- predict(train_logistic,newdata = new,type='response')
head(test_logistic_1,5)
test_logistic_1 <- as.data.frame(test_logistic)
check <- ifelse(test_logistic_1$test_logistic > 0.5,1,0)
head(check)
check <- as.data.frame(check)

colnames(check)[1] <- "is_duplicate"
check$test_id <- seq.int(nrow(check))
head(check)
nrow(check)
check <- check[,c("test_id","is_duplicate")]
check$test_id <- check$test_id - 1
check$test_id <- as.integer(check$test_id)
write.csv(check,".\\test_random_forest.csv",row.names=FALSE)
class(check$test_id)

