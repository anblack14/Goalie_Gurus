
library(Hmisc)
library(tidyverse)
library(DataExplorer)
library(data.table)
library(lme4)

nhl=read.csv('top_56_scorers.csv')
names(nhl)[1]<-"id"
playermax <- nhl %>%
  group_by(id) %>%
  mutate(daysalive = max(daysalive),
         assistsPerGame = mean(assists), 
         goalsPerGame   = mean(goals),
         sumgoals       = max(sumgoals)
  )
library(shiny)

ui <- fluidPage(
  selectInput(inputId = "player",
              label = "Choose a player",
              choices = playermax$lastname),
  dataTableOutput("summary"), 
  plotOutput("sumgoals"),
  verbatimTextOutput("stats")
)

server <- function(input, output) {
  data <- reactive({
    filteredDF <- nhl %>%
      filter(lastname == input$player)
  })
  output$sumgoals <- renderPlot({
    plot(data()$sumgoals, xlim = c(0,max(data()$gameid)), ylim = c(0,900))
  })
  output$stats <- renderPrint({
    summary(data()$sumgoals)
  })
}

shinyApp(ui = ui, server = server)