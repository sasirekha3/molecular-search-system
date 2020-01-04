# Molecular Search System (MoSS)

Undergrad major-project submitted in partial fulfillment of the requirements for the award of the Degree of Bachelor of Technology.

## Abstract 
At the Indian Institute of Chemical Technology, there is a requirement for a chemical database that stores physical and chemical properties of samples submitted for record keeping. These molecules have properties such as structure, molecular weight, formula, SMILES, IUPAC name, sample code etc. We have developed a database, as well as a website, that will allow permitted users to upload new molecules, search existing molecules by structure and query string, and be informed of updates made to the database. The Molecular Search System is also able to generate a report and is secure throughout the entire session. We have opted to build the web application using PostgreSQL and Django to satisfy the above requirement. We have used an open-source RDBMS data cartridge, called Bingo, to store and operate on molecular representations in the database. Additionally, we have used Indigo toolkit to generate 2D coordinates of SMILES IDs, and Kekule.js to render these 2D coordinates onto the browser. All the technologies used in this project are open-source and free of cost.

## Architecture Diagram
![Architecture Diagram](/docs/diagram.png)

## Documentation
[PDF Documentation](/docs/FinalMajorProjectDocumentation.pdf)