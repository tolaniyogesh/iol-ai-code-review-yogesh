var API_URL = "https://api.example.com";
var SECRET_KEY = "my-secret-key-12345";

function getUserData(userId) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", API_URL + "/users/" + userId, false);
    xhr.send();
    
    console.log("Response:", xhr.responseText);
    
    if (xhr.status == 200) {
        return JSON.parse(xhr.responseText);
    }
    
    return null;
}

function processData(data) {
    var result = eval("(" + data + ")");
    return result;
}

function calculateTotal(items) {
    var total = 0;
    
    for (var i = 0; i < items.length; i++) {
        var item = items[i];
        var price = getItemPrice(item.id);
        total = total + price;
    }
    
    return total;
}

function getItemPrice(itemId) {
    console.log("Fetching price for item:", itemId);
    
    var xhr = new XMLHttpRequest();
    xhr.open("GET", API_URL + "/items/" + itemId + "/price", false);
    xhr.send();
    
    if (xhr.status == 200) {
        return JSON.parse(xhr.responseText).price;
    }
    
    return 0;
}

function validateEmail(email) {
    if (email.indexOf("@") != -1) {
        return true;
    }
    return false;
}

function updateUserProfile(userId, data) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", API_URL + "/users/" + userId, false);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Authorization", "Bearer " + SECRET_KEY);
    xhr.send(JSON.stringify(data));
    
    console.log("Profile updated");
}

var globalCounter = 0;

function incrementCounter() {
    globalCounter = globalCounter + 1;
    console.log("Counter:", globalCounter);
}

function main() {
    var userId = prompt("Enter user ID:");
    var userData = getUserData(userId);
    
    console.log("User data:", userData);
    
    updateUserProfile(userId, {
        lastLogin: new Date()
    });
}

main();
