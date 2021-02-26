$(document).ready(function() { 
    var myForm = $("#reply-topic-form");
    myForm.submit(function(e){
        e.preventDefault();                     // it stops the page from loading, its mandatory else after submitting form, page will give JsonResponse instead of displaying a success msg by ajax call
        var formData = $(this).serialize();         // 'this' gives us the form tag fetched from above
        // console.log(formData);
        output = "";
        $.ajax({
            method: "POST",
            url: myForm.attr("data-url"),
            data: formData,
            success: handleFormSuccess,
            error: handleFormError,
        })

        function handleFormSuccess(data, textStatus, jqXHR) {
            console.log(data);
            if (data['status'] == 'Save') {
                $("#reply-success-msg").text("Reply Submitted Successfully");
                $("#reply-success-msg").show();
            }
            // console.log(textStatus);
            // console.log(jqXHR);
            myForm[0].reset();
            console.log(data.post_data[0][2]);
            last_post = data.post_data[0]
            output += "<div class='card mb-2'><div class='card-body p-3'><div class='row mb-3'><div class='col-6'><strong class='text-muted'>" + last_post[0] + 
                        "</strong></div><div class='col-6 text-right'><small class='text-muted'>Just Now</small></div></div>" + last_post[2] + "</div></div>"
            $("#last-post").html(output);
        }

        function handleFormError(jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        }
        
    });

    // $("#reply-btn").click(function() {
    //     console.log("btn clicked");
    //     let msg = $("#msg").val();
    //     let csr = $("input[name=csrfmiddlewaretoken]").val();
    //     // console.log(msg)
    //     // console.log(csr)
    //     mydata = { csr: csr, message: msg}
    //     $.ajax({
    //         url: "{% url 'boards:reply_topic' topic.board.pk topic.pk %}",
    //         method: "POST",
    //         data: mydata,
    //         success: function(data){
    //             console.log(data);
    //             if (data.status == "Save") {
    //                 console.log("Form submitted Successfully")
    //             }
    //             if (data.status == 0) {
    //                 console.log("Unable to submit Form")
    //             }
    //         }

    //     })
    // });
});