target =  document.querySelector('*');
target.addEventListener('paste', pasteHandler);

function pasteHandler(e) {
	if (e.clipboardData) {
		// get items from clipboard
		var items = e.clipboardData.items;
		if (items) {
			 // loop through items looking for images
			 for (var i = 0; i < items.length; i++) {
					if (items[i].type.indexOf("image") !== -1) {
						 // represent the image as file
						 var blob = items[i].getAsFile();
						 var URLObj = window.URL || window.webkitURL;
						 var source = URLObj.createObjectURL(blob);
						 var reader = new FileReader();
						 reader.onload = function(e) {
							 document.getElementById("id_imagen_container").value=reader.result;
							 document.getElementById("id_imagen").src=reader.result;
						 }
						 reader.readAsDataURL(blob);
					}
				}
			}
	 }
}


