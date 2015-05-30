
setUpPackages <- function(){
  packages.needed <- c("dplyr")
  
  packages.notInstalled <- packages.needed[!packages.needed %in% rownames(installed.packages())]
  
  if (length(packages.notInstalled) > 0) install.packages(packages.notInstalled, dependencies = T)
  
  sapply(packages.needed, require, character.only=TRUE)
  
}

setUpPackages()