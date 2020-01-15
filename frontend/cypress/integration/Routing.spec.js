import { createYield } from "typescript";

const HOME_URL = "http://localhost:3000/";

describe("Routing", () => {
  it("can load content on the Upload Student Roster page", () => {
    cy.visit(HOME_URL + "upload-student-roster");
    cy.contains("Upload Student Roster Page");
  });
  it("can load content on the Upload Module Marks page", () => {
    cy.visit(HOME_URL + "upload-module-marks");
    cy.contains("Drag and drop files here, or click to select files");
    cy.contains("Upload CSV Files to Database");
  });

  it("can load content on the View All Data page", () => {
    cy.visit(HOME_URL + "view-all-data");
    cy.contains("All Module Grade Data");
  });
});