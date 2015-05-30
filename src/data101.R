source("util.R")

data.folder <- "../data/csv/"

tiposContrato.path <- paste(data.folder, "tipos_contrato.csv", sep="")
irps.path <- paste(data.folder, "irps.csv", sep="")

tiposContrato.data <- read.csv(tiposContrato.path)
irps.data <- read.csv(irps.path)



irps.pb <- irps.data %>% filter(UF.da.UASG.gerenciadora.da.IRP=="PB")
