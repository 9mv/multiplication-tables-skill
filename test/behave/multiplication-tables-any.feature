Feature: multiplication-tables-any

  Scenario: ask any table 1
     Given a catala speaking user
      When the user says "preguntar qualsevol taula de multiplicar"
      Then "multiplication-tables-skill" should reply with dialog from "number.any.response.dialog"

  Scenario: ask any table 2
     Given a catala speaking user
      When the user says "practicar una taula de multiplicar qualsevol"
      Then "multiplication-tables-skill" should reply with dialog from "number.any.response.dialog"

  Scenario: any disordered table
     Given a catala speaking user
      When the user says "practicar qualsevol taula desordenada"
      Then "multiplication-tables-skill" should reply with dialog from "number.any.response.dialog"
