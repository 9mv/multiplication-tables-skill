Feature: multiplication-tables-all

  Scenario: ask all tables
     Given a catala speaking user
      When the user says "pregunta'm multiplicacions de totes les taules"
      Then "multiplication-tables-skill" should reply with dialog from "all.response.dialog"

  Scenario: ask all tables ordered
     Given a catala speaking user
      When the user says "pregunta'm multiplicacions ordenades"
      Then "multiplication-tables-skill" should reply with dialog from "all.response.dialog"


