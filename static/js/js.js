$(document).ready(function () {

    var postsDelete = $(".de");
    postsDelete.click(function (e) {
        var url = $(this).data("url");
        var data = { pk: $(this).data("id") };
        var card = $(this).parent().parent().parent();
        $.ajax({
            url: url,
            data: data,
            dataType: "json",
            type: 'get',
            success: function (response) {
                if (response['status'] === "ok") {
                    card.remove();
                }
            }
        })
    });
    // LIKE
    $("#likeForm").submit(function (e) {
        var url = $(this).data("url");
        var method = $(this).attr("method")
        var data = $(this).serialize()
        $.ajax({
            type: method,
            url: url,
            data: data,
            dataType: "json",
            success: function (response) {
                if (response['action'] === "like") {
                    $("#likeBtn").css("color", "red");
                    var likes = $("#likes").text();
                    likes++;
                    $("#likes").text(likes);
                } else {
                    $("#likeBtn").css("color", "black");
                    var likes = $("#likes").text();
                    likes--;
                    $("#likes").text(likes);
                }
            },
        });
        return false;
    });

    // LEAVE MESSAGE
    $("#commentForm").submit(function () {
        $.ajax({
            type: $(this).attr("method"),
            url: $(this).data("url"),
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                var comments = $("#comments");
                comments.prepend(
                    "<li class='comment'><div class='author'><img src=" + response['photo_url'] +  " class='author-img'><h4 class='title is-4'>"+ response['full_name'] +"</h4></div><hr><p>"+ response['comment'] +"</p></li>"
                );
                $("#id_content").val = ""
            },
        });
        return false;
    });

})