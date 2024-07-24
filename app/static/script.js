// $(document).ready(function() {
//     let timer;
//     $('#inputText').on('keydown', function(event) {
//         clearTimeout(timer);
//         if (event.which === 32) { // 32 adalah kode key untuk spasi
//             $('.text-translate').hide();
//         var text = $(this).val();
        
//         // Tampilkan animasi loading
//         $('.box-saran').show();
//         $('#results').hide();
//         $('.loading').show();
        
//         timer = setTimeout(function() {
//             $.ajax({
//                 url: '/correct',
//                 method: 'POST',
//                 contentType: 'application/json',
//                 data: JSON.stringify({ text: text }),
//                 success: function(response) {
//                     $('#results').empty();
//                     $('#results').show();
//                     $('.loading').hide(); // Sembunyikan animasi loading
                    
//                     if (response.correct) {
//                         $('.box-saran').hide(); // Sembunyikan jika correct = true
//                     } else {
//                         $('.box-saran').show(); // Tampilkan jika correct = false
//                         $.each(response.data, function(index, item) {
//                             $('#results').append('<li data-id="' + item.id + '">' + item.correct + '</li>');
//                         });
//                         // Tambahkan event listener untuk elemen <li>
//                         $('#results li').on('click', function() {
//                             var txt = $(this).text();
//                             $('#inputText').val(txt);
//                             $('#results').empty();
//                             $('.box-saran').hide(); // Sembunyikan jika correct = true
//                         });
//                     }
//                 },
//                 error: function() {
//                     $('.loading').hide(); // Sembunyikan animasi loading jika ada kesalahan
//                 }
//             });
//         }, 500); // Menunggu 500ms setelah pengguna berhenti mengetik sebelum mengirim permintaan
//         }
        
//     });
// });
function send_text(txt) {
    timer = setTimeout(function() {
        $.ajax({
            url: '/submit',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ text: txt }),
            success: function(response) {
                // console.log(response.hasil);
                $('.text-translate').html(response.hasil);
                $('.content-detils').html(response.tag_detil_result);
                if (response.status_ambigu){
                    $('.ambigous-detils').html(response.tag_ambigu);
                } else{
                    $('.ambigous-detils').html("");
                }
            },
            error: function() {
                console.log("gagal");
            }
        });
    }, 500); // Menunggu 500ms setelah pengguna berhenti mengetik sebelum mengirim permintaan
}

$(document).ready(function() {
    let timer;
    $('#inputText').on('input', function() {
        clearTimeout(timer);
        // $('.text-translate').hide();
        var text = $(this).val();
        
        // Tampilkan animasi loading
        $('.box-saran').show();
        $('#results').hide();
        $('.loading').show();
        
        send_text(text);



        timer = setTimeout(function() {
            $.ajax({
                url: '/correct',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ text: text }),
                success: function(response) {
                    $('#results').empty();
                    $('#results').show();
                    $('.loading').hide(); // Sembunyikan animasi loading
                    
                    if (response.correct) {
                        $('.box-saran').hide(); // Sembunyikan jika correct = true
                    } else {
                        $('.box-saran').show(); // Tampilkan jika correct = false
                        $.each(response.data, function(index, item) {
                            $('#results').append('<li data-id="' + item.id + '">' + item.correct + '</li>');
                        });
                        // Tambahkan event listener untuk elemen <li>
                        $('#results li').on('click', function() {
                            var txt = $(this).text();
                            $('#inputText').val(txt);
                            $('#results').empty();
                            $('.box-saran').hide(); // Sembunyikan jika correct = true
                            send_text(txt);
                        });
                    }
                },
                error: function() {
                    $('.loading').hide(); // Sembunyikan animasi loading jika ada kesalahan
                }
            });
        }, 500); // Menunggu 500ms setelah pengguna berhenti mengetik sebelum mengirim permintaan
    });

    // $('#results li').on('click', function() {
    //     console.log("SUGGEST");
    // });
});
