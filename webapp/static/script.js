document.addEventListener('DOMContentLoaded', function() {
    // Get all rows in the table
    var rows = document.querySelectorAll('#myTable tr');

    // Add click event listener to each row
    rows.forEach(function(row) {
        row.addEventListener('click', function() {
            // Get the character ID from the clicked row
            var characterId = row.getAttribute('data-character-id');

            // Get the character first name and TV show from the row cells
            var characterFirstName = row.cells[1].innerText;
            var characterTvShow = row.cells[3].innerText;
            var actorFirstName = row.cells[4].innerText;

            // Construct the URL for the character route
            var characterRoute = '/character/' + characterFirstName + '_' + characterTvShow + '_' + actorFirstName;

            // Redirect to the character route
            window.location.href = characterRoute;
        });
    });
});

document.getElementById("back-button").addEventListener("click", function() {
            window.location.href = "/";
        });
