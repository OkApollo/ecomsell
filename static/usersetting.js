var userdet = document.getElementById("userdetails")
var purchases = document.getElementById("purchases")
var editdet = document.getElementById("editdet")
var address_saved = document.getElementById("addresses")
var notifs = document.getElementById("notifs")

// document.getElementById("userdetails_content").style.display = "block";

userdet.addEventListener("click",()=>{
    // console.log("WORKED")
    document.getElementById("userdetails_content").style.display = "block";
    document.getElementById("purchases_content").style.display = "none";
    document.getElementById("editdet_content").style.display = "none";
    document.getElementById("address_content").style.display = "none";
    document.getElementById("notifs_content").style.display = "none";
})

purchases.addEventListener("click",()=>{
    // console.log("WORKED")
    document.getElementById("purchases_content").style.display = "block";
    document.getElementById("userdetails_content").style.display = "none"
    document.getElementById("editdet_content").style.display = "none"
    document.getElementById("address_content").style.display = "none"
    document.getElementById("notifs_content").style.display = "none"

})

editdet.addEventListener("click",()=>{
    // console.log("WORKED")
    document.getElementById("editdet_content").style.display = "block";
    document.getElementById("userdetails_content").style.display = "none"
    document.getElementById("purchases_content").style.display = "none"
    document.getElementById("notifs_content").style.display = "none"
    document.getElementById("address_content").style.display = "none"
})

address_saved.addEventListener("click",()=>{
    // console.log("WORKED")
    document.getElementById("address_content").style.display = "block";
    document.getElementById("userdetails_content").style.display = "none"
    document.getElementById("editdet_content").style.display = "none"
    document.getElementById("notifs_content").style.display = "none"
    document.getElementById("purchases_content").style.display = "none"    
})

notifs.addEventListener("click",()=>{
    // console.log("WORKED")
    document.getElementById("notifs_content").style.display = "block";
    document.getElementById("userdetails_content").style.display = "none"
    document.getElementById("editdet_content").style.display = "none"
    document.getElementById("address_content").style.display = "none"
    document.getElementById("purchases_content").style.display = "none"    
})