$('#image_file').change(function (event) {
    const inputFile = event.target;
    const fileName = inputFile.files[0].name;
    const label = $(inputFile).next(); // The label element

    label.text(fileName);

    const selectedImage = $('#image_review');
    const card = $('.card-rev');

    if (inputFile.files && inputFile.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
            selectedImage.attr('src', e.target.result);
            card.css('display', 'block'); // Show the card
        };

        reader.readAsDataURL(inputFile.files[0]);
    }
});


$('#model_file').change(function (event) {
    const inputFile = event.target;
    const fileName = inputFile.files[0].name;
    const label = $(inputFile).next(); // The label element

    label.text(fileName);
});

