const columnDefs = [
  { field: "title" },
  { field: "link" },
  { field: "source_link" },
  { field: "cite" },

  { field: "publication_doi" },

  { field: "authors" }


];



// let the grid know which columns and what data to use
const gridOptions = {
  columnDefs: columnDefs

};

document.addEventListener('DOMContentLoaded', () => {
    const gridDiv = document.querySelector('#myGrid');
    new agGrid.Grid(gridDiv, gridOptions);

fetch('../static/results.json')
    .then((response) => response.json())
    .then((data) => gridOptions.api.setRowData(data));

});