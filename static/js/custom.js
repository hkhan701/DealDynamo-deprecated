$(document).ready(function() {
    console.log("Ready!");


    // Manage edit-name-button text
    $('#edit-name').on('hide.bs.collapse', function() {
        $('a.edit-name-button').html("Edit");
    });
    $('#edit-name').on('show.bs.collapse', function() {
        $('a.edit-name-button').html("Close");
    });


    // Validate password
    $("#submit-button").click(function(event) {
        var pass = $("#pass").val();
        var confirmation = $("#confirmation").val();
        var regex = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,32}$/;
        if (!pass.match(regex)) {
            event.preventDefault();
            alert("Password must be 8-32 characters long and contain at least one number and one special character.");
        } else if (pass != confirmation) {
            event.preventDefault();
            alert("Password and confirmation do not match. Please re-enter them and try again.");
        }
    });

    // Function to handle running the config
    $("button.run-config-button").click(function() {
        if (validateConfig()) {
            $.post("/start_config", $("form.save-config-form").serialize())
                .done(function(response) {
                    console.log(response);
                    location.reload(true);
                })
                .fail(function(response) {
                    console.log(response);
                });
        }
    });

    // Function to handle stopping the config
    $("button.stop-config-button").click(function() {
        // Add logic to stop the config here
        $.post("/stop_config", $("form.save-config-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response);
            });
    });


    // Resend validation email
    $("a.verify-button").click(function(event) {
        event.preventDefault();
        $(this).html("Sending email");
        $(this).css('pointer-events', 'none');
        $(this).addClass("text-muted");
        $.post("/verify", $("form.verify-form").serialize())
            .done(function(response) {
                console.log(response);
                $("a.verify-button").html("Email sent");
            })
            .fail(function(response) {
                console.log(response)
            });
    });
    
    // Save config
    $("button.save-config-button").click(function() {
        // If validation passes, proceed with saving config
        $.post("/save_config", $("form.save-config-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response);
            });
    });

    // Function to validate config settings before pressing run
    function validateConfig() {
        // Perform validation for each input field
        // Example validation: Check if minimum savings threshold is a positive number
        var minimumSavingsThreshold = parseInt($("#minimum_savings_threshold").val());
        if (isNaN(minimumSavingsThreshold) || minimumSavingsThreshold <= 0) {
            alert("Minimum savings threshold must be a positive number.");
            return false; // Validation failed
        }
    
        var cleanupDaysThreshold = parseInt($("#cleanup_days_threshold").val());
        if (isNaN(cleanupDaysThreshold) || cleanupDaysThreshold < 0) {
            alert("Cleanup days threshold must be a non-negative number.");
            return false; // Validation failed
        }
    
        var maximumPostsPerSession = parseInt($("#maximum_posts_per_session").val());
        if (isNaN(maximumPostsPerSession) || maximumPostsPerSession <= 0) {
            alert("Maximum posts per session must be a positive number.");
            return false; // Validation failed
        }
    
        var delayBetweenPosts = parseInt($("#delay_between_posts").val());
        if (isNaN(delayBetweenPosts) || delayBetweenPosts <= 0) {
            alert("Delay between posts must be a positive number.");
            return false; // Validation failed
        }
    
        var delayBetweenSessions = parseInt($("#delay_between_sessions").val());
        if (isNaN(delayBetweenSessions) || delayBetweenSessions <= 0) {
            alert("Delay between sessions must be a positive number.");
            return false; // Validation failed
        }
    
        var recentlyUpdatedHourThreshold = parseInt($("#recently_updated_hour_threshold").val());
        if (isNaN(recentlyUpdatedHourThreshold) || recentlyUpdatedHourThreshold < 0) {
            alert("Recently updated hour threshold must be a positive number.");
            return false; // Validation failed
        }
    
        var specialMessageThreshold = parseInt($("#special_message_threshold").val());
        if (isNaN(specialMessageThreshold) || specialMessageThreshold < 0) {
            alert("Special message threshold must be a non-negative number.");
            return false; // Validation failed
        }

        // Validate start time format (HH:MM)
        var startTime = $("#start_time").val();
        if (!/^([01]\d|2[0-3]):([0-5]\d)$/.test(startTime)) {
            alert("Start time must be in the format HH:MM (24-hour format).");
            return false; // Validation failed
        }

        // Validate end time format (HH:MM)
        var endTime = $("#end_time").val();
        if (!/^([01]\d|2[0-3]):([0-5]\d)$/.test(endTime)) {
            alert("End time must be in the format HH:MM (24-hour format).");
            return false; // Validation failed
        }

        // Check if either FB page id with access token or FB group link with at least 1 login is provided
        var fbPageId = $("#fb_page_id").val();
        var accessToken = $("#access_token").val();
        var fbGroupLink = $("#fb_group_link").val();
        var loginEmails = $("input[name='email[]']");
        var loginPasswords = $("input[name='password[]']");
        var hasValidLogin = false;
    
        // Loop through login fields to check if at least one entry has both email and password filled
        for (var i = 0; i < loginEmails.length; i++) {
            var email = $(loginEmails[i]).val();
            var password = $(loginPasswords[i]).val();
            if (email && password) {
                hasValidLogin = true;
                break;
            }
        }
    
        if ((fbPageId && accessToken) || (fbGroupLink && hasValidLogin)) {
            return true; // Validation passed
        } else {
            alert("Please provide either FB page id with access token or FB group link with at least 1 login.");
            return false; // Validation failed
        }
    }


    // Change Name
    $("button.change-name-button").click(function() {
        $.post("/change_name", $("form.change-name-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });


    // Delete account
    $("button.second-delete").click(function(event) {
        if (confirm("Are you sure you want to delete your account?")) {
            console.log("Deleting account");
            $.post("/delete_account", $("form.delete-account-form").serialize())
                .done(function(response) {
                    console.log(response);
                    location.href = "/";
                })
                .fail(function(response) {
                    console.log(response)
                });
        } else {
            event.preventDefault();
            $("div.delete-account").collapse("hide");
        }
    });


    // Toggle delete button
    $("div.delete-account").on('hide.bs.collapse', function() {
        $("div.account-card").removeClass("border-danger");
        $("div.account-card").addClass("border-secondary");
        $("p.delete-warning").removeClass("text-danger");
        $("button.first-delete").html("Delete account");
    });
    $("div.delete-account").on('show.bs.collapse', function() {
        $("div.account-card").removeClass("border-secondary");
        $("div.account-card").addClass("border-danger");
        $("p.delete-warning").addClass("text-danger");
        $("button.first-delete").html("Hide the red button!");
    });

});
