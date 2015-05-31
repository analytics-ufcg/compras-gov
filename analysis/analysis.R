data <- read.csv('itens_pregoes_000103047.csv',header=F)
names(data) <- c('LICITACAO','DATA','QUANTIDADE','VALOR')
data$LICITACAO <- as.character(data$LICITACAO)
data_2 <- data[data$VALOR>0,]
data_2$VALOR_UNI <- with(data_2,VALOR/QUANTIDADE)
