Feature: multiplication-tables-basic

  Scenario: initialize skill
     Given a catala speaking user
      When the user says "pregunta'm les taules de multiplicar"
      Then "multiplication-tables-skill" should reply with dialog from "which.dialog"

  Scenario: ask a table
     Given a catala speaking user
      When the user says "practicar la taula de multiplicar del 8"
      Then "multiplication-tables-skill" should reply with dialog from "number.response.dialog"

  Scenario: ask a disordered specific table 
     Given a catala speaking user
      When the user says "practiquem la taula del 9 en desordre"
      Then "multiplication-tables-skill" should reply with dialog from "number.response.dialog"

  Scenario: ask an ordered specific table
     Given a catala speaking user
      When the user says "pregunta la taula del 2 en ordre"
      Then "multiplication-tables-skill" should reply with dialog from "number.response.dialog"

  Scenario: initialize skill ordered
     Given a catala speaking user
      When the user says "pregunta'm les taules de multiplicar ordenades"
      Then "multiplication-tables-skill" should reply with dialog from "which.dialog"
   
  Scenario: failed initialization skill
     Given a catala speaking user
      When the user says "pregunta'm la taula del 3 qualsevol"
      Then "multiplication-tables-skill" should reply with dialog from "which.table.dialog"