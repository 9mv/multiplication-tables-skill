Feature: Multiplication Tables Skill game

  Scenario: initialize skill
     Given an english speaking user
      When the user says "pregunta'm les taules de multiplicar"
      Then "multiplication-tables-skill" should reply with dialog from "which.dialog"

  Scenario: ask a table
     Given an english speaking user
      When the user says "practicar la taula de multiplicar del 3"
      Then "multiplication-tables-skill" should reply with dialog from "number.response.dialog"

  Scenario: ask a disordered specific table 
     Given an english speaking user
      When the user says "practiquem la taula del 3 en desordre"
      Then "multiplication-tables-skill" should reply with dialog from "number.response.dialog"

  Scenario: ask an ordered specific table
     Given an english speaking user
      When the user says "pregunta la taula del 2 en ordre"
      Then "multiplication-tables-skill" should reply with dialog from "number.response.dialog"

  Scenario: ask any table 1
     Given an english speaking user
      When the user says "preguntar qualsevol taula de multiplicar"
      Then "multiplication-tables-skill" should reply with dialog from "number.any.response.dialog"

  Scenario: ask any table 2
     Given an english speaking user
      When the user says "practicar una taula de multiplicar qualsevol"
      Then "multiplication-tables-skill" should reply with dialog from "number.any.response.dialog"

  Scenario: initialize skill ordered
     Given an english speaking user
      When the user says "pregunta'm les taules de multiplicar ordenades"
      Then "multiplication-tables-skill" should reply with dialog from "which.dialog"
   
  Scenario: failed initialization skill
     Given an english speaking user
      When the user says "pregunta'm la taula del 3 qualsevol"
      Then "multiplication-tables-skill" should reply with dialog from "which.table.dialog"

  Scenario: any disordered table
     Given an english speaking user
      When the user says "practicar qualsevol taula desordenada"
      Then "multiplication-tables-skill" should reply with dialog from "number.any.response.dialog"

  Scenario: ask all tables
     Given an english speaking user
      When the user says "pregunta'm multiplicacions de totes les taules"
      Then "multiplication-tables-skill" should reply with dialog from "all.response.dialog"

  Scenario: ask all tables ordered
     Given an english speaking user
      When the user says "pregunta'm multiplicacions ordenades"
      Then "multiplication-tables-skill" should reply with dialog from "all.response.dialog"


