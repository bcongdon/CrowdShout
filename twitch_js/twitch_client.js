// Do NOT include this line if you are using the built js version!
//var irc = require("tmi.js");

var options = {
    options: {
        debug: true
    },
    connection: {
        random: "chat",
        reconnect: true
    },
    identity: {
        username: "REDACTED",
        password: "oauth:REDACTED"
    },
    channels: ["#imaqtpie","#trumpSC","#sodapoppin"]
};
var client = new irc.client(options)

setupClient()

function onButtonClick(){
    newChannel = document.getElementById('channelSelect').value
    //switchChannel(newChannel)
    topChannels()
}

function switchChannel(channel){
    channel.forEach(function(obj){
        client.join(obj)
    });
}

function topChannels(){
    client.api({
        url: "https://api.twitch.tv/kraken/streams/featured"
        }, function(err, res, body) {
            var topChannels = body['featured'].map(function(obj){
                return obj['stream']['channel']['name']
            });
            switchChannel(topChannels)
    });
}

function stopClient(){
    client.disconnect()
}

function setupClient(){
    client = new irc.client(options)

    client.on("chat", function (channel, user, message, self) {
        // Do your stuff.
        var urlRegEx = new RegExp(/(^|\s)((https?:\/\/)?[\w-]+(\.[a-z-]+)+\.?(:\d+)?(\/\S*)?)/)
        if(urlRegEx.test(message)) {
            //alert("url inside");
            message = message.match(urlRegEx)[0]
            var row = document.createElement("tr");                 // Create a <li> node
    
            var textnode = document.createTextNode(message);         // Create a text node
            node.appendChild(textnode); 
            document.getElementById("myTable").appendChild(node); 
        }
    });
    client.connect()
    console.log(client)

    
}