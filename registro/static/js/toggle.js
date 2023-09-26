/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function toggleLeftDropdown() {
  document.getElementById("leftDropdown").classList.toggle("show");
  console.log(document.getElementById("leftDropdown").style.backgroundColor.toString());
	//console.log(document.getElementById("leftDropdown").classList.toString());
}

function toggleRightDropdown() {
  document.getElementById("rightDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
} 

