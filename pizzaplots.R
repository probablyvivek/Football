#Install Libraries
install.packages("devtools")
devtools::install_github("abhiamishra/ggshakeR")
install.packages("worldfootballR")

#Load the library
library(ggshakeR)
library(worldfootballR)
library(tidyverse)

#Single Player Plot
single_player <- fb_player_scouting_report("https://fbref.com/en/players/5eae500a/Romelu-Lukaku", pos_versus = "primary")
pizza <- plot_pizza(data = single_player, type = "single", template = "forward", 
                    colour_poss = "#41ab5d", 
                    colour_att = "#fec44f", 
                    colour_def = "#de2d26", 
                    season = "Last 365 Days", 
                    theme = "dark")
pizza
#use ggsave to save the plot with filename have tjhe name of the player in the same folder with  width = 2900, height = 2800, units = "px")
ggsave(pizza, filename = "Romelu_Lukaku.png", width = 2900, height = 2800, units = "px")



#Comparison Plot
data1 <- fb_player_scouting_report("https://fbref.com/en/players/1f44ac21/Erling-Haaland", pos_versus = "primary")
data2 <- fb_player_scouting_report("https://fbref.com/en/players/5eae500a/Romelu-Lukaku", pos_versus = "primary")
data <- rbind(data1, data2)


comp_pizza <- plot_pizza(data = data, type = "comparison", template = "forward",
                         player_1 = "Erling Haaland",
                         player_2 = "Romelu Lukaku",
                         season_player_1 = "Last 365 Days",
                         season_player_2 = "Last 365 Days",
                         colour_compare = "#f4ae01",
                         theme = "black")
image <- comp_pizza

#use ggsave to save the plot with filename have the name of the player as f string
ggsave(image, filename = "Haaland vs Lukaku.png", width = 2900, height = 2800, units = "px")
