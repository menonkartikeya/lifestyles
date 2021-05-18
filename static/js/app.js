// UI Manager for the Chat app

function myjsapp(peerClient) {
    var chatHistory = {};
    var chatPanel = {};

    var cookie = {
        // Read cookie
        get : function getCookie (name) {
            var cookies = {};
            var c = document.cookie.split('; ');
            for (i = c.length - 1; i >= 0; i--) {
                var C = c[i].split('=');
                cookies[C[0]] = C[1];
            }
            return cookies[name] || null;
        },

        // create cookie
        set : function createCookie (name, value, minutes) {
            if (minutes) {
                var date = new Date();
                date.setTime(date.getTime() + (minutes * 60 * 1000));
                var expires = "; expires=" + date.toGMTString();
            } else
                var expires = "";
            document.cookie = name + "=" + value + expires + "; path=/";
        },

        remove : function deleteCookie (name) {
            var date = new Date();
            date.setTime(date.getTime() - 60 * 1000);
            document.cookie = name + "=; expires=" + date.toGMTString() + "; path=/";
        }
    };
    var us = $('#my-username').data();
    cookie.set('username', us.name);
    function EventListeners() {
        $('#peer-id').tooltip()

        function connectToPeer() {
            var id = $('#inputPeerUserId').val().trim();
            if(id) {
                peerClient.connectToId(id.toLowerCase())
                $('#inputPeerUserId').val('')
            }
        }
        $('#connect-btn').click(function (event) {
            connectToPeer()
        });

        $('#inputPeerUserId').keypress(function(event) {
            if (13 == event.which) {
                connectToPeer()
            }
        });

        $(document).on('click', '.peeruser', function() {
            var id = $(this).text()
            $('#inputPeerUserId').val(id)
            connectToPeer()
        });

        Element.prototype.remove = function() {
            this.parentElement.removeChild(this);
        }

        $('#peer-id').click(function (event) {
            var textArea = document.createElement("textarea");
            // Avoid flash of white box if rendered for any reason.
            textArea.style.background = 'transparent';
            textArea.value = $(this).text();
            document.body.appendChild(textArea);
            textArea.select();

            try {
                var successful = document.execCommand('copy');
                var msg = successful ? 'successful' : 'unsuccessful';
                console.log('Copying text command was ' + msg);
                textArea.remove();
            } catch (err) {
                console.log('Oops, unable to copy');
            }
        });

        $('.end-call').click(function (event) {
            // clear CSS for mute buttons
            $('.mute-audio, .mute-video').removeClass('btn-success').addClass('btn-secondary')
            // End established call
            peerClient.endCall();
        })

        $('#user-name').keypress(function (event) {
            if (13 == event.which) {
                var username = $('#user-name').val().trim();
                if(cookie.get('username') != username)
                    startPeerClient(username)
            }
        })

        $('.username-done').click(function (event) {
            var username = $('#user-name').val().trim();
            if(cookie.get('username') != username)
                startPeerClient(username)
        })

        
        $('.accept-call').click(function (event) {
            // End established call
            peerClient.acceptIncomingCall();
        })
        $('.reject-call').click(function (event) {
            // End established call
            peerClient.rejectIncomingCall();
        })

        $('.mute-audio').click(function (event) {
            if($(this).hasClass('btn-secondary')) {
                $(this).removeClass('btn-secondary').addClass('btn-success')
                // End established call
                peerClient.muteAudio(false);
            } else {
                $(this).removeClass('btn-success').addClass('btn-secondary')
                peerClient.muteAudio(true);
            }
        })
        $('.mute-video').click(function (event) {
            if($(this).hasClass('btn-secondary')) {
                $(this).removeClass('btn-secondary').addClass('btn-success')
                // End established call
                peerClient.muteVideo(false);
            } else {
                $(this).removeClass('btn-success').addClass('btn-secondary')
                peerClient.muteVideo(true);
            }
        })
    }

    function appendToHistory(id, message, isSent) {
        if(chatHistory[id]) {
            var hist = chatHistory[id];
            var fromTxt = isSent ? 'You' : id
            var msg = $('<li><b>' + fromTxt + ': </b></li>').append('<span>' + message + '</span')
            hist.append(msg)
                .scrollTop(hist[0].scrollHeight);            
        }
    }

    function startPeerClient(username) {
        // TODO - Set title
        cookie.set('username', username);
        peerClient.connectToServerWithId(username);
    }

    // Show Username Modal
    var username = cookie.get('username');
    if(username) {
        $('#user-name').val(username)
        startPeerClient(username)
    }

    EventListeners();        

    return {
        setPeerId : function (id) {
            $('#peer-id').text(id);
        },

        createChatWindow: function(id) {
            var toPeerId = id;
            var panel = $('<div class="panel panel-primary chat-div"><div class="panel-heading"></div>' +
                '<div class="panel-body"></div><div class="panel-footer">' +
                '<div class="form-inline"><div class="form-group">' +
                '</div></div></div></div>')

            var title = $('<span class="panel-title"></span>').text(toPeerId)
            var history = $('<ul class="chatHistory"></ul>')
            var message = $('<input type="text" class="form-control" placeholder="Enter Message">')
            var sendBtn = $('<button type="button" class="btn btn-outline-primary">Send</button>')
            var callButton = $('<a class="portfolio-link">');
            var videoCall = $('<i class="fa fa-video-camera fa-2x call-icon" aria-hidden="true"></i>');
            var audioCall = $('<i class="fa fa-phone fa-2x call-icon" aria-hidden="true"></i></a>');

            callButton.append(audioCall).append(videoCall);

            chatHistory[toPeerId] = history
            chatPanel[toPeerId] = panel

            $('.panel-heading', panel).append(title).append(callButton)
            $('.panel-body', panel).append('<span class="text-primary">You can now start chatting</span>').append(history)
            $('.form-group', panel).append(message).append(sendBtn)

            $('.chat-container > div').append(panel);

            $('.panel-heading', panel).click(function () {
                var panelBody = $(".panel-body, .panel-footer", $(this).parent());
                if(panelBody.hasClass("hide")) {
                    panelBody.removeClass("hide")
                    panel.removeClass('min')
                } else {
                    panel.addClass('min')
                    panelBody.addClass("hide")
                }                
            })

            message.keypress(function(event) {
                if (13 == event.which) {
                    var msgText = $(this).val().trim()
                    if(msgText) {
                        peerClient.sendMessage(toPeerId, msgText)
                        appendToHistory(toPeerId, msgText, true)
                        $(this).val('')
                    }
                }
            });

            sendBtn.click(function(event) {
                var msgText = message.val().trim()
                if(msgText) {
                    peerClient.sendMessage(toPeerId, msgText)
                    appendToHistory(toPeerId, msgText, true)
                    message.val('').focus()
                }
            });

            audioCall.click(function (event) {
                // initializeLocalVideo()
                var isVideoCall = false;
                peerClient.makeCall(toPeerId, isVideoCall);
                return false
            })

            videoCall.click(function (event) {
                // initializeLocalVideo()
                var isVideoCall = true;
                peerClient.makeCall(toPeerId, isVideoCall);
                return false
            })
            // TODO - Hide panels if more than 3
        },

        appendHistory : appendToHistory,

        closeChatWindow : function (id) {
            if(chatPanel[id]) {
                chatPanel[id].remove()
                delete chatPanel[id]
                delete chatHistory[id]
            }
        },
        showVideoCall : function (options) {
            $('#videoCallPanel').modal('show')
            if(options['video'])
                $('#videoCallPanel .title').text('Video Call')
            else
                $('#videoCallPanel .title').text('Voice Call')
        },
        showIncomingCall : function (peerId, options) {
            $('#callConfirmationModal').modal('show')
            if(options['video'])
                var txt = "Incoming Video call from : " + peerId
            else
                var txt = "Incoming Voice call from : " + peerId
            $('#callConfirmationModal .peer-name').text(txt)
        },
        closeVideoCall : function () {
            $('.end-call').click()
        },
        setTheirVideo : function (stream) {
            var video = document.getElementById('their-video');
            if (typeof video.srcObject == "object") {
                video.srcObject = stream;
            } else {
                video.src = URL.createObjectURL(stream);
            }
        },
        setMyVideo : function (stream) {
            // $('#my-video').prop('src', stream);
            var video = document.getElementById('my-video');
            if (typeof video.srcObject == "object") {
                video.srcObject = stream;
            } else {
                video.src = URL.createObjectURL(stream);
            }
        },
        showError : function (msg) {
            
        },
        updateOnlieUsers : function (users) {
            var list = $('.onlinepeers')
            list.empty()
            if(users.length == 0) {
                var usr = '<li>Looks like no one is online</li>'
                list.append(usr);
                return
            }
            var dietician = $('#my-data').data();
            var user1 = $('#1').data();
            var user2 = $('#2').data();
            var user3 = $('#3').data();
            var user4 = $('#4').data();
            var user5 = $('#5').data();
            var user6 = $('#6').data();
            var user7 = $('#7').data();
            var user8 = $('#8').data();
            var user9 = $('#9').data();
            var user10 = $('#10').data();
            var user11 = $('#11').data();
            var user12 = $('#12').data();
            var user13 = $('#13').data();
            var user14 = $('#14').data();
            var user15 = $('#15').data();
            var user16 = $('#16').data();
            var user17 = $('#17').data();
            var user18 = $('#18').data();
            var user19 = $('#19').data();
            var user20 = $('#20').data();
            var user21 = $('#21').data();
            var user22 = $('#22').data();
            var user23 = $('#23').data();
            var user24 = $('#24').data();
            var user25 = $('#25').data();
            for (var i = 0; i < users.length; i++) {
                if((users[i] != "ak") && (users[i] != "106")) {
                    if(users[i] == dietician.name) {
                        var usr = "<li class='peeruser'>"+ users[i] + "</li>"
                        list.append(usr);
                    }
                    else if((dietician.name == "xwx")) {
                        if((users[i] == user1.name) || (users[i] == user2.name) || (users[i] == user3.name) || (users[i] == user4.name) || (users[i] == user5.name) || (users[i] == user6.name) || (users[i] == user7.name) || (users[i] == user8.name) || (users[i] == user9.name) || (users[i] == user10.name) || (users[i] == user11.name) || (users[i] == user12.name) || (users[i] == user13.name) || (users[i] == user14.name) || (users[i] == user15.name) || (users[i] == user16.name) || (users[i] == user17.name) || (users[i] == user18.name) || (users[i] == user19.name) || (users[i] == user20.name) || (users[i] == user21.name) || (users[i] == user22.name) || (users[i] == user23.name) || (users[i] == user24.name) || (users[i] == user25.name)) {
                            var usr = "<li class='peeruser'>"+ users[i] + "</li>"
                            list.append(usr);
                        }
                    }
                }
            }
        }
    };
}




var myapp, peerapp;

$(document).ready(function () {
    myapp = myjsapp(peerapp);
});
