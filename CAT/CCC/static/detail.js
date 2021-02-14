$('#detailModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget)
  var branch = button.data('job_branch') 
  var build_time = button.data('job_time')
  var modules = button.data('job_modules')

  var modal = $(this)

  var title = "Branch - " + branch 
  title += "Build Time - " + build_time
  modal.find('.modal-title').text(title)

  tbody = modal.find('.modal-body table tbody')
  tbody_html = ''
  modules = modules.split(' ').slice(0, -1);
  for (var i=0; i<modules.length; i++) {
    let module = modules[i].split('_')
    let module_name = module[0]
    let module_tag = module[1]
    let module_hash = module[2]
    let loop = i + 1

    tbody_html += '<tr><td>' + loop + '</td>'
    tbody_html += '<td>' + module_name + '</td>'
    tbody_html += '<td>' + module_tag + '</td>'
    tbody_html += '<td>' + module_hash + '</td></tr>'
  }
  tbody.html(tbody_html)
});
