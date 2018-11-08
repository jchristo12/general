#Joe's User Defined Functions

#display the number of missing values per variable
missing_values <- function(dataframe){
  m <- as.data.frame(colSums(is.na(dataframe)))
  colnames(m) <- "NA.count"
  m$NA.percent <- m$NA.count/dim(dataframe)[1]
  return(m)
}

#create a correlation heatmap
cor_heatmap <- function(dataset){
  require(reshape2)
  require(ggplot2)
  matrix <- cor(dataset, use="pairwise.complete.obs", method="pearson")
  matrix[lower.tri(matrix)] <- NA
  melted.cor <- melt(matrix, na.rm=TRUE)
  #create the heatmap plot
  cor.heatmap <- ggplot(data=melted.cor, aes(x=Var2, y=Var1, fill=value)) +
    geom_tile(color="white") +
    scale_fill_gradient2(low="blue", mid="white", high="red", midpoint=0, limit=c(-1,1), space="Lab", name="Correlation\n") +
    geom_text(aes(Var2, Var1, label=round(value,2)), color="black", size=2) +
    theme(axis.text.x=element_text(angle=45, hjust=1))
  return(cor.heatmap)
}

#create a frequency table between two variables
freq_table <- function(x, var1, var2){
  t <- addmargins(table(x[[var1]], x[[var2]]))
  z <- t[,2] / t[,3]
  output <- cbind(t, "% Pos"=z)
  return(output)
}

#create subset (easy way to subset data based on variable names in a droplist)
create_subset <- function(train_data, droplist){
  subdat <- train_data[, !names(train_data) %in% droplist]
  return(subdat)
}

#create decision tree imputed values for specified columns of data
impute_trees <- function(df, cols){
  require(rpart)
  for(i in cols){
    form <- formula(paste0(i, "~."))
    #differnt treatment if the variable is factor or not
    if(is.factor(df[[i]])){
      fit <- rpart(form, data=df, method="class")
      imp <- factor(ifelse(is.na(df[[i]]), predict(fit, df, type="class"), df[[i]]), labels=levels(df[[i]]))
    } else{
      fit <- rpart(form, data=df)
      imp <- ifelse(is.na(df[[i]]), predict(fit, df), df[[i]])
    }
    df[[paste0("imp_",i)]] <- imp
  }
  return(df)
}

#create decision tree imputed values for specified columns of data
store_impute_fit <- function(df, cols){
  require(rpart)
  fits <- vector("list", length=length(cols))
  for(i in cols){
    n <- which(cols == i)
    form <- formula(paste0(i, "~."))
    #differnt treatment if the variable is factor or not
    if(is.factor(df[[i]])){
      fit <- rpart(form, data=df, method="class")
    } else{
      fit <- rpart(form, data=df)
    }
    fits[[n]] <- fit
  }
  return(fits)
}

#impute test data with training objects
impute_test <- function(obj.list, test.df, cols){
  for(i in cols){
    n <- which(cols == i)
    if(is.factor(test.df[[i]])){
      imp <- factor(ifelse(is.na(test.df[[i]]), predict(obj.list[[n]], test.df, type="class"), test.df[[i]]), labels=levels(test.df[[i]]))
    } else{
      imp <- ifelse(is.na(test.df[[i]]), predict(obj.list[[n]], test.df), test.df[[i]])
    }
    test.df[[paste0("imp_",i)]] <- imp
  }
  return(test.df)
}


#create dummy variables for all categorical variables
one_hot_encode <- function(df){
  #load required packages
  require(dummies)
  require(dplyr)
  #find all categorical variables
  cat_vars <- df %>%
    select_if(is.factor) %>%
    names()
  #loop through and perform one hot encoding for all cat variables
  for(i in cat_vars){
    ohe <- dummy(i, data=df)
    df <- cbind(df, ohe)
  }
  #remove the original categorical variables
  df_clean <- create_subset(df, cat_vars)
  
  return(df_clean)
}


#plot a ROC curve
rocplot <- function(preds, actuals, ...){
  require(ROCR)
  pred = prediction(preds, actuals)
  perf = performance(pred, "tpr", "fpr")
  par(mfrow=c(1,1))
  plot(perf, ...)
}

#predict function for regsubsets
predict.regsubsets <- function(object, newdata, id, ...){
  form <- as.formula(object$call[[2]])
  mat <- model.matrix(form, newdata)
  coefi <- coef(object, id=id)
  xvars <- names(coefi)
  mat[,xvars] %*% coefi
}

#scale test data using the training data parameters
scale_std_test <- function(train.data, test.data){
  train.scaled <- scale(train.data)
  test.scaled <- scale(test.data, center=attr(train.scaled, "scaled:center"), scale=attr(train.scaled, "scaled:scale"))
  return(test.scaled)
}

#scale based on max and min
scale_maxmin <- function(train.data, test.data){
  maxs <- apply(train.data, 2, max, na.rm=TRUE)
  mins <- apply(train.data, 2, min, na.rm=TRUE)
  output <- scale(train.data, center=mins, scale=maxs-mins)
  return(output)
}

#scale TEST data based on max and min
scale_maxmin_test <- function(train.data, test.data){
  maxs <- apply(train.data, 2, max, na.rm=TRUE)
  mins <- apply(train.data, 2, min, na.rm=TRUE)
  output <- scale(test.data, center=mins, scale=maxs-mins)
  return(output)
}

#K-means clustering Scree plot
wssplot <- function(df, nc=15, seed=666){
  wss <- (nrow(df)-1)*sum(apply(df,2,var))
  for (i in 2:nc) {
    set.seed(seed)
    wss[i] <- sum(kmeans(df, centers=i)$withinss)}
  plot(1:nc, wss, type="b", xlab="Number of Clusters",
       ylab="Within groups sum of squares")}

#3d biplot for PCA
biplot3d <- function(pca, pcs=3, lwd=4){
  #add the labels
  text3d(pca$loadings[,1:pcs], texts=rownames(pca$loadings), col="red")
  #create the coordinates for the arrows
  coords <- NULL
  for(i in 1:nrow(pca$loadings)){
    coords <- rbind(coords, rbind(c(0,0,0), pca$loadings[i, 1:pcs]))
  }
  lines3d(coords, col="red", lwd=lwd)
}
