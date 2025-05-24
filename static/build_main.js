const columnDefs = [

  { field: "Query" },
  { field: "Results" },
  { field: "Time" }


];



// let the grid know which columns and what data to use
const gridOptions = {
  columnDefs: columnDefs

};

document.addEventListener('DOMContentLoaded', () => {
    const gridDiv = document.querySelector('#myGrid');
    new agGrid.Grid(gridDiv, gridOptions);
fetch('../static/sample_pubmed.json')
    .then((response) => response.json())
    .then((data) => gridOptions.api.setRowData(data));

});