window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

x="houssem";
function deletee(e)
{alert("dddd")
  fetch('/venues/' + e , {
            method: 'DELETE',
            body: JSON.stringify({
              'completed': e
            }),
            headers: {
              'Content-Type': 'application/json'
            }
          })

}
	
