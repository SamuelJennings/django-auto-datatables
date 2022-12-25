const url = document.querySelector("table").dataset.url;
var datatable = null;

function hyperlink() {
  return function (data, type, row) {
    return type === "display" && data ?
      '<a class="px-2" data-bs-toggle="offcanvas" href="#offcanvasright" role="button" aria-controls="offcanvasright"><i class="fas fa-binoculars" data-url="' + data + '"></i></a>' :
      ""
  }
};


fetch(url, {
    method: 'OPTIONS'
  })
  .then((response) => response.json())
  .then((properties) => {

    datatable = new DataTable('table', {
      ...properties,
      columnDefs: [{
        targets: 0,
        data: null,
        render: hyperlink(),
      }, ],
      serverSide: true,
      ajax: {
        url: url,
        data: {
          format: 'datatables'
        },
      }
    })
  })