#Loading the libraries
library(reactable)
library(reactablefmtr)
library(readr)
library(dplyr)
library(webshot2)

#Getting the data
data <- read_csv("../R/ISLTeam.csv")

#setting the colors to be used while making the table
color_set <- c("#f7c844","#429460","#2e6d9e")

#creating the dataframe
df <- data %>% 
  rename(Team = 'Name') %>% 
  rename(GA = 'Goals Faced') %>% 
  rename(GF = 'Goals') %>% 
  rename (W = "Wins") %>% 
  rename (D = "Draws") %>% 
  rename (L = "Losses") %>% 
  mutate(Points = (W*3+D)) %>% 
  mutate(GD = GF-GA) %>% 
  mutate_at(c("W", "D", "L", "GF", "GA", "GD", "Points"),
            as.numeric) %>% 
  arrange(desc(Points), desc(GD)) %>% 
  mutate (Rank = (rank = row_number(desc(Points)))) %>% 
  mutate (Playoffs = ifelse(Rank<5, "Yes", "No")) %>% 
  mutate (playoff_cols = case_when(Playoffs == "Yes" ~ "#77AC97", TRUE ~ "#ff6f69")) %>% 
  mutate (GD_Cols = case_when(GD >= 0 ~ "#77AC97", TRUE ~ "#ff6f69")) %>% 
  unite(Record, W, D, L, sep = "-") %>% 
  select(Team, Record, GF, GA, GD, Points, Playoffs, playoff_cols, GD_Cols)


#Creating the table
table <- reactable(df,
          theme = nytimes(),
          sortable = FALSE,
          pagination = FALSE,
          highlight = TRUE,
          striped = TRUE,
          compact = TRUE,
          defaultColDef = colDef(align = "center"),
          
          #Formatting the Columns
          columns = list(
            Team = colDef(width = 150,
              cell = merge_column(df, "Record", merged_position = "below", size = 12, merged_weight = "bold"),
              style = list(borderRight = "1px dotted #777", fontFamily = "Trebuchet MS", fontSize = "14px")
            ),
            Record = colDef(show = FALSE),
            
            GF = colDef(
              maxWidth = 55,
              cell = color_tiles(df, bias = 1.3, box_shadow = TRUE),
              style = list(fontFamily = "Trebuchet MS", fontSize = "14px")
            ),
            
            GA = colDef(
              maxWidth = 55,
              cell = color_tiles(df, bias = 0.6, box_shadow = TRUE),
              style = list(fontFamily = "Trebuchet MS", fontSize = "14px")
            ),
            
            GD = colDef(
              maxWidth = 80,
              cell = pill_buttons(df, number_fmt = function(value) sprintf("%+0.1f", value), 
                                  colors = "transparent", opacity = 0, bold_text = TRUE, 
                                  text_color_ref = "GD_Cols"),
            style = list(borderRight = "1px dotted #777", fontFamily = "Trebuchet MS", fontSize = "14px")
            ),
            GD_Cols = colDef(show = FALSE),
            
            Playoffs = colDef(
              width = 100,
              align = "center",
              cell = pill_buttons(df, color_ref = "playoff_cols", opacity = 0.7, box_shadow = TRUE),
              style = list(fontFamily = "Trebuchet MS", fontSize = "14px",borderLeft = "1px dotted #777")
            ),
            playoff_cols = colDef(show = FALSE),
            
            Points =  colDef(
              width = 180,
              cell = data_bars(df, text_size = 13, box_shadow = TRUE),
              style = list(fontFamily = "Trebuchet MS", fontSize = "14px")
            )
          )
)
#Adding the titles and subtitles to the table
table <- table %>% 
  add_title("Indian Super League League Table 2021-22", 
            margin = margin(0, 0, 10, 0), 
            font_size = 20, 
            font_weight ="bold",
            text_transform = "capitalize") %>% 
  add_subtitle("Dated: 23-01-2022", font_size = 12, font_color = "Grey") %>% 
  add_source("Table created by: Vivek Tiwari", font_size = 12, font_color = "Grey")
  
#Saving the table
save_reactable(table, "leagueTable.png")

